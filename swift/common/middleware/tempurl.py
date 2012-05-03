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
string|'"""\nTempURL Middleware\n\nAllows the creation of URLs to provide temporary access to objects.\n\nFor example, a website may wish to provide a link to download a large\nobject in Swift, but the Swift account has no public access. The\nwebsite can generate a URL that will provide GET access for a limited\ntime to the resource. When the web browser user clicks on the link,\nthe browser will download the object directly from Swift, obviating\nthe need for the website to act as a proxy for the request.\n\nIf the user were to share the link with all his friends, or\naccidentally post it on a forum, etc. the direct access would be\nlimited to the expiration time set when the website created the link.\n\nTo create such temporary URLs, first an X-Account-Meta-Temp-URL-Key\nheader must be set on the Swift account. Then, an HMAC-SHA1 (RFC 2104)\nsignature is generated using the HTTP method to allow (GET or PUT),\nthe Unix timestamp the access should be allowed until, the full path\nto the object, and the key set on the account.\n\nFor example, here is code generating the signature for a GET for 60\nseconds on /v1/AUTH_account/container/object::\n\n    import hmac\n    from hashlib import sha1\n    from time import time\n    method = \'GET\'\n    expires = int(time() + 60)\n    path = \'/v1/AUTH_account/container/object\'\n    key = \'mykey\'\n    hmac_body = \'%s\\\\n%s\\\\n%s\' % (method, expires, path)\n    sig = hmac.new(key, hmac_body, sha1).hexdigest()\n\nBe certain to use the full path, from the /v1/ onward.\n\nLet\'s say the sig ends up equaling\nda39a3ee5e6b4b0d3255bfef95601890afd80709 and expires ends up\n1323479485. Then, for example, the website could provide a link to::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/object?\n    temp_url_sig=da39a3ee5e6b4b0d3255bfef95601890afd80709&\n    temp_url_expires=1323479485\n\nAny alteration of the resource path or query arguments would result\nin 401 Unauthorized. Similary, a PUT where GET was the allowed method\nwould 401. HEAD is allowed if GET or PUT is allowed.\n\nUsing this in combination with browser form post translation\nmiddleware could also allow direct-from-browser uploads to specific\nlocations in Swift.\n\nNote that changing the X-Account-Meta-Temp-URL-Key will invalidate\nany previously generated temporary URLs within 60 seconds (the\nmemcache time for the key).\n"""'
newline|'\n'
nl|'\n'
DECL|variable|__all__
name|'__all__'
op|'='
op|'['
string|"'TempURL'"
op|','
string|"'filter_factory'"
op|','
nl|'\n'
string|"'DEFAULT_INCOMING_REMOVE_HEADERS'"
op|','
nl|'\n'
string|"'DEFAULT_INCOMING_ALLOW_HEADERS'"
op|','
nl|'\n'
string|"'DEFAULT_OUTGOING_REMOVE_HEADERS'"
op|','
nl|'\n'
string|"'DEFAULT_OUTGOING_ALLOW_HEADERS'"
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
name|'import'
name|'hmac'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'sha1'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'basename'
newline|'\n'
name|'from'
name|'StringIO'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'gmtime'
op|','
name|'strftime'
op|','
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
op|','
name|'unquote'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'parse_qs'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'make_pre_authed_env'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_UNAUTHORIZED'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#: Default headers to remove from incoming requests. Simply a whitespace'
nl|'\n'
comment|"#: delimited list of header names and names can optionally end with '*' to"
nl|'\n'
comment|'#: indicate a prefix match. DEFAULT_INCOMING_ALLOW_HEADERS is a list of'
nl|'\n'
comment|'#: exceptions to these removals.'
nl|'\n'
DECL|variable|DEFAULT_INCOMING_REMOVE_HEADERS
name|'DEFAULT_INCOMING_REMOVE_HEADERS'
op|'='
string|"'x-timestamp'"
newline|'\n'
nl|'\n'
comment|'#: Default headers as exceptions to DEFAULT_INCOMING_REMOVE_HEADERS. Simply a'
nl|'\n'
comment|'#: whitespace delimited list of header names and names can optionally end with'
nl|'\n'
comment|"#: '*' to indicate a prefix match."
nl|'\n'
DECL|variable|DEFAULT_INCOMING_ALLOW_HEADERS
name|'DEFAULT_INCOMING_ALLOW_HEADERS'
op|'='
string|"''"
newline|'\n'
nl|'\n'
comment|'#: Default headers to remove from outgoing responses. Simply a whitespace'
nl|'\n'
comment|"#: delimited list of header names and names can optionally end with '*' to"
nl|'\n'
comment|'#: indicate a prefix match. DEFAULT_OUTGOING_ALLOW_HEADERS is a list of'
nl|'\n'
comment|'#: exceptions to these removals.'
nl|'\n'
DECL|variable|DEFAULT_OUTGOING_REMOVE_HEADERS
name|'DEFAULT_OUTGOING_REMOVE_HEADERS'
op|'='
string|"'x-object-meta-*'"
newline|'\n'
nl|'\n'
comment|'#: Default headers as exceptions to DEFAULT_OUTGOING_REMOVE_HEADERS. Simply a'
nl|'\n'
comment|'#: whitespace delimited list of header names and names can optionally end with'
nl|'\n'
comment|"#: '*' to indicate a prefix match."
nl|'\n'
DECL|variable|DEFAULT_OUTGOING_ALLOW_HEADERS
name|'DEFAULT_OUTGOING_ALLOW_HEADERS'
op|'='
string|"'x-object-meta-public-*'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TempURL
name|'class'
name|'TempURL'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    WSGI Middleware to grant temporary URLs specific access to Swift\n    resources. See the overview for more information.\n\n    This middleware understands the following configuration settings::\n\n        incoming_remove_headers\n            The headers to remove from incoming requests. Simply a\n            whitespace delimited list of header names and names can\n            optionally end with \'*\' to indicate a prefix match.\n            incoming_allow_headers is a list of exceptions to these\n            removals.\n            Default: x-timestamp\n\n        incoming_allow_headers\n            The headers allowed as exceptions to\n            incoming_remove_headers. Simply a whitespace delimited\n            list of header names and names can optionally end with\n            \'*\' to indicate a prefix match.\n            Default: None\n\n        outgoing_remove_headers\n            The headers to remove from outgoing responses. Simply a\n            whitespace delimited list of header names and names can\n            optionally end with \'*\' to indicate a prefix match.\n            outgoing_allow_headers is a list of exceptions to these\n            removals.\n            Default: x-object-meta-*\n\n        outgoing_allow_headers\n            The headers allowed as exceptions to\n            outgoing_remove_headers. Simply a whitespace delimited\n            list of header names and names can optionally end with\n            \'*\' to indicate a prefix match.\n            Default: x-object-meta-public-*\n\n    :param app: The next WSGI filter or app in the paste.deploy\n                chain.\n    :param conf: The configuration dict for the middleware.\n    """'
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
comment|'#: The next WSGI application/filter in the paste.deploy pipeline.'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
comment|'#: The filter configuration dict.'
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
comment|'#: The logger to use with this middleware.'
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'tempurl'"
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_INCOMING_REMOVE_HEADERS'
newline|'\n'
name|'if'
string|"'incoming_remove_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'incoming_remove_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
string|"'HTTP_'"
op|'+'
name|'h'
op|'.'
name|'upper'
op|'('
op|')'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'_'"
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to remove from incoming requests. Uppercase WSGI env style,'
nl|'\n'
comment|'#: like `HTTP_X_PRIVATE`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_remove_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to remove from incoming requests.'
nl|'\n'
comment|'#: Uppercase WSGI env style, like `HTTP_X_SENSITIVE_*`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_remove_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_INCOMING_ALLOW_HEADERS'
newline|'\n'
name|'if'
string|"'incoming_allow_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'incoming_allow_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
string|"'HTTP_'"
op|'+'
name|'h'
op|'.'
name|'upper'
op|'('
op|')'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'_'"
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to allow in incoming requests. Uppercase WSGI env style,'
nl|'\n'
comment|'#: like `HTTP_X_MATCHES_REMOVE_PREFIX_BUT_OKAY`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_allow_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to allow in incoming requests. Uppercase'
nl|'\n'
comment|'#: WSGI env style, like `HTTP_X_MATCHES_REMOVE_PREFIX_BUT_OKAY_*`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_allow_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_OUTGOING_REMOVE_HEADERS'
newline|'\n'
name|'if'
string|"'outgoing_remove_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'outgoing_remove_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to remove from outgoing responses. Lowercase, like'
nl|'\n'
comment|'#: `x-account-meta-temp-url-key`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_remove_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to remove from outgoing responses.'
nl|'\n'
comment|'#: Lowercase, like `x-account-meta-private-*`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_remove_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_OUTGOING_ALLOW_HEADERS'
newline|'\n'
name|'if'
string|"'outgoing_allow_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'outgoing_allow_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to allow in outgoing responses. Lowercase, like'
nl|'\n'
comment|'#: `x-matches-remove-prefix-but-okay`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_allow_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to allow in outgoing responses.'
nl|'\n'
comment|'#: Lowercase, like `x-matches-remove-prefix-but-okay-*`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_allow_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
comment|'#: HTTP user agent to use for subrequests.'
nl|'\n'
name|'self'
op|'.'
name|'agent'
op|'='
string|"'%(orig)s TempURL'"
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
string|'"""\n        Main hook into the WSGI paste.deploy filter/app pipeline.\n\n        :param env: The WSGI environment dict.\n        :param start_response: The WSGI start_response hook.\n        :returns: Response as per WSGI.\n        """'
newline|'\n'
name|'temp_url_sig'
op|','
name|'temp_url_expires'
op|'='
name|'self'
op|'.'
name|'_get_temp_url_info'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'temp_url_sig'
name|'is'
name|'None'
name|'and'
name|'temp_url_expires'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
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
dedent|''
name|'if'
name|'not'
name|'temp_url_sig'
name|'or'
name|'not'
name|'temp_url_expires'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'self'
op|'.'
name|'_get_account'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'account'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'key'
op|'='
name|'self'
op|'.'
name|'_get_key'
op|'('
name|'env'
op|','
name|'account'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'key'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'HEAD'"
op|':'
newline|'\n'
indent|'            '
name|'hmac_val'
op|'='
name|'self'
op|'.'
name|'_get_hmac'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'key'
op|','
nl|'\n'
name|'request_method'
op|'='
string|"'GET'"
op|')'
newline|'\n'
name|'if'
name|'temp_url_sig'
op|'!='
name|'hmac_val'
op|':'
newline|'\n'
indent|'                '
name|'hmac_val'
op|'='
name|'self'
op|'.'
name|'_get_hmac'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'key'
op|','
nl|'\n'
name|'request_method'
op|'='
string|"'PUT'"
op|')'
newline|'\n'
name|'if'
name|'temp_url_sig'
op|'!='
name|'hmac_val'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'hmac_val'
op|'='
name|'self'
op|'.'
name|'_get_hmac'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'key'
op|')'
newline|'\n'
name|'if'
name|'temp_url_sig'
op|'!='
name|'hmac_val'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'_clean_incoming_headers'
op|'('
name|'env'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'lambda'
name|'req'
op|':'
name|'None'
newline|'\n'
name|'env'
op|'['
string|"'swift.authorize_override'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'env'
op|'['
string|"'REMOTE_USER'"
op|']'
op|'='
string|"'.wsgi.tempurl'"
newline|'\n'
nl|'\n'
DECL|function|_start_response
name|'def'
name|'_start_response'
op|'('
name|'status'
op|','
name|'headers'
op|','
name|'exc_info'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'self'
op|'.'
name|'_clean_outgoing_headers'
op|'('
name|'headers'
op|')'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'GET'"
op|':'
newline|'\n'
indent|'                '
name|'already'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'h'
op|','
name|'v'
name|'in'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'content-disposition'"
op|':'
newline|'\n'
indent|'                        '
name|'already'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'already'
op|':'
newline|'\n'
indent|'                    '
name|'headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'Content-Disposition'"
op|','
nl|'\n'
string|"'attachment; filename=%s'"
op|'%'
nl|'\n'
op|'('
name|'quote'
op|'('
name|'basename'
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|')'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'start_response'
op|'('
name|'status'
op|','
name|'headers'
op|','
name|'exc_info'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'_start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_account
dedent|''
name|'def'
name|'_get_account'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns just the account for the request, if it\'s an object GET, PUT,\n        or HEAD request; otherwise, None is returned.\n\n        :param env: The WSGI environment for the request.\n        :returns: Account str or None.\n        """'
newline|'\n'
name|'account'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
name|'in'
op|'('
string|"'GET'"
op|','
string|"'PUT'"
op|','
string|"'HEAD'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'parts'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'4'
op|')'
newline|'\n'
comment|"# Must be five parts, ['', 'v1', 'a', 'c', 'o'], must be a v1"
nl|'\n'
comment|'# request, have account, container, and object values, and the'
nl|'\n'
comment|"# object value can't just have '/'s."
nl|'\n'
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'=='
number|'5'
name|'and'
name|'not'
name|'parts'
op|'['
number|'0'
op|']'
name|'and'
name|'parts'
op|'['
number|'1'
op|']'
op|'=='
string|"'v1'"
name|'and'
name|'parts'
op|'['
number|'2'
op|']'
name|'and'
name|'parts'
op|'['
number|'3'
op|']'
name|'and'
name|'parts'
op|'['
number|'4'
op|']'
op|'.'
name|'strip'
op|'('
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'account'
op|'='
name|'parts'
op|'['
number|'2'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'account'
newline|'\n'
nl|'\n'
DECL|member|_get_temp_url_info
dedent|''
name|'def'
name|'_get_temp_url_info'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the provided temporary URL parameters (sig, expires),\n        if given and syntactically valid. Either sig or expires could\n        be None if not provided. If provided, expires is also\n        converted to an int if possible or 0 if not, and checked for\n        expiration (returns 0 if expired).\n\n        :param env: The WSGI environment for the request.\n        :returns: (sig, expires) as described above.\n        """'
newline|'\n'
name|'temp_url_sig'
op|'='
name|'temp_url_expires'
op|'='
name|'None'
newline|'\n'
name|'qs'
op|'='
name|'parse_qs'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'QUERY_STRING'"
op|','
string|"''"
op|')'
op|')'
newline|'\n'
name|'if'
string|"'temp_url_sig'"
name|'in'
name|'qs'
op|':'
newline|'\n'
indent|'            '
name|'temp_url_sig'
op|'='
name|'qs'
op|'['
string|"'temp_url_sig'"
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'if'
string|"'temp_url_expires'"
name|'in'
name|'qs'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'temp_url_expires'
op|'='
name|'int'
op|'('
name|'qs'
op|'['
string|"'temp_url_expires'"
op|']'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                '
name|'temp_url_expires'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'temp_url_expires'
op|'<'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'temp_url_expires'
op|'='
number|'0'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'temp_url_sig'
op|','
name|'temp_url_expires'
newline|'\n'
nl|'\n'
DECL|member|_get_key
dedent|''
name|'def'
name|'_get_key'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'account'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the X-Account-Meta-Temp-URL-Key header value for the\n        account, or None if none is set.\n\n        :param env: The WSGI environment for the request.\n        :param account: Account str.\n        :returns: X-Account-Meta-Temp-URL-Key str value, or None.\n        """'
newline|'\n'
name|'key'
op|'='
name|'None'
newline|'\n'
name|'memcache'
op|'='
name|'env'
op|'.'
name|'get'
op|'('
string|"'swift.cache'"
op|')'
newline|'\n'
name|'if'
name|'memcache'
op|':'
newline|'\n'
indent|'            '
name|'key'
op|'='
name|'memcache'
op|'.'
name|'get'
op|'('
string|"'temp-url-key/%s'"
op|'%'
name|'account'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'key'
op|':'
newline|'\n'
indent|'            '
name|'newenv'
op|'='
name|'make_pre_authed_env'
op|'('
name|'env'
op|','
string|"'HEAD'"
op|','
string|"'/v1/'"
op|'+'
name|'account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'agent'
op|')'
newline|'\n'
name|'newenv'
op|'['
string|"'CONTENT_LENGTH'"
op|']'
op|'='
string|"'0'"
newline|'\n'
name|'newenv'
op|'['
string|"'wsgi.input'"
op|']'
op|'='
name|'StringIO'
op|'('
string|"''"
op|')'
newline|'\n'
name|'key'
op|'='
op|'['
name|'None'
op|']'
newline|'\n'
nl|'\n'
DECL|function|_start_response
name|'def'
name|'_start_response'
op|'('
name|'status'
op|','
name|'response_headers'
op|','
name|'exc_info'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'h'
op|','
name|'v'
name|'in'
name|'response_headers'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'x-account-meta-temp-url-key'"
op|':'
newline|'\n'
indent|'                        '
name|'key'
op|'['
number|'0'
op|']'
op|'='
name|'v'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'i'
op|'='
name|'iter'
op|'('
name|'self'
op|'.'
name|'app'
op|'('
name|'newenv'
op|','
name|'_start_response'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'i'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'StopIteration'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'key'
op|'='
name|'key'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'key'
name|'and'
name|'memcache'
op|':'
newline|'\n'
indent|'                '
name|'memcache'
op|'.'
name|'set'
op|'('
string|"'temp-url-key/%s'"
op|'%'
name|'account'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'60'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'key'
newline|'\n'
nl|'\n'
DECL|member|_get_hmac
dedent|''
name|'def'
name|'_get_hmac'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'expires'
op|','
name|'key'
op|','
name|'request_method'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the hexdigest string of the HMAC-SHA1 (RFC 2104) for\n        the request.\n\n        :param env: The WSGI environment for the request.\n        :param expires: Unix timestamp as an int for when the URL\n                        expires.\n        :param key: Key str, from the X-Account-Meta-Temp-URL-Key of\n                    the account.\n        :param request_method: Optional override of the request in\n                               the WSGI env. For example, if a HEAD\n                               does not match, you may wish to\n                               override with GET to still allow the\n                               HEAD.\n        :returns: hexdigest str of the HMAC-SHA1 for the request.\n        """'
newline|'\n'
name|'if'
name|'not'
name|'request_method'
op|':'
newline|'\n'
indent|'            '
name|'request_method'
op|'='
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
newline|'\n'
dedent|''
name|'return'
name|'hmac'
op|'.'
name|'new'
op|'('
name|'key'
op|','
string|"'%s\\n%s\\n%s'"
op|'%'
op|'('
name|'request_method'
op|','
name|'expires'
op|','
nl|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|','
name|'sha1'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|_invalid
dedent|''
name|'def'
name|'_invalid'
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
string|'"""\n        Performs the necessary steps to indicate a WSGI 401\n        Unauthorized response to the request.\n\n        :param env: The WSGI environment for the request.\n        :param start_response: The WSGI start_response hook.\n        :returns: 401 response as per WSGI.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_log_request'
op|'('
name|'env'
op|','
name|'HTTP_UNAUTHORIZED'
op|')'
newline|'\n'
name|'body'
op|'='
string|"'401 Unauthorized: Temp URL invalid\\n'"
newline|'\n'
name|'start_response'
op|'('
string|"'401 Unauthorized'"
op|','
nl|'\n'
op|'['
op|'('
string|"'Content-Type'"
op|','
string|"'text/plain'"
op|')'
op|','
nl|'\n'
op|'('
string|"'Content-Length'"
op|','
name|'str'
op|'('
name|'len'
op|'('
name|'body'
op|')'
op|')'
op|')'
op|']'
op|')'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'HEAD'"
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|']'
newline|'\n'
dedent|''
name|'return'
op|'['
name|'body'
op|']'
newline|'\n'
nl|'\n'
DECL|member|_clean_incoming_headers
dedent|''
name|'def'
name|'_clean_incoming_headers'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Removes any headers from the WSGI environment as per the\n        middleware configuration for incoming requests.\n\n        :param env: The WSGI environment for the request.\n        """'
newline|'\n'
name|'for'
name|'h'
name|'in'
name|'env'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remove'
op|'='
name|'h'
name|'in'
name|'self'
op|'.'
name|'incoming_remove_headers'
newline|'\n'
name|'if'
name|'not'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'incoming_remove_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'h'
name|'in'
name|'self'
op|'.'
name|'incoming_allow_headers'
op|':'
newline|'\n'
indent|'                    '
name|'remove'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'incoming_allow_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'False'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'env'
op|'['
name|'h'
op|']'
newline|'\n'
nl|'\n'
DECL|member|_clean_outgoing_headers
dedent|''
dedent|''
dedent|''
name|'def'
name|'_clean_outgoing_headers'
op|'('
name|'self'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Removes any headers as per the middleware configuration for\n        outgoing responses.\n\n        :param headers: A WSGI start_response style list of headers,\n                        [(\'header1\', \'value), (\'header2\', \'value),\n                         ...]\n        :returns: The same headers list, but with some headers\n                  removed as per the middlware configuration for\n                  outgoing responses.\n        """'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'headers'
op|')'
newline|'\n'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remove'
op|'='
name|'h'
name|'in'
name|'self'
op|'.'
name|'outgoing_remove_headers'
newline|'\n'
name|'if'
name|'not'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'outgoing_remove_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'h'
name|'in'
name|'self'
op|'.'
name|'outgoing_allow_headers'
op|':'
newline|'\n'
indent|'                    '
name|'remove'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'outgoing_allow_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'False'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'headers'
op|'['
name|'h'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|_log_request
dedent|''
name|'def'
name|'_log_request'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'response_status_int'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Used when a request might not be logged by the underlying\n        WSGI application, but we\'d still like to record what\n        happened. An early 401 Unauthorized is a good example of\n        this.\n\n        :param env: The WSGI environment for the request.\n        :param response_status_int: The HTTP status we\'ll be replying\n                                    to the request with.\n        """'
newline|'\n'
name|'the_request'
op|'='
name|'quote'
op|'('
name|'unquote'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'PATH_INFO'"
op|')'
name|'or'
string|"'/'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'env'
op|'.'
name|'get'
op|'('
string|"'QUERY_STRING'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'the_request'
op|'='
name|'the_request'
op|'+'
string|"'?'"
op|'+'
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
newline|'\n'
dedent|''
name|'client'
op|'='
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_CLUSTER_CLIENT_IP'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'client'
name|'and'
string|"'HTTP_X_FORWARDED_FOR'"
name|'in'
name|'env'
op|':'
newline|'\n'
comment|'# remote host for other lbs'
nl|'\n'
indent|'            '
name|'client'
op|'='
name|'env'
op|'['
string|"'HTTP_X_FORWARDED_FOR'"
op|']'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
op|'['
number|'0'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'client'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|'='
name|'env'
op|'.'
name|'get'
op|'('
string|"'REMOTE_ADDR'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"' '"
op|'.'
name|'join'
op|'('
name|'quote'
op|'('
name|'str'
op|'('
name|'x'
op|')'
op|')'
name|'for'
name|'x'
name|'in'
op|'('
nl|'\n'
name|'client'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'REMOTE_ADDR'"
op|')'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'strftime'
op|'('
string|"'%d/%b/%Y/%H/%M/%S'"
op|','
name|'gmtime'
op|'('
op|')'
op|')'
op|','
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'REQUEST_METHOD'"
op|')'
name|'or'
string|"'GET'"
op|','
nl|'\n'
name|'the_request'
op|','
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'SERVER_PROTOCOL'"
op|')'
name|'or'
string|"'1.0'"
op|','
nl|'\n'
name|'response_status_int'
op|','
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_REFERER'"
op|')'
name|'or'
string|"'-'"
op|','
nl|'\n'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
name|'or'
string|"'-'"
op|')'
op|'+'
string|"' TempURL'"
op|','
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_AUTH_TOKEN'"
op|')'
name|'or'
string|"'-'"
op|','
nl|'\n'
string|"'-'"
op|','
nl|'\n'
string|"'-'"
op|','
nl|'\n'
string|"'-'"
op|','
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'swift.trans_id'"
op|')'
name|'or'
string|"'-'"
op|','
nl|'\n'
string|"'-'"
op|','
nl|'\n'
string|"'-'"
op|','
nl|'\n'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
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
string|'""" Returns the WSGI filter for use with paste.deploy. """'
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
name|'return'
name|'lambda'
name|'app'
op|':'
name|'TempURL'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
