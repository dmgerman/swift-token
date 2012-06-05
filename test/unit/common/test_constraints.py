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
name|'test'
op|'.'
name|'unit'
name|'import'
name|'MockTrue'
newline|'\n'
nl|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPBadRequest'
op|','
name|'HTTPLengthRequired'
op|','
name|'HTTPRequestEntityTooLarge'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'constraints'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestConstraints
name|'class'
name|'TestConstraints'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_empty
indent|'    '
name|'def'
name|'test_check_metadata_empty'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_good
dedent|''
name|'def'
name|'test_check_metadata_good'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-Name'"
op|':'
string|"'Value'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_empty_name
dedent|''
name|'def'
name|'test_check_metadata_empty_name'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-'"
op|':'
string|"'Value'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'HTTPBadRequest'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_name_length
dedent|''
name|'def'
name|'test_check_metadata_name_length'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'name'
op|'='
string|"'a'"
op|'*'
name|'constraints'
op|'.'
name|'MAX_META_NAME_LENGTH'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-%s'"
op|'%'
name|'name'
op|':'
string|"'v'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'name'
op|'='
string|"'a'"
op|'*'
op|'('
name|'constraints'
op|'.'
name|'MAX_META_NAME_LENGTH'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-%s'"
op|'%'
name|'name'
op|':'
string|"'v'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_value_length
dedent|''
name|'def'
name|'test_check_metadata_value_length'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
string|"'a'"
op|'*'
name|'constraints'
op|'.'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-Name'"
op|':'
name|'value'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'value'
op|'='
string|"'a'"
op|'*'
op|'('
name|'constraints'
op|'.'
name|'MAX_META_VALUE_LENGTH'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Meta-Name'"
op|':'
name|'value'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_count
dedent|''
name|'def'
name|'test_check_metadata_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'x'
name|'in'
name|'xrange'
op|'('
name|'constraints'
op|'.'
name|'MAX_META_COUNT'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'['
string|"'X-Object-Meta-%d'"
op|'%'
name|'x'
op|']'
op|'='
string|"'v'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'headers'
op|'['
string|"'X-Object-Meta-Too-Many'"
op|']'
op|'='
string|"'v'"
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_metadata_size
dedent|''
name|'def'
name|'test_check_metadata_size'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'size'
op|'='
number|'0'
newline|'\n'
name|'chunk'
op|'='
name|'constraints'
op|'.'
name|'MAX_META_NAME_LENGTH'
op|'+'
name|'constraints'
op|'.'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'x'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'size'
op|'+'
name|'chunk'
op|'<'
name|'constraints'
op|'.'
name|'MAX_META_OVERALL_SIZE'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'['
string|"'X-Object-Meta-%04d%s'"
op|'%'
nl|'\n'
op|'('
name|'x'
op|','
string|"'a'"
op|'*'
op|'('
name|'constraints'
op|'.'
name|'MAX_META_NAME_LENGTH'
op|'-'
number|'4'
op|')'
op|')'
op|']'
op|'='
string|"'v'"
op|'*'
name|'constraints'
op|'.'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'size'
op|'+='
name|'chunk'
newline|'\n'
name|'x'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'headers'
op|'['
string|"'X-Object-Meta-9999%s'"
op|'%'
nl|'\n'
op|'('
string|"'a'"
op|'*'
op|'('
name|'constraints'
op|'.'
name|'MAX_META_NAME_LENGTH'
op|'-'
number|'4'
op|')'
op|')'
op|']'
op|'='
string|"'v'"
op|'*'
name|'constraints'
op|'.'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_metadata'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object'"
op|')'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_object_creation_content_length
dedent|''
name|'def'
name|'test_check_object_creation_content_length'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'constraints'
op|'.'
name|'MAX_FILE_SIZE'
op|')'
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'constraints'
op|'.'
name|'MAX_FILE_SIZE'
op|'+'
number|'1'
op|')'
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
nl|'\n'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
op|','
nl|'\n'
name|'HTTPRequestEntityTooLarge'
op|')'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'Transfer-Encoding'"
op|':'
string|"'chunked'"
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
nl|'\n'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
op|','
nl|'\n'
name|'HTTPLengthRequired'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_object_creation_name_length
dedent|''
name|'def'
name|'test_check_object_creation_name_length'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'Transfer-Encoding'"
op|':'
string|"'chunked'"
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
name|'name'
op|'='
string|"'o'"
op|'*'
name|'constraints'
op|'.'
name|'MAX_OBJECT_NAME_LENGTH'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
name|'name'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'name'
op|'='
string|"'o'"
op|'*'
op|'('
name|'constraints'
op|'.'
name|'MAX_OBJECT_NAME_LENGTH'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
nl|'\n'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'headers'
op|'='
name|'headers'
op|')'
op|','
name|'name'
op|')'
op|','
nl|'\n'
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_object_creation_content_type
dedent|''
name|'def'
name|'test_check_object_creation_content_type'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'Transfer-Encoding'"
op|':'
string|"'chunked'"
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'Transfer-Encoding'"
op|':'
string|"'chunked'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
nl|'\n'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
op|','
nl|'\n'
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_object_creation_bad_content_type
dedent|''
name|'def'
name|'test_check_object_creation_bad_content_type'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'Transfer-Encoding'"
op|':'
string|"'chunked'"
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'\\xff\\xff'"
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
nl|'\n'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'headers'
op|'='
name|'headers'
op|')'
op|','
string|"'object_name'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'Content-Type'"
name|'in'
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_object_manifest_header
dedent|''
name|'def'
name|'test_check_object_manifest_header'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Manifest'"
op|':'
string|"'container/prefix'"
op|','
string|"'Content-Length'"
op|':'
nl|'\n'
string|"'0'"
op|','
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
op|')'
op|','
string|"'manifest'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'resp'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Manifest'"
op|':'
string|"'container'"
op|','
string|"'Content-Length'"
op|':'
string|"'0'"
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
op|')'
op|','
string|"'manifest'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Manifest'"
op|':'
string|"'/container/prefix'"
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
string|"'0'"
op|','
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
op|')'
op|','
string|"'manifest'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Manifest'"
op|':'
string|"'container/prefix?query=param'"
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
string|"'0'"
op|','
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
op|')'
op|','
string|"'manifest'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Manifest'"
op|':'
string|"'container/prefix&query=param'"
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
string|"'0'"
op|','
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
op|')'
op|','
string|"'manifest'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'constraints'
op|'.'
name|'check_object_creation'
op|'('
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Object-Manifest'"
op|':'
string|"'http://host/container/prefix'"
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
string|"'0'"
op|','
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|'}'
op|')'
op|','
string|"'manifest'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'resp'
op|','
name|'HTTPBadRequest'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_mount
dedent|''
name|'def'
name|'test_check_mount'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'constraints'
op|'.'
name|'check_mount'
op|'('
string|"''"
op|','
string|"''"
op|')'
op|')'
newline|'\n'
name|'constraints'
op|'.'
name|'os'
op|'='
name|'MockTrue'
op|'('
op|')'
comment|'# mock os module'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'constraints'
op|'.'
name|'check_mount'
op|'('
string|"'/srv'"
op|','
string|"'1'"
op|')'
op|')'
newline|'\n'
name|'reload'
op|'('
name|'constraints'
op|')'
comment|'# put it back'
newline|'\n'
nl|'\n'
DECL|member|test_check_float
dedent|''
name|'def'
name|'test_check_float'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'constraints'
op|'.'
name|'check_float'
op|'('
string|"''"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'constraints'
op|'.'
name|'check_float'
op|'('
string|"'0'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_check_utf8
dedent|''
name|'def'
name|'test_check_utf8'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'unicode_sample'
op|'='
string|"u'\\uc77c\\uc601'"
newline|'\n'
name|'valid_utf8_str'
op|'='
name|'unicode_sample'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
name|'invalid_utf8_str'
op|'='
name|'unicode_sample'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
op|'['
op|':'
op|':'
op|'-'
number|'1'
op|']'
newline|'\n'
nl|'\n'
name|'for'
name|'false_argument'
name|'in'
op|'['
name|'None'
op|','
nl|'\n'
string|"''"
op|','
nl|'\n'
name|'invalid_utf8_str'
op|','
nl|'\n'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'constraints'
op|'.'
name|'check_utf8'
op|'('
name|'false_argument'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'true_argument'
name|'in'
op|'['
string|"'this is ascii and utf-8, too'"
op|','
nl|'\n'
name|'unicode_sample'
op|','
nl|'\n'
name|'valid_utf8_str'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'constraints'
op|'.'
name|'check_utf8'
op|'('
name|'true_argument'
op|')'
op|')'
newline|'\n'
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
