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
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'spawn'
op|','
name|'Timeout'
op|','
name|'listen'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'bufferedhttp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestBufferedHTTP
name|'class'
name|'TestBufferedHTTP'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_http_connect
indent|'    '
name|'def'
name|'test_http_connect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'bindsock'
op|'='
name|'listen'
op|'('
op|'('
string|"'127.0.0.1'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
DECL|function|accept
name|'def'
name|'accept'
op|'('
name|'expected_par'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'Timeout'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'sock'
op|','
name|'addr'
op|'='
name|'bindsock'
op|'.'
name|'accept'
op|'('
op|')'
newline|'\n'
name|'fp'
op|'='
name|'sock'
op|'.'
name|'makefile'
op|'('
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'write'
op|'('
string|"'HTTP/1.1 200 OK\\r\\nContent-Length: 8\\r\\n\\r\\n'"
nl|'\n'
string|"'RESPONSE'"
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'flush'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|','
nl|'\n'
string|"'PUT /dev/%s/path/..%%25/?omg&no=%%7f HTTP/1.1\\r\\n'"
op|'%'
nl|'\n'
name|'expected_par'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
name|'while'
name|'line'
name|'and'
name|'line'
op|'!='
string|"'\\r\\n'"
op|':'
newline|'\n'
indent|'                        '
name|'headers'
op|'['
name|'line'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'line'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'1'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'content-length'"
op|']'
op|','
string|"'7'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-header'"
op|']'
op|','
string|"'value'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|','
string|"'REQUEST\\r\\n'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'BaseException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'err'
newline|'\n'
dedent|''
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'for'
name|'par'
name|'in'
op|'('
string|"'par'"
op|','
number|'1357'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'event'
op|'='
name|'spawn'
op|'('
name|'accept'
op|','
name|'par'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'Timeout'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'='
name|'bufferedhttp'
op|'.'
name|'http_connect'
op|'('
string|"'127.0.0.1'"
op|','
nl|'\n'
name|'bindsock'
op|'.'
name|'getsockname'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|','
string|"'dev'"
op|','
name|'par'
op|','
string|"'PUT'"
op|','
nl|'\n'
string|"'/path/..%/'"
op|','
op|'{'
string|"'content-length'"
op|':'
number|'7'
op|','
string|"'x-header'"
op|':'
nl|'\n'
string|"'value'"
op|'}'
op|','
name|'query_string'
op|'='
string|"'omg&no=%7f'"
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'send'
op|'('
string|"'REQUEST\\r\\n'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'body'
op|'='
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'reason'
op|','
string|"'OK'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'body'
op|','
string|"'RESPONSE'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'err'
op|'='
name|'event'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
name|'err'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_nonstr_header_values
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_nonstr_header_values'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|class|MockHTTPSConnection
indent|'        '
name|'class'
name|'MockHTTPSConnection'
op|'('
name|'object'
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
name|'hostport'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|putrequest
dedent|''
name|'def'
name|'putrequest'
op|'('
name|'self'
op|','
name|'method'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|putheader
dedent|''
name|'def'
name|'putheader'
op|'('
name|'self'
op|','
name|'header'
op|','
op|'*'
name|'values'
op|')'
op|':'
newline|'\n'
comment|'# Essentially what Python 2.7 does that caused us problems.'
nl|'\n'
indent|'                '
string|"'\\r\\n\\t'"
op|'.'
name|'join'
op|'('
name|'values'
op|')'
newline|'\n'
nl|'\n'
DECL|member|endheaders
dedent|''
name|'def'
name|'endheaders'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'origHTTPSConnection'
op|'='
name|'bufferedhttp'
op|'.'
name|'HTTPSConnection'
newline|'\n'
name|'bufferedhttp'
op|'.'
name|'HTTPSConnection'
op|'='
name|'MockHTTPSConnection'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'bufferedhttp'
op|'.'
name|'http_connect'
op|'('
string|"'127.0.0.1'"
op|','
number|'8080'
op|','
string|"'sda'"
op|','
number|'1'
op|','
string|"'GET'"
op|','
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-one'"
op|':'
string|"'1'"
op|','
string|"'x-two'"
op|':'
number|'2'
op|','
string|"'x-three'"
op|':'
number|'3.0'
op|','
nl|'\n'
string|"'x-four'"
op|':'
op|'{'
string|"'crazy'"
op|':'
string|"'value'"
op|'}'
op|'}'
op|','
name|'ssl'
op|'='
name|'True'
op|')'
newline|'\n'
name|'bufferedhttp'
op|'.'
name|'http_connect_raw'
op|'('
string|"'127.0.0.1'"
op|','
number|'8080'
op|','
string|"'GET'"
op|','
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-one'"
op|':'
string|"'1'"
op|','
string|"'x-two'"
op|':'
number|'2'
op|','
string|"'x-three'"
op|':'
number|'3.0'
op|','
nl|'\n'
string|"'x-four'"
op|':'
op|'{'
string|"'crazy'"
op|':'
string|"'value'"
op|'}'
op|'}'
op|','
name|'ssl'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'bufferedhttp'
op|'.'
name|'HTTPSConnection'
op|'='
name|'origHTTPSConnection'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
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
