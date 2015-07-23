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
name|'mock'
newline|'\n'
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
op|'.'
name|'acl'
name|'import'
name|'format_acl'
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
name|'swift'
op|'.'
name|'common'
name|'import'
name|'constraints'
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
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'StoragePolicy'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'get_sys_meta_prefix'
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
name|'test'
op|'.'
name|'unit'
name|'import'
name|'patch_policies'
newline|'\n'
nl|'\n'
nl|'\n'
op|'@'
name|'patch_policies'
op|'('
op|'['
name|'StoragePolicy'
op|'('
number|'0'
op|','
string|"'zero'"
op|','
name|'True'
op|','
name|'object_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|')'
op|']'
op|')'
newline|'\n'
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
nl|'\n'
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
name|'container_ring'
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
string|"'/v1/AUTH_bob'"
op|','
op|'{'
string|"'PATH_INFO'"
op|':'
string|"'/v1/AUTH_bob'"
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
DECL|member|test_swift_owner
dedent|''
name|'def'
name|'test_swift_owner'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'owner_headers'
op|'='
op|'{'
nl|'\n'
string|"'x-account-meta-temp-url-key'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-account-meta-temp-url-key-2'"
op|':'
string|"'value'"
op|'}'
newline|'\n'
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
string|"'a'"
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
name|'headers'
op|'='
name|'owner_headers'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
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
name|'assertEquals'
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
name|'for'
name|'key'
name|'in'
name|'owner_headers'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'not'
name|'in'
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
op|','
name|'environ'
op|'='
op|'{'
string|"'swift_owner'"
op|':'
name|'True'
op|'}'
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
name|'headers'
op|'='
name|'owner_headers'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
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
name|'assertEquals'
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
name|'for'
name|'key'
name|'in'
name|'owner_headers'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_deleted_account
dedent|''
dedent|''
name|'def'
name|'test_get_deleted_account'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp_headers'
op|'='
op|'{'
nl|'\n'
string|"'x-account-status'"
op|':'
string|"'deleted'"
op|','
nl|'\n'
op|'}'
newline|'\n'
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
string|"'a'"
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
number|'404'
op|','
name|'headers'
op|'='
name|'resp_headers'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
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
name|'assertEquals'
op|'('
number|'410'
op|','
name|'resp'
op|'.'
name|'status_int'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_long_acct_names
dedent|''
name|'def'
name|'test_long_acct_names'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'long_acct_name'
op|'='
string|"'%sLongAccountName'"
op|'%'
op|'('
nl|'\n'
string|"'Very'"
op|'*'
op|'('
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|'//'
number|'4'
op|')'
op|')'
newline|'\n'
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
name|'long_acct_name'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/%s'"
op|'%'
name|'long_acct_name'
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
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
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
name|'assertEquals'
op|'('
number|'400'
op|','
name|'resp'
op|'.'
name|'status_int'
op|')'
newline|'\n'
nl|'\n'
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
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'controller'
op|'.'
name|'GET'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
number|'400'
op|','
name|'resp'
op|'.'
name|'status_int'
op|')'
newline|'\n'
nl|'\n'
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
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'controller'
op|'.'
name|'POST'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
number|'400'
op|','
name|'resp'
op|'.'
name|'status_int'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_make_callback_func
dedent|''
name|'def'
name|'_make_callback_func'
op|'('
name|'self'
op|','
name|'context'
op|')'
op|':'
newline|'\n'
DECL|function|callback
indent|'        '
name|'def'
name|'callback'
op|'('
name|'ipaddr'
op|','
name|'port'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'method'
op|','
name|'path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'None'
op|','
name|'query_string'
op|'='
name|'None'
op|','
name|'ssl'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'context'
op|'['
string|"'method'"
op|']'
op|'='
name|'method'
newline|'\n'
name|'context'
op|'['
string|"'path'"
op|']'
op|'='
name|'path'
newline|'\n'
name|'context'
op|'['
string|"'headers'"
op|']'
op|'='
name|'headers'
name|'or'
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'return'
name|'callback'
newline|'\n'
nl|'\n'
DECL|member|test_sys_meta_headers_PUT
dedent|''
name|'def'
name|'test_sys_meta_headers_PUT'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check that headers in sys meta namespace make it through'
nl|'\n'
comment|'# the proxy controller'
nl|'\n'
indent|'        '
name|'sys_meta_key'
op|'='
string|"'%stest'"
op|'%'
name|'get_sys_meta_prefix'
op|'('
string|"'account'"
op|')'
newline|'\n'
name|'sys_meta_key'
op|'='
name|'sys_meta_key'
op|'.'
name|'title'
op|'('
op|')'
newline|'\n'
name|'user_meta_key'
op|'='
string|"'X-Account-Meta-Test'"
newline|'\n'
comment|'# allow PUTs to account...'
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'allow_account_management'
op|'='
name|'True'
newline|'\n'
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
string|"'a'"
op|')'
newline|'\n'
name|'context'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'callback'
op|'='
name|'self'
op|'.'
name|'_make_callback_func'
op|'('
name|'context'
op|')'
newline|'\n'
name|'hdrs_in'
op|'='
op|'{'
name|'sys_meta_key'
op|':'
string|"'foo'"
op|','
nl|'\n'
name|'user_meta_key'
op|':'
string|"'bar'"
op|','
nl|'\n'
string|"'x-timestamp'"
op|':'
string|"'1.0'"
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
op|','
name|'headers'
op|'='
name|'hdrs_in'
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
name|'give_connect'
op|'='
name|'callback'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'controller'
op|'.'
name|'PUT'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'method'"
op|']'
op|','
string|"'PUT'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'sys_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'sys_meta_key'
op|']'
op|','
string|"'foo'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'user_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'user_meta_key'
op|']'
op|','
string|"'bar'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
string|"'x-timestamp'"
op|']'
op|','
string|"'1.0'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sys_meta_headers_POST
dedent|''
name|'def'
name|'test_sys_meta_headers_POST'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check that headers in sys meta namespace make it through'
nl|'\n'
comment|'# the proxy controller'
nl|'\n'
indent|'        '
name|'sys_meta_key'
op|'='
string|"'%stest'"
op|'%'
name|'get_sys_meta_prefix'
op|'('
string|"'account'"
op|')'
newline|'\n'
name|'sys_meta_key'
op|'='
name|'sys_meta_key'
op|'.'
name|'title'
op|'('
op|')'
newline|'\n'
name|'user_meta_key'
op|'='
string|"'X-Account-Meta-Test'"
newline|'\n'
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
string|"'a'"
op|')'
newline|'\n'
name|'context'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'callback'
op|'='
name|'self'
op|'.'
name|'_make_callback_func'
op|'('
name|'context'
op|')'
newline|'\n'
name|'hdrs_in'
op|'='
op|'{'
name|'sys_meta_key'
op|':'
string|"'foo'"
op|','
nl|'\n'
name|'user_meta_key'
op|':'
string|"'bar'"
op|','
nl|'\n'
string|"'x-timestamp'"
op|':'
string|"'1.0'"
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
op|','
name|'headers'
op|'='
name|'hdrs_in'
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
name|'give_connect'
op|'='
name|'callback'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'controller'
op|'.'
name|'POST'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'method'"
op|']'
op|','
string|"'POST'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'sys_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'sys_meta_key'
op|']'
op|','
string|"'foo'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'user_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'user_meta_key'
op|']'
op|','
string|"'bar'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
string|"'x-timestamp'"
op|']'
op|','
string|"'1.0'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_make_user_and_sys_acl_headers_data
dedent|''
name|'def'
name|'_make_user_and_sys_acl_headers_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'acl'
op|'='
op|'{'
nl|'\n'
string|"'admin'"
op|':'
op|'['
string|"'AUTH_alice'"
op|','
string|"'AUTH_bob'"
op|']'
op|','
nl|'\n'
string|"'read-write'"
op|':'
op|'['
string|"'AUTH_carol'"
op|']'
op|','
nl|'\n'
string|"'read-only'"
op|':'
op|'['
op|']'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'user_prefix'
op|'='
string|"'x-account-'"
comment|'# external, user-facing'
newline|'\n'
name|'user_headers'
op|'='
op|'{'
op|'('
name|'user_prefix'
op|'+'
string|"'access-control'"
op|')'
op|':'
name|'format_acl'
op|'('
nl|'\n'
name|'version'
op|'='
number|'2'
op|','
name|'acl_dict'
op|'='
name|'acl'
op|')'
op|'}'
newline|'\n'
name|'sys_prefix'
op|'='
name|'get_sys_meta_prefix'
op|'('
string|"'account'"
op|')'
comment|'# internal, system-facing'
newline|'\n'
name|'sys_headers'
op|'='
op|'{'
op|'('
name|'sys_prefix'
op|'+'
string|"'core-access-control'"
op|')'
op|':'
name|'format_acl'
op|'('
nl|'\n'
name|'version'
op|'='
number|'2'
op|','
name|'acl_dict'
op|'='
name|'acl'
op|')'
op|'}'
newline|'\n'
name|'return'
name|'user_headers'
op|','
name|'sys_headers'
newline|'\n'
nl|'\n'
DECL|member|test_account_acl_headers_translated_for_GET_HEAD
dedent|''
name|'def'
name|'test_account_acl_headers_translated_for_GET_HEAD'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Verify that a GET/HEAD which receives X-Account-Sysmeta-Acl-* headers'
nl|'\n'
comment|'# from the account server will remap those headers to X-Account-Acl-*'
nl|'\n'
nl|'\n'
indent|'        '
name|'hdrs_ext'
op|','
name|'hdrs_int'
op|'='
name|'self'
op|'.'
name|'_make_user_and_sys_acl_headers_data'
op|'('
op|')'
newline|'\n'
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
string|"'acct'"
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'verb'
name|'in'
op|'('
string|"'GET'"
op|','
string|"'HEAD'"
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
string|"'/v1/acct'"
op|','
name|'environ'
op|'='
op|'{'
string|"'swift_owner'"
op|':'
name|'True'
op|'}'
op|')'
newline|'\n'
name|'controller'
op|'.'
name|'GETorHEAD_base'
op|'='
name|'lambda'
op|'*'
name|'_'
op|':'
name|'Response'
op|'('
nl|'\n'
name|'headers'
op|'='
name|'hdrs_int'
op|','
name|'environ'
op|'='
op|'{'
nl|'\n'
string|"'PATH_INFO'"
op|':'
string|"'/acct'"
op|','
nl|'\n'
string|"'REQUEST_METHOD'"
op|':'
name|'verb'
op|','
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'method'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
name|'verb'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'method'
op|'('
name|'req'
op|')'
newline|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'hdrs_ext'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'value'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
name|'header'
op|')'
op|','
name|'value'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# blank ACLs should result in no header'
nl|'\n'
indent|'                    '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'header'
name|'not'
name|'in'
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_add_acls_impossible_cases
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_add_acls_impossible_cases'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# For test coverage: verify that defensive coding does defend, in cases'
nl|'\n'
comment|"# that shouldn't arise naturally"
nl|'\n'
nl|'\n'
comment|"# add_acls should do nothing if REQUEST_METHOD isn't HEAD/GET/PUT/POST"
nl|'\n'
indent|'        '
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
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
string|"'a'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/a'"
newline|'\n'
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'='
string|"'OPTIONS'"
newline|'\n'
name|'controller'
op|'.'
name|'add_acls_from_sys_metadata'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'1'
op|','
name|'len'
op|'('
name|'resp'
op|'.'
name|'headers'
op|')'
op|')'
comment|'# we always get Content-Type'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'2'
op|','
name|'len'
op|'('
name|'resp'
op|'.'
name|'environ'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_memcache_key_impossible_cases
dedent|''
name|'def'
name|'test_memcache_key_impossible_cases'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# For test coverage: verify that defensive coding does defend, in cases'
nl|'\n'
comment|"# that shouldn't arise naturally"
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertRaises'
op|'('
nl|'\n'
name|'ValueError'
op|','
nl|'\n'
name|'lambda'
op|':'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'get_container_memcache_key'
op|'('
nl|'\n'
string|"'/a'"
op|','
name|'None'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_stripping_swift_admin_headers
dedent|''
name|'def'
name|'test_stripping_swift_admin_headers'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Verify that a GET/HEAD which receives privileged headers from the'
nl|'\n'
comment|'# account server will strip those headers for non-swift_owners'
nl|'\n'
nl|'\n'
indent|'        '
name|'hdrs_ext'
op|','
name|'hdrs_int'
op|'='
name|'self'
op|'.'
name|'_make_user_and_sys_acl_headers_data'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'x-account-meta-harmless'"
op|':'
string|"'hi mom'"
op|','
nl|'\n'
string|"'x-account-meta-temp-url-key'"
op|':'
string|"'s3kr1t'"
op|','
nl|'\n'
op|'}'
newline|'\n'
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
string|"'acct'"
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'verb'
name|'in'
op|'('
string|"'GET'"
op|','
string|"'HEAD'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'env'
name|'in'
op|'('
op|'{'
string|"'swift_owner'"
op|':'
name|'True'
op|'}'
op|','
op|'{'
string|"'swift_owner'"
op|':'
name|'False'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/acct'"
op|','
name|'environ'
op|'='
name|'env'
op|')'
newline|'\n'
name|'controller'
op|'.'
name|'GETorHEAD_base'
op|'='
name|'lambda'
op|'*'
name|'_'
op|':'
name|'Response'
op|'('
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|','
name|'environ'
op|'='
op|'{'
nl|'\n'
string|"'PATH_INFO'"
op|':'
string|"'/acct'"
op|','
nl|'\n'
string|"'REQUEST_METHOD'"
op|':'
name|'verb'
op|','
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'method'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
name|'verb'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'method'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-account-meta-harmless'"
op|')'
op|','
nl|'\n'
string|"'hi mom'"
op|')'
newline|'\n'
name|'privileged_header_present'
op|'='
op|'('
nl|'\n'
string|"'x-account-meta-temp-url-key'"
name|'in'
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'privileged_header_present'
op|','
name|'env'
op|'['
string|"'swift_owner'"
op|']'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
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
