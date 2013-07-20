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
string|'"""\nThis StaticWeb WSGI middleware will serve container data as a static web site\nwith index file and error file resolution and optional file listings. This mode\nis normally only active for anonymous requests. If you want to use it with\nauthenticated requests, set the ``X-Web-Mode: true`` header on the request.\n\nThe ``staticweb`` filter should be added to the pipeline in your\n``/etc/swift/proxy-server.conf`` file just after any auth middleware. Also, the\nconfiguration section for the ``staticweb`` middleware itself needs to be\nadded. For example::\n\n    [DEFAULT]\n    ...\n\n    [pipeline:main]\n    pipeline = catch_errors healthcheck proxy-logging cache ratelimit tempauth\n               staticweb proxy-logging proxy-server\n\n    ...\n\n    [filter:staticweb]\n    use = egg:swift#staticweb\n\nAny publicly readable containers (for example, ``X-Container-Read: .r:*``, see\n`acls`_ for more information on this) will be checked for\nX-Container-Meta-Web-Index and X-Container-Meta-Web-Error header values::\n\n    X-Container-Meta-Web-Index  <index.name>\n    X-Container-Meta-Web-Error  <error.name.suffix>\n\nIf X-Container-Meta-Web-Index is set, any <index.name> files will be served\nwithout having to specify the <index.name> part. For instance, setting\n``X-Container-Meta-Web-Index: index.html`` will be able to serve the object\n.../pseudo/path/index.html with just .../pseudo/path or .../pseudo/path/\n\nIf X-Container-Meta-Web-Error is set, any errors (currently just 401\nUnauthorized and 404 Not Found) will instead serve the\n.../<status.code><error.name.suffix> object. For instance, setting\n``X-Container-Meta-Web-Error: error.html`` will serve .../404error.html for\nrequests for paths not found.\n\nFor pseudo paths that have no <index.name>, this middleware can serve HTML file\nlistings if you set the ``X-Container-Meta-Web-Listings: true`` metadata item\non the container.\n\nIf listings are enabled, the listings can have a custom style sheet by setting\nthe X-Container-Meta-Web-Listings-CSS header. For instance, setting\n``X-Container-Meta-Web-Listings-CSS: listing.css`` will make listings link to\nthe .../listing.css style sheet. If you "view source" in your browser on a\nlisting page, you will see the well defined document structure that can be\nstyled.\n\nThe content-type of directory marker objects can be modified by setting\nthe ``X-Container-Meta-Web-Directory-Type`` header.  If the header is not set,\napplication/directory is used by default.  Directory marker objects are\n0-byte objects that represent directories to create a simulated hierarchical\nstructure.\n\nExample usage of this middleware via ``swift``:\n\n    Make the container publicly readable::\n\n        swift post -r \'.r:*\' container\n\n    You should be able to get objects directly, but no index.html resolution or\n    listings.\n\n    Set an index file directive::\n\n        swift post -m \'web-index:index.html\' container\n\n    You should be able to hit paths that have an index.html without needing to\n    type the index.html part.\n\n    Turn on listings::\n\n        swift post -m \'web-listings: true\' container\n\n    Now you should see object listings for paths and pseudo paths that have no\n    index.html.\n\n    Enable a custom listings style sheet::\n\n        swift post -m \'web-listings-css:listings.css\' container\n\n    Set an error file::\n\n        swift post -m \'web-error:error.html\' container\n\n    Now 401\'s should load 401error.html, 404\'s should load 404error.html, etc.\n\n    Set Content-Type of directory marker object::\n\n        swift post -m \'web-directory-type:text/directory\' container\n\n    Now 0-byte objects with a content-type of text/directory will be treated\n    as directories rather than objects.\n"""'
newline|'\n'
nl|'\n'
nl|'\n'
name|'import'
name|'cgi'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
name|'as'
name|'urllib_quote'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'human_readable'
op|','
name|'split_path'
op|','
name|'config_true_value'
op|','
name|'json'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'make_pre_authed_env'
op|','
name|'WSGIContext'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'is_success'
op|','
name|'is_redirection'
op|','
name|'HTTP_NOT_FOUND'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Response'
op|','
name|'HTTPMovedPermanently'
op|','
name|'HTTPNotFound'
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
name|'get_container_info'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|ensure_utf8_bytes
name|'def'
name|'ensure_utf8_bytes'
op|'('
name|'value'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'isinstance'
op|'('
name|'value'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'value'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'value'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|quote
dedent|''
name|'def'
name|'quote'
op|'('
name|'value'
op|','
name|'safe'
op|'='
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Patched version of urllib.quote that encodes utf-8 strings before quoting\n    """'
newline|'\n'
name|'return'
name|'urllib_quote'
op|'('
name|'ensure_utf8_bytes'
op|'('
name|'value'
op|')'
op|','
name|'safe'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|_StaticWebContext
dedent|''
name|'class'
name|'_StaticWebContext'
op|'('
name|'WSGIContext'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    The Static Web WSGI middleware filter; serves container data as a\n    static web site. See `staticweb`_ for an overview.\n\n    This _StaticWebContext is used by StaticWeb with each request\n    that might need to be handled to make keeping contextual\n    information about the request a bit simpler than storing it in\n    the WSGI env.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'staticweb'
op|','
name|'version'
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
name|'WSGIContext'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'staticweb'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'='
name|'version'
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
name|'self'
op|'.'
name|'app'
op|'='
name|'staticweb'
op|'.'
name|'app'
newline|'\n'
name|'self'
op|'.'
name|'agent'
op|'='
string|"'%(orig)s StaticWeb'"
newline|'\n'
comment|'# Results from the last call to self._get_container_info.'
nl|'\n'
name|'self'
op|'.'
name|'_index'
op|'='
name|'self'
op|'.'
name|'_error'
op|'='
name|'self'
op|'.'
name|'_listings'
op|'='
name|'self'
op|'.'
name|'_listings_css'
op|'='
name|'self'
op|'.'
name|'_dir_type'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|_error_response
dedent|''
name|'def'
name|'_error_response'
op|'('
name|'self'
op|','
name|'response'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sends the error response to the remote client, possibly resolving a\n        custom error response body based on x-container-meta-web-error.\n\n        :param response: The error response we should default to sending.\n        :param env: The original request WSGI environment.\n        :param start_response: The WSGI start_response hook.\n        """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'_error'
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
name|'self'
op|'.'
name|'_response_headers'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'response'
newline|'\n'
dedent|''
name|'save_response_status'
op|'='
name|'self'
op|'.'
name|'_response_status'
newline|'\n'
name|'save_response_headers'
op|'='
name|'self'
op|'.'
name|'_response_headers'
newline|'\n'
name|'save_response_exc_info'
op|'='
name|'self'
op|'.'
name|'_response_exc_info'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'make_pre_authed_env'
op|'('
nl|'\n'
name|'env'
op|','
string|"'GET'"
op|','
string|"'/%s/%s/%s/%s%s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'version'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
op|','
name|'self'
op|'.'
name|'_error'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'agent'
op|','
name|'swift_source'
op|'='
string|"'SW'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'is_success'
op|'('
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
name|'save_response_status'
op|','
name|'self'
op|'.'
name|'_response_headers'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'start_response'
op|'('
name|'save_response_status'
op|','
name|'save_response_headers'
op|','
nl|'\n'
name|'save_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'response'
newline|'\n'
nl|'\n'
DECL|member|_get_container_info
dedent|''
name|'def'
name|'_get_container_info'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Retrieves x-container-meta-web-index, x-container-meta-web-error,\n        x-container-meta-web-listings, x-container-meta-web-listings-css,\n        and x-container-meta-web-directory-type from memcache or from the\n        cluster and stores the result in memcache and in self._index,\n        self._error, self._listings, self._listings_css and self._dir_type.\n\n        :param env: The WSGI environment dict.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_index'
op|'='
name|'self'
op|'.'
name|'_error'
op|'='
name|'self'
op|'.'
name|'_listings'
op|'='
name|'self'
op|'.'
name|'_listings_css'
op|'='
name|'self'
op|'.'
name|'_dir_type'
op|'='
name|'None'
newline|'\n'
name|'container_info'
op|'='
name|'get_container_info'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'app'
op|','
name|'swift_source'
op|'='
string|"'SW'"
op|')'
newline|'\n'
name|'if'
name|'is_success'
op|'('
name|'container_info'
op|'['
string|"'status'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'meta'
op|'='
name|'container_info'
op|'.'
name|'get'
op|'('
string|"'meta'"
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_index'
op|'='
name|'meta'
op|'.'
name|'get'
op|'('
string|"'web-index'"
op|','
string|"''"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_error'
op|'='
name|'meta'
op|'.'
name|'get'
op|'('
string|"'web-error'"
op|','
string|"''"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_listings'
op|'='
name|'meta'
op|'.'
name|'get'
op|'('
string|"'web-listings'"
op|','
string|"''"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_listings_css'
op|'='
name|'meta'
op|'.'
name|'get'
op|'('
string|"'web-listings-css'"
op|','
string|"''"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_dir_type'
op|'='
name|'meta'
op|'.'
name|'get'
op|'('
string|"'web-directory-type'"
op|','
string|"''"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|_listing
dedent|''
dedent|''
name|'def'
name|'_listing'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|','
name|'prefix'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sends an HTML object listing to the remote client.\n\n        :param env: The original WSGI environment dict.\n        :param start_response: The original WSGI start_response hook.\n        :param prefix: Any prefix desired for the container listing.\n        """'
newline|'\n'
name|'if'
name|'not'
name|'config_true_value'
op|'('
name|'self'
op|'.'
name|'_listings'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPNotFound'
op|'('
op|')'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'_start_response'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_error_response'
op|'('
name|'resp'
op|','
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'tmp_env'
op|'='
name|'make_pre_authed_env'
op|'('
nl|'\n'
name|'env'
op|','
string|"'GET'"
op|','
string|"'/%s/%s/%s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'version'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'agent'
op|','
name|'swift_source'
op|'='
string|"'SW'"
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'delimiter=/&format=json'"
newline|'\n'
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'            '
name|'tmp_env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'+='
string|"'&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'prefix'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'prefix'
op|'='
string|"''"
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'tmp_env'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_success'
op|'('
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_error_response'
op|'('
name|'resp'
op|','
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'listing'
op|'='
name|'None'
newline|'\n'
name|'body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'if'
name|'body'
op|':'
newline|'\n'
indent|'            '
name|'listing'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'body'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'listing'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPNotFound'
op|'('
op|')'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'_start_response'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_error_response'
op|'('
name|'resp'
op|','
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'{'
string|"'Content-Type'"
op|':'
string|"'text/html; charset=UTF-8'"
op|'}'
newline|'\n'
name|'body'
op|'='
string|'\'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 \''
string|'\'Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\\n\''
string|"'<html>\\n'"
string|"' <head>\\n'"
string|"'  <title>Listing of %s</title>\\n'"
op|'%'
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_listings_css'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'+='
string|'\'  <link rel="stylesheet" type="text/css" \''
string|'\'href="%s" />\\n\''
op|'%'
op|'('
name|'self'
op|'.'
name|'_build_css_path'
op|'('
name|'prefix'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'+='
string|'\'  <style type="text/css">\\n\''
string|"'   h1 {font-size: 1em; font-weight: bold;}\\n'"
string|"'   th {text-align: left; padding: 0px 1em 0px 1em;}\\n'"
string|"'   td {padding: 0px 1em 0px 1em;}\\n'"
string|"'   a {text-decoration: none;}\\n'"
string|"'  </style>\\n'"
newline|'\n'
dedent|''
name|'body'
op|'+='
string|"' </head>\\n'"
string|"' <body>\\n'"
string|'\'  <h1 id="title">Listing of %s</h1>\\n\''
string|'\'  <table id="listing">\\n\''
string|'\'   <tr id="heading">\\n\''
string|'\'    <th class="colname">Name</th>\\n\''
string|'\'    <th class="colsize">Size</th>\\n\''
string|'\'    <th class="coldate">Date</th>\\n\''
string|"'   </tr>\\n'"
op|'%'
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'+='
string|'\'   <tr id="parent" class="item">\\n\''
string|'\'    <td class="colname"><a href="../">../</a></td>\\n\''
string|'\'    <td class="colsize">&nbsp;</td>\\n\''
string|'\'    <td class="coldate">&nbsp;</td>\\n\''
string|"'   </tr>\\n'"
newline|'\n'
dedent|''
name|'for'
name|'item'
name|'in'
name|'listing'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'subdir'"
name|'in'
name|'item'
op|':'
newline|'\n'
indent|'                '
name|'subdir'
op|'='
name|'ensure_utf8_bytes'
op|'('
name|'item'
op|'['
string|"'subdir'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'                    '
name|'subdir'
op|'='
name|'subdir'
op|'['
name|'len'
op|'('
name|'prefix'
op|')'
op|':'
op|']'
newline|'\n'
dedent|''
name|'body'
op|'+='
string|'\'   <tr class="item subdir">\\n\''
string|'\'    <td class="colname"><a href="%s">%s</a></td>\\n\''
string|'\'    <td class="colsize">&nbsp;</td>\\n\''
string|'\'    <td class="coldate">&nbsp;</td>\\n\''
string|"'   </tr>\\n'"
op|'%'
op|'('
name|'quote'
op|'('
name|'subdir'
op|')'
op|','
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'subdir'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'item'
name|'in'
name|'listing'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'name'"
name|'in'
name|'item'
op|':'
newline|'\n'
indent|'                '
name|'name'
op|'='
name|'ensure_utf8_bytes'
op|'('
name|'item'
op|'['
string|"'name'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'                    '
name|'name'
op|'='
name|'name'
op|'['
name|'len'
op|'('
name|'prefix'
op|')'
op|':'
op|']'
newline|'\n'
dedent|''
name|'content_type'
op|'='
name|'ensure_utf8_bytes'
op|'('
name|'item'
op|'['
string|"'content_type'"
op|']'
op|')'
newline|'\n'
name|'bytes'
op|'='
name|'ensure_utf8_bytes'
op|'('
name|'human_readable'
op|'('
name|'item'
op|'['
string|"'bytes'"
op|']'
op|')'
op|')'
newline|'\n'
name|'last_modified'
op|'='
op|'('
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'item'
op|'['
string|"'last_modified'"
op|']'
op|')'
op|'.'
nl|'\n'
name|'split'
op|'('
string|"'.'"
op|')'
op|'['
number|'0'
op|']'
op|'.'
name|'replace'
op|'('
string|"'T'"
op|','
string|"' '"
op|')'
op|')'
newline|'\n'
name|'body'
op|'+='
string|'\'   <tr class="item %s">\\n\''
string|'\'    <td class="colname"><a href="%s">%s</a></td>\\n\''
string|'\'    <td class="colsize">%s</td>\\n\''
string|'\'    <td class="coldate">%s</td>\\n\''
string|"'   </tr>\\n'"
op|'%'
op|'('
string|"' '"
op|'.'
name|'join'
op|'('
string|"'type-'"
op|'+'
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'t'
op|'.'
name|'lower'
op|'('
op|')'
op|','
name|'quote'
op|'='
name|'True'
op|')'
nl|'\n'
name|'for'
name|'t'
name|'in'
name|'content_type'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|')'
op|','
nl|'\n'
name|'quote'
op|'('
name|'name'
op|')'
op|','
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'name'
op|')'
op|','
nl|'\n'
name|'bytes'
op|','
name|'ensure_utf8_bytes'
op|'('
name|'last_modified'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'body'
op|'+='
string|"'  </table>\\n'"
string|"' </body>\\n'"
string|"'</html>\\n'"
newline|'\n'
name|'resp'
op|'='
name|'Response'
op|'('
name|'headers'
op|'='
name|'headers'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_build_css_path
dedent|''
name|'def'
name|'_build_css_path'
op|'('
name|'self'
op|','
name|'prefix'
op|'='
string|"''"
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Constructs a relative path from a given prefix within the container.\n        URLs and paths starting with \'/\' are not modified.\n\n        :param prefix: The prefix for the container listing.\n        """'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_listings_css'
op|'.'
name|'startswith'
op|'('
op|'('
string|"'/'"
op|','
string|"'http://'"
op|','
string|"'https://'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'css_path'
op|'='
name|'quote'
op|'('
name|'self'
op|'.'
name|'_listings_css'
op|','
string|"':/'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'css_path'
op|'='
string|"'../'"
op|'*'
name|'prefix'
op|'.'
name|'count'
op|'('
string|"'/'"
op|')'
op|'+'
name|'quote'
op|'('
name|'self'
op|'.'
name|'_listings_css'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'css_path'
newline|'\n'
nl|'\n'
DECL|member|handle_container
dedent|''
name|'def'
name|'handle_container'
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
string|'"""\n        Handles a possible static web request for a container.\n\n        :param env: The original WSGI environment dict.\n        :param start_response: The original WSGI start_response hook.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_get_container_info'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'_listings'
name|'and'
name|'not'
name|'self'
op|'.'
name|'_index'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'config_true_value'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_WEB_MODE'"
op|','
string|"'f'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPNotFound'
op|'('
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
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
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'/'"
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPMovedPermanently'
op|'('
nl|'\n'
name|'location'
op|'='
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+'
string|"'/'"
op|')'
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'_index'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_listing'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'tmp_env'
op|'='
name|'dict'
op|'('
name|'env'
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
string|"'%s StaticWeb'"
op|'%'
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'SW'"
newline|'\n'
name|'tmp_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+='
name|'self'
op|'.'
name|'_index'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'tmp_env'
op|')'
newline|'\n'
name|'status_int'
op|'='
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
newline|'\n'
name|'if'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_listing'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'not'
name|'is_success'
op|'('
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
op|')'
name|'and'
name|'not'
name|'is_redirection'
op|'('
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_error_response'
op|'('
name|'resp'
op|','
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
name|'self'
op|'.'
name|'_response_headers'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|handle_object
dedent|''
name|'def'
name|'handle_object'
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
string|'"""\n        Handles a possible static web request for an object. This object could\n        resolve into an index or listing request.\n\n        :param env: The original WSGI environment dict.\n        :param start_response: The original WSGI start_response hook.\n        """'
newline|'\n'
name|'tmp_env'
op|'='
name|'dict'
op|'('
name|'env'
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
string|"'%s StaticWeb'"
op|'%'
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'SW'"
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'tmp_env'
op|')'
newline|'\n'
name|'status_int'
op|'='
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_get_container_info'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'is_success'
op|'('
name|'status_int'
op|')'
name|'or'
name|'is_redirection'
op|'('
name|'status_int'
op|')'
op|':'
newline|'\n'
comment|'# Treat directory marker objects as not found'
nl|'\n'
indent|'            '
name|'if'
name|'not'
name|'self'
op|'.'
name|'_dir_type'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_dir_type'
op|'='
string|"'application/directory'"
newline|'\n'
dedent|''
name|'content_length'
op|'='
name|'self'
op|'.'
name|'_response_header_value'
op|'('
string|"'content-length'"
op|')'
newline|'\n'
name|'content_length'
op|'='
name|'int'
op|'('
name|'content_length'
op|')'
name|'if'
name|'content_length'
name|'else'
number|'0'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_response_header_value'
op|'('
string|"'content-type'"
op|')'
op|'=='
name|'self'
op|'.'
name|'_dir_type'
name|'and'
name|'content_length'
op|'<='
number|'1'
op|':'
newline|'\n'
indent|'                '
name|'status_int'
op|'='
name|'HTTP_NOT_FOUND'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
name|'self'
op|'.'
name|'_response_headers'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'status_int'
op|'!='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
comment|"# Retaining the previous code's behavior of not using custom error"
nl|'\n'
comment|'# pages for non-404 errors.'
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'_error'
op|'='
name|'None'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_error_response'
op|'('
name|'resp'
op|','
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'_listings'
name|'and'
name|'not'
name|'self'
op|'.'
name|'_index'
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
name|'status_int'
op|'='
name|'HTTP_NOT_FOUND'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_index'
op|':'
newline|'\n'
indent|'            '
name|'tmp_env'
op|'='
name|'dict'
op|'('
name|'env'
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
string|"'%s StaticWeb'"
op|'%'
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'SW'"
newline|'\n'
name|'if'
name|'tmp_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'/'"
op|':'
newline|'\n'
indent|'                '
name|'tmp_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+='
string|"'/'"
newline|'\n'
dedent|''
name|'tmp_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+='
name|'self'
op|'.'
name|'_index'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'tmp_env'
op|')'
newline|'\n'
name|'status_int'
op|'='
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
newline|'\n'
name|'if'
name|'is_success'
op|'('
name|'status_int'
op|')'
name|'or'
name|'is_redirection'
op|'('
name|'status_int'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'/'"
op|':'
newline|'\n'
indent|'                    '
name|'resp'
op|'='
name|'HTTPMovedPermanently'
op|'('
nl|'\n'
name|'location'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+'
string|"'/'"
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
name|'self'
op|'.'
name|'_response_headers'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'/'"
op|':'
newline|'\n'
indent|'                '
name|'tmp_env'
op|'='
name|'make_pre_authed_env'
op|'('
nl|'\n'
name|'env'
op|','
string|"'GET'"
op|','
string|"'/%s/%s/%s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'version'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'agent'
op|','
name|'swift_source'
op|'='
string|"'SW'"
op|')'
newline|'\n'
name|'tmp_env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'limit=1&format=json&delimiter'"
string|"'=/&limit=1&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'self'
op|'.'
name|'obj'
op|'+'
string|"'/'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'tmp_env'
op|')'
newline|'\n'
name|'body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_success'
op|'('
name|'self'
op|'.'
name|'_get_status_int'
op|'('
op|')'
op|')'
name|'or'
name|'not'
name|'body'
name|'or'
name|'not'
name|'json'
op|'.'
name|'loads'
op|'('
name|'body'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'resp'
op|'='
name|'HTTPNotFound'
op|'('
op|')'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'_start_response'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_error_response'
op|'('
name|'resp'
op|','
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'HTTPMovedPermanently'
op|'('
name|'location'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+'
string|"'/'"
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'_listing'
op|'('
name|'env'
op|','
name|'start_response'
op|','
name|'self'
op|'.'
name|'obj'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|StaticWeb
dedent|''
dedent|''
dedent|''
name|'class'
name|'StaticWeb'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    The Static Web WSGI middleware filter; serves container data as a static\n    web site. See `staticweb`_ for an overview.\n\n    The proxy logs created for any subrequests made will have swift.source set\n    to "SW".\n\n    :param app: The next WSGI application/filter in the paste.deploy pipeline.\n    :param conf: The filter configuration dict.\n    """'
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
string|'"""\n        Main hook into the WSGI paste.deploy filter/app pipeline.\n\n        :param env: The WSGI environment dict.\n        :param start_response: The WSGI start_response hook.\n        """'
newline|'\n'
name|'env'
op|'['
string|"'staticweb.start_time'"
op|']'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
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
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
number|'2'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
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
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
name|'not'
name|'in'
op|'('
string|"'HEAD'"
op|','
string|"'GET'"
op|')'
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
name|'env'
op|'.'
name|'get'
op|'('
string|"'REMOTE_USER'"
op|')'
name|'and'
name|'not'
name|'config_true_value'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_WEB_MODE'"
op|','
string|"'f'"
op|')'
op|')'
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
name|'container'
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
name|'context'
op|'='
name|'_StaticWebContext'
op|'('
name|'self'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'if'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'context'
op|'.'
name|'handle_object'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'context'
op|'.'
name|'handle_container'
op|'('
name|'env'
op|','
name|'start_response'
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
string|'"""Returns a Static Web WSGI filter for use with paste.deploy."""'
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
nl|'\n'
DECL|function|staticweb_filter
name|'def'
name|'staticweb_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'StaticWeb'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'staticweb_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
