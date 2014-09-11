begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack Foundation'
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
name|'time'
newline|'\n'
name|'from'
name|'xml'
op|'.'
name|'sax'
name|'import'
name|'saxutils'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPOk'
op|','
name|'HTTPNoContent'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'json'
op|','
name|'Timestamp'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeAccountBroker
name|'class'
name|'FakeAccountBroker'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Quacks like an account broker, but doesn\'t actually do anything. Responds\n    like an account broker would for a real, empty account with no metadata.\n    """'
newline|'\n'
DECL|member|get_info
name|'def'
name|'get_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'now'
op|'='
name|'Timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'.'
name|'internal'
newline|'\n'
name|'return'
op|'{'
string|"'container_count'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'object_count'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'bytes_used'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'created_at'"
op|':'
name|'now'
op|','
nl|'\n'
string|"'put_timestamp'"
op|':'
name|'now'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|list_containers_iter
dedent|''
name|'def'
name|'list_containers_iter'
op|'('
name|'self'
op|','
op|'*'
name|'_'
op|','
op|'**'
name|'__'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|metadata
name|'def'
name|'metadata'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get_policy_stats
dedent|''
name|'def'
name|'get_policy_stats'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'{'
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_response_headers
dedent|''
dedent|''
name|'def'
name|'get_response_headers'
op|'('
name|'broker'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'resp_headers'
op|'='
op|'{'
nl|'\n'
string|"'X-Account-Container-Count'"
op|':'
name|'info'
op|'['
string|"'container_count'"
op|']'
op|','
nl|'\n'
string|"'X-Account-Object-Count'"
op|':'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
string|"'X-Account-Bytes-Used'"
op|':'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'Timestamp'
op|'('
name|'info'
op|'['
string|"'created_at'"
op|']'
op|')'
op|'.'
name|'normal'
op|','
nl|'\n'
string|"'X-PUT-Timestamp'"
op|':'
name|'Timestamp'
op|'('
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|')'
op|'.'
name|'normal'
op|'}'
newline|'\n'
name|'policy_stats'
op|'='
name|'broker'
op|'.'
name|'get_policy_stats'
op|'('
op|')'
newline|'\n'
name|'for'
name|'policy_idx'
op|','
name|'stats'
name|'in'
name|'policy_stats'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'policy'
op|'='
name|'POLICIES'
op|'.'
name|'get_by_index'
op|'('
name|'policy_idx'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'policy'
op|':'
newline|'\n'
indent|'            '
name|'continue'
newline|'\n'
dedent|''
name|'header_prefix'
op|'='
string|"'X-Account-Storage-Policy-%s-%%s'"
op|'%'
name|'policy'
op|'.'
name|'name'
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'stats'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'header_name'
op|'='
name|'header_prefix'
op|'%'
name|'key'
op|'.'
name|'replace'
op|'('
string|"'_'"
op|','
string|"'-'"
op|')'
newline|'\n'
name|'resp_headers'
op|'['
name|'header_name'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
dedent|''
name|'resp_headers'
op|'.'
name|'update'
op|'('
op|'('
name|'key'
op|','
name|'value'
op|')'
nl|'\n'
name|'for'
name|'key'
op|','
op|'('
name|'value'
op|','
name|'timestamp'
op|')'
name|'in'
nl|'\n'
name|'broker'
op|'.'
name|'metadata'
op|'.'
name|'items'
op|'('
op|')'
name|'if'
name|'value'
op|'!='
string|"''"
op|')'
newline|'\n'
name|'return'
name|'resp_headers'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|account_listing_response
dedent|''
name|'def'
name|'account_listing_response'
op|'('
name|'account'
op|','
name|'req'
op|','
name|'response_content_type'
op|','
name|'broker'
op|'='
name|'None'
op|','
nl|'\n'
name|'limit'
op|'='
string|"''"
op|','
name|'marker'
op|'='
string|"''"
op|','
name|'end_marker'
op|'='
string|"''"
op|','
name|'prefix'
op|'='
string|"''"
op|','
nl|'\n'
name|'delimiter'
op|'='
string|"''"
op|','
name|'reverse'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'broker'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'broker'
op|'='
name|'FakeAccountBroker'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'resp_headers'
op|'='
name|'get_response_headers'
op|'('
name|'broker'
op|')'
newline|'\n'
nl|'\n'
name|'account_list'
op|'='
name|'broker'
op|'.'
name|'list_containers_iter'
op|'('
name|'limit'
op|','
name|'marker'
op|','
name|'end_marker'
op|','
nl|'\n'
name|'prefix'
op|','
name|'delimiter'
op|','
name|'reverse'
op|')'
newline|'\n'
name|'if'
name|'response_content_type'
op|'=='
string|"'application/json'"
op|':'
newline|'\n'
indent|'        '
name|'data'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
op|'('
name|'name'
op|','
name|'object_count'
op|','
name|'bytes_used'
op|','
name|'is_subdir'
op|')'
name|'in'
name|'account_list'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'is_subdir'
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'.'
name|'append'
op|'('
op|'{'
string|"'subdir'"
op|':'
name|'name'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'.'
name|'append'
op|'('
op|'{'
string|"'name'"
op|':'
name|'name'
op|','
string|"'count'"
op|':'
name|'object_count'
op|','
nl|'\n'
string|"'bytes'"
op|':'
name|'bytes_used'
op|'}'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'account_list'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'data'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'response_content_type'
op|'.'
name|'endswith'
op|'('
string|"'/xml'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'output_list'
op|'='
op|'['
string|'\'<?xml version="1.0" encoding="UTF-8"?>\''
op|','
nl|'\n'
string|"'<account name=%s>'"
op|'%'
name|'saxutils'
op|'.'
name|'quoteattr'
op|'('
name|'account'
op|')'
op|']'
newline|'\n'
name|'for'
op|'('
name|'name'
op|','
name|'object_count'
op|','
name|'bytes_used'
op|','
name|'is_subdir'
op|')'
name|'in'
name|'account_list'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'is_subdir'
op|':'
newline|'\n'
indent|'                '
name|'output_list'
op|'.'
name|'append'
op|'('
nl|'\n'
string|"'<subdir name=%s />'"
op|'%'
name|'saxutils'
op|'.'
name|'quoteattr'
op|'('
name|'name'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'item'
op|'='
string|"'<container><name>%s</name><count>%s</count>'"
string|"'<bytes>%s</bytes></container>'"
op|'%'
op|'('
name|'saxutils'
op|'.'
name|'escape'
op|'('
name|'name'
op|')'
op|','
name|'object_count'
op|','
name|'bytes_used'
op|')'
newline|'\n'
name|'output_list'
op|'.'
name|'append'
op|'('
name|'item'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'output_list'
op|'.'
name|'append'
op|'('
string|"'</account>'"
op|')'
newline|'\n'
name|'account_list'
op|'='
string|"'\\n'"
op|'.'
name|'join'
op|'('
name|'output_list'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'account_list'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPNoContent'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'resp_headers'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'content_type'
op|'='
name|'response_content_type'
newline|'\n'
name|'resp'
op|'.'
name|'charset'
op|'='
string|"'utf-8'"
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'account_list'
op|'='
string|"'\\n'"
op|'.'
name|'join'
op|'('
name|'r'
op|'['
number|'0'
op|']'
name|'for'
name|'r'
name|'in'
name|'account_list'
op|')'
op|'+'
string|"'\\n'"
newline|'\n'
dedent|''
name|'ret'
op|'='
name|'HTTPOk'
op|'('
name|'body'
op|'='
name|'account_list'
op|','
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'resp_headers'
op|')'
newline|'\n'
name|'ret'
op|'.'
name|'content_type'
op|'='
name|'response_content_type'
newline|'\n'
name|'ret'
op|'.'
name|'charset'
op|'='
string|"'utf-8'"
newline|'\n'
name|'return'
name|'ret'
newline|'\n'
dedent|''
endmarker|''
end_unit
