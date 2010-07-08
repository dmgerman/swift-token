#!/usr/bin/python
# Copyright (c) 2010 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import with_statement
import errno
import glob
import os
import resource
import signal
import sys
import time

ALL_SERVERS = ['account-auditor', 'account-server', 'container-auditor',
    'container-replicator', 'container-server', 'container-updater',
    'object-auditor', 'object-server', 'object-replicator', 'object-updater',
    'proxy-server', 'account-replicator', 'auth-server', 'account-reaper']
GRACEFUL_SHUTDOWN_SERVERS = ['account-server', 'container-server',
    'object-server', 'proxy-server', 'auth-server']
MAX_DESCRIPTORS = 32768
MAX_MEMORY = (1024 * 1024 * 1024) * 2 # 2 GB

_, server, command = sys.argv
if server == 'all':
    servers = ALL_SERVERS
else:
    if '-' not in server:
        server = '%s-server' % server
    servers = [server]
command = command.lower()

def pid_files(server):
    if os.path.exists('/var/run/swift/%s.pid' % server):
        pid_files = ['/var/run/swift/%s.pid' % server]
    else:
        pid_files = glob.glob('/var/run/swift/%s/*.pid' % server)
    for pid_file in pid_files:
        pid = int(open(pid_file).read().strip())
        yield pid_file, pid

def do_start(server, once=False):
    server_type = '-'.join(server.split('-')[:-1])

    for pid_file, pid in pid_files(server):
        if os.path.exists('/proc/%s' % pid):
            print "%s appears to already be running: %s" % (server, pid_file)
            return
        else:
            print "Removing stale pid file %s" % pid_file
            os.unlink(pid_file)

    try:
        resource.setrlimit(resource.RLIMIT_NOFILE,
                (MAX_DESCRIPTORS, MAX_DESCRIPTORS))
        resource.setrlimit(resource.RLIMIT_DATA,
                (MAX_MEMORY, MAX_MEMORY))
    except ValueError:
        print "Unable to increase file descriptor limit.  Running as non-root?"
    os.environ['PYTHON_EGG_CACHE'] = '/tmp'

    def launch(ini_file, pid_file):
        pid = os.fork()
        if pid == 0:
            os.setsid()
            with open(os.devnull, 'r+b') as nullfile:
                for desc in (0, 1, 2): # close stdio
                    try:
                        os.dup2(nullfile.fileno(), desc)
                    except OSError:
                        pass
            try:
                if once:
                    os.execl('/usr/bin/swift-%s' % server, server,
                        ini_file, 'once')
                else:
                    os.execl('/usr/bin/swift-%s' % server, server, ini_file)
            except OSError:
                print 'unable to launch %s' % server
            sys.exit(0)
        else:
            fp = open(pid_file, 'w')
            fp.write('%d\n' % pid)
            fp.close()
    try:
        os.mkdir('/var/run/swift')
    except OSError, err:
        if err.errno == errno.EACCES:
            sys.exit('Unable to create /var/run/swift.  Running as non-root?')
        elif err.errno != errno.EEXIST:
            raise
    if os.path.exists('/etc/swift/%s-server.conf' % server_type):
        if once:
            print 'Running %s once' % server
        else:
            print 'Starting %s' % server
        launch('/etc/swift/%s-server.conf' % server_type,
                    '/var/run/swift/%s.pid' % server)
    else:
        try:
            os.mkdir('/var/run/swift/%s' % server)
        except OSError, err:
            if err.errno == errno.EACCES:
                sys.exit(
                    'Unable to create /var/run/swift.  Running as non-root?')
            elif err.errno != errno.EEXIST:
                raise
        if once:
            print 'Running %ss once' % server
        else:
            print 'Starting %ss' % server
        for num, ini_file in enumerate(glob.glob('/etc/swift/%s-server/*.conf' % server_type)):
            launch(ini_file, '/var/run/swift/%s/%d.pid' % (server, num))

def do_stop(server, graceful=False):
    if graceful and server in GRACEFUL_SHUTDOWN_SERVERS:
        sig = signal.SIGHUP
    else:
        sig = signal.SIGTERM

    did_anything = False
    pfiles = pid_files(server)
    for pid_file, pid in pfiles:
        did_anything = True
        try:
            print 'Stopping %s  pid: %s  signal: %s' % (server, pid, sig)
            os.kill(pid, sig)
        except OSError:
            print "Process %d not running" % pid
        try:
            os.unlink(pid_file)
        except OSError:
            pass
    for pid_file, pid in pfiles:
        for _ in xrange(150): # 15 seconds
            if not os.path.exists('/proc/%s' % pid):
                break
            time.sleep(0.1)
        else:
            print 'Waited 15 seconds for pid %s (%s) to die; giving up' % \
                  (pid, pid_file)
    if not did_anything:
        print 'No %s running' % server

if command == 'start':
    for server in servers:
        do_start(server)

if command == 'stop':
    for server in servers:
        do_stop(server)

if command == 'shutdown':
    for server in servers:
        do_stop(server, graceful=True)

if command == 'restart':
    for server in servers:
        do_stop(server)
    for server in servers:
        do_start(server)

if command == 'reload':
    for server in servers:
        do_stop(server, graceful=True)
        do_start(server)

if command == 'once':
    for server in servers:
        do_start(server, once=True)
