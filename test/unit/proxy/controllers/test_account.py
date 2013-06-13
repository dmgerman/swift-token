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
name|'mock'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
newline|'\n'
nl|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
name|'import'
name|'server'
name|'as'
name|'proxy_server'
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
name|'headers_to_account_info'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'fake_http_connect'
op|','
name|'FakeRing'
op|','
name|'FakeMemcache'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccountController
name|'class'
name|'TestAccountController'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
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
name|'proxy_server'
op|'.'
name|'Application'
op|'('
name|'None'
op|','
name|'FakeMemcache'
op|'('
op|')'
op|','
nl|'\n'
name|'account_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|','
nl|'\n'
name|'container_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|','
nl|'\n'
name|'object_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_account_info_in_response_env
dedent|''
name|'def'
name|'test_account_info_in_response_env'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'AccountController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'AUTH_bob'"
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.http_connect'"
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|','
number|'200'
op|','
name|'body'
op|'='
string|"''"
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/AUTH_bob'"
op|','
op|'{'
string|"'PATH_INFO'"
op|':'
string|"'/AUTH_bob'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'controller'
op|'.'
name|'HEAD'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'2'
op|','
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'swift.account/AUTH_bob'"
name|'in'
name|'resp'
op|'.'
name|'environ'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'headers_to_account_info'
op|'('
name|'resp'
op|'.'
name|'headers'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'swift.account/AUTH_bob'"
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
