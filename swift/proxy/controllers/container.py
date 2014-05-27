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
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'public'
op|','
name|'csv_append'
op|','
name|'normalize_timestamp'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_metadata'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'constraints'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_ACCEPTED'
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
name|'Controller'
op|','
name|'delay_denial'
op|','
name|'cors_validation'
op|','
name|'clear_info_cache'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
op|','
name|'POLICY'
op|','
name|'POLICY_INDEX'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPBadRequest'
op|','
name|'HTTPForbidden'
op|','
name|'HTTPNotFound'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerController
name|'class'
name|'ContainerController'
op|'('
name|'Controller'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""WSGI controller for container requests"""'
newline|'\n'
DECL|variable|server_type
name|'server_type'
op|'='
string|"'Container'"
newline|'\n'
nl|'\n'
comment|'# Ensure these are all lowercase'
nl|'\n'
DECL|variable|pass_through_headers
name|'pass_through_headers'
op|'='
op|'['
string|"'x-container-read'"
op|','
string|"'x-container-write'"
op|','
nl|'\n'
string|"'x-container-sync-key'"
op|','
string|"'x-container-sync-to'"
op|','
nl|'\n'
string|"'x-versions-location'"
op|','
name|'POLICY_INDEX'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'container_name'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Controller'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_name'
op|'='
name|'unquote'
op|'('
name|'account_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_name'
op|'='
name|'unquote'
op|'('
name|'container_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_x_remove_headers
dedent|''
name|'def'
name|'_x_remove_headers'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'st'
op|'='
name|'self'
op|'.'
name|'server_type'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'return'
op|'['
string|"'x-remove-%s-read'"
op|'%'
name|'st'
op|','
nl|'\n'
string|"'x-remove-%s-write'"
op|'%'
name|'st'
op|','
nl|'\n'
string|"'x-remove-versions-location'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|_convert_policy_to_index
dedent|''
name|'def'
name|'_convert_policy_to_index'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Helper method to convert a policy name (from a request from a client)\n        to a policy index (for a request to a backend).\n\n        :param req: incoming request\n        """'
newline|'\n'
name|'policy_name'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
name|'POLICY'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'policy_name'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'policy'
op|'='
name|'POLICIES'
op|'.'
name|'get_by_name'
op|'('
name|'policy_name'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'policy'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'content_type'
op|'='
string|'"text/plain"'
op|','
nl|'\n'
name|'body'
op|'='
op|'('
string|'"Invalid %s \'%s\'"'
nl|'\n'
op|'%'
op|'('
name|'POLICY'
op|','
name|'policy_name'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'policy'
op|'.'
name|'is_deprecated'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
string|"'Storage Policy %r is deprecated'"
op|'%'
op|'('
name|'policy'
op|'.'
name|'name'
op|')'
newline|'\n'
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'int'
op|'('
name|'policy'
op|')'
newline|'\n'
nl|'\n'
DECL|member|clean_acls
dedent|''
name|'def'
name|'clean_acls'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
string|"'swift.clean_acl'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'header'
name|'in'
op|'('
string|"'x-container-read'"
op|','
string|"'x-container-write'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'header'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'req'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
op|'='
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.clean_acl'"
op|']'
op|'('
name|'header'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|GETorHEAD
dedent|''
name|'def'
name|'GETorHEAD'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handler for HTTP GET/HEAD requests."""'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'account_info'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
name|'req'
op|')'
op|'['
number|'1'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'part'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|'.'
name|'get_part'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'GETorHEAD_base'
op|'('
nl|'\n'
name|'req'
op|','
name|'_'
op|'('
string|"'Container'"
op|')'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|','
name|'part'
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|')'
newline|'\n'
name|'if'
string|"'swift.authorize'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'acl'
op|'='
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-container-read'"
op|')'
newline|'\n'
name|'aresp'
op|'='
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
op|'('
name|'req'
op|')'
newline|'\n'
name|'if'
name|'aresp'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'aresp'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift_owner'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'key'
name|'in'
name|'self'
op|'.'
name|'app'
op|'.'
name|'swift_owner_headers'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'key'
name|'in'
name|'resp'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'del'
name|'resp'
op|'.'
name|'headers'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'delay_denial'
newline|'\n'
op|'@'
name|'cors_validation'
newline|'\n'
DECL|member|GET
name|'def'
name|'GET'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handler for HTTP GET requests."""'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'GETorHEAD'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'delay_denial'
newline|'\n'
op|'@'
name|'cors_validation'
newline|'\n'
DECL|member|HEAD
name|'def'
name|'HEAD'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handler for HTTP HEAD requests."""'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'GETorHEAD'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'cors_validation'
newline|'\n'
DECL|member|PUT
name|'def'
name|'PUT'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""HTTP PUT request handler."""'
newline|'\n'
name|'error_response'
op|'='
name|'self'
op|'.'
name|'clean_acls'
op|'('
name|'req'
op|')'
name|'or'
name|'check_metadata'
op|'('
name|'req'
op|','
string|"'container'"
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'error_response'
newline|'\n'
dedent|''
name|'policy_index'
op|'='
name|'self'
op|'.'
name|'_convert_policy_to_index'
op|'('
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift_owner'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'key'
name|'in'
name|'self'
op|'.'
name|'app'
op|'.'
name|'swift_owner_headers'
op|':'
newline|'\n'
indent|'                '
name|'req'
op|'.'
name|'headers'
op|'.'
name|'pop'
op|'('
name|'key'
op|','
name|'None'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'container_name'
op|')'
op|'>'
name|'constraints'
op|'.'
name|'MAX_CONTAINER_NAME_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|"'Container name length of %d longer than %d'"
op|'%'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'container_name'
op|')'
op|','
nl|'\n'
name|'constraints'
op|'.'
name|'MAX_CONTAINER_NAME_LENGTH'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'account_partition'
op|','
name|'accounts'
op|','
name|'container_count'
op|'='
name|'self'
op|'.'
name|'account_info'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'accounts'
name|'and'
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_autocreate'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'autocreate_account'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'account_partition'
op|','
name|'accounts'
op|','
name|'container_count'
op|'='
name|'self'
op|'.'
name|'account_info'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'accounts'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'max_containers_per_account'
op|'>'
number|'0'
name|'and'
name|'container_count'
op|'>='
name|'self'
op|'.'
name|'app'
op|'.'
name|'max_containers_per_account'
name|'and'
name|'self'
op|'.'
name|'account_name'
name|'not'
name|'in'
name|'self'
op|'.'
name|'app'
op|'.'
name|'max_containers_whitelist'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPForbidden'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|"'Reached container limit of %s'"
op|'%'
name|'self'
op|'.'
name|'app'
op|'.'
name|'max_containers_per_account'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'container_partition'
op|','
name|'containers'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'_backend_requests'
op|'('
name|'req'
op|','
name|'len'
op|'('
name|'containers'
op|')'
op|','
nl|'\n'
name|'account_partition'
op|','
name|'accounts'
op|','
nl|'\n'
name|'policy_index'
op|')'
newline|'\n'
name|'clear_info_cache'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|','
nl|'\n'
name|'container_partition'
op|','
string|"'PUT'"
op|','
name|'req'
op|'.'
name|'swift_entity_path'
op|','
name|'headers'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'cors_validation'
newline|'\n'
DECL|member|POST
name|'def'
name|'POST'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""HTTP POST request handler."""'
newline|'\n'
name|'error_response'
op|'='
name|'self'
op|'.'
name|'clean_acls'
op|'('
name|'req'
op|')'
name|'or'
name|'check_metadata'
op|'('
name|'req'
op|','
string|"'container'"
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'error_response'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift_owner'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'key'
name|'in'
name|'self'
op|'.'
name|'app'
op|'.'
name|'swift_owner_headers'
op|':'
newline|'\n'
indent|'                '
name|'req'
op|'.'
name|'headers'
op|'.'
name|'pop'
op|'('
name|'key'
op|','
name|'None'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'account_partition'
op|','
name|'accounts'
op|','
name|'container_count'
op|'='
name|'self'
op|'.'
name|'account_info'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'accounts'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'container_partition'
op|','
name|'containers'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'generate_request_headers'
op|'('
name|'req'
op|','
name|'transfer'
op|'='
name|'True'
op|')'
newline|'\n'
name|'clear_info_cache'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|','
name|'container_partition'
op|','
string|"'POST'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|','
op|'['
name|'headers'
op|']'
op|'*'
name|'len'
op|'('
name|'containers'
op|')'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'cors_validation'
newline|'\n'
DECL|member|DELETE
name|'def'
name|'DELETE'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""HTTP DELETE request handler."""'
newline|'\n'
name|'account_partition'
op|','
name|'accounts'
op|','
name|'container_count'
op|'='
name|'self'
op|'.'
name|'account_info'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'accounts'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'container_partition'
op|','
name|'containers'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'_backend_requests'
op|'('
name|'req'
op|','
name|'len'
op|'('
name|'containers'
op|')'
op|','
nl|'\n'
name|'account_partition'
op|','
name|'accounts'
op|')'
newline|'\n'
name|'clear_info_cache'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'req'
op|'.'
name|'environ'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account_name'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'container_ring'
op|','
name|'container_partition'
op|','
string|"'DELETE'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|','
name|'headers'
op|')'
newline|'\n'
comment|'# Indicates no server had the container'
nl|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_ACCEPTED'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|_backend_requests
dedent|''
name|'def'
name|'_backend_requests'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'n_outgoing'
op|','
name|'account_partition'
op|','
name|'accounts'
op|','
nl|'\n'
name|'policy_index'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'additional'
op|'='
op|'{'
string|"'X-Timestamp'"
op|':'
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'}'
newline|'\n'
name|'if'
name|'policy_index'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'additional'
op|'['
string|"'X-Backend-Storage-Policy-Default'"
op|']'
op|'='
name|'int'
op|'('
name|'POLICIES'
op|'.'
name|'default'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'additional'
op|'['
name|'POLICY_INDEX'
op|']'
op|'='
name|'str'
op|'('
name|'policy_index'
op|')'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
name|'self'
op|'.'
name|'generate_request_headers'
op|'('
name|'req'
op|','
name|'transfer'
op|'='
name|'True'
op|','
nl|'\n'
name|'additional'
op|'='
name|'additional'
op|')'
nl|'\n'
name|'for'
name|'_junk'
name|'in'
name|'range'
op|'('
name|'n_outgoing'
op|')'
op|']'
newline|'\n'
nl|'\n'
name|'for'
name|'i'
op|','
name|'account'
name|'in'
name|'enumerate'
op|'('
name|'accounts'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'='
name|'i'
op|'%'
name|'len'
op|'('
name|'headers'
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'['
name|'i'
op|']'
op|'['
string|"'X-Account-Partition'"
op|']'
op|'='
name|'account_partition'
newline|'\n'
name|'headers'
op|'['
name|'i'
op|']'
op|'['
string|"'X-Account-Host'"
op|']'
op|'='
name|'csv_append'
op|'('
nl|'\n'
name|'headers'
op|'['
name|'i'
op|']'
op|'.'
name|'get'
op|'('
string|"'X-Account-Host'"
op|')'
op|','
nl|'\n'
string|"'%(ip)s:%(port)s'"
op|'%'
name|'account'
op|')'
newline|'\n'
name|'headers'
op|'['
name|'i'
op|']'
op|'['
string|"'X-Account-Device'"
op|']'
op|'='
name|'csv_append'
op|'('
nl|'\n'
name|'headers'
op|'['
name|'i'
op|']'
op|'.'
name|'get'
op|'('
string|"'X-Account-Device'"
op|')'
op|','
nl|'\n'
name|'account'
op|'['
string|"'device'"
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'headers'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
