begin_unit
comment|'#!/usr/bin/python -u'
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
name|'from'
name|'os'
name|'import'
name|'listdir'
op|','
name|'unlink'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'join'
name|'as'
name|'path_join'
newline|'\n'
name|'from'
name|'unittest'
name|'import'
name|'main'
op|','
name|'TestCase'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'direct_client'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'hash_path'
op|','
name|'readconf'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'diskfile'
name|'import'
name|'write_metadata'
op|','
name|'read_metadata'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_servers'
op|','
name|'reset_environment'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_data_file_path
name|'def'
name|'get_data_file_path'
op|'('
name|'obj_dir'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'files'
op|'='
name|'sorted'
op|'('
name|'listdir'
op|'('
name|'obj_dir'
op|')'
op|','
name|'reverse'
op|'='
name|'True'
op|')'
newline|'\n'
name|'for'
name|'filename'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'path_join'
op|'('
name|'obj_dir'
op|','
name|'filename'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectFailures
dedent|''
dedent|''
name|'class'
name|'TestObjectFailures'
op|'('
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
op|'('
name|'self'
op|'.'
name|'pids'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'account_ring'
op|','
name|'self'
op|'.'
name|'container_ring'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_ring'
op|','
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'configs'
op|')'
op|'='
name|'reset_environment'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'kill_servers'
op|'('
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_setup_data_file
dedent|''
name|'def'
name|'_setup_data_file'
op|'('
name|'self'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'data'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container'
op|')'
newline|'\n'
name|'client'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'data'
op|')'
newline|'\n'
name|'odata'
op|'='
name|'client'
op|'.'
name|'get_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'odata'
op|','
name|'data'
op|')'
newline|'\n'
name|'opart'
op|','
name|'onodes'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'onode'
op|'='
name|'onodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'node_id'
op|'='
op|'('
name|'onode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
newline|'\n'
name|'device'
op|'='
name|'onode'
op|'['
string|"'device'"
op|']'
newline|'\n'
name|'hash_str'
op|'='
name|'hash_path'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'obj_server_conf'
op|'='
name|'readconf'
op|'('
name|'self'
op|'.'
name|'configs'
op|'['
string|"'object'"
op|']'
op|'%'
name|'node_id'
op|')'
newline|'\n'
name|'devices'
op|'='
name|'obj_server_conf'
op|'['
string|"'app:object-server'"
op|']'
op|'['
string|"'devices'"
op|']'
newline|'\n'
name|'obj_dir'
op|'='
string|"'%s/%s/objects/%s/%s/%s/'"
op|'%'
op|'('
name|'devices'
op|','
nl|'\n'
name|'device'
op|','
name|'opart'
op|','
nl|'\n'
name|'hash_str'
op|'['
op|'-'
number|'3'
op|':'
op|']'
op|','
name|'hash_str'
op|')'
newline|'\n'
name|'data_file'
op|'='
name|'get_data_file_path'
op|'('
name|'obj_dir'
op|')'
newline|'\n'
name|'return'
name|'onode'
op|','
name|'opart'
op|','
name|'data_file'
newline|'\n'
nl|'\n'
DECL|member|run_quarantine
dedent|''
name|'def'
name|'run_quarantine'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'data_file'
op|'='
name|'self'
op|'.'
name|'_setup_data_file'
op|'('
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
string|"'VERIFY'"
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'metadata'
op|'='
name|'read_metadata'
op|'('
name|'fpointer'
op|')'
newline|'\n'
dedent|''
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|'='
string|"'badetag'"
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'write_metadata'
op|'('
name|'fpointer'
op|','
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'odata'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
nl|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'odata'
op|','
string|"'VERIFY'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'raise'
name|'Exception'
op|'('
string|'"Did not quarantine object"'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_quarantine_range_etag
dedent|''
dedent|''
name|'def'
name|'run_quarantine_range_etag'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|'='
string|"'container-range-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'object-range-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'data_file'
op|'='
name|'self'
op|'.'
name|'_setup_data_file'
op|'('
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
string|"'RANGE'"
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'metadata'
op|'='
name|'read_metadata'
op|'('
name|'fpointer'
op|')'
newline|'\n'
dedent|''
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|'='
string|"'badetag'"
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'write_metadata'
op|'('
name|'fpointer'
op|','
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'header'
op|','
name|'result'
name|'in'
op|'['
op|'('
op|'{'
string|"'Range'"
op|':'
string|"'bytes=0-2'"
op|'}'
op|','
string|"'RAN'"
op|')'
op|','
nl|'\n'
op|'('
op|'{'
string|"'Range'"
op|':'
string|"'bytes=1-11'"
op|'}'
op|','
string|"'ANGE'"
op|')'
op|','
nl|'\n'
op|'('
op|'{'
string|"'Range'"
op|':'
string|"'bytes=0-11'"
op|'}'
op|','
string|"'RANGE'"
op|')'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'odata'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
nl|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'headers'
op|'='
name|'header'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'odata'
op|','
name|'result'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'raise'
name|'Exception'
op|'('
string|'"Did not quarantine object"'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_quarantine_zero_byte_get
dedent|''
dedent|''
name|'def'
name|'run_quarantine_zero_byte_get'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|'='
string|"'container-zbyte-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'object-zbyte-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'data_file'
op|'='
name|'self'
op|'.'
name|'_setup_data_file'
op|'('
name|'container'
op|','
name|'obj'
op|','
string|"'DATA'"
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'metadata'
op|'='
name|'read_metadata'
op|'('
name|'fpointer'
op|')'
newline|'\n'
dedent|''
name|'unlink'
op|'('
name|'data_file'
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|','
string|"'w'"
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'write_metadata'
op|'('
name|'fpointer'
op|','
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|','
name|'conn_timeout'
op|'='
number|'1'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'1'
op|')'
newline|'\n'
name|'raise'
name|'Exception'
op|'('
string|'"Did not quarantine object"'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_quarantine_zero_byte_head
dedent|''
dedent|''
name|'def'
name|'run_quarantine_zero_byte_head'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|'='
string|"'container-zbyte-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'object-zbyte-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'data_file'
op|'='
name|'self'
op|'.'
name|'_setup_data_file'
op|'('
name|'container'
op|','
name|'obj'
op|','
string|"'DATA'"
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'metadata'
op|'='
name|'read_metadata'
op|'('
name|'fpointer'
op|')'
newline|'\n'
dedent|''
name|'unlink'
op|'('
name|'data_file'
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|','
string|"'w'"
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'write_metadata'
op|'('
name|'fpointer'
op|','
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_head_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|','
name|'conn_timeout'
op|'='
number|'1'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'1'
op|')'
newline|'\n'
name|'raise'
name|'Exception'
op|'('
string|'"Did not quarantine object"'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_quarantine_zero_byte_post
dedent|''
dedent|''
name|'def'
name|'run_quarantine_zero_byte_post'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|'='
string|"'container-zbyte-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'object-zbyte-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'data_file'
op|'='
name|'self'
op|'.'
name|'_setup_data_file'
op|'('
name|'container'
op|','
name|'obj'
op|','
string|"'DATA'"
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'metadata'
op|'='
name|'read_metadata'
op|'('
name|'fpointer'
op|')'
newline|'\n'
dedent|''
name|'unlink'
op|'('
name|'data_file'
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'open'
op|'('
name|'data_file'
op|','
string|"'w'"
op|')'
name|'as'
name|'fpointer'
op|':'
newline|'\n'
indent|'            '
name|'write_metadata'
op|'('
name|'fpointer'
op|','
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_post_object'
op|'('
nl|'\n'
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
op|'{'
string|"'X-Object-Meta-1'"
op|':'
string|"'One'"
op|','
string|"'X-Object-Meta-Two'"
op|':'
string|"'Two'"
op|'}'
op|','
nl|'\n'
name|'conn_timeout'
op|'='
number|'1'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'1'
op|')'
newline|'\n'
name|'raise'
name|'Exception'
op|'('
string|'"Did not quarantine object"'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_runner
dedent|''
dedent|''
name|'def'
name|'test_runner'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'run_quarantine'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'run_quarantine_range_etag'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'run_quarantine_zero_byte_get'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'run_quarantine_zero_byte_head'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'run_quarantine_zero_byte_post'
op|'('
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
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
