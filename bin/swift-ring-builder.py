#!/usr/bin/python -uO
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

import cPickle as pickle
from errno import EEXIST
from gzip import GzipFile
from os import mkdir
from os.path import basename, dirname, exists, join as pathjoin
from sys import argv, exit
from time import time

from swift.common.ring import RingBuilder


MAJOR_VERSION = 1
MINOR_VERSION = 1
EXIT_RING_CHANGED = 0
EXIT_RING_UNCHANGED = 1
EXIT_ERROR  = 2


def search_devs(builder, search_value):
    # d<device_id>z<zone>-<ip>:<port>/<device_name>_<meta>
    orig_search_value = search_value
    match = []
    if search_value.startswith('d'):
        i = 1
        while i < len(search_value) and search_value[i].isdigit():
            i += 1
        match.append(('id', int(search_value[1:i])))
        search_value = search_value[i:]
    if search_value.startswith('z'):
        i = 1
        while i < len(search_value) and search_value[i].isdigit():
            i += 1
        match.append(('zone', int(search_value[1:i])))
        search_value = search_value[i:]
    if search_value.startswith('-'):
        search_value = search_value[1:]
    if len(search_value) and search_value[0].isdigit():
        i = 1
        while i < len(search_value) and search_value[i] in '0123456789.':
            i += 1
        match.append(('ip', search_value[:i]))
        search_value = search_value[i:]
    if search_value.startswith(':'):
        i = 1
        while i < len(search_value) and search_value[i].isdigit():
            i += 1
        match.append(('port', int(search_value[1:i])))
        search_value = search_value[i:]
    if search_value.startswith('/'):
        i = 1
        while i < len(search_value) and search_value[i] != '_':
            i += 1
        match.append(('device', search_value[1:i]))
        search_value = search_value[i:]
    if search_value.startswith('_'):
        match.append(('meta', search_value[1:]))
        search_value = ''
    if search_value:
        raise ValueError('Invalid <search-value>: %s' % repr(orig_search_value))
    devs = []
    for dev in builder.devs:
        if not dev:
            continue
        matched = True
        for key, value in match:
            if key == 'meta':
                if value not in dev.get(key):
                    matched = False
            elif dev.get(key) != value:
                matched = False
        if matched:
            devs.append(dev)
    return devs


SEARCH_VALUE_HELP = '''
    The <search-value> can be of the form:
    d<device_id>z<zone>-<ip>:<port>/<device_name>_<meta>
    Any part is optional, but you must include at least one part.
    Examples:
        d74              Matches the device id 74
        z1               Matches devices in zone 1
        z1-1.2.3.4       Matches devices in zone 1 with the ip 1.2.3.4
        1.2.3.4          Matches devices in any zone with the ip 1.2.3.4
        z1:5678          Matches devices in zone 1 using port 5678
        :5678            Matches devices that use port 5678
        /sdb1            Matches devices with the device name sdb1
        _shiny           Matches devices with shiny in the meta data
        _"snet: 5.6.7.8" Matches devices with snet: 5.6.7.8 in the meta data
    Most specific example:
        d74z1-1.2.3.4:5678/sdb1_"snet: 5.6.7.8"
    Nerd explanation:
        All items require their single character prefix except the ip, in which
        case the - is optional unless the device id or zone is also included.
'''.strip()

CREATE_HELP = '''
ring_builder <builder_file> create <part_power> <replicas> <min_part_hours>
    Creates <builder_file> with 2^<part_power> partitions and <replicas>.
    <min_part_hours> is number of hours to restrict moving a partition more
    than once.
'''.strip()

SEARCH_HELP = '''
ring_builder <builder_file> search <search-value>
    Shows information about matching devices.

    %(SEARCH_VALUE_HELP)s
'''.strip() % globals()

