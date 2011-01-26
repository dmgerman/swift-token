begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Licensed under the Apache License, Version 2.0 (the "License");'
nl|'\n'
comment|'# you may not use this file except in compliance with the License.'
nl|'\n'
comment|'# You may obtain a copy of the License at'
nl|'\n'
comment|'#'
nl|'\n'
comment|'#    http://www.apache.org/licenses/LICENSE-2.0'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Unless required by applicable law or agreed to in writing, software'
nl|'\n'
comment|'# distributed under the License is distributed on an "AS IS" BASIS,'
nl|'\n'
comment|'# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or'
nl|'\n'
comment|'# implied.'
nl|'\n'
comment|'# See the License for the specific language governing permissions and'
nl|'\n'
comment|'# limitations under the License.'
nl|'\n'
nl|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'random'
op|','
name|'shuffle'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkstemp'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'spawn'
op|','
name|'patcher'
op|','
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'server'
name|'import'
name|'DATADIR'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'bufferedhttp'
name|'import'
name|'http_connect'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'ContainerBroker'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'ConnectionTimeout'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'Ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'whataremyips'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'daemon'
name|'import'
name|'Daemon'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerUpdater
name|'class'
name|'ContainerUpdater'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Update container information in account listings."""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
string|"'container-updater'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'devices'"
op|','
string|"'/srv/node'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'mount_check'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
string|"'true'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'true'"
op|','
string|"'t'"
op|','
string|"'1'"
op|','
string|"'on'"
op|','
string|"'yes'"
op|','
string|"'y'"
op|')'
newline|'\n'
name|'swift_dir'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'swift_dir'"
op|','
string|"'/etc/swift'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'interval'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'interval'"
op|','
number|'300'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'account.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'concurrency'"
op|','
number|'4'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slowdown'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'slowdown'"
op|','
number|'0.01'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'node_timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'node_timeout'"
op|','
number|'3'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn_timeout'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'conn_timeout'"
op|','
number|'0.5'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'no_changes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'account_suppressions'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'account_suppression_time'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'account_suppression_time'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'new_account_suppressions'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_account_ring
dedent|''
name|'def'
name|'get_account_ring'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Get the account ring.  Load it if it hasn\'t been yet."""'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'account_ring'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Loading account ring from %s'"
op|')'
op|','
name|'self'
op|'.'
name|'account_ring_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'Ring'
op|'('
name|'self'
op|'.'
name|'account_ring_path'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'account_ring'
newline|'\n'
nl|'\n'
DECL|member|get_paths
dedent|''
name|'def'
name|'get_paths'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get paths to all of the partitions on each drive to be processed.\n\n        :returns: a list of paths\n        """'
newline|'\n'
name|'paths'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'device'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'dev_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'device'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'ismount'
op|'('
name|'dev_path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warn'
op|'('
name|'_'
op|'('
string|"'%s is not mounted'"
op|')'
op|','
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'con_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'dev_path'
op|','
name|'DATADIR'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'con_path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'partition'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'con_path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'paths'
op|'.'
name|'append'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'con_path'
op|','
name|'partition'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'shuffle'
op|'('
name|'paths'
op|')'
newline|'\n'
name|'return'
name|'paths'
newline|'\n'
nl|'\n'
DECL|member|_load_suppressions
dedent|''
name|'def'
name|'_load_suppressions'
op|'('
name|'self'
op|','
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
name|'filename'
op|','
string|"'r'"
op|')'
name|'as'
name|'tmpfile'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'line'
name|'in'
name|'tmpfile'
op|':'
newline|'\n'
indent|'                    '
name|'account'
op|','
name|'until'
op|'='
name|'line'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'until'
op|'='
name|'float'
op|'('
name|'until'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_suppressions'
op|'['
name|'account'
op|']'
op|'='
name|'until'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'ERROR with loading suppressions from %s: '"
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'filename'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
dedent|''
name|'def'
name|'run_forever'
op|'('
name|'self'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'        '
string|'"""\n        Run the updator continuously.\n        """'
newline|'\n'
name|'time'
op|'.'
name|'sleep'
op|'('
name|'random'
op|'('
op|')'
op|'*'
name|'self'
op|'.'
name|'interval'
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Begin container update sweep'"
op|')'
op|')'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'now'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'expired_suppressions'
op|'='
op|'['
name|'a'
name|'for'
name|'a'
op|','
name|'u'
name|'in'
name|'self'
op|'.'
name|'account_suppressions'
op|'.'
name|'iteritems'
op|'('
op|')'
name|'if'
name|'u'
op|'<'
name|'now'
op|']'
newline|'\n'
name|'for'
name|'account'
name|'in'
name|'expired_suppressions'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'self'
op|'.'
name|'account_suppressions'
op|'['
name|'account'
op|']'
newline|'\n'
dedent|''
name|'pid2filename'
op|'='
op|'{'
op|'}'
newline|'\n'
comment|"# read from account ring to ensure it's fresh"
nl|'\n'
name|'self'
op|'.'
name|'get_account_ring'
op|'('
op|')'
op|'.'
name|'get_nodes'
op|'('
string|"''"
op|')'
newline|'\n'
name|'for'
name|'path'
name|'in'
name|'self'
op|'.'
name|'get_paths'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'while'
name|'len'
op|'('
name|'pid2filename'
op|')'
op|'>='
name|'self'
op|'.'
name|'concurrency'
op|':'
newline|'\n'
indent|'                    '
name|'pid'
op|'='
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_load_suppressions'
op|'('
name|'pid2filename'
op|'['
name|'pid'
op|']'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                        '
name|'del'
name|'pid2filename'
op|'['
name|'pid'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'fd'
op|','
name|'tmpfilename'
op|'='
name|'mkstemp'
op|'('
op|')'
newline|'\n'
name|'os'
op|'.'
name|'close'
op|'('
name|'fd'
op|')'
newline|'\n'
name|'pid'
op|'='
name|'os'
op|'.'
name|'fork'
op|'('
op|')'
newline|'\n'
name|'if'
name|'pid'
op|':'
newline|'\n'
indent|'                    '
name|'pid2filename'
op|'['
name|'pid'
op|']'
op|'='
name|'tmpfilename'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'patcher'
op|'.'
name|'monkey_patch'
op|'('
name|'all'
op|'='
name|'False'
op|','
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'no_changes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'new_account_suppressions'
op|'='
name|'open'
op|'('
name|'tmpfilename'
op|','
string|"'w'"
op|')'
newline|'\n'
name|'forkbegin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_sweep'
op|'('
name|'path'
op|')'
newline|'\n'
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'forkbegin'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Container update sweep of %(path)s completed: '"
nl|'\n'
string|"'%(elapsed).02fs, %(success)s successes, %(fail)s '"
nl|'\n'
string|"'failures, %(no_change)s with no changes'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'path'"
op|':'
name|'path'
op|','
string|"'elapsed'"
op|':'
name|'elapsed'
op|','
nl|'\n'
string|"'success'"
op|':'
name|'self'
op|'.'
name|'successes'
op|','
string|"'fail'"
op|':'
name|'self'
op|'.'
name|'failures'
op|','
nl|'\n'
string|"'no_change'"
op|':'
name|'self'
op|'.'
name|'no_changes'
op|'}'
op|')'
newline|'\n'
name|'sys'
op|'.'
name|'exit'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'while'
name|'pid2filename'
op|':'
newline|'\n'
indent|'                '
name|'pid'
op|'='
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'_load_suppressions'
op|'('
name|'pid2filename'
op|'['
name|'pid'
op|']'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                    '
name|'del'
name|'pid2filename'
op|'['
name|'pid'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Container update sweep completed: %.02fs'"
op|')'
op|','
nl|'\n'
name|'elapsed'
op|')'
newline|'\n'
name|'if'
name|'elapsed'
op|'<'
name|'self'
op|'.'
name|'interval'
op|':'
newline|'\n'
indent|'                '
name|'time'
op|'.'
name|'sleep'
op|'('
name|'self'
op|'.'
name|'interval'
op|'-'
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
dedent|''
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Run the updater once.\n        """'
newline|'\n'
name|'patcher'
op|'.'
name|'monkey_patch'
op|'('
name|'all'
op|'='
name|'False'
op|','
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Begin container update single threaded sweep'"
op|')'
op|')'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'no_changes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'path'
name|'in'
name|'self'
op|'.'
name|'get_paths'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'container_sweep'
op|'('
name|'path'
op|')'
newline|'\n'
dedent|''
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Container update single threaded sweep completed: '"
nl|'\n'
string|"'%(elapsed).02fs, %(success)s successes, %(fail)s failures, '"
nl|'\n'
string|"'%(no_change)s with no changes'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'elapsed'"
op|':'
name|'elapsed'
op|','
string|"'success'"
op|':'
name|'self'
op|'.'
name|'successes'
op|','
nl|'\n'
string|"'fail'"
op|':'
name|'self'
op|'.'
name|'failures'
op|','
string|"'no_change'"
op|':'
name|'self'
op|'.'
name|'no_changes'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|container_sweep
dedent|''
name|'def'
name|'container_sweep'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Walk the path looking for container DBs and process them.\n\n        :param path: path to walk\n        """'
newline|'\n'
name|'for'
name|'root'
op|','
name|'dirs'
op|','
name|'files'
name|'in'
name|'os'
op|'.'
name|'walk'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'file'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'file'
op|'.'
name|'endswith'
op|'('
string|"'.db'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'process_container'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'root'
op|','
name|'file'
op|')'
op|')'
newline|'\n'
name|'time'
op|'.'
name|'sleep'
op|'('
name|'self'
op|'.'
name|'slowdown'
op|')'
newline|'\n'
nl|'\n'
DECL|member|process_container
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'process_container'
op|'('
name|'self'
op|','
name|'dbfile'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Process a container, and update the information in the account.\n\n        :param dbfile: container DB to process\n        """'
newline|'\n'
name|'broker'
op|'='
name|'ContainerBroker'
op|'('
name|'dbfile'
op|','
name|'logger'
op|'='
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
comment|"# Don't send updates if the container was auto-created since it"
nl|'\n'
comment|"# definitely doesn't have up to date statistics."
nl|'\n'
name|'if'
name|'float'
op|'('
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|')'
op|'<='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'account_suppressions'
op|'.'
name|'get'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|','
number|'0'
op|')'
op|'>'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'if'
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|'>'
name|'info'
op|'['
string|"'reported_put_timestamp'"
op|']'
name|'or'
name|'info'
op|'['
string|"'delete_timestamp'"
op|']'
op|'>'
name|'info'
op|'['
string|"'reported_delete_timestamp'"
op|']'
name|'or'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|'!='
name|'info'
op|'['
string|"'reported_object_count'"
op|']'
name|'or'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|'!='
name|'info'
op|'['
string|"'reported_bytes_used'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'container'
op|'='
string|"'/%s/%s'"
op|'%'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|','
name|'info'
op|'['
string|"'container'"
op|']'
op|')'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'get_account_ring'
op|'('
op|')'
op|'.'
name|'get_nodes'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|')'
newline|'\n'
name|'events'
op|'='
op|'['
name|'spawn'
op|'('
name|'self'
op|'.'
name|'container_report'
op|','
name|'node'
op|','
name|'part'
op|','
name|'container'
op|','
nl|'\n'
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|','
name|'info'
op|'['
string|"'delete_timestamp'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|')'
nl|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|']'
newline|'\n'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'event'
name|'in'
name|'events'
op|':'
newline|'\n'
indent|'                '
name|'if'
number|'200'
op|'<='
name|'event'
op|'.'
name|'wait'
op|'('
op|')'
op|'<'
number|'300'
op|':'
newline|'\n'
indent|'                    '
name|'successes'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'successes'
op|'>'
name|'failures'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'successes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Update report sent for %(container)s %(dbfile)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'container'"
op|':'
name|'container'
op|','
string|"'dbfile'"
op|':'
name|'dbfile'
op|'}'
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'reported'
op|'('
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'delete_timestamp'"
op|']'
op|','
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Update report failed for %(container)s %(dbfile)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'container'"
op|':'
name|'container'
op|','
string|"'dbfile'"
op|':'
name|'dbfile'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_suppressions'
op|'['
name|'info'
op|'['
string|"'account'"
op|']'
op|']'
op|'='
name|'until'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
name|'self'
op|'.'
name|'account_suppression_time'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'new_account_suppressions'
op|':'
newline|'\n'
indent|'                    '
name|'print'
op|'>>'
name|'self'
op|'.'
name|'new_account_suppressions'
op|','
name|'info'
op|'['
string|"'account'"
op|']'
op|','
name|'until'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'no_changes'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|container_report
dedent|''
dedent|''
name|'def'
name|'container_report'
op|'('
name|'self'
op|','
name|'node'
op|','
name|'part'
op|','
name|'container'
op|','
name|'put_timestamp'
op|','
nl|'\n'
name|'delete_timestamp'
op|','
name|'count'
op|','
name|'bytes'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Report container info to an account server.\n\n        :param node: node dictionary from the account ring\n        :param part: partition the account is on\n        :param container: container name\n        :param put_timestamp: put timestamp\n        :param delete_timestamp: delete timestamp\n        :param count: object count in the container\n        :param bytes: bytes used in the container\n        """'
newline|'\n'
name|'with'
name|'ConnectionTimeout'
op|'('
name|'self'
op|'.'
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'='
name|'http_connect'
op|'('
nl|'\n'
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'PUT'"
op|','
name|'container'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Put-Timestamp'"
op|':'
name|'put_timestamp'
op|','
nl|'\n'
string|"'X-Delete-Timestamp'"
op|':'
name|'delete_timestamp'
op|','
nl|'\n'
string|"'X-Object-Count'"
op|':'
name|'count'
op|','
nl|'\n'
string|"'X-Bytes-Used'"
op|':'
name|'bytes'
op|','
nl|'\n'
string|"'X-Account-Override-Deleted'"
op|':'
string|"'yes'"
op|'}'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR account update failed with '"
nl|'\n'
string|"'%(ip)s:%(port)s/%(device)s (will retry later): '"
op|')'
op|','
name|'node'
op|')'
newline|'\n'
name|'return'
number|'500'
newline|'\n'
dedent|''
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'self'
op|'.'
name|'node_timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'.'
name|'status'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'getEffectiveLevel'
op|'('
op|')'
op|'<='
name|'logging'
op|'.'
name|'DEBUG'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception with %(ip)s:%(port)s/%(device)s'"
op|')'
op|','
name|'node'
op|')'
newline|'\n'
dedent|''
name|'return'
number|'500'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
