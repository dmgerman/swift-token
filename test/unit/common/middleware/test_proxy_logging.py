begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
name|'urllib'
name|'import'
name|'quote'
op|','
name|'unquote'
newline|'\n'
name|'import'
name|'cStringIO'
name|'as'
name|'StringIO'
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
name|'proxy_logging'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'body'
op|'='
op|'['
string|"'FAKE APP'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'body'
op|'='
name|'body'
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
name|'start_response'
op|'('
string|"'200 OK'"
op|','
op|'['
op|'('
string|"'Content-Type'"
op|','
string|"'text/plain'"
op|')'
op|']'
op|')'
newline|'\n'
name|'while'
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'read'
op|'('
number|'5'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'body'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FileLikeExceptor
dedent|''
dedent|''
name|'class'
name|'FileLikeExceptor'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
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
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'len'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
op|'('
string|"'of some sort'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|','
name|'len'
op|'='
number|'1024'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
op|'('
string|"'of some sort'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeAppReadline
dedent|''
dedent|''
name|'class'
name|'FakeAppReadline'
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
name|'start_response'
op|'('
string|"'200 OK'"
op|','
op|'['
op|'('
string|"'Content-Type'"
op|','
string|"'text/plain'"
op|')'
op|']'
op|')'
newline|'\n'
name|'line'
op|'='
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
name|'return'
op|'['
string|'"FAKE APP"'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeLogger
dedent|''
dedent|''
name|'class'
name|'FakeLogger'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
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
indent|'        '
name|'self'
op|'.'
name|'msg'
op|'='
string|"''"
newline|'\n'
nl|'\n'
DECL|member|info
dedent|''
name|'def'
name|'info'
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
name|'msg'
op|'='
name|'string'
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
DECL|class|TestProxyLogging
dedent|''
name|'class'
name|'TestProxyLogging'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_basic_req
indent|'    '
name|'def'
name|'test_basic_req'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
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
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'resp_body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'3'
op|']'
op|','
string|"'GET'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'4'
op|']'
op|','
string|"'/'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'5'
op|']'
op|','
string|"'HTTP/1.0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'6'
op|']'
op|','
string|"'200'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp_body'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'11'
op|']'
op|','
name|'str'
op|'('
name|'len'
op|'('
name|'resp_body'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_multi_segment_resp
dedent|''
name|'def'
name|'test_multi_segment_resp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
nl|'\n'
op|'['
string|"'some'"
op|','
string|"'chunks'"
op|','
string|"'of data'"
op|']'
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
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
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'resp_body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'3'
op|']'
op|','
string|"'GET'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'4'
op|']'
op|','
string|"'/'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'5'
op|']'
op|','
string|"'HTTP/1.0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'6'
op|']'
op|','
string|"'200'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp_body'
op|','
string|"'somechunksof data'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'11'
op|']'
op|','
name|'str'
op|'('
name|'len'
op|'('
name|'resp_body'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_log_headers
dedent|''
name|'def'
name|'test_log_headers'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'log_headers'"
op|':'
string|"'yes'"
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
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
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
op|'['
name|'x'
name|'for'
name|'x'
name|'in'
name|'resp'
op|']'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'='
name|'unquote'
op|'('
name|'log_parts'
op|'['
number|'14'
op|']'
op|')'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'Host: localhost:80'"
name|'in'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_upload_size
dedent|''
name|'def'
name|'test_upload_size'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'log_headers'"
op|':'
string|"'yes'"
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'wsgi.input'"
op|':'
name|'StringIO'
op|'.'
name|'StringIO'
op|'('
string|"'some stuff'"
op|')'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
op|'['
name|'x'
name|'for'
name|'x'
name|'in'
name|'resp'
op|']'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'10'
op|']'
op|','
name|'str'
op|'('
name|'len'
op|'('
string|"'some stuff'"
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_upload_line
dedent|''
name|'def'
name|'test_upload_line'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeAppReadline'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'log_headers'"
op|':'
string|"'yes'"
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'wsgi.input'"
op|':'
name|'StringIO'
op|'.'
name|'StringIO'
op|'('
nl|'\n'
string|"'some stuff\\nsome other stuff\\n'"
op|')'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'10'
op|']'
op|','
name|'str'
op|'('
name|'len'
op|'('
string|"'some stuff\\n'"
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_log_query_string
dedent|''
name|'def'
name|'test_log_query_string'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'QUERY_STRING'"
op|':'
string|"'x=3'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
op|'['
name|'x'
name|'for'
name|'x'
name|'in'
name|'resp'
op|']'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'unquote'
op|'('
name|'log_parts'
op|'['
number|'4'
op|']'
op|')'
op|','
string|"'/?x=3'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_client_logging
dedent|''
name|'def'
name|'test_client_logging'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'REMOTE_ADDR'"
op|':'
string|"'1.2.3.4'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
op|'['
name|'x'
name|'for'
name|'x'
name|'in'
name|'resp'
op|']'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'0'
op|']'
op|','
string|"'1.2.3.4'"
op|')'
comment|'# client ip'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'1'
op|']'
op|','
string|"'1.2.3.4'"
op|')'
comment|'# remote addr'
newline|'\n'
nl|'\n'
DECL|member|test_proxy_client_logging
dedent|''
name|'def'
name|'test_proxy_client_logging'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'REMOTE_ADDR'"
op|':'
string|"'1.2.3.4'"
op|','
nl|'\n'
string|"'HTTP_X_FORWARDED_FOR'"
op|':'
string|"'4.5.6.7,8.9.10.11'"
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
op|'['
name|'x'
name|'for'
name|'x'
name|'in'
name|'resp'
op|']'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'0'
op|']'
op|','
string|"'4.5.6.7'"
op|')'
comment|'# client ip'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'1'
op|']'
op|','
string|"'1.2.3.4'"
op|')'
comment|'# remote addr'
newline|'\n'
nl|'\n'
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'REMOTE_ADDR'"
op|':'
string|"'1.2.3.4'"
op|','
nl|'\n'
string|"'HTTP_X_CLUSTER_CLIENT_IP'"
op|':'
string|"'4.5.6.7'"
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'exhaust_generator'
op|'='
op|'['
name|'x'
name|'for'
name|'x'
name|'in'
name|'resp'
op|']'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'0'
op|']'
op|','
string|"'4.5.6.7'"
op|')'
comment|'# client ip'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'1'
op|']'
op|','
string|"'1.2.3.4'"
op|')'
comment|'# remote addr'
newline|'\n'
nl|'\n'
DECL|member|test_facility
dedent|''
name|'def'
name|'test_facility'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'log_headers'"
op|':'
string|"'yes'"
op|','
string|"'access_log_facility'"
op|':'
string|"'whatever'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_filter
dedent|''
name|'def'
name|'test_filter'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'factory'
op|'='
name|'proxy_logging'
op|'.'
name|'filter_factory'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'callable'
op|'('
name|'factory'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'callable'
op|'('
name|'factory'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_unread_body
dedent|''
name|'def'
name|'test_unread_body'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
nl|'\n'
name|'FakeApp'
op|'('
op|'['
string|"'some'"
op|','
string|"'stuff'"
op|']'
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
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
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'read_first_chunk'
op|'='
name|'next'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'close'
op|'('
op|')'
comment|'# raise a GeneratorExit in middleware app_iter loop'
newline|'\n'
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'6'
op|']'
op|','
string|"'499'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'11'
op|']'
op|','
string|"'4'"
op|')'
comment|'# write length'
newline|'\n'
nl|'\n'
DECL|member|test_disconnect_on_readline
dedent|''
name|'def'
name|'test_disconnect_on_readline'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
name|'FakeAppReadline'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'wsgi.input'"
op|':'
name|'FileLikeExceptor'
op|'('
op|')'
op|'}'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
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
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'6'
op|']'
op|','
string|"'499'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'10'
op|']'
op|','
string|"'-'"
op|')'
comment|'# read length'
newline|'\n'
nl|'\n'
DECL|member|test_disconnect_on_read
dedent|''
name|'def'
name|'test_disconnect_on_read'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'proxy_logging'
op|'.'
name|'ProxyLoggingMiddleware'
op|'('
nl|'\n'
name|'FakeApp'
op|'('
op|'['
string|"'some'"
op|','
string|"'stuff'"
op|']'
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'access_logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'wsgi.input'"
op|':'
name|'FileLikeExceptor'
op|'('
op|')'
op|'}'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
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
name|'log_parts'
op|'='
name|'app'
op|'.'
name|'access_logger'
op|'.'
name|'msg'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'6'
op|']'
op|','
string|"'499'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'log_parts'
op|'['
number|'10'
op|']'
op|','
string|"'-'"
op|')'
comment|'# read length'
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