ADD_HELP = '''
ring_builder <builder_file> add z<zone>-<ip>:<port>/<device_name>_<meta> <wght>
    Adds a device to the ring with the given information. No partitions will be
    assigned to the new device until after running 'rebalance'. This is so you
    can make multiple device changes and rebalance them all just once.
'''.strip()

SET_WEIGHT_HELP = '''
ring_builder <builder_file> set_weight <search-value> <weight>
    Resets the device's weight. No partitions will be reassigned to or from the
    device until after running 'rebalance'. This is so you can make multiple
    device changes and rebalance them all just once.

    %(SEARCH_VALUE_HELP)s
'''.strip() % globals()

SET_INFO_HELP = '''
ring_builder <builder_file> set_info <search-value>
                                     <ip>:<port>/<device_name>_<meta>
    Resets the device's information. This information isn't used to assign
    partitions, so you can use 'write_ring' afterward to rewrite the current
    ring with the newer device information. Any of the parts are optional
    in the final <ip>:<port>/<device_name>_<meta> parameter; just give what you
    want to change. For instance set_info d74 _"snet: 5.6.7.8" would just
    update the meta data for device id 74.

    %(SEARCH_VALUE_HELP)s
'''.strip() % globals()

REMOVE_HELP = '''
ring_builder <builder_file> remove <search-value>
    Removes the device(s) from the ring. This should normally just be used for
    a device that has failed. For a device you wish to decommission, it's best
    to set its weight to 0, wait for it to drain all its data, then use this
    remove command. This will not take effect until after running 'rebalance'.
    This is so you can make multiple device changes and rebalance them all just
    once.

    %(SEARCH_VALUE_HELP)s
'''.strip() % globals()

SET_MIN_PART_HOURS_HELP = '''
ring_builder <builder_file> set_min_part_hours <hours>
    Changes the <min_part_hours> to the given <hours>. This should be set to
    however long a full replication/update cycle takes. We're working on a way
    to determine this more easily than scanning logs.
'''.strip()


