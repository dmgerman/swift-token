begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
comment|'# Copyright (c) 2010 OpenStack, LLC.'
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
name|'unittest'
newline|'\n'
name|'from'
name|'os'
name|'import'
name|'kill'
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
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'sleep'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'client'
newline|'\n'
name|'from'
name|'common'
name|'import'
name|'get_to_final_state'
op|','
name|'kill_pids'
op|','
name|'reset_environment'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccountFailures
name|'class'
name|'TestAccountFailures'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|setUp
indent|'    '
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'pids'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'account_ring'
op|','
name|'self'
op|'.'
name|'container_ring'
op|','
name|'self'
op|'.'
name|'object_ring'
op|','
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'self'
op|'.'
name|'account'
op|'='
name|'reset_environment'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'kill_pids'
op|'('
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_main
dedent|''
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container1'
op|'='
string|"'container1'"
newline|'\n'
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container1'
op|')'
newline|'\n'
name|'container2'
op|'='
string|"'container2'"
newline|'\n'
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'0'
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'client'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container2'
op|','
string|"'object1'"
op|','
string|"'1234'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'0'
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'1'
op|','
number|'4'
op|')'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'apart'
op|','
name|'anodes'
op|'='
name|'self'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|')'
newline|'\n'
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'anodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
nl|'\n'
name|'client'
op|'.'
name|'delete_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container1'
op|')'
newline|'\n'
name|'client'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container2'
op|','
string|"'object2'"
op|','
string|"'12345'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'1'
op|','
number|'4'
op|')'
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'ps'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'n'
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
name|'ps'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
string|"'/usr/bin/swift-container-updater'"
op|','
nl|'\n'
string|"'/etc/swift/container-server/%d.conf'"
op|'%'
name|'n'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'p'
name|'in'
name|'ps'
op|':'
newline|'\n'
indent|'            '
name|'p'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'2'
op|','
number|'9'
op|')'
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'9'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'anodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'/usr/bin/swift-account-server'"
op|','
nl|'\n'
string|"'/etc/swift/account-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'anodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6002'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'sleep'
op|'('
number|'2'
op|')'
newline|'\n'
comment|'# This is the earlier object count and bytes because the first node'
nl|'\n'
comment|"# doesn't have the newest udpates yet."
nl|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'1'
op|','
number|'4'
op|')'
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
comment|'# This is the earlier count and bytes because the first node'
nl|'\n'
comment|"# doesn't have the newest udpates yet."
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
comment|"# This okay because the first node hasn't got the update that"
nl|'\n'
comment|'# container1 was deleted yet.'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'client'
op|'.'
name|'head_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
op|','
op|'('
number|'2'
op|','
number|'2'
op|','
number|'9'
op|')'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'count'"
op|']'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'9'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
