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
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
name|'import'
name|'replicator'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'normalize_timestamp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestReplicator
name|'class'
name|'TestReplicator'
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
name|'orig_ring'
op|'='
name|'replicator'
op|'.'
name|'db_replicator'
op|'.'
name|'ring'
op|'.'
name|'Ring'
newline|'\n'
name|'replicator'
op|'.'
name|'db_replicator'
op|'.'
name|'ring'
op|'.'
name|'Ring'
op|'='
name|'lambda'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|':'
name|'None'
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
name|'replicator'
op|'.'
name|'db_replicator'
op|'.'
name|'ring'
op|'.'
name|'Ring'
op|'='
name|'self'
op|'.'
name|'orig_ring'
newline|'\n'
nl|'\n'
DECL|member|test_report_up_to_date
dedent|''
name|'def'
name|'test_report_up_to_date'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'repl'
op|'='
name|'replicator'
op|'.'
name|'ContainerReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'info'
op|'='
op|'{'
string|"'put_timestamp'"
op|':'
name|'normalize_timestamp'
op|'('
number|'1'
op|')'
op|','
nl|'\n'
string|"'delete_timestamp'"
op|':'
name|'normalize_timestamp'
op|'('
number|'0'
op|')'
op|','
nl|'\n'
string|"'object_count'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'bytes_used'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'reported_put_timestamp'"
op|':'
name|'normalize_timestamp'
op|'('
number|'1'
op|')'
op|','
nl|'\n'
string|"'reported_delete_timestamp'"
op|':'
name|'normalize_timestamp'
op|'('
number|'0'
op|')'
op|','
nl|'\n'
string|"'reported_object_count'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'reported_bytes_used'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'delete_timestamp'"
op|']'
op|'='
name|'normalize_timestamp'
op|'('
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'reported_delete_timestamp'"
op|']'
op|'='
name|'normalize_timestamp'
op|'('
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|'='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'reported_object_count'"
op|']'
op|'='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|'='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'reported_bytes_used'"
op|']'
op|'='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|'='
name|'normalize_timestamp'
op|'('
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
op|')'
newline|'\n'
name|'info'
op|'['
string|"'reported_put_timestamp'"
op|']'
op|'='
name|'normalize_timestamp'
op|'('
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'repl'
op|'.'
name|'report_up_to_date'
op|'('
name|'info'
op|')'
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