if __name__ == '__main__':
    if len(argv) < 2:
        print '''
ring_builder %(MAJOR_VERSION)s.%(MINOR_VERSION)s

%(CREATE_HELP)s

ring_builder <builder_file>
    Shows information about the ring and the devices within.

%(SEARCH_HELP)s

%(ADD_HELP)s

%(SET_WEIGHT_HELP)s

%(SET_INFO_HELP)s

%(REMOVE_HELP)s

ring_builder <builder_file> rebalance
    Attempts to rebalance the ring by reassigning partitions that haven't been
    recently reassigned.

ring_builder <builder_file> validate
    Just runs the validation routines on the ring.

ring_builder <builder_file> write_ring
    Just rewrites the distributable ring file. This is done automatically after
    a successful rebalance, so really this is only useful after one or more
    'set_info' calls when no rebalance is needed but you want to send out the
    new device information.

%(SET_MIN_PART_HOURS_HELP)s

Quick list: create search add set_weight set_info remove rebalance write_ring
            set_min_part_hours
Exit codes: 0 = ring changed, 1 = ring did not change, 2 = error
'''.strip() % globals()
        exit(EXIT_RING_UNCHANGED)

    if exists(argv[1]):
        builder = pickle.load(open(argv[1], 'rb'))
        for dev in builder.devs:
            if dev and 'meta' not in dev:
                dev['meta'] = ''
    elif len(argv) < 3 or argv[2] != 'create':
        print 'Ring Builder file does not exist: %s' % argv[1]
        exit(EXIT_ERROR)
    elif argv[2] == 'create':
        if len(argv) < 6:
            print CREATE_HELP
            exit(EXIT_RING_UNCHANGED)
        builder = RingBuilder(int(argv[3]), int(argv[4]), int(argv[5]))
        backup_dir = pathjoin(dirname(argv[1]), 'backups')
        try:
            mkdir(backup_dir)
        except OSError, err:
            if err.errno != EEXIST:
                raise
        pickle.dump(builder, open(pathjoin(backup_dir,
            '%d.' % time() + basename(argv[1])), 'wb'), protocol=2)
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_CHANGED)

    backup_dir = pathjoin(dirname(argv[1]), 'backups')
    try:
        mkdir(backup_dir)
    except OSError, err:
        if err.errno != EEXIST:
            raise

    ring_file = argv[1]
    if ring_file.endswith('.builder'):
        ring_file = ring_file[:-len('.builder')]
    ring_file += '.ring.gz'

    if len(argv) == 2:
        print '%s, build version %d' % (argv[1], builder.version)
        zones = 0
        balance = 0
        if builder.devs:
            zones = len(set(d['zone'] for d in builder.devs if d is not None))
            balance = builder.get_balance()
        print '%d partitions, %d replicas, %d zones, %d devices, %.02f ' \
              'balance' % (builder.parts, builder.replicas, zones,
                           len([d for d in builder.devs if d]), balance)
        print 'The minimum number of hours before a partition can be ' \
              'reassigned is %s' % builder.min_part_hours
        if builder.devs:
            print 'Devices:    id  zone      ip address  port      name ' \
                  'weight partitions balance meta'
            weighted_parts = builder.parts * builder.replicas / \
                sum(d['weight'] for d in builder.devs if d is not None)
            for dev in builder.devs:
                if dev is None:
                    continue
                if not dev['weight']:
                    if dev['parts']:
                        balance = 999.99
                    else:
                        balance = 0
                else:
                    balance = 100.0 * dev['parts'] / \
                              (dev['weight'] * weighted_parts) - 100.0
                print '         %5d %5d %15s %5d %9s %6.02f %10s %7.02f %s' % \
                    (dev['id'], dev['zone'], dev['ip'], dev['port'],
                     dev['device'], dev['weight'], dev['parts'], balance,
                     dev['meta'])
        exit(EXIT_RING_UNCHANGED)

    if argv[2] == 'search':
        if len(argv) < 4:
            print SEARCH_HELP
            exit(EXIT_RING_UNCHANGED)
        devs = search_devs(builder, argv[3])
        if not devs:
            print 'No matching devices found'
            exit(EXIT_ERROR)
        print 'Devices:    id  zone      ip address  port      name ' \
              'weight partitions balance meta'
        weighted_parts = builder.parts * builder.replicas / \
            sum(d['weight'] for d in builder.devs if d is not None)
        for dev in devs:
            if not dev['weight']:
                if dev['parts']:
                    balance = 999.99
                else:
                    balance = 0
            else:
                balance = 100.0 * dev['parts'] / \
                          (dev['weight'] * weighted_parts) - 100.0
            print '         %5d %5d %15s %5d %9s %6.02f %10s %7.02f %s' % \
                (dev['id'], dev['zone'], dev['ip'], dev['port'],
                 dev['device'], dev['weight'], dev['parts'], balance,
                 dev['meta'])
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'add':
        # add z<zone>-<ip>:<port>/<device_name>_<meta> <wght>
        if len(argv) < 5:
            print ADD_HELP
            exit(EXIT_RING_UNCHANGED)

        if not argv[3].startswith('z'):
            print 'Invalid add value: %s' % argv[3]
            exit(EXIT_ERROR)
        i = 1
        while i < len(argv[3]) and argv[3][i].isdigit():
            i += 1
        zone = int(argv[3][1:i])
        rest = argv[3][i:]

        if not rest.startswith('-'):
            print 'Invalid add value: %s' % argv[3]
            exit(EXIT_ERROR)
        i = 1
        while i < len(rest) and rest[i] in '0123456789.':
            i += 1
        ip = rest[1:i]
        rest = rest[i:]

        if not rest.startswith(':'):
            print 'Invalid add value: %s' % argv[3]
            exit(EXIT_ERROR)
        i = 1
        while i < len(rest) and rest[i].isdigit():
            i += 1
        port = int(rest[1:i])
        rest = rest[i:]

        if not rest.startswith('/'):
            print 'Invalid add value: %s' % argv[3]
            exit(EXIT_ERROR)
        i = 1
        while i < len(rest) and rest[i] != '_':
            i += 1
        device_name = rest[1:i]
        rest = rest[i:]

        meta = ''
        if rest.startswith('_'):
            meta = rest[1:]

        weight = float(argv[4])

        for dev in builder.devs:
            if dev is None:
                continue
            if dev['ip'] == ip and dev['port'] == port and \
                    dev['device'] == device_name:
                print 'Device %d already uses %s:%d/%s.' % \
                      (dev['id'], dev['ip'], dev['port'], dev['device'])
                exit(EXIT_ERROR)

        next_dev_id = 0
        if builder.devs:
            next_dev_id = max(d['id'] for d in builder.devs if d) + 1
        builder.add_dev({'id': next_dev_id, 'zone': zone, 'ip': ip,
                         'port': port, 'device': device_name, 'weight': weight,
                         'meta': meta})
        print 'Device z%s-%s:%s/%s_"%s" with %s weight got id %s' % \
              (zone, ip, port, device_name, meta, weight, next_dev_id)
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'set_weight':
        if len(argv) != 5:
            print SET_WEIGHT_HELP
            exit(EXIT_RING_UNCHANGED)
        devs = search_devs(builder, argv[3])
        weight = float(argv[4])
        if not devs:
            print 'No matching devices found'
            exit(EXIT_ERROR)
        if len(devs) > 1:
            print 'Matched more than one device:'
            for dev in devs:
                print '    d%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_' \
                      '"%(meta)s"' % dev
            if raw_input('Are you sure you want to update the weight for '
                         'these %s devices? (y/N) ' % len(devs)) != 'y':
                print 'Aborting device modifications'
                exit(EXIT_ERROR)
        for dev in devs:
            builder.set_dev_weight(dev['id'], weight)
            print 'd%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_"%(meta)s" ' \
                  'weight set to %(weight)s' % dev
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'set_info':
        if len(argv) != 5:
            print SET_INFO_HELP
            exit(EXIT_RING_UNCHANGED)
        devs = search_devs(builder, argv[3])
        change_value = argv[4]
        change = []
        if len(change_value) and change_value[0].isdigit():
            i = 1
            while i < len(change_value) and change_value[i] in '0123456789.':
                i += 1
            change.append(('ip', change_value[:i]))
            change_value = change_value[i:]
        if change_value.startswith(':'):
            i = 1
            while i < len(change_value) and change_value[i].isdigit():
                i += 1
            change.append(('port', int(change_value[1:i])))
            change_value = change_value[i:]
        if change_value.startswith('/'):
            i = 1
            while i < len(change_value) and change_value[i] != '_':
                i += 1
            change.append(('device', change_value[1:i]))
            change_value = change_value[i:]
        if change_value.startswith('_'):
            change.append(('meta', change_value[1:]))
            change_value = ''
        if change_value or not change:
            raise ValueError('Invalid set info change value: %s' %
                             repr(argv[4]))
        if not devs:
            print 'No matching devices found'
            exit(EXIT_ERROR)
        if len(devs) > 1:
            print 'Matched more than one device:'
            for dev in devs:
                print '    d%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_' \
                      '"%(meta)s"' % dev
            if raw_input('Are you sure you want to update the info for '
                         'these %s devices? (y/N) ' % len(devs)) != 'y':
                print 'Aborting device modifications'
                exit(EXIT_ERROR)
        for dev in devs:
            orig_dev_string = \
                'd%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_"%(meta)s"' % dev
            test_dev = dict(dev)
            for key, value in change:
                test_dev[key] = value
            for check_dev in builder.devs:
                if not check_dev or check_dev['id'] == test_dev['id']:
                    continue
                if check_dev['ip'] == test_dev['ip'] and \
                        check_dev['port'] == test_dev['port'] and \
                        check_dev['device'] == test_dev['device']:
                    print 'Device %d already uses %s:%d/%s.' % \
                          (check_dev['id'], check_dev['ip'], check_dev['port'],
                           check_dev['device'])
                    exit(EXIT_ERROR)
            for key, value in change:
                dev[key] = value
            new_dev_string = \
                'd%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_"%(meta)s"' % dev
            print 'Device %s is now %s' % (orig_dev_string, new_dev_string)
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'remove':
        if len(argv) < 4:
            print REMOVE_HELP
            exit(EXIT_RING_UNCHANGED)
        devs = search_devs(builder, argv[3])
        if not devs:
            print 'No matching devices found'
            exit(EXIT_ERROR)
        if len(devs) > 1:
            print 'Matched more than one device:'
            for dev in devs:
                print '    d%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_' \
                      '"%(meta)s"' % dev
            if raw_input('Are you sure you want to remove these %s devices? '
                         '(y/N) ' % len(devs)) != 'y':
                print 'Aborting device removals'
                exit(EXIT_ERROR)
        for dev in devs:
            builder.remove_dev(dev['id'])
            print 'd%(id)sz%(zone)s-%(ip)s:%(port)s/%(device)s_"%(meta)s" ' \
                  'marked for removal and will be removed next rebalance.' % dev
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'rebalance':
        devs_changed = builder.devs_changed
        last_balance = builder.get_balance()
        parts, balance = builder.rebalance()
        if not parts:
            print 'No partitions could be reassigned.'
            print 'Either none need to be or none can be due to ' \
                  'min_part_hours [%s].' % builder.min_part_hours
            exit(EXIT_RING_UNCHANGED)
        if not devs_changed and abs(last_balance - balance) < 1:
            print 'Cowardly refusing to save rebalance as it did not change ' \
                  'at least 1%.'
            exit(EXIT_RING_UNCHANGED)
        builder.validate()
        print 'Reassigned %d (%.02f%%) partitions. Balance is now %.02f.' % \
              (parts, 100.0 * parts / builder.parts, balance)
        if balance > 5:
            print '-' * 79
            print 'NOTE: Balance of %.02f indicates you should push this ' % \
                  balance
            print '      ring, wait at least %d hours, and rebalance/repush.' \
                  % builder.min_part_hours
            print '-' * 79
        ts = time()
        pickle.dump(builder.get_ring(),
                    GzipFile(pathjoin(backup_dir, '%d.' % ts +
                        basename(ring_file)), 'wb'), protocol=2)
        pickle.dump(builder, open(pathjoin(backup_dir,
            '%d.' % ts + basename(argv[1])), 'wb'), protocol=2)
        pickle.dump(builder.get_ring(), GzipFile(ring_file, 'wb'), protocol=2)
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_CHANGED)

    elif argv[2] == 'validate':
        builder.validate()
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'write_ring':
        pickle.dump(builder.get_ring(),
                    GzipFile(pathjoin(backup_dir, '%d.' % time() +
                        basename(ring_file)), 'wb'), protocol=2)
        pickle.dump(builder.get_ring(), GzipFile(ring_file, 'wb'), protocol=2)
        exit(EXIT_RING_CHANGED)

    elif argv[2] == 'pretend_min_part_hours_passed':
        builder.pretend_min_part_hours_passed()
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_UNCHANGED)

    elif argv[2] == 'set_min_part_hours':
        if len(argv) < 4:
            print SET_MIN_PART_HOURS_HELP
            exit(EXIT_RING_UNCHANGED)
        builder.change_min_part_hours(int(argv[3]))
        print 'The minimum number of hours before a partition can be ' \
              'reassigned is now set to %s' % argv[3]
        pickle.dump(builder, open(argv[1], 'wb'), protocol=2)
        exit(EXIT_RING_UNCHANGED)

    print 'Unknown command: %s' % argv[2]
    exit(EXIT_ERROR)
