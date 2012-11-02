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
comment|'# NOTE: swift_conn'
nl|'\n'
comment|"# You'll see swift_conn passed around a few places in this file. This is the"
nl|'\n'
comment|'# source httplib connection of whatever it is attached to.'
nl|'\n'
comment|'#   It is used when early termination of reading from the connection should'
nl|'\n'
comment|"# happen, such as when a range request is satisfied but there's still more the"
nl|'\n'
comment|'# source connection would like to send. To prevent having to read all the data'
nl|'\n'
comment|'# that could be left, the source connection can be .close() and then reads'
nl|'\n'
comment|'# commence to empty out any buffers.'
nl|'\n'
comment|'#   These shenanigans are to ensure all related objects can be garbage'
nl|'\n'
comment|"# collected. We've seen objects hang around forever otherwise."
nl|'\n'
nl|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'shuffle'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'normalize_timestamp'
op|','
name|'public'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_metadata'
op|','
name|'MAX_CONTAINER_NAME_LENGTH'
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
name|'get_container_memcache_key'
op|','
name|'headers_to_container_info'
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
op|','
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
op|','
name|'nodes'
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
name|'shuffle'
op|'('
name|'nodes'
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
name|'part'
op|','
name|'nodes'
op|','
name|'req'
op|'.'
name|'path_info'
op|','
name|'len'
op|'('
name|'nodes'
op|')'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|':'
newline|'\n'
comment|'# set the memcache container size for ratelimiting'
nl|'\n'
indent|'            '
name|'cache_key'
op|'='
name|'get_container_memcache_key'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|'.'
name|'set'
op|'('
nl|'\n'
name|'cache_key'
op|','
nl|'\n'
name|'headers_to_container_info'
op|'('
name|'resp'
op|'.'
name|'headers'
op|','
name|'resp'
op|'.'
name|'status_int'
op|')'
op|','
nl|'\n'
name|'timeout'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'recheck_container_existence'
op|')'
newline|'\n'
nl|'\n'
dedent|''
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
op|'('
string|"'x-container-read'"
op|','
string|"'x-container-write'"
op|','
nl|'\n'
string|"'x-container-sync-key'"
op|','
string|"'x-container-sync-to'"
op|')'
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
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'container_name'
op|')'
op|'>'
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
nl|'\n'
name|'autocreate'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_autocreate'
op|')'
newline|'\n'
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
op|'['
op|']'
newline|'\n'
name|'for'
name|'account'
name|'in'
name|'accounts'
op|':'
newline|'\n'
indent|'            '
name|'nheaders'
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
op|','
nl|'\n'
string|"'x-trans-id'"
op|':'
name|'self'
op|'.'
name|'trans_id'
op|','
nl|'\n'
string|"'X-Account-Host'"
op|':'
string|"'%(ip)s:%(port)s'"
op|'%'
name|'account'
op|','
nl|'\n'
string|"'X-Account-Partition'"
op|':'
name|'account_partition'
op|','
nl|'\n'
string|"'X-Account-Device'"
op|':'
name|'account'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
string|"'Connection'"
op|':'
string|"'close'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'transfer_headers'
op|'('
name|'req'
op|'.'
name|'headers'
op|','
name|'nheaders'
op|')'
newline|'\n'
name|'headers'
op|'.'
name|'append'
op|'('
name|'nheaders'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|':'
newline|'\n'
indent|'            '
name|'cache_key'
op|'='
name|'get_container_memcache_key'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|'.'
name|'delete'
op|'('
name|'cache_key'
op|')'
newline|'\n'
dedent|''
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
name|'path_info'
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
nl|'\n'
name|'autocreate'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_autocreate'
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
op|','
nl|'\n'
string|"'x-trans-id'"
op|':'
name|'self'
op|'.'
name|'trans_id'
op|','
nl|'\n'
string|"'Connection'"
op|':'
string|"'close'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'transfer_headers'
op|'('
name|'req'
op|'.'
name|'headers'
op|','
name|'headers'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|'.'
name|'delete'
op|'('
name|'get_container_memcache_key'
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
op|')'
newline|'\n'
dedent|''
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
name|'path_info'
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
op|'['
op|']'
newline|'\n'
name|'for'
name|'account'
name|'in'
name|'accounts'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'.'
name|'append'
op|'('
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
op|','
nl|'\n'
string|"'X-Trans-Id'"
op|':'
name|'self'
op|'.'
name|'trans_id'
op|','
nl|'\n'
string|"'X-Account-Host'"
op|':'
string|"'%(ip)s:%(port)s'"
op|'%'
name|'account'
op|','
nl|'\n'
string|"'X-Account-Partition'"
op|':'
name|'account_partition'
op|','
nl|'\n'
string|"'X-Account-Device'"
op|':'
name|'account'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
string|"'Connection'"
op|':'
string|"'close'"
op|'}'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|':'
newline|'\n'
indent|'            '
name|'cache_key'
op|'='
name|'get_container_memcache_key'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'memcache'
op|'.'
name|'delete'
op|'('
name|'cache_key'
op|')'
newline|'\n'
dedent|''
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
name|'path_info'
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
dedent|''
dedent|''
endmarker|''
end_unit
