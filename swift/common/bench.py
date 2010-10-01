begin_unit
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
name|'uuid'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'random'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'urlparse'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
op|'.'
name|'pools'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
op|'.'
name|'httplib'
name|'import'
name|'CannotSendRequest'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'TRUE_VALUES'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
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
nl|'\n'
DECL|class|ConnectionPool
name|'class'
name|'ConnectionPool'
op|'('
name|'eventlet'
op|'.'
name|'pools'
op|'.'
name|'Pool'
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
op|','
name|'url'
op|','
name|'size'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'url'
op|'='
name|'url'
newline|'\n'
name|'eventlet'
op|'.'
name|'pools'
op|'.'
name|'Pool'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'size'
op|','
name|'size'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create
dedent|''
name|'def'
name|'create'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'client'
op|'.'
name|'http_connection'
op|'('
name|'self'
op|'.'
name|'url'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Bench
dedent|''
dedent|''
name|'class'
name|'Bench'
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
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'user'
op|'='
name|'conf'
op|'.'
name|'user'
newline|'\n'
name|'self'
op|'.'
name|'key'
op|'='
name|'conf'
op|'.'
name|'key'
newline|'\n'
name|'self'
op|'.'
name|'auth_url'
op|'='
name|'conf'
op|'.'
name|'auth'
newline|'\n'
name|'self'
op|'.'
name|'use_proxy'
op|'='
name|'conf'
op|'.'
name|'use_proxy'
name|'in'
name|'TRUE_VALUES'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'            '
name|'url'
op|','
name|'token'
op|'='
name|'client'
op|'.'
name|'get_auth'
op|'('
name|'self'
op|'.'
name|'auth_url'
op|','
name|'self'
op|'.'
name|'user'
op|','
name|'self'
op|'.'
name|'key'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'token'
op|'='
name|'token'
newline|'\n'
name|'self'
op|'.'
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
name|'if'
name|'conf'
op|'.'
name|'url'
op|'=='
string|"''"
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'url'
op|'='
name|'url'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'url'
op|'='
name|'conf'
op|'.'
name|'url'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'token'
op|'='
string|"'SlapChop!'"
newline|'\n'
name|'self'
op|'.'
name|'account'
op|'='
name|'conf'
op|'.'
name|'account'
newline|'\n'
name|'self'
op|'.'
name|'url'
op|'='
name|'conf'
op|'.'
name|'url'
newline|'\n'
name|'self'
op|'.'
name|'ip'
op|','
name|'self'
op|'.'
name|'port'
op|'='
name|'self'
op|'.'
name|'url'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
number|'2'
op|']'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'container_name'
op|'='
name|'conf'
op|'.'
name|'container_name'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'object_size'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'object_size'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_sources'
op|'='
name|'conf'
op|'.'
name|'object_sources'
newline|'\n'
name|'self'
op|'.'
name|'files'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'object_sources'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'object_sources'
op|'='
name|'self'
op|'.'
name|'object_sources'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'files'
op|'='
op|'['
name|'file'
op|'('
name|'f'
op|','
string|"'rb'"
op|')'
op|'.'
name|'read'
op|'('
op|')'
name|'for'
name|'f'
name|'in'
name|'self'
op|'.'
name|'object_sources'
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'put_concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'put_concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'get_concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get_concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'del_concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'del_concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_objects'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'num_objects'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_gets'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'num_gets'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'timeout'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'conf'
op|'.'
name|'devices'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'names'
op|'='
name|'names'
newline|'\n'
name|'self'
op|'.'
name|'conn_pool'
op|'='
name|'ConnectionPool'
op|'('
name|'self'
op|'.'
name|'url'
op|','
nl|'\n'
name|'max'
op|'('
name|'self'
op|'.'
name|'put_concurrency'
op|','
name|'self'
op|'.'
name|'get_concurrency'
op|','
nl|'\n'
name|'self'
op|'.'
name|'del_concurrency'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_log_status
dedent|''
name|'def'
name|'_log_status'
op|'('
name|'self'
op|','
name|'title'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'total'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'beginbeat'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'%s %s [%s failures], %.01f/s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'complete'
op|','
name|'title'
op|','
name|'self'
op|'.'
name|'failures'
op|','
nl|'\n'
op|'('
name|'float'
op|'('
name|'self'
op|'.'
name|'complete'
op|')'
op|'/'
name|'total'
op|')'
op|','
nl|'\n'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|connection
name|'def'
name|'connection'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'hc'
op|'='
name|'self'
op|'.'
name|'conn_pool'
op|'.'
name|'get'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'hc'
newline|'\n'
dedent|''
name|'except'
name|'CannotSendRequest'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|'"CannotSendRequest.  Skipping..."'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'hc'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
name|'hc'
op|'='
name|'self'
op|'.'
name|'conn_pool'
op|'.'
name|'create'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'conn_pool'
op|'.'
name|'put'
op|'('
name|'hc'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pool'
op|'='
name|'eventlet'
op|'.'
name|'GreenPool'
op|'('
name|'self'
op|'.'
name|'concurrency'
op|')'
newline|'\n'
name|'events'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'beginbeat'
op|'='
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'heartbeat'
op|'-='
number|'13'
comment|'# just to get the first report quicker'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'complete'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'total'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pool'
op|'.'
name|'spawn_n'
op|'('
name|'self'
op|'.'
name|'_run'
op|','
name|'i'
op|')'
newline|'\n'
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
name|'self'
op|'.'
name|'msg'
op|'+'
string|"' **FINAL**'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchController
dedent|''
dedent|''
name|'class'
name|'BenchController'
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
op|','
name|'logger'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'names'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'delete'
op|'='
name|'conf'
op|'.'
name|'delete'
name|'in'
name|'TRUE_VALUES'
newline|'\n'
name|'self'
op|'.'
name|'gets'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'num_gets'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'puts'
op|'='
name|'BenchPUT'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'puts'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'gets'
op|':'
newline|'\n'
indent|'            '
name|'gets'
op|'='
name|'BenchGET'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'gets'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'delete'
op|':'
newline|'\n'
indent|'            '
name|'dels'
op|'='
name|'BenchDELETE'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'dels'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchDELETE
dedent|''
dedent|''
dedent|''
name|'class'
name|'BenchDELETE'
op|'('
name|'Bench'
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
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Bench'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'self'
op|'.'
name|'del_concurrency'
newline|'\n'
name|'self'
op|'.'
name|'total'
op|'='
name|'len'
op|'('
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
string|"'DEL'"
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'heartbeat'
op|'>='
number|'15'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
string|"'DEL'"
op|')'
newline|'\n'
dedent|''
name|'device'
op|','
name|'partition'
op|','
name|'name'
op|'='
name|'self'
op|'.'
name|'names'
op|'.'
name|'pop'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'connection'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'                    '
name|'client'
op|'.'
name|'delete_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
name|'name'
op|','
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
name|'self'
op|'.'
name|'ip'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'device'
op|'}'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_delete_object'
op|'('
name|'node'
op|','
name|'partition'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'complete'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchGET
dedent|''
dedent|''
name|'class'
name|'BenchGET'
op|'('
name|'Bench'
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
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Bench'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'self'
op|'.'
name|'get_concurrency'
newline|'\n'
name|'self'
op|'.'
name|'total'
op|'='
name|'self'
op|'.'
name|'total_gets'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
string|"'GETS'"
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'heartbeat'
op|'>='
number|'15'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
string|"'GETS'"
op|')'
newline|'\n'
dedent|''
name|'device'
op|','
name|'partition'
op|','
name|'name'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'connection'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'                    '
name|'client'
op|'.'
name|'get_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
name|'name'
op|','
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
name|'self'
op|'.'
name|'ip'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'device'
op|'}'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'node'
op|','
name|'partition'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'complete'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchPUT
dedent|''
dedent|''
name|'class'
name|'BenchPUT'
op|'('
name|'Bench'
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
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Bench'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'self'
op|'.'
name|'put_concurrency'
newline|'\n'
name|'self'
op|'.'
name|'total'
op|'='
name|'self'
op|'.'
name|'total_objects'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
string|"'PUTS'"
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'self'
op|'.'
name|'connection'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'                '
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
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
dedent|''
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'heartbeat'
op|'>='
number|'15'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
string|"'PUTS'"
op|')'
newline|'\n'
dedent|''
name|'name'
op|'='
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|'.'
name|'hex'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'object_sources'
op|':'
newline|'\n'
indent|'            '
name|'source'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'files'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'source'
op|'='
string|"'0'"
op|'*'
name|'self'
op|'.'
name|'object_size'
newline|'\n'
dedent|''
name|'device'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
newline|'\n'
name|'partition'
op|'='
name|'str'
op|'('
name|'random'
op|'.'
name|'randint'
op|'('
number|'1'
op|','
number|'3000'
op|')'
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'connection'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'                    '
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
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
name|'name'
op|','
name|'source'
op|','
nl|'\n'
name|'content_length'
op|'='
name|'len'
op|'('
name|'source'
op|')'
op|','
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
name|'self'
op|'.'
name|'ip'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'device'
op|'}'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_put_object'
op|'('
name|'node'
op|','
name|'partition'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
name|'name'
op|','
name|'source'
op|','
nl|'\n'
name|'content_length'
op|'='
name|'len'
op|'('
name|'source'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'names'
op|'.'
name|'append'
op|'('
op|'('
name|'device'
op|','
name|'partition'
op|','
name|'name'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'complete'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
