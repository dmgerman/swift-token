begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack, LLC.'
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
name|'from'
name|'httplib'
name|'import'
name|'HTTPConnection'
newline|'\n'
name|'from'
name|'os'
name|'import'
name|'kill'
op|','
name|'path'
newline|'\n'
name|'from'
name|'signal'
name|'import'
name|'SIGTERM'
newline|'\n'
name|'from'
name|'subprocess'
name|'import'
name|'Popen'
op|','
name|'PIPE'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'sleep'
op|','
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'get_auth'
op|','
name|'head_account'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'Ring'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
name|'import'
name|'CHECK_SERVER_TIMEOUT'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|start_server
name|'def'
name|'start_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|','
name|'check'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'server'
op|'='
name|'port2server'
op|'['
name|'port'
op|']'
newline|'\n'
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'path'
op|'.'
name|'exists'
op|'('
string|"'/etc/swift/%s-server/%s.conf'"
op|'%'
nl|'\n'
op|'('
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|','
name|'server'
op|'['
op|'-'
number|'1'
op|']'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'pids'
op|'['
name|'server'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-%s-server'"
op|'%'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%s.conf'"
op|'%'
op|'('
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|','
name|'server'
op|'['
op|'-'
number|'1'
op|']'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'if'
name|'check'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'check_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'pids'
op|'['
name|'server'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-%s-server'"
op|'%'
name|'server'
op|','
nl|'\n'
string|"'/etc/swift/%s-server.conf'"
op|'%'
name|'server'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'if'
name|'check'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'check_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_server
dedent|''
name|'def'
name|'check_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|','
name|'timeout'
op|'='
name|'CHECK_SERVER_TIMEOUT'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'server'
op|'='
name|'port2server'
op|'['
name|'port'
op|']'
newline|'\n'
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'int'
op|'('
name|'server'
op|'['
op|'-'
number|'1'
op|']'
op|')'
op|'>'
number|'4'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'path'
op|'='
string|"'/connect/1/2'"
newline|'\n'
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|'=='
string|"'container'"
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'+='
string|"'/3'"
newline|'\n'
dedent|''
name|'elif'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'+='
string|"'/3/4'"
newline|'\n'
dedent|''
name|'try_until'
op|'='
name|'time'
op|'('
op|')'
op|'+'
name|'timeout'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'='
name|'HTTPConnection'
op|'('
string|"'127.0.0.1'"
op|','
name|'port'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'GET'"
op|','
name|'path'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
comment|"# 404 because it's a nonsense path (and mount_check is false)"
nl|'\n'
comment|'# 507 in case the test target is a VM using mount_check'
nl|'\n'
name|'if'
name|'resp'
op|'.'
name|'status'
name|'not'
name|'in'
op|'('
number|'404'
op|','
number|'507'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Unexpected status %s'"
op|'%'
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
dedent|''
name|'break'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'try_until'
op|':'
newline|'\n'
indent|'                    '
name|'print'
name|'err'
newline|'\n'
name|'print'
string|"'Giving up on %s:%s after %s seconds.'"
op|'%'
op|'('
nl|'\n'
name|'server'
op|','
name|'port'
op|','
name|'timeout'
op|')'
newline|'\n'
name|'raise'
name|'err'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'try_until'
op|'='
name|'time'
op|'('
op|')'
op|'+'
name|'timeout'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'url'
op|','
name|'token'
op|'='
name|'get_auth'
op|'('
string|"'http://127.0.0.1:8080/auth/v1.0'"
op|','
nl|'\n'
string|"'test:tester'"
op|','
string|"'testing'"
op|')'
newline|'\n'
name|'account'
op|'='
name|'url'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'head_account'
op|'('
name|'url'
op|','
name|'token'
op|')'
newline|'\n'
name|'return'
name|'url'
op|','
name|'token'
op|','
name|'account'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'try_until'
op|':'
newline|'\n'
indent|'                    '
name|'print'
name|'err'
newline|'\n'
name|'print'
string|"'Giving up on proxy:8080 after 30 seconds.'"
newline|'\n'
name|'raise'
name|'err'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|kill_server
dedent|''
name|'def'
name|'kill_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'kill'
op|'('
name|'pids'
op|'['
name|'port2server'
op|'['
name|'port'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'print'
name|'err'
newline|'\n'
dedent|''
name|'try_until'
op|'='
name|'time'
op|'('
op|')'
op|'+'
number|'30'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'='
name|'HTTPConnection'
op|'('
string|"'127.0.0.1'"
op|','
name|'port'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'GET'"
op|','
string|"'/'"
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'try_until'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Still answering on port %s after 30 seconds'"
op|'%'
name|'port'
op|')'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|kill_servers
dedent|''
dedent|''
name|'def'
name|'kill_servers'
op|'('
name|'port2server'
op|','
name|'pids'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'for'
name|'port'
name|'in'
name|'port2server'
op|':'
newline|'\n'
indent|'        '
name|'kill_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|kill_nonprimary_server
dedent|''
dedent|''
name|'def'
name|'kill_nonprimary_server'
op|'('
name|'primary_nodes'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'primary_ports'
op|'='
op|'['
name|'n'
op|'['
string|"'port'"
op|']'
name|'for'
name|'n'
name|'in'
name|'primary_nodes'
op|']'
newline|'\n'
name|'for'
name|'port'
op|','
name|'server'
name|'in'
name|'port2server'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'port'
name|'in'
name|'primary_ports'
op|':'
newline|'\n'
indent|'            '
name|'server_type'
op|'='
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'Cannot figure out server type for %r'"
op|'%'
name|'primary_nodes'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'port'
op|','
name|'server'
name|'in'
name|'list'
op|'('
name|'port2server'
op|'.'
name|'iteritems'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|'=='
name|'server_type'
name|'and'
name|'port'
name|'not'
name|'in'
name|'primary_ports'
op|':'
newline|'\n'
indent|'            '
name|'kill_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
name|'return'
name|'port'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|reset_environment
dedent|''
dedent|''
dedent|''
name|'def'
name|'reset_environment'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'p'
op|'='
name|'Popen'
op|'('
string|'"resetswift 2>&1"'
op|','
name|'shell'
op|'='
name|'True'
op|','
name|'stdout'
op|'='
name|'PIPE'
op|')'
newline|'\n'
name|'stdout'
op|','
name|'_stderr'
op|'='
name|'p'
op|'.'
name|'communicate'
op|'('
op|')'
newline|'\n'
name|'print'
name|'stdout'
newline|'\n'
name|'pids'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'port2server'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'config_dict'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'server'
op|','
name|'port'
name|'in'
op|'['
op|'('
string|"'account'"
op|','
number|'6002'
op|')'
op|','
op|'('
string|"'container'"
op|','
number|'6001'
op|')'
op|','
nl|'\n'
op|'('
string|"'object'"
op|','
number|'6000'
op|')'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'number'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'9'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'port2server'
op|'['
name|'port'
op|'+'
op|'('
name|'number'
op|'*'
number|'10'
op|')'
op|']'
op|'='
string|"'%s%d'"
op|'%'
op|'('
name|'server'
op|','
name|'number'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'port'
name|'in'
name|'port2server'
op|':'
newline|'\n'
indent|'            '
name|'start_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|','
name|'check'
op|'='
name|'False'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'port'
name|'in'
name|'port2server'
op|':'
newline|'\n'
indent|'            '
name|'check_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
dedent|''
name|'port2server'
op|'['
number|'8080'
op|']'
op|'='
string|"'proxy'"
newline|'\n'
name|'url'
op|','
name|'token'
op|','
name|'account'
op|'='
name|'start_server'
op|'('
number|'8080'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
name|'account_ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift/account.ring.gz'"
op|')'
newline|'\n'
name|'container_ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift/container.ring.gz'"
op|')'
newline|'\n'
name|'object_ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift/object.ring.gz'"
op|')'
newline|'\n'
name|'for'
name|'name'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'server'
name|'in'
op|'('
name|'name'
op|','
string|"'%s-replicator'"
op|'%'
name|'name'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'config_dict'
op|'['
name|'server'
op|']'
op|'='
string|"'/etc/swift/%s-server/%%d.conf'"
op|'%'
name|'name'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
name|'BaseException'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'raise'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'kill_servers'
op|'('
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'pids'
op|','
name|'port2server'
op|','
name|'account_ring'
op|','
name|'container_ring'
op|','
name|'object_ring'
op|','
name|'url'
op|','
name|'token'
op|','
name|'account'
op|','
name|'config_dict'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_to_final_state
dedent|''
name|'def'
name|'get_to_final_state'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'processes'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'job'
name|'in'
op|'('
string|"'account-replicator'"
op|','
string|"'container-replicator'"
op|','
nl|'\n'
string|"'object-replicator'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'number'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'9'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'path'
op|'.'
name|'exists'
op|'('
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'number'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'processes'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-%s'"
op|'%'
name|'job'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'number'
op|')'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'process'
name|'in'
name|'processes'
op|':'
newline|'\n'
indent|'        '
name|'process'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'processes'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'job'
name|'in'
op|'('
string|"'container-updater'"
op|','
string|"'object-updater'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'number'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'5'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'processes'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-%s'"
op|'%'
name|'job'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'number'
op|')'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'process'
name|'in'
name|'processes'
op|':'
newline|'\n'
indent|'        '
name|'process'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'processes'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'job'
name|'in'
op|'('
string|"'account-replicator'"
op|','
string|"'container-replicator'"
op|','
nl|'\n'
string|"'object-replicator'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'number'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'9'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'path'
op|'.'
name|'exists'
op|'('
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'number'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'processes'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-%s'"
op|'%'
name|'job'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'number'
op|')'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'process'
name|'in'
name|'processes'
op|':'
newline|'\n'
indent|'        '
name|'process'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
