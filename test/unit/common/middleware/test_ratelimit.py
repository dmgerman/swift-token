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
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'threading'
name|'import'
name|'Thread'
newline|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeLogger'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'ratelimit'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
name|'import'
name|'get_container_memcache_key'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'memcached'
name|'import'
name|'MemcacheConnectionError'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeMemcache
name|'class'
name|'FakeMemcache'
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
name|'store'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'error_on_incr'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'init_incr_return_neg'
op|'='
name|'False'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
name|'def'
name|'get'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'store'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
newline|'\n'
nl|'\n'
DECL|member|set
dedent|''
name|'def'
name|'set'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'value'
op|','
name|'serialize'
op|'='
name|'False'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|incr
dedent|''
name|'def'
name|'incr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'delta'
op|'='
number|'1'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'error_on_incr'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'MemcacheConnectionError'
op|'('
string|"'Memcache restarting'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'init_incr_return_neg'
op|':'
newline|'\n'
comment|'# simulate initial hit, force reset of memcache'
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'init_incr_return_neg'
op|'='
name|'False'
newline|'\n'
name|'return'
op|'-'
number|'10000000'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'store'
op|'.'
name|'setdefault'
op|'('
name|'key'
op|','
number|'0'
op|')'
op|')'
op|'+'
name|'int'
op|'('
name|'delta'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'return'
name|'int'
op|'('
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|decr
dedent|''
name|'def'
name|'decr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'delta'
op|'='
number|'1'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'incr'
op|'('
name|'key'
op|','
name|'delta'
op|'='
op|'-'
name|'delta'
op|','
name|'timeout'
op|'='
name|'timeout'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|soft_lock
name|'def'
name|'soft_lock'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'0'
op|','
name|'retries'
op|'='
number|'5'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|delete
dedent|''
name|'def'
name|'delete'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|mock_http_connect
dedent|''
dedent|''
name|'def'
name|'mock_http_connect'
op|'('
name|'response'
op|','
name|'headers'
op|'='
name|'None'
op|','
name|'with_exc'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|class|FakeConn
indent|'    '
name|'class'
name|'FakeConn'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'        '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'status'
op|','
name|'headers'
op|','
name|'with_exc'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'status'
op|'='
name|'status'
newline|'\n'
name|'self'
op|'.'
name|'reason'
op|'='
string|"'Fake'"
newline|'\n'
name|'self'
op|'.'
name|'host'
op|'='
string|"'1.2.3.4'"
newline|'\n'
name|'self'
op|'.'
name|'port'
op|'='
string|"'1234'"
newline|'\n'
name|'self'
op|'.'
name|'with_exc'
op|'='
name|'with_exc'
newline|'\n'
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|getresponse
dedent|''
dedent|''
name|'def'
name|'getresponse'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'with_exc'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'test'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|getheader
dedent|''
name|'def'
name|'getheader'
op|'('
name|'self'
op|','
name|'header'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'amt'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"''"
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'lambda'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|':'
name|'FakeConn'
op|'('
name|'response'
op|','
name|'headers'
op|','
name|'with_exc'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
dedent|''
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__call__
indent|'    '
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
string|"'204 No Content'"
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|start_response
dedent|''
dedent|''
name|'def'
name|'start_response'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|dummy_filter_factory
dedent|''
name|'def'
name|'dummy_filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'conf'
op|'='
name|'global_conf'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'.'
name|'update'
op|'('
name|'local_conf'
op|')'
newline|'\n'
nl|'\n'
DECL|function|limit_filter
name|'def'
name|'limit_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ratelimit'
op|'.'
name|'RateLimitMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|','
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'limit_filter'
newline|'\n'
nl|'\n'
DECL|variable|time_ticker
dedent|''
name|'time_ticker'
op|'='
number|'0'
newline|'\n'
DECL|variable|time_override
name|'time_override'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|mock_sleep
name|'def'
name|'mock_sleep'
op|'('
name|'x'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'global'
name|'time_ticker'
newline|'\n'
name|'time_ticker'
op|'+='
name|'x'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|mock_time
dedent|''
name|'def'
name|'mock_time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'global'
name|'time_override'
newline|'\n'
name|'global'
name|'time_ticker'
newline|'\n'
name|'if'
name|'time_override'
op|':'
newline|'\n'
indent|'        '
name|'cur_time'
op|'='
name|'time_override'
op|'.'
name|'pop'
op|'('
number|'0'
op|')'
newline|'\n'
name|'if'
name|'cur_time'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'time_override'
op|'='
op|'['
name|'None'
name|'if'
name|'i'
name|'is'
name|'None'
name|'else'
name|'i'
op|'+'
name|'time_ticker'
nl|'\n'
name|'for'
name|'i'
name|'in'
name|'time_override'
op|']'
newline|'\n'
name|'return'
name|'time_ticker'
newline|'\n'
dedent|''
name|'return'
name|'cur_time'
newline|'\n'
dedent|''
name|'return'
name|'time_ticker'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestRateLimit
dedent|''
name|'class'
name|'TestRateLimit'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|_reset_time
indent|'    '
name|'def'
name|'_reset_time'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'time_ticker'
newline|'\n'
name|'time_ticker'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|setUp
dedent|''
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
name|'was_sleep'
op|'='
name|'eventlet'
op|'.'
name|'sleep'
newline|'\n'
name|'eventlet'
op|'.'
name|'sleep'
op|'='
name|'mock_sleep'
newline|'\n'
name|'self'
op|'.'
name|'was_time'
op|'='
name|'time'
op|'.'
name|'time'
newline|'\n'
name|'time'
op|'.'
name|'time'
op|'='
name|'mock_time'
newline|'\n'
name|'self'
op|'.'
name|'_reset_time'
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
name|'eventlet'
op|'.'
name|'sleep'
op|'='
name|'self'
op|'.'
name|'was_sleep'
newline|'\n'
name|'time'
op|'.'
name|'time'
op|'='
name|'self'
op|'.'
name|'was_time'
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'callable_func'
op|','
name|'num'
op|','
name|'rate'
op|','
name|'check_time'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'time_ticker'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'for'
name|'x'
name|'in'
name|'range'
op|'('
number|'0'
op|','
name|'num'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'result'
op|'='
name|'callable_func'
op|'('
op|')'
newline|'\n'
dedent|''
name|'end'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'total_time'
op|'='
name|'float'
op|'('
name|'num'
op|')'
op|'/'
name|'rate'
op|'-'
number|'1.0'
op|'/'
name|'rate'
comment|"# 1st request isn't limited"
newline|'\n'
comment|'# Allow for one second of variation in the total time.'
nl|'\n'
name|'time_diff'
op|'='
name|'abs'
op|'('
name|'total_time'
op|'-'
op|'('
name|'end'
op|'-'
name|'begin'
op|')'
op|')'
newline|'\n'
name|'if'
name|'check_time'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'round'
op|'('
name|'total_time'
op|','
number|'1'
op|')'
op|','
name|'round'
op|'('
name|'time_ticker'
op|','
number|'1'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'time_diff'
newline|'\n'
nl|'\n'
DECL|member|test_get_container_maxrate
dedent|''
name|'def'
name|'test_get_container_maxrate'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conf_dict'
op|'='
op|'{'
string|"'container_ratelimit_10'"
op|':'
number|'200'
op|','
nl|'\n'
string|"'container_ratelimit_50'"
op|':'
number|'100'
op|','
nl|'\n'
string|"'container_ratelimit_75'"
op|':'
number|'30'
op|'}'
newline|'\n'
name|'test_ratelimit'
op|'='
name|'dummy_filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'test_ratelimit'
op|'.'
name|'get_container_maxrate'
op|'('
number|'0'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'test_ratelimit'
op|'.'
name|'get_container_maxrate'
op|'('
number|'5'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'test_ratelimit'
op|'.'
name|'get_container_maxrate'
op|'('
number|'10'
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'test_ratelimit'
op|'.'
name|'get_container_maxrate'
op|'('
number|'60'
op|')'
op|','
number|'72'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'test_ratelimit'
op|'.'
name|'get_container_maxrate'
op|'('
number|'160'
op|')'
op|','
number|'30'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_ratelimitable_key_tuples
dedent|''
name|'def'
name|'test_get_ratelimitable_key_tuples'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'current_rate'
op|'='
number|'13'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|','
nl|'\n'
string|"'container_ratelimit_3'"
op|':'
number|'200'
op|'}'
newline|'\n'
name|'fake_memcache'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'fake_memcache'
op|'.'
name|'store'
op|'['
name|'get_container_memcache_key'
op|'('
string|"'a'"
op|','
string|"'c'"
op|')'
op|']'
op|'='
op|'{'
string|"'container_size'"
op|':'
number|'5'
op|'}'
newline|'\n'
name|'the_app'
op|'='
name|'ratelimit'
op|'.'
name|'RateLimitMiddleware'
op|'('
name|'None'
op|','
name|'conf_dict'
op|','
nl|'\n'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'the_app'
op|'.'
name|'memcache_client'
op|'='
name|'fake_memcache'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_app'
op|'.'
name|'get_ratelimitable_key_tuples'
op|'('
nl|'\n'
string|"'DELETE'"
op|','
string|"'a'"
op|','
name|'None'
op|','
name|'None'
op|')'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_app'
op|'.'
name|'get_ratelimitable_key_tuples'
op|'('
nl|'\n'
string|"'PUT'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
name|'None'
op|')'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_app'
op|'.'
name|'get_ratelimitable_key_tuples'
op|'('
nl|'\n'
string|"'DELETE'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
name|'None'
op|')'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_app'
op|'.'
name|'get_ratelimitable_key_tuples'
op|'('
nl|'\n'
string|"'GET'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_app'
op|'.'
name|'get_ratelimitable_key_tuples'
op|'('
nl|'\n'
string|"'PUT'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_account_ratelimit
dedent|''
name|'def'
name|'test_account_ratelimit'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'current_rate'
op|'='
number|'5'
newline|'\n'
name|'num_calls'
op|'='
number|'50'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'ratelimit'
op|'.'
name|'filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'for'
name|'meth'
op|','
name|'exp_time'
name|'in'
op|'['
op|'('
string|"'DELETE'"
op|','
number|'9.8'
op|')'
op|','
op|'('
string|"'GET'"
op|','
number|'0'
op|')'
op|','
nl|'\n'
op|'('
string|"'POST'"
op|','
number|'0'
op|')'
op|','
op|'('
string|"'PUT'"
op|','
number|'9.8'
op|')'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a%s/c'"
op|'%'
name|'meth'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
name|'meth'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'make_app_call'
op|'='
name|'lambda'
op|':'
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'start_response'
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
name|'_run'
op|'('
name|'make_app_call'
op|','
name|'num_calls'
op|','
name|'current_rate'
op|','
nl|'\n'
name|'check_time'
op|'='
name|'bool'
op|'('
name|'exp_time'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'round'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|','
number|'1'
op|')'
op|','
name|'exp_time'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_reset_time'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_ratelimit_set_incr
dedent|''
dedent|''
name|'def'
name|'test_ratelimit_set_incr'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'current_rate'
op|'='
number|'5'
newline|'\n'
name|'num_calls'
op|'='
number|'50'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'ratelimit'
op|'.'
name|'filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
string|"'PUT'"
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'.'
name|'init_incr_return_neg'
op|'='
name|'True'
newline|'\n'
name|'make_app_call'
op|'='
name|'lambda'
op|':'
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'start_response'
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
name|'_run'
op|'('
name|'make_app_call'
op|','
name|'num_calls'
op|','
name|'current_rate'
op|','
name|'check_time'
op|'='
name|'False'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'round'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|','
number|'1'
op|')'
op|','
number|'9.8'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_ratelimit_whitelist
dedent|''
name|'def'
name|'test_ratelimit_whitelist'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'time_ticker'
newline|'\n'
name|'current_rate'
op|'='
number|'2'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|','
nl|'\n'
string|"'max_sleep_time_seconds'"
op|':'
number|'2'
op|','
nl|'\n'
string|"'account_whitelist'"
op|':'
string|"'a'"
op|','
nl|'\n'
string|"'account_blacklist'"
op|':'
string|"'b'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'dummy_filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|class|rate_caller
name|'class'
name|'rate_caller'
op|'('
name|'Thread'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'parent'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'Thread'
op|'.'
name|'__init__'
op|'('
name|'self'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'parent'
op|'='
name|'parent'
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
indent|'                '
name|'self'
op|'.'
name|'result'
op|'='
name|'self'
op|'.'
name|'parent'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'nt'
op|'='
number|'5'
newline|'\n'
name|'threads'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
name|'nt'
op|')'
op|':'
newline|'\n'
DECL|variable|rc
indent|'            '
name|'rc'
op|'='
name|'rate_caller'
op|'('
name|'self'
op|')'
newline|'\n'
name|'rc'
op|'.'
name|'start'
op|'('
op|')'
newline|'\n'
name|'threads'
op|'.'
name|'append'
op|'('
name|'rc'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'thread'
name|'in'
name|'threads'
op|':'
newline|'\n'
indent|'            '
name|'thread'
op|'.'
name|'join'
op|'('
op|')'
newline|'\n'
dedent|''
name|'the_498s'
op|'='
op|'['
name|'t'
name|'for'
name|'t'
name|'in'
name|'threads'
name|'if'
string|"''"
op|'.'
name|'join'
op|'('
name|'t'
op|'.'
name|'result'
op|')'
op|'.'
name|'startswith'
op|'('
string|"'Slow down'"
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_498s'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'time_ticker'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_ratelimit_blacklist
dedent|''
name|'def'
name|'test_ratelimit_blacklist'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'time_ticker'
newline|'\n'
name|'current_rate'
op|'='
number|'2'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|','
nl|'\n'
string|"'max_sleep_time_seconds'"
op|':'
number|'2'
op|','
nl|'\n'
string|"'account_whitelist'"
op|':'
string|"'a'"
op|','
nl|'\n'
string|"'account_blacklist'"
op|':'
string|"'b'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'dummy_filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'.'
name|'BLACK_LIST_SLEEP'
op|'='
number|'0'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/b/c'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|class|rate_caller
name|'class'
name|'rate_caller'
op|'('
name|'Thread'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'parent'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'Thread'
op|'.'
name|'__init__'
op|'('
name|'self'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'parent'
op|'='
name|'parent'
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
indent|'                '
name|'self'
op|'.'
name|'result'
op|'='
name|'self'
op|'.'
name|'parent'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'nt'
op|'='
number|'5'
newline|'\n'
name|'threads'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
name|'nt'
op|')'
op|':'
newline|'\n'
DECL|variable|rc
indent|'            '
name|'rc'
op|'='
name|'rate_caller'
op|'('
name|'self'
op|')'
newline|'\n'
name|'rc'
op|'.'
name|'start'
op|'('
op|')'
newline|'\n'
name|'threads'
op|'.'
name|'append'
op|'('
name|'rc'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'thread'
name|'in'
name|'threads'
op|':'
newline|'\n'
indent|'            '
name|'thread'
op|'.'
name|'join'
op|'('
op|')'
newline|'\n'
dedent|''
name|'the_497s'
op|'='
op|'['
name|'t'
name|'for'
name|'t'
name|'in'
name|'threads'
name|'if'
string|"''"
op|'.'
name|'join'
op|'('
name|'t'
op|'.'
name|'result'
op|')'
op|'.'
name|'startswith'
op|'('
string|"'Your account'"
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'the_497s'
op|')'
op|','
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'time_ticker'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_ratelimit_max_rate_double
dedent|''
name|'def'
name|'test_ratelimit_max_rate_double'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'time_ticker'
newline|'\n'
name|'global'
name|'time_override'
newline|'\n'
name|'current_rate'
op|'='
number|'2'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|','
nl|'\n'
string|"'clock_accuracy'"
op|':'
number|'100'
op|','
nl|'\n'
string|"'max_sleep_time_seconds'"
op|':'
number|'1'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'dummy_filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'.'
name|'log_sleep_time_seconds'
op|'='
number|'.00001'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
string|"'PUT'"
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'time_override'
op|'='
op|'['
number|'0'
op|','
number|'0'
op|','
number|'0'
op|','
number|'0'
op|','
name|'None'
op|']'
newline|'\n'
comment|'# simulates 4 requests coming in at same time, then sleeping'
nl|'\n'
name|'r'
op|'='
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'mock_sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
name|'r'
op|'='
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'mock_sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
name|'r'
op|'='
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'['
number|'0'
op|']'
op|','
string|"'Slow down'"
op|')'
newline|'\n'
name|'mock_sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
name|'r'
op|'='
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'['
number|'0'
op|']'
op|','
string|"'Slow down'"
op|')'
newline|'\n'
name|'mock_sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
name|'r'
op|'='
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'['
number|'0'
op|']'
op|','
string|"'204 No Content'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_ratelimit_max_rate_multiple_acc
dedent|''
name|'def'
name|'test_ratelimit_max_rate_multiple_acc'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'num_calls'
op|'='
number|'4'
newline|'\n'
name|'current_rate'
op|'='
number|'2'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|','
nl|'\n'
string|"'max_sleep_time_seconds'"
op|':'
number|'2'
op|'}'
newline|'\n'
name|'fake_memcache'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'the_app'
op|'='
name|'ratelimit'
op|'.'
name|'RateLimitMiddleware'
op|'('
name|'None'
op|','
name|'conf_dict'
op|','
nl|'\n'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'the_app'
op|'.'
name|'memcache_client'
op|'='
name|'fake_memcache'
newline|'\n'
name|'req'
op|'='
name|'lambda'
op|':'
name|'None'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
string|"'PUT'"
newline|'\n'
nl|'\n'
DECL|class|rate_caller
name|'class'
name|'rate_caller'
op|'('
name|'Thread'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'name'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'myname'
op|'='
name|'name'
newline|'\n'
name|'Thread'
op|'.'
name|'__init__'
op|'('
name|'self'
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
indent|'                '
name|'for'
name|'j'
name|'in'
name|'range'
op|'('
name|'num_calls'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'result'
op|'='
name|'the_app'
op|'.'
name|'handle_ratelimit'
op|'('
name|'req'
op|','
name|'self'
op|'.'
name|'myname'
op|','
nl|'\n'
string|"'c'"
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'nt'
op|'='
number|'15'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'threads'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
name|'nt'
op|')'
op|':'
newline|'\n'
DECL|variable|rc
indent|'            '
name|'rc'
op|'='
name|'rate_caller'
op|'('
string|"'a%s'"
op|'%'
name|'i'
op|')'
newline|'\n'
name|'rc'
op|'.'
name|'start'
op|'('
op|')'
newline|'\n'
name|'threads'
op|'.'
name|'append'
op|'('
name|'rc'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'thread'
name|'in'
name|'threads'
op|':'
newline|'\n'
indent|'            '
name|'thread'
op|'.'
name|'join'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'time_took'
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
name|'assertEquals'
op|'('
number|'1.5'
op|','
name|'round'
op|'('
name|'time_took'
op|','
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_call_invalid_path
dedent|''
name|'def'
name|'test_call_invalid_path'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'SCRIPT_NAME'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'PATH_INFO'"
op|':'
string|"'//v1/AUTH_1234567890'"
op|','
nl|'\n'
string|"'SERVER_NAME'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'SERVER_PORT'"
op|':'
string|"'80'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'FakeMemcache'
op|'('
op|')'
op|','
nl|'\n'
string|"'SERVER_PROTOCOL'"
op|':'
string|"'HTTP/1.0'"
op|'}'
newline|'\n'
nl|'\n'
name|'app'
op|'='
name|'lambda'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|':'
op|'['
string|"'fake_app'"
op|']'
newline|'\n'
name|'rate_mid'
op|'='
name|'ratelimit'
op|'.'
name|'RateLimitMiddleware'
op|'('
name|'app'
op|','
op|'{'
op|'}'
op|','
nl|'\n'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|class|a_callable
name|'class'
name|'a_callable'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__call__
indent|'            '
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'rate_mid'
op|'.'
name|'__call__'
op|'('
name|'env'
op|','
name|'a_callable'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'fake_app'"
op|'=='
name|'resp'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_no_memcache
dedent|''
name|'def'
name|'test_no_memcache'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'current_rate'
op|'='
number|'13'
newline|'\n'
name|'num_calls'
op|'='
number|'5'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'ratelimit'
op|'.'
name|'filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'None'
newline|'\n'
name|'make_app_call'
op|'='
name|'lambda'
op|':'
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'start_response'
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
name|'_run'
op|'('
name|'make_app_call'
op|','
name|'num_calls'
op|','
name|'current_rate'
op|','
name|'check_time'
op|'='
name|'False'
op|')'
newline|'\n'
name|'time_took'
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
name|'assertEquals'
op|'('
name|'round'
op|'('
name|'time_took'
op|','
number|'1'
op|')'
op|','
number|'0'
op|')'
comment|'# no memcache, no limiting'
newline|'\n'
nl|'\n'
DECL|member|test_restarting_memcache
dedent|''
name|'def'
name|'test_restarting_memcache'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'current_rate'
op|'='
number|'2'
newline|'\n'
name|'num_calls'
op|'='
number|'5'
newline|'\n'
name|'conf_dict'
op|'='
op|'{'
string|"'account_ratelimit'"
op|':'
name|'current_rate'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'test_ratelimit'
op|'='
name|'ratelimit'
op|'.'
name|'filter_factory'
op|'('
name|'conf_dict'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'ratelimit'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
string|"'PUT'"
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'.'
name|'error_on_incr'
op|'='
name|'True'
newline|'\n'
name|'make_app_call'
op|'='
name|'lambda'
op|':'
name|'self'
op|'.'
name|'test_ratelimit'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'start_response'
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
name|'_run'
op|'('
name|'make_app_call'
op|','
name|'num_calls'
op|','
name|'current_rate'
op|','
name|'check_time'
op|'='
name|'False'
op|')'
newline|'\n'
name|'time_took'
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
name|'assertEquals'
op|'('
name|'round'
op|'('
name|'time_took'
op|','
number|'1'
op|')'
op|','
number|'0'
op|')'
comment|'# no memcache, no limiting'
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
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
