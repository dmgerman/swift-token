begin_unit
comment|'# Copyright (c) 2014 OpenStack Foundation'
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
string|'"""\nObject versioning in swift is implemented by setting a flag on the container\nto tell swift to version all objects in the container. The flag is the\n``X-Versions-Location`` header on the container, and its value is the\ncontainer where the versions are stored. It is recommended to use a different\n``X-Versions-Location`` container for each container that is being versioned.\n\nWhen data is ``PUT`` into a versioned container (a container with the\nversioning flag turned on), the existing data in the file is redirected to a\nnew object and the data in the ``PUT`` request is saved as the data for the\nversioned object. The new object name (for the previous version) is\n``<versions_container>/<length><object_name>/<timestamp>``, where ``length``\nis the 3-character zero-padded hexadecimal length of the ``<object_name>`` and\n``<timestamp>`` is the timestamp of when the previous version was created.\n\nA ``GET`` to a versioned object will return the current version of the object\nwithout having to do any request redirects or metadata lookups.\n\nA ``POST`` to a versioned object will update the object metadata as normal,\nbut will not create a new version of the object. In other words, new versions\nare only created when the content of the object changes.\n\nA ``DELETE`` to a versioned object will only remove the current version of the\nobject. If you have 5 total versions of the object, you must delete the\nobject 5 times to completely remove the object.\n\n--------------------------------------------------\nHow to Enable Object Versioning in a Swift Cluster\n--------------------------------------------------\n\nThis middleware was written as an effort to refactor parts of the proxy server,\nso this functionality was already available in previous releases and every\nattempt was made to maintain backwards compatibility. To allow operators to\nperform a seamless upgrade, it is not required to add the middleware to the\nproxy pipeline and the flag ``allow_versions`` in the container server\nconfiguration files are still valid. In future releases, ``allow_versions``\nwill be deprecated in favor of adding this middleware to the pipeline to enable\nor disable the feature.\n\nIn case the middleware is added to the proxy pipeline, you must also\nset ``allow_versioned_writes`` to ``True`` in the middleware options\nto enable the information about this middleware to be returned in a /info\nrequest.\n\nUpgrade considerations: If ``allow_versioned_writes`` is set in the filter\nconfiguration, you can leave the ``allow_versions`` flag in the container\nserver configuration files untouched. If you decide to disable or remove the\n``allow_versions`` flag, you must re-set any existing containers that had\nthe \'X-Versions-Location\' flag configured so that it can now be tracked by the\nversioned_writes middleware.\n\n-----------------------\nExamples Using ``curl``\n-----------------------\n\nFirst, create a container with the ``X-Versions-Location`` header or add the\nheader to an existing container. Also make sure the container referenced by\nthe ``X-Versions-Location`` exists. In this example, the name of that\ncontainer is "versions"::\n\n    curl -i -XPUT -H "X-Auth-Token: <token>" \\\n-H "X-Versions-Location: versions" http://<storage_url>/container\n    curl -i -XPUT -H "X-Auth-Token: <token>" http://<storage_url>/versions\n\nCreate an object (the first version)::\n\n    curl -i -XPUT --data-binary 1 -H "X-Auth-Token: <token>" \\\nhttp://<storage_url>/container/myobject\n\nNow create a new version of that object::\n\n    curl -i -XPUT --data-binary 2 -H "X-Auth-Token: <token>" \\\nhttp://<storage_url>/container/myobject\n\nSee a listing of the older versions of the object::\n\n    curl -i -H "X-Auth-Token: <token>" \\\nhttp://<storage_url>/versions?prefix=008myobject/\n\nNow delete the current version of the object and see that the older version is\ngone::\n\n    curl -i -XDELETE -H "X-Auth-Token: <token>" \\\nhttp://<storage_url>/container/myobject\n    curl -i -H "X-Auth-Token: <token>" \\\nhttp://<storage_url>/versions?prefix=008myobject/\n\n---------------------------------------------------\nHow to Disable Object Versioning in a Swift Cluster\n---------------------------------------------------\n\nIf you want to disable all functionality, set ``allow_versioned_writes`` to\n``False`` in the middleware options.\n\nDisable versioning from a container (x is any value except empty)::\n\n    curl -i -XPOST -H "X-Auth-Token: <token>" \\\n-H "X-Remove-Versions-Location: x" http://<storage_url>/container\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'six'
newline|'\n'
name|'from'
name|'six'
op|'.'
name|'moves'
op|'.'
name|'urllib'
op|'.'
name|'parse'
name|'import'
name|'quote'
op|','
name|'unquote'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'Timestamp'
op|','
name|'json'
op|','
name|'register_swift_info'
op|','
name|'config_true_value'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'get_sys_meta_prefix'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'WSGIContext'
op|','
name|'make_pre_authed_request'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
op|','
name|'HTTPException'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
op|'('
nl|'\n'
name|'check_account_format'
op|','
name|'check_container_format'
op|','
name|'check_destination_header'
op|')'
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
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
op|'('
nl|'\n'
name|'is_success'
op|','
name|'is_client_error'
op|','
name|'HTTP_NOT_FOUND'
op|')'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPPreconditionFailed'
op|','
name|'HTTPServiceUnavailable'
op|','
name|'HTTPServerError'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
op|'('
nl|'\n'
name|'ListingIterNotFound'
op|','
name|'ListingIterError'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|VersionedWritesContext
name|'class'
name|'VersionedWritesContext'
op|'('
name|'WSGIContext'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'wsgi_app'
op|','
name|'logger'
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
name|'wsgi_app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
nl|'\n'
DECL|member|_listing_iter
dedent|''
name|'def'
name|'_listing_iter'
op|'('
name|'self'
op|','
name|'account_name'
op|','
name|'lcontainer'
op|','
name|'lprefix'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'page'
name|'in'
name|'self'
op|'.'
name|'_listing_pages_iter'
op|'('
name|'account_name'
op|','
nl|'\n'
name|'lcontainer'
op|','
name|'lprefix'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'item'
name|'in'
name|'page'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'item'
newline|'\n'
nl|'\n'
DECL|member|_listing_pages_iter
dedent|''
dedent|''
dedent|''
name|'def'
name|'_listing_pages_iter'
op|'('
name|'self'
op|','
name|'account_name'
op|','
name|'lcontainer'
op|','
name|'lprefix'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'marker'
op|'='
string|"''"
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'lreq'
op|'='
name|'make_pre_authed_request'
op|'('
nl|'\n'
name|'env'
op|','
name|'method'
op|'='
string|"'GET'"
op|','
name|'swift_source'
op|'='
string|"'VW'"
op|','
nl|'\n'
name|'path'
op|'='
string|"'/v1/%s/%s'"
op|'%'
op|'('
name|'account_name'
op|','
name|'lcontainer'
op|')'
op|')'
newline|'\n'
name|'lreq'
op|'.'
name|'environ'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'format=json&prefix=%s&marker=%s'"
op|'%'
op|'('
name|'quote'
op|'('
name|'lprefix'
op|')'
op|','
nl|'\n'
name|'quote'
op|'('
name|'marker'
op|')'
op|')'
newline|'\n'
name|'lresp'
op|'='
name|'lreq'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_success'
op|'('
name|'lresp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'lresp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'ListingIterNotFound'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'is_client_error'
op|'('
name|'lresp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'HTTPPreconditionFailed'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'ListingIterError'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'lresp'
op|'.'
name|'body'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
nl|'\n'
dedent|''
name|'sublisting'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'lresp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'sublisting'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'marker'
op|'='
name|'sublisting'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'name'"
op|']'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
name|'yield'
name|'sublisting'
newline|'\n'
nl|'\n'
DECL|member|handle_obj_versions_put
dedent|''
dedent|''
name|'def'
name|'handle_obj_versions_put'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'object_versions'
op|','
nl|'\n'
name|'object_name'
op|','
name|'policy_index'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'ret'
op|'='
name|'None'
newline|'\n'
nl|'\n'
comment|'# do a HEAD request to check object versions'
nl|'\n'
name|'_headers'
op|'='
op|'{'
string|"'X-Newest'"
op|':'
string|"'True'"
op|','
nl|'\n'
string|"'X-Backend-Storage-Policy-Index'"
op|':'
name|'policy_index'
op|','
nl|'\n'
string|"'x-auth-token'"
op|':'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-token'"
op|')'
op|'}'
newline|'\n'
nl|'\n'
comment|'# make a pre_auth request in case the user has write access'
nl|'\n'
comment|'# to container, but not READ. This was allowed in previous version'
nl|'\n'
comment|'# (i.e., before middleware) so keeping the same behavior here'
nl|'\n'
name|'head_req'
op|'='
name|'make_pre_authed_request'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'path'
op|'='
name|'req'
op|'.'
name|'path_info'
op|','
nl|'\n'
name|'headers'
op|'='
name|'_headers'
op|','
name|'method'
op|'='
string|"'HEAD'"
op|','
name|'swift_source'
op|'='
string|"'VW'"
op|')'
newline|'\n'
name|'hresp'
op|'='
name|'head_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
nl|'\n'
name|'is_dlo_manifest'
op|'='
string|"'X-Object-Manifest'"
name|'in'
name|'req'
op|'.'
name|'headers'
name|'or'
string|"'X-Object-Manifest'"
name|'in'
name|'hresp'
op|'.'
name|'headers'
newline|'\n'
nl|'\n'
comment|"# if there's an existing object, then copy it to"
nl|'\n'
comment|'# X-Versions-Location'
nl|'\n'
name|'if'
name|'is_success'
op|'('
name|'hresp'
op|'.'
name|'status_int'
op|')'
name|'and'
name|'not'
name|'is_dlo_manifest'
op|':'
newline|'\n'
indent|'            '
name|'lcontainer'
op|'='
name|'object_versions'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'prefix_len'
op|'='
string|"'%03x'"
op|'%'
name|'len'
op|'('
name|'object_name'
op|')'
newline|'\n'
name|'lprefix'
op|'='
name|'prefix_len'
op|'+'
name|'object_name'
op|'+'
string|"'/'"
newline|'\n'
name|'ts_source'
op|'='
name|'hresp'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift_x_timestamp'"
op|')'
newline|'\n'
name|'if'
name|'ts_source'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'ts_source'
op|'='
name|'time'
op|'.'
name|'mktime'
op|'('
name|'time'
op|'.'
name|'strptime'
op|'('
nl|'\n'
name|'hresp'
op|'.'
name|'headers'
op|'['
string|"'last-modified'"
op|']'
op|','
nl|'\n'
string|"'%a, %d %b %Y %H:%M:%S GMT'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'new_ts'
op|'='
name|'Timestamp'
op|'('
name|'ts_source'
op|')'
op|'.'
name|'internal'
newline|'\n'
name|'vers_obj_name'
op|'='
name|'lprefix'
op|'+'
name|'new_ts'
newline|'\n'
name|'copy_headers'
op|'='
op|'{'
nl|'\n'
string|"'Destination'"
op|':'
string|"'%s/%s'"
op|'%'
op|'('
name|'lcontainer'
op|','
name|'vers_obj_name'
op|')'
op|','
nl|'\n'
string|"'x-auth-token'"
op|':'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-token'"
op|')'
op|'}'
newline|'\n'
nl|'\n'
comment|'# COPY implementation sets X-Newest to True when it internally'
nl|'\n'
comment|"# does a GET on source object. So, we don't have to explicity"
nl|'\n'
comment|'# set it in request headers here.'
nl|'\n'
name|'copy_req'
op|'='
name|'make_pre_authed_request'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'path'
op|'='
name|'req'
op|'.'
name|'path_info'
op|','
nl|'\n'
name|'headers'
op|'='
name|'copy_headers'
op|','
name|'method'
op|'='
string|"'COPY'"
op|','
name|'swift_source'
op|'='
string|"'VW'"
op|')'
newline|'\n'
name|'copy_resp'
op|'='
name|'copy_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'is_success'
op|'('
name|'copy_resp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
comment|'# success versioning previous existing object'
nl|'\n'
comment|'# return None and handle original request'
nl|'\n'
indent|'                '
name|'ret'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'is_client_error'
op|'('
name|'copy_resp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
comment|'# missing container or bad permissions'
nl|'\n'
indent|'                    '
name|'ret'
op|'='
name|'HTTPPreconditionFailed'
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
comment|'# could not copy the data, bail'
nl|'\n'
indent|'                    '
name|'ret'
op|'='
name|'HTTPServiceUnavailable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'hresp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
name|'or'
name|'is_dlo_manifest'
op|':'
newline|'\n'
comment|'# nothing to version'
nl|'\n'
comment|'# return None and handle original request'
nl|'\n'
indent|'                '
name|'ret'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# if not HTTP_NOT_FOUND, return error immediately'
nl|'\n'
indent|'                '
name|'ret'
op|'='
name|'hresp'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'return'
name|'ret'
newline|'\n'
nl|'\n'
DECL|member|handle_obj_versions_delete
dedent|''
name|'def'
name|'handle_obj_versions_delete'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'object_versions'
op|','
nl|'\n'
name|'account_name'
op|','
name|'container_name'
op|','
name|'object_name'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'lcontainer'
op|'='
name|'object_versions'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'prefix_len'
op|'='
string|"'%03x'"
op|'%'
name|'len'
op|'('
name|'object_name'
op|')'
newline|'\n'
name|'lprefix'
op|'='
name|'prefix_len'
op|'+'
name|'object_name'
op|'+'
string|"'/'"
newline|'\n'
name|'item_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'_item'
name|'in'
name|'self'
op|'.'
name|'_listing_iter'
op|'('
name|'account_name'
op|','
name|'lcontainer'
op|','
name|'lprefix'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'item_list'
op|'.'
name|'append'
op|'('
name|'_item'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ListingIterNotFound'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'except'
name|'HTTPPreconditionFailed'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPPreconditionFailed'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ListingIterError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPServerError'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'item_list'
op|':'
newline|'\n'
comment|"# we're about to start making COPY requests - need to validate the"
nl|'\n'
comment|'# write access to the versioned container'
nl|'\n'
indent|'            '
name|'if'
string|"'swift.authorize'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|':'
newline|'\n'
indent|'                '
name|'container_info'
op|'='
name|'get_container_info'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
name|'container_info'
op|'.'
name|'get'
op|'('
string|"'write_acl'"
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
indent|'                    '
name|'return'
name|'aresp'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'while'
name|'len'
op|'('
name|'item_list'
op|')'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'previous_version'
op|'='
name|'item_list'
op|'.'
name|'pop'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# there are older versions so copy the previous version to the'
nl|'\n'
comment|'# current object and delete the previous version'
nl|'\n'
name|'prev_obj_name'
op|'='
name|'previous_version'
op|'['
string|"'name'"
op|']'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
nl|'\n'
name|'copy_path'
op|'='
string|"'/v1/'"
op|'+'
name|'account_name'
op|'+'
string|"'/'"
op|'+'
name|'lcontainer'
op|'+'
string|"'/'"
op|'+'
name|'prev_obj_name'
newline|'\n'
nl|'\n'
name|'copy_headers'
op|'='
op|'{'
string|"'X-Newest'"
op|':'
string|"'True'"
op|','
nl|'\n'
string|"'Destination'"
op|':'
name|'container_name'
op|'+'
string|"'/'"
op|'+'
name|'object_name'
op|','
nl|'\n'
string|"'x-auth-token'"
op|':'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-token'"
op|')'
op|'}'
newline|'\n'
nl|'\n'
name|'copy_req'
op|'='
name|'make_pre_authed_request'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'path'
op|'='
name|'copy_path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'copy_headers'
op|','
name|'method'
op|'='
string|"'COPY'"
op|','
name|'swift_source'
op|'='
string|"'VW'"
op|')'
newline|'\n'
name|'copy_resp'
op|'='
name|'copy_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
nl|'\n'
comment|"# if the version isn't there, keep trying with previous version"
nl|'\n'
name|'if'
name|'copy_resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'copy_resp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'is_client_error'
op|'('
name|'copy_resp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
comment|'# some user error, maybe permissions'
nl|'\n'
indent|'                    '
name|'return'
name|'HTTPPreconditionFailed'
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
comment|'# could not copy the data, bail'
nl|'\n'
indent|'                    '
name|'return'
name|'HTTPServiceUnavailable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
comment|'# reset these because the COPY changed them'
nl|'\n'
dedent|''
dedent|''
name|'new_del_req'
op|'='
name|'make_pre_authed_request'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'path'
op|'='
name|'copy_path'
op|','
name|'method'
op|'='
string|"'DELETE'"
op|','
nl|'\n'
name|'swift_source'
op|'='
string|"'VW'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'new_del_req'
newline|'\n'
nl|'\n'
comment|"# remove 'X-If-Delete-At', since it is not for the older copy"
nl|'\n'
name|'if'
string|"'X-If-Delete-At'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'X-If-Delete-At'"
op|']'
newline|'\n'
dedent|''
name|'break'
newline|'\n'
nl|'\n'
comment|'# handle DELETE request here in case it was modified'
nl|'\n'
dedent|''
name|'return'
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handle_container_request
dedent|''
name|'def'
name|'handle_container_request'
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
name|'app_resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_response_headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_response_headers'
op|'='
op|'['
op|']'
newline|'\n'
dedent|''
name|'sysmeta_version_hdr'
op|'='
name|'get_sys_meta_prefix'
op|'('
string|"'container'"
op|')'
op|'+'
string|"'versions-location'"
newline|'\n'
name|'location'
op|'='
string|"''"
newline|'\n'
name|'for'
name|'key'
op|','
name|'val'
name|'in'
name|'self'
op|'.'
name|'_response_headers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
name|'sysmeta_version_hdr'
op|':'
newline|'\n'
indent|'                '
name|'location'
op|'='
name|'val'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'location'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_response_headers'
op|'.'
name|'extend'
op|'('
op|'['
op|'('
string|"'X-Versions-Location'"
op|','
name|'location'
op|')'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
nl|'\n'
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
name|'app_resp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|VersionedWritesMiddleware
dedent|''
dedent|''
name|'class'
name|'VersionedWritesMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
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
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'versioned_writes'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|container_request
dedent|''
name|'def'
name|'container_request'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'start_response'
op|','
name|'enabled'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sysmeta_version_hdr'
op|'='
name|'get_sys_meta_prefix'
op|'('
string|"'container'"
op|')'
op|'+'
string|"'versions-location'"
newline|'\n'
nl|'\n'
comment|'# set version location header as sysmeta'
nl|'\n'
name|'if'
string|"'X-Versions-Location'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'val'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Versions-Location'"
op|')'
newline|'\n'
name|'if'
name|'val'
op|':'
newline|'\n'
comment|'# diferently from previous version, we are actually'
nl|'\n'
comment|'# returning an error if user tries to set versions location'
nl|'\n'
comment|'# while feature is explicitly disabled.'
nl|'\n'
indent|'                '
name|'if'
name|'not'
name|'config_true_value'
op|'('
name|'enabled'
op|')'
name|'and'
name|'req'
op|'.'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'POST'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'Versioned Writes is disabled'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'location'
op|'='
name|'check_container_format'
op|'('
name|'req'
op|','
name|'val'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
name|'sysmeta_version_hdr'
op|']'
op|'='
name|'location'
newline|'\n'
nl|'\n'
comment|'# reset original header to maintain sanity'
nl|'\n'
comment|'# now only sysmeta is source of Versions Location'
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'X-Versions-Location'"
op|']'
op|'='
string|"''"
newline|'\n'
nl|'\n'
comment|'# if both headers are in the same request'
nl|'\n'
comment|'# adding location takes precendence over removing'
nl|'\n'
name|'if'
string|"'X-Remove-Versions-Location'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'del'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'X-Remove-Versions-Location'"
op|']'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# empty value is the same as X-Remove-Versions-Location'
nl|'\n'
indent|'                '
name|'req'
op|'.'
name|'headers'
op|'['
string|"'X-Remove-Versions-Location'"
op|']'
op|'='
string|"'x'"
newline|'\n'
nl|'\n'
comment|'# handle removing versions container'
nl|'\n'
dedent|''
dedent|''
name|'val'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Remove-Versions-Location'"
op|')'
newline|'\n'
name|'if'
name|'val'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'headers'
op|'.'
name|'update'
op|'('
op|'{'
name|'sysmeta_version_hdr'
op|':'
string|"''"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'update'
op|'('
op|'{'
string|"'X-Versions-Location'"
op|':'
string|"''"
op|'}'
op|')'
newline|'\n'
name|'del'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'X-Remove-Versions-Location'"
op|']'
newline|'\n'
nl|'\n'
comment|'# send request and translate sysmeta headers from response'
nl|'\n'
dedent|''
name|'vw_ctx'
op|'='
name|'VersionedWritesContext'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'return'
name|'vw_ctx'
op|'.'
name|'handle_container_request'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|object_request
dedent|''
name|'def'
name|'object_request'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
name|'allow_versioned_writes'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'account_name'
op|'='
name|'unquote'
op|'('
name|'account'
op|')'
newline|'\n'
name|'container_name'
op|'='
name|'unquote'
op|'('
name|'container'
op|')'
newline|'\n'
name|'object_name'
op|'='
name|'unquote'
op|'('
name|'obj'
op|')'
newline|'\n'
name|'container_info'
op|'='
name|'None'
newline|'\n'
name|'resp'
op|'='
name|'None'
newline|'\n'
name|'is_enabled'
op|'='
name|'config_true_value'
op|'('
name|'allow_versioned_writes'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'DELETE'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'container_info'
op|'='
name|'get_container_info'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'COPY'"
name|'and'
string|"'Destination'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'Destination-Account'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                '
name|'account_name'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'Destination-Account'"
op|')'
newline|'\n'
name|'account_name'
op|'='
name|'check_account_format'
op|'('
name|'req'
op|','
name|'account_name'
op|')'
newline|'\n'
dedent|''
name|'container_name'
op|','
name|'object_name'
op|'='
name|'check_destination_header'
op|'('
name|'req'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|'"/%s/%s/%s/%s"'
op|'%'
op|'('
nl|'\n'
name|'version'
op|','
name|'account_name'
op|','
name|'container_name'
op|','
name|'object_name'
op|')'
newline|'\n'
name|'container_info'
op|'='
name|'get_container_info'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'container_info'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
comment|'# To maintain backwards compatibility, container version'
nl|'\n'
comment|'# location could be stored as sysmeta or not, need to check both.'
nl|'\n'
comment|'# If stored as sysmeta, check if middleware is enabled. If sysmeta'
nl|'\n'
comment|'# is not set, but versions property is set in container_info, then'
nl|'\n'
comment|'# for backwards compatibility feature is enabled.'
nl|'\n'
dedent|''
name|'object_versions'
op|'='
name|'container_info'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'sysmeta'"
op|','
op|'{'
op|'}'
op|')'
op|'.'
name|'get'
op|'('
string|"'versions-location'"
op|')'
newline|'\n'
name|'if'
name|'object_versions'
name|'and'
name|'isinstance'
op|'('
name|'object_versions'
op|','
name|'six'
op|'.'
name|'text_type'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'object_versions'
op|'='
name|'object_versions'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'not'
name|'object_versions'
op|':'
newline|'\n'
indent|'            '
name|'object_versions'
op|'='
name|'container_info'
op|'.'
name|'get'
op|'('
string|"'versions'"
op|')'
newline|'\n'
comment|'# if allow_versioned_writes is not set in the configuration files'
nl|'\n'
comment|"# but 'versions' is configured, enable feature to maintain"
nl|'\n'
comment|'# backwards compatibility'
nl|'\n'
name|'if'
name|'not'
name|'allow_versioned_writes'
name|'and'
name|'object_versions'
op|':'
newline|'\n'
indent|'                '
name|'is_enabled'
op|'='
name|'True'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'is_enabled'
name|'and'
name|'object_versions'
op|':'
newline|'\n'
indent|'            '
name|'object_versions'
op|'='
name|'unquote'
op|'('
name|'object_versions'
op|')'
newline|'\n'
name|'vw_ctx'
op|'='
name|'VersionedWritesContext'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'COPY'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'policy_idx'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'X-Backend-Storage-Policy-Index'"
op|','
nl|'\n'
name|'container_info'
op|'['
string|"'storage_policy'"
op|']'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'vw_ctx'
op|'.'
name|'handle_obj_versions_put'
op|'('
nl|'\n'
name|'req'
op|','
name|'object_versions'
op|','
name|'object_name'
op|','
name|'policy_idx'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
comment|'# handle DELETE'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'vw_ctx'
op|'.'
name|'handle_obj_versions_delete'
op|'('
nl|'\n'
name|'req'
op|','
name|'object_versions'
op|','
name|'account_name'
op|','
nl|'\n'
name|'container_name'
op|','
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'resp'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
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
comment|'# making a duplicate, because if this is a COPY request, we will'
nl|'\n'
comment|"# modify the PATH_INFO to find out if the 'Destination' is in a"
nl|'\n'
comment|'# versioned container'
nl|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|'.'
name|'copy'
op|'('
op|')'
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
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
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
nl|'\n'
comment|'# In case allow_versioned_writes is set in the filter configuration,'
nl|'\n'
comment|'# the middleware becomes the authority on whether object'
nl|'\n'
comment|'# versioning is enabled or not. In case it is not set, then'
nl|'\n'
comment|'# the option in the container configuration is still checked'
nl|'\n'
comment|'# for backwards compatibility'
nl|'\n'
nl|'\n'
comment|'# For a container request, first just check if option is set,'
nl|'\n'
comment|'# can be either true or false.'
nl|'\n'
comment|'# If set, check if enabled when actually trying to set container'
nl|'\n'
comment|'# header. If not set, let request be handled by container server'
nl|'\n'
comment|'# for backwards compatibility.'
nl|'\n'
comment|'# For an object request, also check if option is set (either T or F).'
nl|'\n'
comment|'# If set, check if enabled when checking versions container in'
nl|'\n'
comment|"# sysmeta property. If it is not set check 'versions' property in"
nl|'\n'
comment|'# container_info'
nl|'\n'
dedent|''
name|'allow_versioned_writes'
op|'='
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_versioned_writes'"
op|')'
newline|'\n'
name|'if'
name|'allow_versioned_writes'
name|'and'
name|'container'
name|'and'
name|'not'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'container_request'
op|'('
name|'req'
op|','
name|'start_response'
op|','
nl|'\n'
name|'allow_versioned_writes'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
name|'as'
name|'error_response'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'error_response'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'obj'
name|'and'
name|'req'
op|'.'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'COPY'"
op|','
string|"'DELETE'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'object_request'
op|'('
nl|'\n'
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
name|'allow_versioned_writes'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
name|'as'
name|'error_response'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'error_response'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
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
name|'if'
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_versioned_writes'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'register_swift_info'
op|'('
string|"'versioned_writes'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|obj_versions_filter
dedent|''
name|'def'
name|'obj_versions_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'VersionedWritesMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'obj_versions_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
