begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack, LLC.'
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
name|'test'
op|'.'
name|'unit'
op|'.'
name|'proxy'
name|'import'
name|'test_server'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
op|'.'
name|'proxy'
op|'.'
name|'test_server'
name|'import'
name|'teardown'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'mem_server'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|setup
name|'def'
name|'setup'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'test_server'
op|'.'
name|'do_setup'
op|'('
name|'mem_server'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestController
dedent|''
name|'class'
name|'TestController'
op|'('
name|'test_server'
op|'.'
name|'TestController'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestProxyServer
dedent|''
name|'class'
name|'TestProxyServer'
op|'('
name|'test_server'
op|'.'
name|'TestProxyServer'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectController
dedent|''
name|'class'
name|'TestObjectController'
op|'('
name|'test_server'
op|'.'
name|'TestObjectController'
op|')'
op|':'
newline|'\n'
DECL|member|test_PUT_no_etag_fallocate
indent|'    '
name|'def'
name|'test_PUT_no_etag_fallocate'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|"# mem server doesn't call fallocate(), believe it or not"
nl|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
comment|'# these tests all go looking in the filesystem'
nl|'\n'
DECL|member|test_policy_IO
dedent|''
name|'def'
name|'test_policy_IO'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|test_PUT_ec
dedent|''
name|'def'
name|'test_PUT_ec'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|test_PUT_ec_multiple_segments
dedent|''
name|'def'
name|'test_PUT_ec_multiple_segments'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|test_PUT_ec_fragment_archive_etag_mismatch
dedent|''
name|'def'
name|'test_PUT_ec_fragment_archive_etag_mismatch'
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
DECL|class|TestContainerController
dedent|''
dedent|''
name|'class'
name|'TestContainerController'
op|'('
name|'test_server'
op|'.'
name|'TestContainerController'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccountController
dedent|''
name|'class'
name|'TestAccountController'
op|'('
name|'test_server'
op|'.'
name|'TestAccountController'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
name|'class'
name|'TestAccountControllerFakeGetResponse'
op|'('
nl|'\n'
DECL|class|TestAccountControllerFakeGetResponse
name|'test_server'
op|'.'
name|'TestAccountControllerFakeGetResponse'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'setup'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'teardown'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
