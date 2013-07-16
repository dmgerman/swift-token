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
name|'mock'
name|'import'
name|'patch'
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
name|'headers_to_container_info'
op|','
name|'headers_to_account_info'
op|','
name|'headers_to_object_info'
op|','
name|'get_container_info'
op|','
name|'get_container_memcache_key'
op|','
name|'get_account_info'
op|','
name|'get_account_memcache_key'
op|','
name|'get_object_env_key'
op|','
name|'_get_cache_key'
op|','
name|'get_info'
op|','
name|'get_object_info'
op|','
name|'Controller'
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
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
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
name|'proxy'
name|'import'
name|'server'
name|'as'
name|'proxy_server'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|FakeResponse_status_int
name|'FakeResponse_status_int'
op|'='
number|'201'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeResponse
name|'class'
name|'FakeResponse'
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
op|','
name|'env'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
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
name|'status_int'
op|'='
name|'FakeResponse_status_int'
newline|'\n'
name|'self'
op|'.'
name|'environ'
op|'='
name|'env'
newline|'\n'
name|'if'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'env_key'
op|'='
name|'get_object_env_key'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'cache_key'
op|','
name|'env_key'
op|'='
name|'_get_cache_key'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'account'
name|'and'
name|'container'
name|'and'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'='
name|'headers_to_object_info'
op|'('
name|'headers'
op|','
name|'FakeResponse_status_int'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'account'
name|'and'
name|'container'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'='
name|'headers_to_container_info'
op|'('
name|'headers'
op|','
name|'FakeResponse_status_int'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'='
name|'headers_to_account_info'
op|'('
name|'headers'
op|','
name|'FakeResponse_status_int'
op|')'
newline|'\n'
dedent|''
name|'env'
op|'['
name|'env_key'
op|']'
op|'='
name|'info'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeRequest
dedent|''
dedent|''
name|'class'
name|'FakeRequest'
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
name|'env'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'environ'
op|'='
name|'env'
newline|'\n'
op|'('
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|'='
name|'split_path'
op|'('
name|'path'
op|','
number|'2'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account'
op|'='
name|'account'
newline|'\n'
name|'self'
op|'.'
name|'container'
op|'='
name|'container'
newline|'\n'
name|'self'
op|'.'
name|'obj'
op|'='
name|'obj'
newline|'\n'
name|'if'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'headers'
op|'='
op|'{'
string|"'content-length'"
op|':'
number|'5555'
op|','
nl|'\n'
string|"'content-type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'stype'
op|'='
name|'container'
name|'and'
string|"'container'"
name|'or'
string|"'account'"
newline|'\n'
name|'self'
op|'.'
name|'headers'
op|'='
op|'{'
string|"'x-%s-object-count'"
op|'%'
op|'('
name|'stype'
op|')'
op|':'
number|'1000'
op|','
nl|'\n'
string|"'x-%s-bytes-used'"
op|'%'
op|'('
name|'stype'
op|')'
op|':'
number|'6666'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get_response
dedent|''
dedent|''
name|'def'
name|'get_response'
op|'('
name|'self'
op|','
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'FakeResponse'
op|'('
name|'self'
op|'.'
name|'headers'
op|','
name|'self'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container'
op|','
name|'self'
op|'.'
name|'obj'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeCache
dedent|''
dedent|''
name|'class'
name|'FakeCache'
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
name|'val'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'val'
op|'='
name|'val'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
name|'def'
name|'get'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'val'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestFuncs
dedent|''
dedent|''
name|'class'
name|'TestFuncs'
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
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_GETorHEAD_base
dedent|''
name|'def'
name|'test_GETorHEAD_base'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'base'
op|'='
name|'Controller'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/a/c/o/with/slashes'"
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'http_connect'"
op|','
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
name|'base'
op|'.'
name|'GETorHEAD_base'
op|'('
name|'req'
op|','
string|"'object'"
op|','
name|'FakeRing'
op|'('
op|')'
op|','
string|"'part'"
op|','
nl|'\n'
string|"'/a/c/o/with/slashes'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'swift.object/a/c/o/with/slashes'"
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
nl|'\n'
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'swift.object/a/c/o/with/slashes'"
op|']'
op|'['
string|"'status'"
op|']'
op|','
number|'200'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/a/c/o'"
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'http_connect'"
op|','
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
name|'base'
op|'.'
name|'GETorHEAD_base'
op|'('
name|'req'
op|','
string|"'object'"
op|','
name|'FakeRing'
op|'('
op|')'
op|','
string|"'part'"
op|','
nl|'\n'
string|"'/a/c/o'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'swift.object/a/c/o'"
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
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'swift.object/a/c/o'"
op|']'
op|'['
string|"'status'"
op|']'
op|','
number|'200'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/a/c'"
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'http_connect'"
op|','
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
name|'base'
op|'.'
name|'GETorHEAD_base'
op|'('
name|'req'
op|','
string|"'container'"
op|','
name|'FakeRing'
op|'('
op|')'
op|','
string|"'part'"
op|','
nl|'\n'
string|"'/a/c'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'swift.container/a/c'"
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
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'swift.container/a/c'"
op|']'
op|'['
string|"'status'"
op|']'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/a'"
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'http_connect'"
op|','
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
name|'base'
op|'.'
name|'GETorHEAD_base'
op|'('
name|'req'
op|','
string|"'account'"
op|','
name|'FakeRing'
op|'('
op|')'
op|','
string|"'part'"
op|','
nl|'\n'
string|"'/a'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'swift.account/a'"
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
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'swift.account/a'"
op|']'
op|'['
string|"'status'"
op|']'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_info
dedent|''
name|'def'
name|'test_get_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'global'
name|'FakeResponse_status_int'
newline|'\n'
comment|'# Do a non cached call to account'
nl|'\n'
name|'env'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info_a'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'total_object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|','
op|'{'
string|"'swift.account/a'"
op|':'
name|'info_a'
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# Do an env cached call to account'
nl|'\n'
name|'info_a'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'total_object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|','
op|'{'
string|"'swift.account/a'"
op|':'
name|'info_a'
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# This time do env cached call to account and non cached to container'
nl|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info_c'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_c'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|'['
string|"'swift.account/a'"
op|']'
op|','
name|'info_a'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|'['
string|"'swift.container/a/c'"
op|']'
op|','
name|'info_c'
op|')'
newline|'\n'
nl|'\n'
comment|'# This time do a non cached call to account than non cached to'
nl|'\n'
comment|'# container'
nl|'\n'
name|'env'
op|'='
op|'{'
op|'}'
comment|'# abandon previous call to env'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info_c'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_c'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|'['
string|"'swift.account/a'"
op|']'
op|','
name|'info_a'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|'['
string|"'swift.container/a/c'"
op|']'
op|','
name|'info_c'
op|')'
newline|'\n'
nl|'\n'
comment|'# This time do an env cached call to container while account is not'
nl|'\n'
comment|'# cached'
nl|'\n'
name|'del'
op|'('
name|'env'
op|'['
string|"'swift.account/a'"
op|']'
op|')'
newline|'\n'
name|'info_c'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_c'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_c'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set and account still not cached'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|','
op|'{'
string|"'swift.container/a/c'"
op|':'
name|'info_c'
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# Do a non cached call to account not found with ret_not_found'
nl|'\n'
name|'env'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'FakeResponse_status_int'
op|'='
number|'404'
newline|'\n'
name|'info_a'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|','
name|'ret_not_found'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'FakeResponse_status_int'
op|'='
number|'201'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'total_object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|','
op|'{'
string|"'swift.account/a'"
op|':'
name|'info_a'
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# Do a cached call to account not found with ret_not_found'
nl|'\n'
name|'info_a'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|','
name|'ret_not_found'
op|'='
name|'True'
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|'['
string|"'total_object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
comment|'# Make sure the env cache is set'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|','
op|'{'
string|"'swift.account/a'"
op|':'
name|'info_a'
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# Do a non cached call to account not found without ret_not_found'
nl|'\n'
name|'env'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'FakeResponse_status_int'
op|'='
number|'404'
newline|'\n'
name|'info_a'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'FakeResponse_status_int'
op|'='
number|'201'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|'['
string|"'swift.account/a'"
op|']'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
comment|'# Do a cached call to account not found without ret_not_found'
nl|'\n'
name|'info_a'
op|'='
name|'get_info'
op|'('
name|'None'
op|','
name|'env'
op|','
string|"'a'"
op|')'
newline|'\n'
comment|'# Check that you got proper info'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'info_a'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'env'
op|'['
string|"'swift.account/a'"
op|']'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_container_info_no_cache
dedent|''
name|'def'
name|'test_get_container_info_no_cache'
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
string|'"/v1/AUTH_account/cont"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'get_container_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_container_info_cache
dedent|''
name|'def'
name|'test_get_container_info_cache'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cached'
op|'='
op|'{'
string|"'status'"
op|':'
number|'404'
op|','
nl|'\n'
string|"'bytes'"
op|':'
number|'3333'
op|','
nl|'\n'
string|"'object_count'"
op|':'
number|'10'
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|'"/v1/account/cont"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
name|'cached'
op|')'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'get_container_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
number|'3333'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'object_count'"
op|']'
op|','
number|'10'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_container_info_env
dedent|''
name|'def'
name|'test_get_container_info_env'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cache_key'
op|'='
name|'get_container_memcache_key'
op|'('
string|'"account"'
op|','
string|'"cont"'
op|')'
newline|'\n'
name|'env_key'
op|'='
string|"'swift.%s'"
op|'%'
name|'cache_key'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|'"/v1/account/cont"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
name|'env_key'
op|':'
op|'{'
string|"'bytes'"
op|':'
number|'3867'
op|'}'
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'get_container_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
number|'3867'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_account_info_no_cache
dedent|''
name|'def'
name|'test_get_account_info_no_cache'
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
string|'"/v1/AUTH_account"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'get_account_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
number|'6666'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'total_object_count'"
op|']'
op|','
number|'1000'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_account_info_cache
dedent|''
name|'def'
name|'test_get_account_info_cache'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# The original test that we prefer to preserve'
nl|'\n'
indent|'        '
name|'cached'
op|'='
op|'{'
string|"'status'"
op|':'
number|'404'
op|','
nl|'\n'
string|"'bytes'"
op|':'
number|'3333'
op|','
nl|'\n'
string|"'total_object_count'"
op|':'
number|'10'
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|'"/v1/account/cont"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
name|'cached'
op|')'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'get_account_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
number|'3333'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'total_object_count'"
op|']'
op|','
number|'10'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
comment|'# Here is a more realistic test'
nl|'\n'
name|'cached'
op|'='
op|'{'
string|"'status'"
op|':'
number|'404'
op|','
nl|'\n'
string|"'bytes'"
op|':'
string|"'3333'"
op|','
nl|'\n'
string|"'container_count'"
op|':'
string|"'234'"
op|','
nl|'\n'
string|"'total_object_count'"
op|':'
string|"'10'"
op|','
nl|'\n'
string|"'meta'"
op|':'
op|'{'
op|'}'
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|'"/v1/account/cont"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
name|'cached'
op|')'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'get_account_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
string|"'3333'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'container_count'"
op|']'
op|','
number|'234'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'total_object_count'"
op|']'
op|','
string|"'10'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_account_info_env
dedent|''
name|'def'
name|'test_get_account_info_env'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cache_key'
op|'='
name|'get_account_memcache_key'
op|'('
string|'"account"'
op|')'
newline|'\n'
name|'env_key'
op|'='
string|"'swift.%s'"
op|'%'
name|'cache_key'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|'"/v1/account"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
name|'env_key'
op|':'
op|'{'
string|"'bytes'"
op|':'
number|'3867'
op|'}'
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'get_account_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
number|'3867'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_object_info_env
dedent|''
name|'def'
name|'test_get_object_info_env'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cached'
op|'='
op|'{'
string|"'status'"
op|':'
number|'200'
op|','
nl|'\n'
string|"'length'"
op|':'
number|'3333'
op|','
nl|'\n'
string|"'type'"
op|':'
string|"'application/json'"
op|','
nl|'\n'
string|"'meta'"
op|':'
op|'{'
op|'}'
op|'}'
newline|'\n'
name|'env_key'
op|'='
name|'get_object_env_key'
op|'('
string|'"account"'
op|','
string|'"cont"'
op|','
string|'"obj"'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|'"/v1/account/cont/obj"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
name|'env_key'
op|':'
name|'cached'
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'get_object_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'length'"
op|']'
op|','
number|'3333'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'type'"
op|']'
op|','
string|"'application/json'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_object_info_no_env
dedent|''
name|'def'
name|'test_get_object_info_no_env'
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
string|'"/v1/account/cont/obj"'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.'"
nl|'\n'
string|"'_prepare_pre_auth_info_request'"
op|','
name|'FakeRequest'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'get_object_info'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
string|"'xxx'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'length'"
op|']'
op|','
number|'5555'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'type'"
op|']'
op|','
string|"'text/plain'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_container_info_missing
dedent|''
name|'def'
name|'test_headers_to_container_info_missing'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'headers_to_container_info'
op|'('
op|'{'
op|'}'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'read_acl'"
op|']'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'write_acl'"
op|']'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_container_info_meta
dedent|''
name|'def'
name|'test_headers_to_container_info_meta'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Container-Meta-Whatevs'"
op|':'
number|'14'
op|','
nl|'\n'
string|"'x-container-meta-somethingelse'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'headers_to_container_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|')'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'whatevs'"
op|']'
op|','
number|'14'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'somethingelse'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_container_info_values
dedent|''
name|'def'
name|'test_headers_to_container_info_values'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'x-container-read'"
op|':'
string|"'readvalue'"
op|','
nl|'\n'
string|"'x-container-write'"
op|':'
string|"'writevalue'"
op|','
nl|'\n'
string|"'x-container-sync-key'"
op|':'
string|"'keyvalue'"
op|','
nl|'\n'
string|"'x-container-meta-access-control-allow-origin'"
op|':'
string|"'here'"
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'headers_to_container_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'read_acl'"
op|']'
op|','
string|"'readvalue'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'write_acl'"
op|']'
op|','
string|"'writevalue'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'cors'"
op|']'
op|'['
string|"'allow_origin'"
op|']'
op|','
string|"'here'"
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'['
string|"'x-unused-header'"
op|']'
op|'='
string|"'blahblahblah'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'resp'
op|','
nl|'\n'
name|'headers_to_container_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_account_info_missing
dedent|''
name|'def'
name|'test_headers_to_account_info_missing'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'headers_to_account_info'
op|'('
op|'{'
op|'}'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'bytes'"
op|']'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'container_count'"
op|']'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_account_info_meta
dedent|''
name|'def'
name|'test_headers_to_account_info_meta'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Account-Meta-Whatevs'"
op|':'
number|'14'
op|','
nl|'\n'
string|"'x-account-meta-somethingelse'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'headers_to_account_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|')'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'whatevs'"
op|']'
op|','
number|'14'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'somethingelse'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_account_info_values
dedent|''
name|'def'
name|'test_headers_to_account_info_values'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'x-account-object-count'"
op|':'
string|"'10'"
op|','
nl|'\n'
string|"'x-account-container-count'"
op|':'
string|"'20'"
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'headers_to_account_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'total_object_count'"
op|']'
op|','
string|"'10'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'container_count'"
op|']'
op|','
string|"'20'"
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'['
string|"'x-unused-header'"
op|']'
op|'='
string|"'blahblahblah'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'resp'
op|','
nl|'\n'
name|'headers_to_account_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_object_info_missing
dedent|''
name|'def'
name|'test_headers_to_object_info_missing'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'headers_to_object_info'
op|'('
op|'{'
op|'}'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'status'"
op|']'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'length'"
op|']'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'etag'"
op|']'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_object_info_meta
dedent|''
name|'def'
name|'test_headers_to_object_info_meta'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-Whatevs'"
op|':'
number|'14'
op|','
nl|'\n'
string|"'x-object-meta-somethingelse'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'headers_to_object_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|')'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'whatevs'"
op|']'
op|','
number|'14'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'somethingelse'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_headers_to_object_info_values
dedent|''
name|'def'
name|'test_headers_to_object_info_values'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'content-length'"
op|':'
string|"'1024'"
op|','
nl|'\n'
string|"'content-type'"
op|':'
string|"'application/json'"
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'headers_to_object_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'length'"
op|']'
op|','
string|"'1024'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'['
string|"'type'"
op|']'
op|','
string|"'application/json'"
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'['
string|"'x-unused-header'"
op|']'
op|'='
string|"'blahblahblah'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'resp'
op|','
nl|'\n'
name|'headers_to_object_info'
op|'('
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|','
number|'200'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
