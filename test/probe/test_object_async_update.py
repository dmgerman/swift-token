begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
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
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'direct_client'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_pids'
op|','
name|'reset_environment'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectAsyncUpdate
name|'class'
name|'TestObjectAsyncUpdate'
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
name|'container'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
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
name|'container'
op|')'
newline|'\n'
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
name|'anode'
op|'='
name|'anodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'cpart'
op|','
name|'cnodes'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'cnode'
op|'='
name|'cnodes'
op|'['
number|'0'
op|']'
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
name|'cnode'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid4'
op|'('
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
name|'container'
op|','
name|'obj'
op|','
string|"''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'cnode'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-container-server'"
op|','
nl|'\n'
string|"'/etc/swift/container-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'cnode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6001'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'direct_client'
op|'.'
name|'direct_get_container'
op|'('
name|'cnode'
op|','
name|'cpart'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
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
string|"'swift-object-updater'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
name|'n'
op|','
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
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
name|'direct_client'
op|'.'
name|'direct_get_container'
op|'('
name|'cnode'
op|','
nl|'\n'
name|'cpart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'obj'
name|'in'
name|'objs'
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
