begin_unit
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
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
op|','
name|'Response'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
op|','
name|'cache_from_env'
op|','
name|'get_logger'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'server'
name|'import'
name|'get_container_memcache_key'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MaxSleepTimeHit
name|'class'
name|'MaxSleepTimeHit'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|RateLimitMiddleware
dedent|''
name|'class'
name|'RateLimitMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Rate limiting middleware\n\n    Rate limits requests on both an Account and Container level.  Limits are\n    configurable.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'conf'
op|','
name|'logger'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
name|'if'
name|'logger'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'account_ratelimit'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'account_ratelimit'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_sleep_time_seconds'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_sleep_time_seconds'"
op|','
nl|'\n'
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'clock_accuracy'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'clock_accuracy'"
op|','
number|'1000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ratelimit_whitelist'
op|'='
op|'['
name|'acc'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'acc'
name|'in'
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'account_whitelist'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
nl|'\n'
name|'if'
name|'acc'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'ratelimit_blacklist'
op|'='
op|'['
name|'acc'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'acc'
name|'in'
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'account_blacklist'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
nl|'\n'
name|'if'
name|'acc'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'memcache_client'
op|'='
name|'None'
newline|'\n'
name|'conf_limits'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'conf_key'
name|'in'
name|'conf'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'conf_key'
op|'.'
name|'startswith'
op|'('
string|"'container_ratelimit_'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'cont_size'
op|'='
name|'int'
op|'('
name|'conf_key'
op|'['
name|'len'
op|'('
string|"'container_ratelimit_'"
op|')'
op|':'
op|']'
op|')'
newline|'\n'
name|'rate'
op|'='
name|'float'
op|'('
name|'conf'
op|'['
name|'conf_key'
op|']'
op|')'
newline|'\n'
name|'conf_limits'
op|'.'
name|'append'
op|'('
op|'('
name|'cont_size'
op|','
name|'rate'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'conf_limits'
op|'.'
name|'sort'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ratelimits'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'conf_limits'
op|':'
newline|'\n'
indent|'            '
name|'cur_size'
op|','
name|'cur_rate'
op|'='
name|'conf_limits'
op|'.'
name|'pop'
op|'('
number|'0'
op|')'
newline|'\n'
name|'if'
name|'conf_limits'
op|':'
newline|'\n'
indent|'                '
name|'next_size'
op|','
name|'next_rate'
op|'='
name|'conf_limits'
op|'['
number|'0'
op|']'
newline|'\n'
name|'slope'
op|'='
op|'('
name|'float'
op|'('
name|'next_rate'
op|')'
op|'-'
name|'float'
op|'('
name|'cur_rate'
op|')'
op|')'
op|'/'
op|'('
name|'next_size'
op|'-'
name|'cur_size'
op|')'
newline|'\n'
nl|'\n'
DECL|function|new_scope
name|'def'
name|'new_scope'
op|'('
name|'cur_size'
op|','
name|'slope'
op|','
name|'cur_rate'
op|')'
op|':'
newline|'\n'
comment|'# making new scope for variables'
nl|'\n'
indent|'                    '
name|'return'
name|'lambda'
name|'x'
op|':'
op|'('
name|'x'
op|'-'
name|'cur_size'
op|')'
op|'*'
name|'slope'
op|'+'
name|'cur_rate'
newline|'\n'
dedent|''
name|'line_func'
op|'='
name|'new_scope'
op|'('
name|'cur_size'
op|','
name|'slope'
op|','
name|'cur_rate'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'line_func'
op|'='
name|'lambda'
name|'x'
op|':'
name|'cur_rate'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'container_ratelimits'
op|'.'
name|'append'
op|'('
op|'('
name|'cur_size'
op|','
name|'cur_rate'
op|','
name|'line_func'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_container_maxrate
dedent|''
dedent|''
name|'def'
name|'get_container_maxrate'
op|'('
name|'self'
op|','
name|'container_size'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns number of requests allowed per second for given container size.\n        """'
newline|'\n'
name|'last_func'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'container_size'
op|':'
newline|'\n'
indent|'            '
name|'container_size'
op|'='
name|'int'
op|'('
name|'container_size'
op|')'
newline|'\n'
name|'for'
name|'size'
op|','
name|'rate'
op|','
name|'func'
name|'in'
name|'self'
op|'.'
name|'container_ratelimits'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'container_size'
op|'<'
name|'size'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'last_func'
op|'='
name|'func'
newline|'\n'
dedent|''
name|'if'
name|'last_func'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'last_func'
op|'('
name|'container_size'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_ratelimitable_key_tuples
dedent|''
name|'def'
name|'get_ratelimitable_key_tuples'
op|'('
name|'self'
op|','
name|'req_method'
op|','
name|'account_name'
op|','
nl|'\n'
name|'container_name'
op|'='
name|'None'
op|','
nl|'\n'
name|'obj_name'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns a list of key (used in memcache), ratelimit tuples. Keys\n        should be checked in order.\n\n        :param req_method: HTTP method\n        :param account_name: account name from path\n        :param container_name: container name from path\n        :param obj_name: object name from path\n        """'
newline|'\n'
name|'keys'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'account_ratelimit'
name|'and'
name|'account_name'
name|'and'
op|'('
nl|'\n'
name|'not'
op|'('
name|'container_name'
name|'or'
name|'obj_name'
op|')'
name|'or'
nl|'\n'
op|'('
name|'container_name'
name|'and'
name|'not'
name|'obj_name'
name|'and'
name|'req_method'
op|'=='
string|"'PUT'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'keys'
op|'.'
name|'append'
op|'('
op|'('
string|'"ratelimit/%s"'
op|'%'
name|'account_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account_ratelimit'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'account_name'
name|'and'
name|'container_name'
name|'and'
op|'('
nl|'\n'
op|'('
name|'not'
name|'obj_name'
name|'and'
name|'req_method'
name|'in'
op|'('
string|"'GET'"
op|','
string|"'HEAD'"
op|')'
op|')'
name|'or'
nl|'\n'
op|'('
name|'obj_name'
name|'and'
name|'req_method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'DELETE'"
op|')'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'container_size'
op|'='
name|'None'
newline|'\n'
name|'memcache_key'
op|'='
name|'get_container_memcache_key'
op|'('
name|'account_name'
op|','
nl|'\n'
name|'container_name'
op|')'
newline|'\n'
name|'container_info'
op|'='
name|'self'
op|'.'
name|'memcache_client'
op|'.'
name|'get'
op|'('
name|'memcache_key'
op|')'
newline|'\n'
name|'if'
name|'type'
op|'('
name|'container_info'
op|')'
op|'=='
name|'dict'
op|':'
newline|'\n'
indent|'                '
name|'container_size'
op|'='
name|'container_info'
op|'.'
name|'get'
op|'('
string|"'container_size'"
op|','
number|'0'
op|')'
newline|'\n'
name|'container_rate'
op|'='
name|'self'
op|'.'
name|'get_container_maxrate'
op|'('
name|'container_size'
op|')'
newline|'\n'
name|'if'
name|'container_rate'
op|':'
newline|'\n'
indent|'                    '
name|'keys'
op|'.'
name|'append'
op|'('
op|'('
string|'"ratelimit/%s/%s"'
op|'%'
op|'('
name|'account_name'
op|','
nl|'\n'
name|'container_name'
op|')'
op|','
nl|'\n'
name|'container_rate'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'keys'
newline|'\n'
nl|'\n'
DECL|member|_get_sleep_time
dedent|''
name|'def'
name|'_get_sleep_time'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'max_rate'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Returns the amount of time (a float in seconds) that the app\n        should sleep.  Throws a MaxSleepTimeHit exception if maximum\n        sleep time is exceeded.\n\n        :param key: a memcache key\n        :param max_rate: maximum rate allowed in requests per second\n        '''"
newline|'\n'
name|'now_m'
op|'='
name|'int'
op|'('
name|'round'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'*'
name|'self'
op|'.'
name|'clock_accuracy'
op|')'
op|')'
newline|'\n'
name|'time_per_request_m'
op|'='
name|'int'
op|'('
name|'round'
op|'('
name|'self'
op|'.'
name|'clock_accuracy'
op|'/'
name|'max_rate'
op|')'
op|')'
newline|'\n'
name|'running_time_m'
op|'='
name|'self'
op|'.'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
name|'key'
op|','
nl|'\n'
name|'delta'
op|'='
name|'time_per_request_m'
op|')'
newline|'\n'
name|'need_to_sleep_m'
op|'='
number|'0'
newline|'\n'
name|'request_time_limit'
op|'='
name|'now_m'
op|'+'
op|'('
name|'time_per_request_m'
op|'*'
name|'max_rate'
op|')'
newline|'\n'
name|'if'
name|'running_time_m'
op|'<'
name|'now_m'
op|':'
newline|'\n'
indent|'            '
name|'next_avail_time'
op|'='
name|'int'
op|'('
name|'now_m'
op|'+'
name|'time_per_request_m'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'memcache_client'
op|'.'
name|'set'
op|'('
name|'key'
op|','
name|'str'
op|'('
name|'next_avail_time'
op|')'
op|','
nl|'\n'
name|'serialize'
op|'='
name|'False'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'running_time_m'
op|'-'
name|'now_m'
op|'-'
name|'time_per_request_m'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'need_to_sleep_m'
op|'='
name|'running_time_m'
op|'-'
name|'now_m'
op|'-'
name|'time_per_request_m'
newline|'\n'
nl|'\n'
dedent|''
name|'max_sleep_m'
op|'='
name|'self'
op|'.'
name|'max_sleep_time_seconds'
op|'*'
name|'self'
op|'.'
name|'clock_accuracy'
newline|'\n'
name|'if'
name|'max_sleep_m'
op|'-'
name|'need_to_sleep_m'
op|'<='
name|'self'
op|'.'
name|'clock_accuracy'
op|'*'
number|'0.01'
op|':'
newline|'\n'
comment|'# treat as no-op decrement time'
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'memcache_client'
op|'.'
name|'decr'
op|'('
name|'key'
op|','
name|'delta'
op|'='
name|'time_per_request_m'
op|')'
newline|'\n'
name|'raise'
name|'MaxSleepTimeHit'
op|'('
string|'"Max Sleep Time Exceeded: %s"'
op|'%'
nl|'\n'
name|'need_to_sleep_m'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'float'
op|'('
name|'need_to_sleep_m'
op|')'
op|'/'
name|'self'
op|'.'
name|'clock_accuracy'
newline|'\n'
nl|'\n'
DECL|member|handle_ratelimit
dedent|''
name|'def'
name|'handle_ratelimit'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'account_name'
op|','
name|'container_name'
op|','
name|'obj_name'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Performs rate limiting and account white/black listing.  Sleeps\n        if necessary.\n\n        :param account_name: account name from path\n        :param container_name: container name from path\n        :param obj_name: object name from path\n        '''"
newline|'\n'
name|'if'
name|'account_name'
name|'in'
name|'self'
op|'.'
name|'ratelimit_blacklist'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'Returning 497 because of blacklisting'"
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
string|"'497 Blacklisted'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'Your account has been blacklisted'"
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'account_name'
name|'in'
name|'self'
op|'.'
name|'ratelimit_whitelist'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'for'
name|'key'
op|','
name|'max_rate'
name|'in'
name|'self'
op|'.'
name|'get_ratelimitable_key_tuples'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'method'
op|','
nl|'\n'
name|'account_name'
op|','
nl|'\n'
name|'container_name'
op|'='
name|'container_name'
op|','
nl|'\n'
name|'obj_name'
op|'='
name|'obj_name'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'need_to_sleep'
op|'='
name|'self'
op|'.'
name|'_get_sleep_time'
op|'('
name|'key'
op|','
name|'max_rate'
op|')'
newline|'\n'
name|'if'
name|'need_to_sleep'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                    '
name|'eventlet'
op|'.'
name|'sleep'
op|'('
name|'need_to_sleep'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'MaxSleepTimeHit'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'Returning 498 because of ops '"
op|'+'
string|"'rate limiting (Max Sleep) %s'"
op|'%'
name|'e'
op|')'
newline|'\n'
name|'error_resp'
op|'='
name|'Response'
op|'('
name|'status'
op|'='
string|"'498 Rate Limited'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'Slow down'"
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'return'
name|'error_resp'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
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
string|'"""\n        WSGI entry point.\n        Wraps env in webob.Request object and passes it down.\n\n        :param env: WSGI environment dictionary\n        :param start_response: WSGI callable\n        """'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'memcache_client'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'memcache_client'
op|'='
name|'cache_from_env'
op|'('
name|'env'
op|')'
newline|'\n'
dedent|''
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'req'
op|'.'
name|'path'
op|','
number|'1'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
name|'ratelimit_resp'
op|'='
name|'self'
op|'.'
name|'handle_ratelimit'
op|'('
name|'req'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'if'
name|'ratelimit_resp'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'ratelimit_resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
dedent|''
dedent|''
dedent|''
name|'def'
name|'filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    paste.deploy app factory for creating WSGI proxy apps.\n    """'
newline|'\n'
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
name|'RateLimitMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'limit_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
