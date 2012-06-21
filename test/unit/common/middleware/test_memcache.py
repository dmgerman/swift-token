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
name|'ConfigParser'
name|'import'
name|'NoSectionError'
op|','
name|'NoOptionError'
newline|'\n'
nl|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'memcache'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'memcached'
name|'import'
name|'MemcacheRing'
newline|'\n'
nl|'\n'
DECL|class|FakeApp
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
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
name|'env'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ExcConfigParser
dedent|''
dedent|''
name|'class'
name|'ExcConfigParser'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|read
indent|'    '
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'read called with %r'"
op|'%'
name|'path'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|EmptyConfigParser
dedent|''
dedent|''
name|'class'
name|'EmptyConfigParser'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|read
indent|'    '
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|SetConfigParser
dedent|''
dedent|''
name|'class'
name|'SetConfigParser'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|read
indent|'    '
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
name|'def'
name|'get'
op|'('
name|'self'
op|','
name|'section'
op|','
name|'option'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'section'
op|'=='
string|"'memcache'"
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'option'
op|'=='
string|"'memcache_servers'"
op|':'
newline|'\n'
indent|'                '
name|'return'
string|"'1.2.3.4:5'"
newline|'\n'
dedent|''
name|'elif'
name|'option'
op|'=='
string|"'memcache_serialization_support'"
op|':'
newline|'\n'
indent|'                '
name|'return'
string|"'2'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'NoOptionError'
op|'('
name|'option'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'NoSectionError'
op|'('
name|'option'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|start_response
dedent|''
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
DECL|class|TestCacheMiddleware
dedent|''
name|'class'
name|'TestCacheMiddleware'
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
name|'app'
op|'='
name|'memcache'
op|'.'
name|'MemcacheMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_cache_middleware
dedent|''
name|'def'
name|'test_cache_middleware'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/something'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
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
name|'assertTrue'
op|'('
string|"'swift.cache'"
name|'in'
name|'resp'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|'['
string|"'swift.cache'"
op|']'
op|','
name|'MemcacheRing'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_conf_default_read
dedent|''
name|'def'
name|'test_conf_default_read'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'orig_parser'
op|'='
name|'memcache'
op|'.'
name|'ConfigParser'
newline|'\n'
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'ExcConfigParser'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'app'
op|'='
name|'memcache'
op|'.'
name|'MemcacheMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
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
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'orig_parser'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'str'
op|'('
name|'exc'
op|')'
op|','
nl|'\n'
string|'"read called with \'/etc/swift/memcache.conf\'"'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_conf_set_no_read
dedent|''
name|'def'
name|'test_conf_set_no_read'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'orig_parser'
op|'='
name|'memcache'
op|'.'
name|'ConfigParser'
newline|'\n'
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'ExcConfigParser'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'app'
op|'='
name|'memcache'
op|'.'
name|'MemcacheMiddleware'
op|'('
nl|'\n'
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
string|"'memcache_servers'"
op|':'
string|"'1.2.3.4:5'"
op|','
nl|'\n'
string|"'memcache_serialization_support'"
op|':'
string|"'2'"
op|'}'
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
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'orig_parser'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'exc'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_conf_default
dedent|''
name|'def'
name|'test_conf_default'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'orig_parser'
op|'='
name|'memcache'
op|'.'
name|'ConfigParser'
newline|'\n'
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'EmptyConfigParser'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'app'
op|'='
name|'memcache'
op|'.'
name|'MemcacheMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'orig_parser'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'app'
op|'.'
name|'memcache_servers'
op|','
string|"'127.0.0.1:11211'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_conf_from_extra_conf
dedent|''
name|'def'
name|'test_conf_from_extra_conf'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'orig_parser'
op|'='
name|'memcache'
op|'.'
name|'ConfigParser'
newline|'\n'
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'SetConfigParser'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'app'
op|'='
name|'memcache'
op|'.'
name|'MemcacheMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'orig_parser'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'app'
op|'.'
name|'memcache_servers'
op|','
string|"'1.2.3.4:5'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_conf_from_inline_conf
dedent|''
name|'def'
name|'test_conf_from_inline_conf'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'orig_parser'
op|'='
name|'memcache'
op|'.'
name|'ConfigParser'
newline|'\n'
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'SetConfigParser'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'app'
op|'='
name|'memcache'
op|'.'
name|'MemcacheMiddleware'
op|'('
nl|'\n'
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
string|"'memcache_servers'"
op|':'
string|"'6.7.8.9:10'"
op|'}'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'memcache'
op|'.'
name|'ConfigParser'
op|'='
name|'orig_parser'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'app'
op|'.'
name|'memcache_servers'
op|','
string|"'6.7.8.9:10'"
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
