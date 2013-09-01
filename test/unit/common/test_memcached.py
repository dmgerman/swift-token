begin_unit
comment|'# -*- coding:utf-8 -*-'
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
string|'"""Tests for swift.common.utils"""'
newline|'\n'
nl|'\n'
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'memcached'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'NullLoggingHandler'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ExplodingMockMemcached
name|'class'
name|'ExplodingMockMemcached'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|variable|exploded
indent|'    '
name|'exploded'
op|'='
name|'False'
newline|'\n'
nl|'\n'
DECL|member|sendall
name|'def'
name|'sendall'
op|'('
name|'self'
op|','
name|'string'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'exploded'
op|'='
name|'True'
newline|'\n'
name|'raise'
name|'socket'
op|'.'
name|'error'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'exploded'
op|'='
name|'True'
newline|'\n'
name|'raise'
name|'socket'
op|'.'
name|'error'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'size'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'exploded'
op|'='
name|'True'
newline|'\n'
name|'raise'
name|'socket'
op|'.'
name|'error'
op|'('
op|')'
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
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MockMemcached
dedent|''
dedent|''
name|'class'
name|'MockMemcached'
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
name|'inbuf'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'outbuf'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'cache'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'down'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'exc_on_delete'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'read_return_none'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'close_called'
op|'='
name|'False'
newline|'\n'
nl|'\n'
DECL|member|sendall
dedent|''
name|'def'
name|'sendall'
op|'('
name|'self'
op|','
name|'string'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'down'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'mock is down'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'inbuf'
op|'+='
name|'string'
newline|'\n'
name|'while'
string|"'\\n'"
name|'in'
name|'self'
op|'.'
name|'inbuf'
op|':'
newline|'\n'
indent|'            '
name|'cmd'
op|','
name|'self'
op|'.'
name|'inbuf'
op|'='
name|'self'
op|'.'
name|'inbuf'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|','
number|'1'
op|')'
newline|'\n'
name|'parts'
op|'='
name|'cmd'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'parts'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'set'"
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
op|'='
name|'parts'
op|'['
number|'2'
op|']'
op|','
name|'parts'
op|'['
number|'3'
op|']'
op|','
name|'self'
op|'.'
name|'inbuf'
op|'['
op|':'
name|'int'
op|'('
name|'parts'
op|'['
number|'4'
op|']'
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'inbuf'
op|'='
name|'self'
op|'.'
name|'inbuf'
op|'['
name|'int'
op|'('
name|'parts'
op|'['
number|'4'
op|']'
op|')'
op|'+'
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'<'
number|'6'
name|'or'
name|'parts'
op|'['
number|'5'
op|']'
op|'!='
string|"'noreply'"
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'STORED\\r\\n'"
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'parts'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'add'"
op|':'
newline|'\n'
indent|'                '
name|'value'
op|'='
name|'self'
op|'.'
name|'inbuf'
op|'['
op|':'
name|'int'
op|'('
name|'parts'
op|'['
number|'4'
op|']'
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'inbuf'
op|'='
name|'self'
op|'.'
name|'inbuf'
op|'['
name|'int'
op|'('
name|'parts'
op|'['
number|'4'
op|']'
op|')'
op|'+'
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'parts'
op|'['
number|'1'
op|']'
name|'in'
name|'self'
op|'.'
name|'cache'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'<'
number|'6'
name|'or'
name|'parts'
op|'['
number|'5'
op|']'
op|'!='
string|"'noreply'"
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'NOT_STORED\\r\\n'"
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
op|'='
name|'parts'
op|'['
number|'2'
op|']'
op|','
name|'parts'
op|'['
number|'3'
op|']'
op|','
name|'value'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'<'
number|'6'
name|'or'
name|'parts'
op|'['
number|'5'
op|']'
op|'!='
string|"'noreply'"
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'STORED\\r\\n'"
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'elif'
name|'parts'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'delete'"
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'exc_on_delete'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
string|"'mock is has exc_on_delete set'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'parts'
op|'['
number|'1'
op|']'
name|'in'
name|'self'
op|'.'
name|'cache'
op|':'
newline|'\n'
indent|'                    '
name|'del'
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
string|"'noreply'"
name|'not'
name|'in'
name|'parts'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'DELETED\\r\\n'"
newline|'\n'
dedent|''
dedent|''
name|'elif'
string|"'noreply'"
name|'not'
name|'in'
name|'parts'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'NOT_FOUND\\r\\n'"
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'parts'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'get'"
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'key'
name|'in'
name|'parts'
op|'['
number|'1'
op|':'
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'key'
name|'in'
name|'self'
op|'.'
name|'cache'
op|':'
newline|'\n'
indent|'                        '
name|'val'
op|'='
name|'self'
op|'.'
name|'cache'
op|'['
name|'key'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'VALUE %s %s %s\\r\\n'"
op|'%'
op|'('
nl|'\n'
name|'key'
op|','
name|'val'
op|'['
number|'0'
op|']'
op|','
name|'len'
op|'('
name|'val'
op|'['
number|'2'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'outbuf'
op|'+='
name|'val'
op|'['
number|'2'
op|']'
op|'+'
string|"'\\r\\n'"
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'END\\r\\n'"
newline|'\n'
dedent|''
name|'elif'
name|'parts'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'incr'"
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'parts'
op|'['
number|'1'
op|']'
name|'in'
name|'self'
op|'.'
name|'cache'
op|':'
newline|'\n'
indent|'                    '
name|'val'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
name|'val'
op|'['
number|'2'
op|']'
op|'='
name|'str'
op|'('
name|'int'
op|'('
name|'val'
op|'['
number|'2'
op|']'
op|')'
op|'+'
name|'int'
op|'('
name|'parts'
op|'['
number|'2'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
op|'='
name|'val'
newline|'\n'
name|'self'
op|'.'
name|'outbuf'
op|'+='
name|'str'
op|'('
name|'val'
op|'['
number|'2'
op|']'
op|')'
op|'+'
string|"'\\r\\n'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'NOT_FOUND\\r\\n'"
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'parts'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'decr'"
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'parts'
op|'['
number|'1'
op|']'
name|'in'
name|'self'
op|'.'
name|'cache'
op|':'
newline|'\n'
indent|'                    '
name|'val'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
name|'if'
name|'int'
op|'('
name|'val'
op|'['
number|'2'
op|']'
op|')'
op|'-'
name|'int'
op|'('
name|'parts'
op|'['
number|'2'
op|']'
op|')'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'val'
op|'['
number|'2'
op|']'
op|'='
name|'str'
op|'('
name|'int'
op|'('
name|'val'
op|'['
number|'2'
op|']'
op|')'
op|'-'
name|'int'
op|'('
name|'parts'
op|'['
number|'2'
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'val'
op|'['
number|'2'
op|']'
op|'='
string|"'0'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'cache'
op|'['
name|'parts'
op|'['
number|'1'
op|']'
op|']'
op|'='
name|'val'
newline|'\n'
name|'self'
op|'.'
name|'outbuf'
op|'+='
name|'str'
op|'('
name|'val'
op|'['
number|'2'
op|']'
op|')'
op|'+'
string|"'\\r\\n'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'outbuf'
op|'+='
string|"'NOT_FOUND\\r\\n'"
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'read_return_none'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'down'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'mock is down'"
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'\\n'"
name|'in'
name|'self'
op|'.'
name|'outbuf'
op|':'
newline|'\n'
indent|'            '
name|'response'
op|','
name|'self'
op|'.'
name|'outbuf'
op|'='
name|'self'
op|'.'
name|'outbuf'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|','
number|'1'
op|')'
newline|'\n'
name|'return'
name|'response'
op|'+'
string|"'\\n'"
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'size'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'down'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'mock is down'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'outbuf'
op|')'
op|'>='
name|'size'
op|':'
newline|'\n'
indent|'            '
name|'response'
op|'='
name|'self'
op|'.'
name|'outbuf'
op|'['
op|':'
name|'size'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'outbuf'
op|'='
name|'self'
op|'.'
name|'outbuf'
op|'['
name|'size'
op|':'
op|']'
newline|'\n'
name|'return'
name|'response'
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'close_called'
op|'='
name|'True'
newline|'\n'
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestMemcached
dedent|''
dedent|''
name|'class'
name|'TestMemcached'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Tests for swift.common.memcached"""'
newline|'\n'
nl|'\n'
DECL|member|test_get_conns
name|'def'
name|'test_get_conns'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sock1'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
newline|'\n'
name|'sock1'
op|'.'
name|'bind'
op|'('
op|'('
string|"'127.0.0.1'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'sock1'
op|'.'
name|'listen'
op|'('
number|'1'
op|')'
newline|'\n'
name|'sock1ipport'
op|'='
string|"'%s:%s'"
op|'%'
name|'sock1'
op|'.'
name|'getsockname'
op|'('
op|')'
newline|'\n'
name|'sock2'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
newline|'\n'
name|'sock2'
op|'.'
name|'bind'
op|'('
op|'('
string|"'127.0.0.1'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'sock2'
op|'.'
name|'listen'
op|'('
number|'1'
op|')'
newline|'\n'
name|'orig_port'
op|'='
name|'memcached'
op|'.'
name|'DEFAULT_MEMCACHED_PORT'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'sock2ip'
op|','
name|'memcached'
op|'.'
name|'DEFAULT_MEMCACHED_PORT'
op|'='
name|'sock2'
op|'.'
name|'getsockname'
op|'('
op|')'
newline|'\n'
name|'sock2ipport'
op|'='
string|"'%s:%s'"
op|'%'
op|'('
name|'sock2ip'
op|','
name|'memcached'
op|'.'
name|'DEFAULT_MEMCACHED_PORT'
op|')'
newline|'\n'
comment|"# We're deliberately using sock2ip (no port) here to test that the"
nl|'\n'
comment|'# default port is used.'
nl|'\n'
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
name|'sock1ipport'
op|','
name|'sock2ip'
op|']'
op|')'
newline|'\n'
name|'one'
op|'='
name|'two'
op|'='
name|'True'
newline|'\n'
name|'while'
name|'one'
name|'or'
name|'two'
op|':'
comment|'# Run until we match hosts one and two'
newline|'\n'
indent|'                '
name|'key'
op|'='
name|'uuid4'
op|'('
op|')'
op|'.'
name|'hex'
newline|'\n'
name|'for'
name|'conn'
name|'in'
name|'memcache_client'
op|'.'
name|'_get_conns'
op|'('
name|'key'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'peeripport'
op|'='
string|"'%s:%s'"
op|'%'
name|'conn'
op|'['
number|'2'
op|']'
op|'.'
name|'getpeername'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'peeripport'
name|'in'
op|'('
name|'sock1ipport'
op|','
name|'sock2ipport'
op|')'
op|')'
newline|'\n'
name|'if'
name|'peeripport'
op|'=='
name|'sock1ipport'
op|':'
newline|'\n'
indent|'                        '
name|'one'
op|'='
name|'False'
newline|'\n'
dedent|''
name|'if'
name|'peeripport'
op|'=='
name|'sock2ipport'
op|':'
newline|'\n'
indent|'                        '
name|'two'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'memcached'
op|'.'
name|'DEFAULT_MEMCACHED_PORT'
op|'='
name|'orig_port'
newline|'\n'
nl|'\n'
DECL|member|test_set_get
dedent|''
dedent|''
name|'def'
name|'test_set_get'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
string|"'simple str'"
op|','
string|"'utf8 str \xc3\xa9\xc3\xa0'"
op|']'
op|')'
newline|'\n'
comment|'# As per http://wiki.openstack.org/encoding,'
nl|'\n'
comment|'# we should expect to have unicode'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
string|"'simple str'"
op|','
string|"u'utf8 str \xc3\xa9\xc3\xa0'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'float'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|')'
op|'=='
number|'0'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
name|'timeout'
op|'='
number|'10'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'10'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
name|'time'
op|'='
number|'20'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'20'"
op|')'
newline|'\n'
nl|'\n'
name|'sixtydays'
op|'='
number|'60'
op|'*'
number|'24'
op|'*'
number|'60'
op|'*'
number|'60'
newline|'\n'
name|'esttimeout'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
name|'sixtydays'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
name|'timeout'
op|'='
name|'sixtydays'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
op|'-'
number|'1'
op|'<='
name|'float'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|')'
op|'-'
name|'esttimeout'
op|'<='
number|'1'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
name|'time'
op|'='
name|'sixtydays'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
op|'-'
number|'1'
op|'<='
name|'float'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|')'
op|'-'
name|'esttimeout'
op|'<='
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_incr
dedent|''
name|'def'
name|'test_incr'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'5'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'10'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'11'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
op|'-'
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'6'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
op|'-'
number|'15'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'mock'
op|'.'
name|'read_return_none'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'memcached'
op|'.'
name|'MemcacheConnectionError'
op|','
nl|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|','
string|"'some_key'"
op|','
name|'delta'
op|'='
op|'-'
number|'15'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'mock'
op|'.'
name|'close_called'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_incr_w_timeout
dedent|''
name|'def'
name|'test_incr_w_timeout'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|','
name|'time'
op|'='
number|'55'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'5'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'55'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'delete'
op|'('
string|"'some_key'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'fiftydays'
op|'='
number|'50'
op|'*'
number|'24'
op|'*'
number|'60'
op|'*'
number|'60'
newline|'\n'
name|'esttimeout'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
name|'fiftydays'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|','
name|'time'
op|'='
name|'fiftydays'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'5'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
op|'-'
number|'1'
op|'<='
name|'float'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|')'
op|'-'
name|'esttimeout'
op|'<='
number|'1'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'delete'
op|'('
string|"'some_key'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'5'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|','
name|'time'
op|'='
number|'55'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'10'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_decr
dedent|''
name|'def'
name|'test_decr'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'decr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'incr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'15'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'15'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'decr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'4'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'11'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'decr'
op|'('
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'15'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'mock'
op|'.'
name|'read_return_none'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'memcached'
op|'.'
name|'MemcacheConnectionError'
op|','
nl|'\n'
name|'memcache_client'
op|'.'
name|'decr'
op|','
string|"'some_key'"
op|','
name|'delta'
op|'='
number|'15'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_retry
dedent|''
name|'def'
name|'test_retry'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'logging'
op|'.'
name|'getLogger'
op|'('
op|')'
op|'.'
name|'addHandler'
op|'('
name|'NullLoggingHandler'
op|'('
op|')'
op|')'
newline|'\n'
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
nl|'\n'
op|'['
string|"'1.2.3.4:11211'"
op|','
string|"'1.2.3.5:11211'"
op|']'
op|')'
newline|'\n'
name|'mock1'
op|'='
name|'ExplodingMockMemcached'
op|'('
op|')'
newline|'\n'
name|'mock2'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock2'
op|','
name|'mock2'
op|')'
op|']'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.5:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock1'
op|','
name|'mock1'
op|')'
op|']'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock1'
op|'.'
name|'exploded'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete
dedent|''
name|'def'
name|'test_delete'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'delete'
op|'('
string|"'some_key'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_multi
dedent|''
name|'def'
name|'test_multi'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set_multi'
op|'('
nl|'\n'
op|'{'
string|"'some_key1'"
op|':'
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
string|"'some_key2'"
op|':'
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|'}'
op|','
string|"'multi_key'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'memcache_client'
op|'.'
name|'get_multi'
op|'('
op|'('
string|"'some_key2'"
op|','
string|"'some_key1'"
op|')'
op|','
string|"'multi_key'"
op|')'
op|','
nl|'\n'
op|'['
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set_multi'
op|'('
nl|'\n'
op|'{'
string|"'some_key1'"
op|':'
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
string|"'some_key2'"
op|':'
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|'}'
op|','
string|"'multi_key'"
op|','
nl|'\n'
name|'timeout'
op|'='
number|'10'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'10'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'10'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set_multi'
op|'('
nl|'\n'
op|'{'
string|"'some_key1'"
op|':'
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
string|"'some_key2'"
op|':'
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|'}'
op|','
string|"'multi_key'"
op|','
nl|'\n'
name|'time'
op|'='
number|'20'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'20'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'20'"
op|')'
newline|'\n'
nl|'\n'
name|'fortydays'
op|'='
number|'50'
op|'*'
number|'24'
op|'*'
number|'60'
op|'*'
number|'60'
newline|'\n'
name|'esttimeout'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
name|'fortydays'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set_multi'
op|'('
nl|'\n'
op|'{'
string|"'some_key1'"
op|':'
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
string|"'some_key2'"
op|':'
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|'}'
op|','
string|"'multi_key'"
op|','
nl|'\n'
name|'timeout'
op|'='
name|'fortydays'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
op|'-'
number|'1'
op|'<='
name|'float'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|')'
op|'-'
name|'esttimeout'
op|'<='
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
op|'-'
number|'1'
op|'<='
name|'float'
op|'('
name|'mock'
op|'.'
name|'cache'
op|'.'
name|'values'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|'['
number|'1'
op|']'
op|')'
op|'-'
name|'esttimeout'
op|'<='
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get_multi'
op|'('
nl|'\n'
op|'('
string|"'some_key2'"
op|','
string|"'some_key1'"
op|','
string|"'not_exists'"
op|')'
op|','
string|"'multi_key'"
op|')'
op|','
nl|'\n'
op|'['
op|'['
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|','
name|'None'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_serialization
dedent|''
name|'def'
name|'test_serialization'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'memcache_client'
op|'='
name|'memcached'
op|'.'
name|'MemcacheRing'
op|'('
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|','
nl|'\n'
name|'allow_pickle'
op|'='
name|'True'
op|')'
newline|'\n'
name|'mock'
op|'='
name|'MockMemcached'
op|'('
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_client_cache'
op|'['
string|"'1.2.3.4:11211'"
op|']'
op|'='
op|'['
op|'('
name|'mock'
op|','
name|'mock'
op|')'
op|']'
op|'*'
number|'2'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_allow_pickle'
op|'='
name|'False'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_allow_unpickle'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_allow_unpickle'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
string|"'some_key'"
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_allow_unpickle'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'_allow_pickle'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'memcache_client'
op|'.'
name|'get'
op|'('
string|"'some_key'"
op|')'
op|','
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|']'
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
