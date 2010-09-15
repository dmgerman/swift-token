begin_unit
comment|'# Copyright (c) 2010 OpenStack, LLC.'
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
name|'time'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'timeout'
name|'import'
name|'Timeout'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPForbidden'
op|','
name|'HTTPUnauthorized'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'bufferedhttp'
name|'import'
name|'http_connect_raw'
name|'as'
name|'http_connect'
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
name|'clean_acl'
op|','
name|'parse_acl'
op|','
name|'referrer_allowed'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'cache_from_env'
op|','
name|'split_path'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DevAuth
name|'class'
name|'DevAuth'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Auth Middleware that uses the dev auth server."""'
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
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'reseller_prefix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'reseller_prefix'"
op|','
string|"'AUTH'"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'reseller_prefix'
name|'and'
name|'self'
op|'.'
name|'reseller_prefix'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'_'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'reseller_prefix'
op|'+='
string|"'_'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auth_host'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'ip'"
op|','
string|"'127.0.0.1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auth_port'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'port'"
op|','
number|'11000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ssl'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'ssl'"
op|','
string|"'false'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'true'"
op|','
string|"'on'"
op|','
string|"'1'"
op|','
string|"'yes'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'node_timeout'"
op|','
number|'10'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Accepts a standard WSGI application call, authenticating the request\n        and installing callback hooks for authorization and ACL header\n        validation. For an authenticated request, REMOTE_USER will be set to a\n        comma separated list of the user\'s groups.\n        """'
newline|'\n'
name|'token'
op|'='
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_AUTH_TOKEN'"
op|','
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_STORAGE_TOKEN'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'token'
name|'and'
name|'token'
op|'.'
name|'startswith'
op|'('
name|'self'
op|'.'
name|'reseller_prefix'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'groups'
op|'='
name|'None'
newline|'\n'
name|'memcache_client'
op|'='
name|'cache_from_env'
op|'('
name|'env'
op|')'
newline|'\n'
name|'key'
op|'='
string|"'%s/token/%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'reseller_prefix'
op|','
name|'token'
op|')'
newline|'\n'
name|'cached_auth_data'
op|'='
name|'memcache_client'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
newline|'\n'
name|'if'
name|'cached_auth_data'
op|':'
newline|'\n'
indent|'                '
name|'start'
op|','
name|'expiration'
op|','
name|'groups'
op|'='
name|'cached_auth_data'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
op|'>'
name|'expiration'
op|':'
newline|'\n'
indent|'                    '
name|'groups'
op|'='
name|'None'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'groups'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'Timeout'
op|'('
name|'self'
op|'.'
name|'timeout'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'self'
op|'.'
name|'auth_host'
op|','
name|'self'
op|'.'
name|'auth_port'
op|','
string|"'GET'"
op|','
nl|'\n'
string|"'/token/%s'"
op|'%'
name|'token'
op|','
name|'ssl'
op|'='
name|'self'
op|'.'
name|'ssl'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'resp'
op|'.'
name|'status'
op|'//'
number|'100'
op|'!='
number|'2'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'HTTPUnauthorized'
op|'('
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'expiration'
op|'='
name|'float'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-auth-ttl'"
op|')'
op|')'
newline|'\n'
name|'groups'
op|'='
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-auth-groups'"
op|')'
newline|'\n'
name|'memcache_client'
op|'.'
name|'set'
op|'('
name|'key'
op|','
op|'('
name|'time'
op|'('
op|')'
op|','
name|'expiration'
op|','
name|'groups'
op|')'
op|','
nl|'\n'
name|'timeout'
op|'='
name|'expiration'
op|')'
newline|'\n'
dedent|''
name|'env'
op|'['
string|"'REMOTE_USER'"
op|']'
op|'='
name|'groups'
newline|'\n'
name|'env'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'self'
op|'.'
name|'authorize'
newline|'\n'
name|'env'
op|'['
string|"'swift.clean_acl'"
op|']'
op|'='
name|'clean_acl'
newline|'\n'
comment|'# We know the proxy logs the token, so we augment it just a bit to'
nl|'\n'
comment|'# also log the authenticated user.'
nl|'\n'
name|'user'
op|'='
name|'groups'
name|'and'
name|'groups'
op|'.'
name|'split'
op|'('
string|"','"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
name|'or'
string|"''"
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
string|"'%s,%s'"
op|'%'
op|'('
name|'user'
op|','
name|'token'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'version'
op|','
name|'rest'
op|'='
name|'split_path'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'PATH_INFO'"
op|','
string|"''"
op|')'
op|','
number|'1'
op|','
number|'2'
op|','
name|'True'
op|')'
newline|'\n'
name|'if'
name|'rest'
name|'and'
name|'rest'
op|'.'
name|'startswith'
op|'('
name|'self'
op|'.'
name|'reseller_prefix'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'env'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'self'
op|'.'
name|'authorize'
newline|'\n'
name|'env'
op|'['
string|"'swift.clean_acl'"
op|']'
op|'='
name|'clean_acl'
newline|'\n'
dedent|''
name|'elif'
string|"'swift.authorize'"
name|'not'
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'                '
name|'env'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'self'
op|'.'
name|'denied_response'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|authorize
dedent|''
name|'def'
name|'authorize'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns None if the request is authorized to continue or a standard\n        WSGI response callable if not.\n        """'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'req'
op|'.'
name|'path'
op|','
number|'1'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'account'
name|'or'
name|'not'
name|'account'
op|'.'
name|'startswith'
op|'('
name|'self'
op|'.'
name|'reseller_prefix'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'user_groups'
op|'='
op|'('
name|'req'
op|'.'
name|'remote_user'
name|'or'
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
newline|'\n'
name|'if'
string|"'.reseller_admin'"
name|'in'
name|'user_groups'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'account'
name|'in'
name|'user_groups'
name|'and'
op|'('
name|'req'
op|'.'
name|'method'
op|'!='
string|"'PUT'"
name|'or'
name|'container'
op|')'
op|':'
newline|'\n'
comment|'# If the user is admin for the account and is not trying to do an'
nl|'\n'
comment|'# account PUT...'
nl|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'referrers'
op|','
name|'groups'
op|'='
name|'parse_acl'
op|'('
name|'getattr'
op|'('
name|'req'
op|','
string|"'acl'"
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'if'
name|'referrer_allowed'
op|'('
name|'req'
op|'.'
name|'referer'
op|','
name|'referrers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'req'
op|'.'
name|'remote_user'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'user_group'
name|'in'
name|'user_groups'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'user_group'
name|'in'
name|'groups'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'None'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|denied_response
dedent|''
name|'def'
name|'denied_response'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns a standard WSGI response callable with the status of 403 or 401\n        depending on whether the REMOTE_USER is set or not.\n        """'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'remote_user'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPForbidden'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPUnauthorized'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
dedent|''
dedent|''
dedent|''
name|'def'
name|'filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Returns a WSGI filter app for use with paste.deploy."""'
newline|'\n'
name|'conf'
op|'='
name|'global_conf'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'.'
name|'update'
op|'('
name|'local_conf'
op|')'
newline|'\n'
DECL|function|auth_filter
name|'def'
name|'auth_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'DevAuth'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'auth_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
