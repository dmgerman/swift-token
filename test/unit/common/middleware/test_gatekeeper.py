begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack Foundation'
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
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
op|','
name|'Response'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'gatekeeper'
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
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
newline|'\n'
name|'self'
op|'.'
name|'req'
op|'='
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
name|'self'
op|'.'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'self'
op|'.'
name|'req'
op|','
name|'body'
op|'='
string|"'FAKE APP'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'headers'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestGatekeeper
dedent|''
dedent|''
name|'class'
name|'TestGatekeeper'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
DECL|variable|methods
indent|'    '
name|'methods'
op|'='
op|'['
string|"'PUT'"
op|','
string|"'POST'"
op|','
string|"'GET'"
op|','
string|"'DELETE'"
op|','
string|"'HEAD'"
op|','
string|"'COPY'"
op|','
string|"'OPTIONS'"
op|']'
newline|'\n'
nl|'\n'
DECL|variable|allowed_headers
name|'allowed_headers'
op|'='
op|'{'
string|"'xx-account-sysmeta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'xx-container-sysmeta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'xx-object-sysmeta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-account-meta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-container-meta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-object-meta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-timestamp-foo'"
op|':'
string|"'value'"
op|'}'
newline|'\n'
nl|'\n'
DECL|variable|sysmeta_headers
name|'sysmeta_headers'
op|'='
op|'{'
string|"'x-account-sysmeta-'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-container-sysmeta-'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-object-sysmeta-'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-account-sysmeta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-container-sysmeta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-object-sysmeta-foo'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'X-Account-Sysmeta-BAR'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'X-Container-Sysmeta-BAR'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'X-Object-Sysmeta-BAR'"
op|':'
string|"'value'"
op|'}'
newline|'\n'
nl|'\n'
DECL|variable|forbidden_headers_out
name|'forbidden_headers_out'
op|'='
name|'dict'
op|'('
name|'sysmeta_headers'
op|')'
newline|'\n'
DECL|variable|forbidden_headers_in
name|'forbidden_headers_in'
op|'='
name|'dict'
op|'('
name|'sysmeta_headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_assertHeadersEqual
name|'def'
name|'_assertHeadersEqual'
op|'('
name|'self'
op|','
name|'expected'
op|','
name|'actual'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'key'
name|'in'
name|'expected'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
name|'actual'
op|','
nl|'\n'
string|"'%s missing from %s'"
op|'%'
op|'('
name|'key'
op|','
name|'actual'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_assertHeadersAbsent
dedent|''
dedent|''
name|'def'
name|'_assertHeadersAbsent'
op|'('
name|'self'
op|','
name|'unexpected'
op|','
name|'actual'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'key'
name|'in'
name|'unexpected'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
name|'not'
name|'in'
name|'actual'
op|','
nl|'\n'
string|"'%s is in %s'"
op|'%'
op|'('
name|'key'
op|','
name|'actual'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_app
dedent|''
dedent|''
name|'def'
name|'get_app'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'factory'
op|'='
name|'gatekeeper'
op|'.'
name|'filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
newline|'\n'
name|'return'
name|'factory'
op|'('
name|'app'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_ok_header
dedent|''
name|'def'
name|'test_ok_header'
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
string|"'/v/a/c'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'allowed_headers'
op|')'
newline|'\n'
name|'fake_app'
op|'='
name|'FakeApp'
op|'('
op|')'
newline|'\n'
name|'app'
op|'='
name|'self'
op|'.'
name|'get_app'
op|'('
name|'fake_app'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"'200 OK'"
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertHeadersEqual'
op|'('
name|'self'
op|'.'
name|'allowed_headers'
op|','
name|'fake_app'
op|'.'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_test_reserved_header_removed_inbound
dedent|''
name|'def'
name|'_test_reserved_header_removed_inbound'
op|'('
name|'self'
op|','
name|'method'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'forbidden_headers_in'
op|')'
newline|'\n'
name|'headers'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'allowed_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
name|'method'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
name|'fake_app'
op|'='
name|'FakeApp'
op|'('
op|')'
newline|'\n'
name|'app'
op|'='
name|'self'
op|'.'
name|'get_app'
op|'('
name|'fake_app'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"'200 OK'"
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertHeadersEqual'
op|'('
name|'self'
op|'.'
name|'allowed_headers'
op|','
name|'fake_app'
op|'.'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertHeadersAbsent'
op|'('
name|'self'
op|'.'
name|'forbidden_headers_in'
op|','
nl|'\n'
name|'fake_app'
op|'.'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_reserved_header_removed_inbound
dedent|''
name|'def'
name|'test_reserved_header_removed_inbound'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'method'
name|'in'
name|'self'
op|'.'
name|'methods'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_test_reserved_header_removed_inbound'
op|'('
name|'method'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_test_reserved_header_removed_outbound
dedent|''
dedent|''
name|'def'
name|'_test_reserved_header_removed_outbound'
op|'('
name|'self'
op|','
name|'method'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'forbidden_headers_out'
op|')'
newline|'\n'
name|'headers'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'allowed_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
name|'method'
op|'}'
op|')'
newline|'\n'
name|'fake_app'
op|'='
name|'FakeApp'
op|'('
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
name|'app'
op|'='
name|'self'
op|'.'
name|'get_app'
op|'('
name|'fake_app'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"'200 OK'"
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertHeadersEqual'
op|'('
name|'self'
op|'.'
name|'allowed_headers'
op|','
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertHeadersAbsent'
op|'('
name|'self'
op|'.'
name|'forbidden_headers_out'
op|','
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_reserved_header_removed_outbound
dedent|''
name|'def'
name|'test_reserved_header_removed_outbound'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'method'
name|'in'
name|'self'
op|'.'
name|'methods'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_test_reserved_header_removed_outbound'
op|'('
name|'method'
op|')'
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
