begin_unit
comment|'# Copyright (c) 2011 OpenStack, LLC.'
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
name|'json'
newline|'\n'
name|'from'
name|'sys'
name|'import'
name|'exc_info'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'unittest'
name|'import'
name|'main'
op|','
name|'TestCase'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'internal_client'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'expirer'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'server'
name|'import'
name|'Application'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|not_random
name|'def'
name|'not_random'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'return'
number|'0.5'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|last_not_sleep
dedent|''
name|'last_not_sleep'
op|'='
number|'0'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|not_sleep
name|'def'
name|'not_sleep'
op|'('
name|'seconds'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'global'
name|'last_not_sleep'
newline|'\n'
name|'last_not_sleep'
op|'='
name|'seconds'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MockLogger
dedent|''
name|'class'
name|'MockLogger'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'debugs'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'infos'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'exceptions'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|member|debug
dedent|''
name|'def'
name|'debug'
op|'('
name|'self'
op|','
name|'msg'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'debugs'
op|'.'
name|'append'
op|'('
name|'msg'
op|')'
newline|'\n'
nl|'\n'
DECL|member|info
dedent|''
name|'def'
name|'info'
op|'('
name|'self'
op|','
name|'msg'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'infos'
op|'.'
name|'append'
op|'('
name|'msg'
op|')'
newline|'\n'
nl|'\n'
DECL|member|exception
dedent|''
name|'def'
name|'exception'
op|'('
name|'self'
op|','
name|'msg'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'exceptions'
op|'.'
name|'append'
op|'('
string|"'%s: %s'"
op|'%'
op|'('
name|'msg'
op|','
name|'exc_info'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectExpirer
dedent|''
dedent|''
name|'class'
name|'TestObjectExpirer'
op|'('
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
name|'global'
name|'not_sleep'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'old_loadapp'
op|'='
name|'internal_client'
op|'.'
name|'loadapp'
newline|'\n'
name|'self'
op|'.'
name|'old_sleep'
op|'='
name|'internal_client'
op|'.'
name|'sleep'
newline|'\n'
nl|'\n'
name|'internal_client'
op|'.'
name|'loadapp'
op|'='
name|'lambda'
name|'x'
op|':'
name|'None'
newline|'\n'
name|'internal_client'
op|'.'
name|'sleep'
op|'='
name|'not_sleep'
newline|'\n'
nl|'\n'
DECL|member|teardown
dedent|''
name|'def'
name|'teardown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'internal_client'
op|'.'
name|'sleep'
op|'='
name|'self'
op|'.'
name|'old_sleep'
newline|'\n'
name|'internal_client'
op|'.'
name|'loadapp'
op|'='
name|'self'
op|'.'
name|'loadapp'
newline|'\n'
nl|'\n'
DECL|member|test_report
dedent|''
name|'def'
name|'test_report'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'='
op|'['
op|']'
newline|'\n'
name|'x'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'='
op|'['
op|']'
newline|'\n'
name|'x'
op|'.'
name|'report'
op|'('
name|'final'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'completed'"
name|'in'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'['
op|'-'
number|'1'
op|']'
op|','
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'so far'"
name|'not'
name|'in'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'['
op|'-'
number|'1'
op|']'
op|','
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|')'
newline|'\n'
nl|'\n'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'='
op|'['
op|']'
newline|'\n'
name|'x'
op|'.'
name|'report_last_time'
op|'='
name|'time'
op|'('
op|')'
op|'-'
name|'x'
op|'.'
name|'report_interval'
newline|'\n'
name|'x'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'completed'"
name|'not'
name|'in'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'['
op|'-'
number|'1'
op|']'
op|','
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'so far'"
name|'in'
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|'['
op|'-'
number|'1'
op|']'
op|','
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run_once_nothing_to_do
dedent|''
name|'def'
name|'test_run_once_nothing_to_do'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
string|"'throw error because a string does not have needed methods'"
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
nl|'\n'
op|'['
string|'"Unhandled exception: \'str\' object has no attribute "'
nl|'\n'
string|'"\'get_account_info\'"'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run_once_calls_report
dedent|''
name|'def'
name|'test_run_once_calls_report'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|InternalClient
indent|'        '
name|'class'
name|'InternalClient'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|get_account_info
indent|'            '
name|'def'
name|'get_account_info'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
number|'1'
op|','
number|'2'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
nl|'\n'
op|'['
string|"'Pass beginning; 1 possible containers; 2 possible objects'"
op|','
nl|'\n'
string|"'Pass completed in 0s; 0 objects expired'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_container_timestamp_break
dedent|''
name|'def'
name|'test_container_timestamp_break'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|InternalClient
indent|'        '
name|'class'
name|'InternalClient'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'containers'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'containers'
op|'='
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
number|'1'
op|','
number|'2'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|iter_objects
dedent|''
name|'def'
name|'iter_objects'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'This should not have been called'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'+'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
nl|'\n'
op|'['
string|"'Pass beginning; 1 possible containers; 2 possible objects'"
op|','
nl|'\n'
string|"'Pass completed in 0s; 0 objects expired'"
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# Reverse test to be sure it still would blow up the way expected.'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
nl|'\n'
op|'['
string|"'Unhandled exception: This should not have been called'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_timestamp_break
dedent|''
name|'def'
name|'test_object_timestamp_break'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|InternalClient
indent|'        '
name|'class'
name|'InternalClient'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'containers'
op|','
name|'objects'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'containers'
op|'='
name|'containers'
newline|'\n'
name|'self'
op|'.'
name|'objects'
op|'='
name|'objects'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
number|'1'
op|','
number|'2'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|delete_container
dedent|''
name|'def'
name|'delete_container'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|iter_objects
dedent|''
name|'def'
name|'iter_objects'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'objects'
newline|'\n'
nl|'\n'
DECL|function|should_not_be_called
dedent|''
dedent|''
name|'def'
name|'should_not_be_called'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'This should not have been called'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|','
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'%d-actual-obj'"
op|'%'
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'+'
number|'86400'
op|')'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'='
name|'should_not_be_called'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
nl|'\n'
op|'['
string|"'Pass beginning; 1 possible containers; 2 possible objects'"
op|','
nl|'\n'
string|"'Pass completed in 0s; 0 objects expired'"
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# Reverse test to be sure it still would blow up the way expected.'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'ts'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|','
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'%d-actual-obj'"
op|'%'
name|'ts'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'='
name|'should_not_be_called'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
string|"'Exception while deleting '"
nl|'\n'
string|"'object %d %d-actual-obj This should not have been called: This '"
nl|'\n'
string|"'should not have been called'"
op|'%'
op|'('
name|'ts'
op|','
name|'ts'
op|')'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_failed_delete_keeps_entry
dedent|''
name|'def'
name|'test_failed_delete_keeps_entry'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|InternalClient
indent|'        '
name|'class'
name|'InternalClient'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'containers'
op|','
name|'objects'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'containers'
op|'='
name|'containers'
newline|'\n'
name|'self'
op|'.'
name|'objects'
op|'='
name|'objects'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
number|'1'
op|','
number|'2'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|delete_container
dedent|''
name|'def'
name|'delete_container'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|delete_object
dedent|''
name|'def'
name|'delete_object'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'This should not have been called'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|iter_objects
dedent|''
name|'def'
name|'iter_objects'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'objects'
newline|'\n'
nl|'\n'
DECL|function|deliberately_blow_up
dedent|''
dedent|''
name|'def'
name|'deliberately_blow_up'
op|'('
name|'actual_obj'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'failed to delete actual object'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|should_not_get_called
dedent|''
name|'def'
name|'should_not_get_called'
op|'('
name|'container'
op|','
name|'obj'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'This should not have been called'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'iter_containers'
op|'='
name|'lambda'
op|':'
op|'['
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|']'
newline|'\n'
name|'ts'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'='
name|'deliberately_blow_up'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|','
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'%d-actual-obj'"
op|'%'
name|'ts'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
string|"'Exception while deleting '"
nl|'\n'
string|"'object %d %d-actual-obj failed to delete actual object: failed '"
nl|'\n'
string|"'to delete actual object'"
op|'%'
op|'('
name|'ts'
op|','
name|'ts'
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
nl|'\n'
op|'['
string|"'Pass beginning; 1 possible containers; 2 possible objects'"
op|','
nl|'\n'
string|"'Pass completed in 0s; 0 objects expired'"
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# Reverse test to be sure it still would blow up the way expected.'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'ts'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'='
name|'lambda'
name|'o'
op|','
name|'t'
op|':'
name|'None'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|','
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'%d-actual-obj'"
op|'%'
name|'ts'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
string|"'Exception while deleting '"
nl|'\n'
string|"'object %d %d-actual-obj This should not have been called: This '"
nl|'\n'
string|"'should not have been called'"
op|'%'
op|'('
name|'ts'
op|','
name|'ts'
op|')'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_success_gets_counted
dedent|''
name|'def'
name|'test_success_gets_counted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|InternalClient
indent|'        '
name|'class'
name|'InternalClient'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'containers'
op|','
name|'objects'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'containers'
op|'='
name|'containers'
newline|'\n'
name|'self'
op|'.'
name|'objects'
op|'='
name|'objects'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
number|'1'
op|','
number|'2'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|delete_container
dedent|''
name|'def'
name|'delete_container'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|delete_object
dedent|''
name|'def'
name|'delete_object'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|iter_objects
dedent|''
name|'def'
name|'iter_objects'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'objects'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'='
name|'lambda'
name|'o'
op|','
name|'t'
op|':'
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'report_objects'
op|','
number|'0'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
op|'['
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|')'
op|'}'
op|']'
op|','
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'%d-actual-obj'"
op|'%'
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
op|'}'
op|']'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'report_objects'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
nl|'\n'
op|'['
string|"'Pass beginning; 1 possible containers; 2 possible objects'"
op|','
nl|'\n'
string|"'Pass completed in 0s; 1 objects expired'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_failed_delete_continues_on
dedent|''
name|'def'
name|'test_failed_delete_continues_on'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|InternalClient
indent|'        '
name|'class'
name|'InternalClient'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'containers'
op|','
name|'objects'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'containers'
op|'='
name|'containers'
newline|'\n'
name|'self'
op|'.'
name|'objects'
op|'='
name|'objects'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
number|'1'
op|','
number|'2'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|delete_container
dedent|''
name|'def'
name|'delete_container'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'failed to delete container'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete_object
dedent|''
name|'def'
name|'delete_object'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|iter_objects
dedent|''
name|'def'
name|'iter_objects'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'objects'
newline|'\n'
nl|'\n'
DECL|function|fail_delete_actual_object
dedent|''
dedent|''
name|'def'
name|'fail_delete_actual_object'
op|'('
name|'actual_obj'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'failed to delete actual object'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'cts'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
newline|'\n'
name|'ots'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'86400'
op|')'
newline|'\n'
nl|'\n'
name|'containers'
op|'='
op|'['
nl|'\n'
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'cts'
op|')'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
name|'str'
op|'('
name|'cts'
op|'+'
number|'1'
op|')'
op|'}'
op|','
nl|'\n'
op|']'
newline|'\n'
nl|'\n'
name|'objects'
op|'='
op|'['
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'%d-actual-obj'"
op|'%'
name|'ots'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'%d-next-obj'"
op|'%'
name|'ots'
op|'}'
nl|'\n'
op|']'
newline|'\n'
nl|'\n'
name|'x'
op|'.'
name|'swift'
op|'='
name|'InternalClient'
op|'('
name|'containers'
op|','
name|'objects'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'='
name|'fail_delete_actual_object'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
op|'['
nl|'\n'
string|"'Exception while deleting object %d %d-actual-obj failed to '"
nl|'\n'
string|"'delete actual object: failed to delete actual object'"
op|'%'
nl|'\n'
op|'('
name|'cts'
op|','
name|'ots'
op|')'
op|','
nl|'\n'
string|"'Exception while deleting object %d %d-next-obj failed to delete '"
nl|'\n'
string|"'actual object: failed to delete actual object'"
op|'%'
op|'('
name|'cts'
op|','
name|'ots'
op|')'
op|','
nl|'\n'
string|"'Exception while deleting container %d failed to delete '"
nl|'\n'
string|"'container: failed to delete container'"
op|'%'
name|'cts'
op|','
nl|'\n'
string|"'Exception while deleting object %d %d-actual-obj failed to '"
nl|'\n'
string|"'delete actual object: failed to delete actual object'"
op|'%'
nl|'\n'
op|'('
name|'cts'
op|'+'
number|'1'
op|','
name|'ots'
op|')'
op|','
nl|'\n'
string|"'Exception while deleting object %d %d-next-obj failed to delete '"
nl|'\n'
string|"'actual object: failed to delete actual object'"
op|'%'
op|'('
name|'cts'
op|'+'
number|'1'
op|','
name|'ots'
op|')'
op|','
nl|'\n'
string|"'Exception while deleting container %d failed to delete '"
nl|'\n'
string|"'container: failed to delete container'"
op|'%'
op|'('
name|'cts'
op|'+'
number|'1'
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'infos'
op|','
nl|'\n'
op|'['
string|"'Pass beginning; 1 possible containers; 2 possible objects'"
op|','
nl|'\n'
string|"'Pass completed in 0s; 0 objects expired'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run_forever_initial_sleep_random
dedent|''
name|'def'
name|'test_run_forever_initial_sleep_random'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'last_not_sleep'
newline|'\n'
nl|'\n'
DECL|function|raise_system_exit
name|'def'
name|'raise_system_exit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'SystemExit'
op|'('
string|"'test_run_forever'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'interval'
op|'='
number|'1234'
newline|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
string|"'__file__'"
op|':'
string|"'unit_test'"
op|','
nl|'\n'
string|"'interval'"
op|':'
name|'interval'
op|'}'
op|')'
newline|'\n'
name|'orig_random'
op|'='
name|'expirer'
op|'.'
name|'random'
newline|'\n'
name|'orig_sleep'
op|'='
name|'expirer'
op|'.'
name|'sleep'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'expirer'
op|'.'
name|'random'
op|'='
name|'not_random'
newline|'\n'
name|'expirer'
op|'.'
name|'sleep'
op|'='
name|'not_sleep'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'='
name|'raise_system_exit'
newline|'\n'
name|'x'
op|'.'
name|'run_forever'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'SystemExit'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'expirer'
op|'.'
name|'random'
op|'='
name|'orig_random'
newline|'\n'
name|'expirer'
op|'.'
name|'sleep'
op|'='
name|'orig_sleep'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'str'
op|'('
name|'err'
op|')'
op|','
string|"'test_run_forever'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'last_not_sleep'
op|','
number|'0.5'
op|'*'
name|'interval'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run_forever_catches_usual_exceptions
dedent|''
name|'def'
name|'test_run_forever_catches_usual_exceptions'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raises'
op|'='
op|'['
number|'0'
op|']'
newline|'\n'
nl|'\n'
DECL|function|raise_exceptions
name|'def'
name|'raise_exceptions'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raises'
op|'['
number|'0'
op|']'
op|'+='
number|'1'
newline|'\n'
name|'if'
name|'raises'
op|'['
number|'0'
op|']'
op|'<'
number|'2'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'exception %d'"
op|'%'
name|'raises'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'raise'
name|'SystemExit'
op|'('
string|"'exiting exception %d'"
op|'%'
name|'raises'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'logger'
op|'='
name|'MockLogger'
op|'('
op|')'
newline|'\n'
name|'orig_sleep'
op|'='
name|'expirer'
op|'.'
name|'sleep'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'expirer'
op|'.'
name|'sleep'
op|'='
name|'not_sleep'
newline|'\n'
name|'x'
op|'.'
name|'run_once'
op|'='
name|'raise_exceptions'
newline|'\n'
name|'x'
op|'.'
name|'run_forever'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'SystemExit'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'expirer'
op|'.'
name|'sleep'
op|'='
name|'orig_sleep'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'str'
op|'('
name|'err'
op|')'
op|','
string|"'exiting exception 2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'x'
op|'.'
name|'logger'
op|'.'
name|'exceptions'
op|','
nl|'\n'
op|'['
string|"'Unhandled exception: exception 1'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_actual_object
dedent|''
name|'def'
name|'test_delete_actual_object'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'got_env'
op|'='
op|'['
name|'None'
op|']'
newline|'\n'
nl|'\n'
DECL|function|fake_app
name|'def'
name|'fake_app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'got_env'
op|'['
number|'0'
op|']'
op|'='
name|'env'
newline|'\n'
name|'start_response'
op|'('
string|"'204 No Content'"
op|','
op|'['
op|'('
string|"'Content-Length'"
op|','
string|"'0'"
op|')'
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'internal_client'
op|'.'
name|'loadapp'
op|'='
name|'lambda'
name|'x'
op|':'
name|'fake_app'
newline|'\n'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'ts'
op|'='
string|"'1234'"
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'('
string|"'/path/to/object'"
op|','
name|'ts'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'got_env'
op|'['
number|'0'
op|']'
op|'['
string|"'HTTP_X_IF_DELETE_AT'"
op|']'
op|','
name|'ts'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_actual_object_handles_404
dedent|''
name|'def'
name|'test_delete_actual_object_handles_404'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|fake_app
indent|'        '
name|'def'
name|'fake_app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
string|"'404 Not Found'"
op|','
op|'['
op|'('
string|"'Content-Length'"
op|','
string|"'0'"
op|')'
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'internal_client'
op|'.'
name|'loadapp'
op|'='
name|'lambda'
name|'x'
op|':'
name|'fake_app'
newline|'\n'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'('
string|"'/path/to/object'"
op|','
string|"'1234'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_actual_object_handles_412
dedent|''
name|'def'
name|'test_delete_actual_object_handles_412'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|fake_app
indent|'        '
name|'def'
name|'fake_app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
string|"'412 Precondition Failed'"
op|','
nl|'\n'
op|'['
op|'('
string|"'Content-Length'"
op|','
string|"'0'"
op|')'
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'internal_client'
op|'.'
name|'loadapp'
op|'='
name|'lambda'
name|'x'
op|':'
name|'fake_app'
newline|'\n'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'x'
op|'.'
name|'delete_actual_object'
op|'('
string|"'/path/to/object'"
op|','
string|"'1234'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_actual_object_does_not_handle_odd_stuff
dedent|''
name|'def'
name|'test_delete_actual_object_does_not_handle_odd_stuff'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|fake_app
indent|'        '
name|'def'
name|'fake_app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
string|"'503 Internal Server Error'"
op|','
nl|'\n'
op|'['
op|'('
string|"'Content-Length'"
op|','
string|"'0'"
op|')'
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'internal_client'
op|'.'
name|'loadapp'
op|'='
name|'lambda'
name|'x'
op|':'
name|'fake_app'
newline|'\n'
nl|'\n'
name|'x'
op|'='
name|'expirer'
op|'.'
name|'ObjectExpirer'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'x'
op|'.'
name|'delete_actual_object'
op|'('
string|"'/path/to/object'"
op|','
string|"'1234'"
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
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
number|'503'
op|','
name|'exc'
op|'.'
name|'resp'
op|'.'
name|'status_int'
op|')'
newline|'\n'
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
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
