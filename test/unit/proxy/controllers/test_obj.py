begin_unit
comment|'#!/usr/bin/env python'
nl|'\n'
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
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
nl|'\n'
name|'import'
name|'mock'
newline|'\n'
nl|'\n'
name|'import'
name|'swift'
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
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPException'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeRing'
op|','
name|'FakeMemcache'
op|','
name|'fake_http_connect'
newline|'\n'
nl|'\n'
nl|'\n'
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|set_http_connect
name|'def'
name|'set_http_connect'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'old_connect'
op|'='
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'http_connect'
newline|'\n'
name|'new_connect'
op|'='
name|'fake_http_connect'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'http_connect'
op|'='
name|'new_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'obj'
op|'.'
name|'http_connect'
op|'='
name|'new_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'account'
op|'.'
name|'http_connect'
op|'='
name|'new_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'container'
op|'.'
name|'http_connect'
op|'='
name|'new_connect'
newline|'\n'
name|'yield'
name|'new_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'http_connect'
op|'='
name|'old_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'obj'
op|'.'
name|'http_connect'
op|'='
name|'old_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'account'
op|'.'
name|'http_connect'
op|'='
name|'old_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'container'
op|'.'
name|'http_connect'
op|'='
name|'old_connect'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjControllerWriteAffinity
dedent|''
name|'class'
name|'TestObjControllerWriteAffinity'
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
name|'object_ring'
op|'='
name|'FakeRing'
op|'('
name|'max_more_nodes'
op|'='
number|'9'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'request_node_count'
op|'='
name|'lambda'
name|'replicas'
op|':'
number|'10000000'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'sort_nodes'
op|'='
name|'lambda'
name|'l'
op|':'
name|'l'
comment|'# stop shuffling the primary nodes'
newline|'\n'
nl|'\n'
DECL|member|test_iter_nodes_local_first_noops_when_no_affinity
dedent|''
name|'def'
name|'test_iter_nodes_local_first_noops_when_no_affinity'
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
name|'ObjectController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'write_affinity_is_local_fn'
op|'='
name|'None'
newline|'\n'
nl|'\n'
name|'all_nodes'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_part_nodes'
op|'('
number|'1'
op|')'
newline|'\n'
name|'all_nodes'
op|'.'
name|'extend'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'local_first_nodes'
op|'='
name|'list'
op|'('
name|'controller'
op|'.'
name|'iter_nodes_local_first'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|','
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'maxDiff'
op|'='
name|'None'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'all_nodes'
op|','
name|'local_first_nodes'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_iter_nodes_local_first_moves_locals_first
dedent|''
name|'def'
name|'test_iter_nodes_local_first_moves_locals_first'
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
name|'ObjectController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'write_affinity_is_local_fn'
op|'='
op|'('
nl|'\n'
name|'lambda'
name|'node'
op|':'
name|'node'
op|'['
string|"'region'"
op|']'
op|'=='
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'write_affinity_node_count'
op|'='
name|'lambda'
name|'ring'
op|':'
number|'4'
newline|'\n'
nl|'\n'
name|'all_nodes'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_part_nodes'
op|'('
number|'1'
op|')'
newline|'\n'
name|'all_nodes'
op|'.'
name|'extend'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'local_first_nodes'
op|'='
name|'list'
op|'('
name|'controller'
op|'.'
name|'iter_nodes_local_first'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|','
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# the local nodes move up in the ordering'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
op|'['
number|'1'
op|','
number|'1'
op|','
number|'1'
op|','
number|'1'
op|']'
op|','
nl|'\n'
op|'['
name|'node'
op|'['
string|"'region'"
op|']'
name|'for'
name|'node'
name|'in'
name|'local_first_nodes'
op|'['
op|':'
number|'4'
op|']'
op|']'
op|')'
newline|'\n'
comment|"# we don't skip any nodes"
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'sorted'
op|'('
name|'all_nodes'
op|')'
op|','
name|'sorted'
op|'('
name|'local_first_nodes'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_connect_put_node_timeout
dedent|''
name|'def'
name|'test_connect_put_node_timeout'
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
name|'ObjectController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'conn_timeout'
op|'='
number|'0.1'
newline|'\n'
name|'with'
name|'set_http_connect'
op|'('
number|'200'
op|','
name|'slow_connect'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'nodes'
op|'='
op|'['
name|'dict'
op|'('
name|'ip'
op|'='
string|"''"
op|','
name|'port'
op|'='
string|"''"
op|','
name|'device'
op|'='
string|"''"
op|')'
op|']'
newline|'\n'
name|'res'
op|'='
name|'controller'
op|'.'
name|'_connect_put_node'
op|'('
name|'nodes'
op|','
string|"''"
op|','
string|"''"
op|','
op|'{'
op|'}'
op|','
op|'('
string|"''"
op|','
string|"''"
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'res'
name|'is'
name|'None'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjController
dedent|''
dedent|''
name|'class'
name|'TestObjController'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_PUT_log_info
indent|'    '
name|'def'
name|'test_PUT_log_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# mock out enough to get to the area of the code we want to test'
nl|'\n'
indent|'        '
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.obj.check_object_creation'"
op|','
nl|'\n'
name|'mock'
op|'.'
name|'MagicMock'
op|'('
name|'return_value'
op|'='
name|'None'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'app'
op|'='
name|'mock'
op|'.'
name|'MagicMock'
op|'('
op|')'
newline|'\n'
name|'app'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'.'
name|'return_value'
op|'='
op|'('
number|'1'
op|','
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_nodes'
op|'.'
name|'return_value'
op|'='
op|'('
number|'1'
op|','
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ObjectController'
op|'('
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'controller'
op|'.'
name|'container_info'
op|'='
name|'mock'
op|'.'
name|'MagicMock'
op|'('
name|'return_value'
op|'='
op|'{'
nl|'\n'
string|"'partition'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'nodes'"
op|':'
op|'['
op|'{'
op|'}'
op|']'
op|','
nl|'\n'
string|"'write_acl'"
op|':'
name|'None'
op|','
nl|'\n'
string|"'sync_key'"
op|':'
name|'None'
op|','
nl|'\n'
string|"'versions'"
op|':'
name|'None'
op|'}'
op|')'
newline|'\n'
comment|'# and now test that we add the header to log_info'
nl|'\n'
name|'req'
op|'='
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-copy-from'"
op|']'
op|'='
string|"'somewhere'"
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'controller'
op|'.'
name|'PUT'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
op|'['
string|"'x-copy-from:somewhere'"
op|']'
op|')'
newline|'\n'
comment|"# and then check that we don't do that for originating POSTs"
nl|'\n'
name|'req'
op|'='
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
string|"'POST'"
newline|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-copy-from'"
op|']'
op|'='
string|"'elsewhere'"
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'controller'
op|'.'
name|'PUT'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
name|'None'
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
