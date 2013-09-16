begin_unit
comment|'# Copyright (c) 2013 OpenStack, LLC.'
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
string|'"""\nMiddleware that will provide Static Large Object (SLO) support.\n\nThis feature is very similar to Dynamic Large Object (DLO) support in that\nit allows the user to upload many objects concurrently and afterwards\ndownload them as a single object. It is different in that it does not rely\non eventually consistent container listings to do so. Instead, a user\ndefined manifest of the object segments is used.\n\n----------------------\nUploading the Manifest\n----------------------\n\nAfter the user has uploaded the objects to be concatenated a manifest is\nuploaded. The request must be a PUT with the query parameter::\n\n    ?multipart-manifest=put\n\nThe body of this request will be an ordered list of files in\njson data format. The data to be supplied for each segment is::\n\n    path: the path to the segment (not including account)\n          /container/object_name\n    etag: the etag given back when the segment was PUT\n    size_bytes: the size of the segment in bytes\n\nThe format of the list will be::\n\n    json:\n    [{"path": "/cont/object",\n      "etag": "etagoftheobjectsegment",\n      "size_bytes": 1048576}, ...]\n\nThe number of object segments is limited to a configurable amount, default\n1000. Each segment, except for the final one, must be at least 1 megabyte\n(configurable). On upload, the middleware will head every segment passed in and\nverify the size and etag of each. If any of the objects do not match (not\nfound, size/etag mismatch, below minimum size) then the user will receive a 4xx\nerror response. If everything does match, the user will receive a 2xx response\nand the SLO object is ready for downloading.\n\nBehind the scenes, on success, a json manifest generated from the user input is\nsent to object servers with an extra "X-Static-Large-Object: True" header\nand a modified Content-Type. The parameter: swift_bytes=$total_size will be\nappended to the existing Content-Type, where total_size is the sum of all\nthe included segments\' size_bytes. This extra parameter will be hidden from\nthe user.\n\nManifest files can reference objects in separate containers, which will improve\nconcurrent upload speed. Objects can be referenced by multiple manifests. The\nsegments of a SLO manifest can even be other SLO manifests. Treat them as any\nother object i.e., use the Etag and Content-Length given on the PUT of the\nsub-SLO in the manifest to the parent SLO.\n\n-------------------------\nRetrieving a Large Object\n-------------------------\n\nA GET request to the manifest object will return the concatenation of the\nobjects from the manifest much like DLO. If any of the segments from the\nmanifest are not found or their Etag/Content Length no longer match the\nconnection will drop. In this case a 409 Conflict will be logged in the proxy\nlogs and the user will receive incomplete results.\n\nThe headers from this GET or HEAD request will return the metadata attached\nto the manifest object itself with some exceptions::\n\n    Content-Length: the total size of the SLO (the sum of the sizes of\n                    the segments in the manifest)\n    X-Static-Large-Object: True\n    Etag: the etag of the SLO (generated the same way as DLO)\n\nA GET request with the query parameter::\n\n    ?multipart-manifest=get\n\nWill return the actual manifest file itself. This is generated json and does\nnot match the data sent from the original multipart-manifest=put. This call\'s\nmain purpose is for debugging.\n\nWhen the manifest object is uploaded you are more or less guaranteed that\nevery segment in the manifest exists and matched the specifications.\nHowever, there is nothing that prevents the user from breaking the\nSLO download by deleting/replacing a segment referenced in the manifest. It is\nleft to the user use caution in handling the segments.\n\n-----------------------\nDeleting a Large Object\n-----------------------\n\nA DELETE request will just delete the manifest object itself.\n\nA DELETE with a query parameter::\n\n    ?multipart-manifest=delete\n\nwill delete all the segments referenced in the manifest and then the manifest\nitself. The failure response will be similar to the bulk delete middleware.\n\n------------------------\nModifying a Large Object\n------------------------\n\nPUTs / POSTs will work as expected, PUTs will just overwrite the manifest\nobject for example.\n\n------------------\nContainer Listings\n------------------\n\nIn a container listing the size listed for SLO manifest objects will be the\ntotal_size of the concatenated segments in the manifest. The overall\nX-Container-Bytes-Used for the container (and subsequently for the account)\nwill not reflect total_size of the manifest but the actual size of the json\ndata stored. The reason for this somewhat confusing discrepancy is we want the\ncontainer listing to reflect the size of the manifest object when it is\ndownloaded. We do not, however, want to count the bytes-used twice (for both\nthe manifest and the segments it\'s referring to) in the container and account\nmetadata which can be used for stats purposes.\n"""'
newline|'\n'
nl|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
name|'from'
name|'cStringIO'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'datetime'
name|'import'
name|'datetime'
newline|'\n'
name|'import'
name|'mimetypes'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
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
name|'HTTPBadRequest'
op|','
name|'HTTPServerError'
op|','
name|'HTTPMethodNotAllowed'
op|','
name|'HTTPRequestEntityTooLarge'
op|','
name|'HTTPLengthRequired'
op|','
name|'HTTPOk'
op|','
name|'HTTPPreconditionFailed'
op|','
name|'HTTPException'
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
name|'get_logger'
op|','
name|'config_true_value'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_utf8'
op|','
name|'MAX_BUFFERED_SLO_SEGMENTS'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_NOT_FOUND'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'WSGIContext'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
op|'.'
name|'bulk'
name|'import'
name|'get_response_body'
op|','
name|'ACCEPTABLE_FORMATS'
op|','
name|'Bulk'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|parse_input
name|'def'
name|'parse_input'
op|'('
name|'raw_data'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Given a request will parse the body and return a list of dictionaries\n    :raises: HTTPException on parse errors\n    :returns: a list of dictionaries on success\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'parsed_data'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'raw_data'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPBadRequest'
op|'('
string|'"Manifest must be valid json."'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'req_keys'
op|'='
name|'set'
op|'('
op|'['
string|"'path'"
op|','
string|"'etag'"
op|','
string|"'size_bytes'"
op|']'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'seg_dict'
name|'in'
name|'parsed_data'
op|':'
newline|'\n'
indent|'            '
name|'if'
op|'('
name|'set'
op|'('
name|'seg_dict'
op|')'
op|'!='
name|'req_keys'
name|'or'
nl|'\n'
string|"'/'"
name|'not'
name|'in'
name|'seg_dict'
op|'['
string|"'path'"
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPBadRequest'
op|'('
string|"'Invalid SLO Manifest File'"
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
op|'('
name|'AttributeError'
op|','
name|'TypeError'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPBadRequest'
op|'('
string|"'Invalid SLO Manifest File'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'parsed_data'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|SloContext
dedent|''
name|'class'
name|'SloContext'
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
name|'slo'
op|','
name|'slo_etag'
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
name|'slo'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo_etag'
op|'='
string|'\'"\''
op|'+'
name|'slo_etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|'+'
string|'\'"\''
newline|'\n'
nl|'\n'
DECL|member|handle_slo_put
dedent|''
name|'def'
name|'handle_slo_put'
op|'('
name|'self'
op|','
name|'req'
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
name|'req'
op|'.'
name|'environ'
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'i'
name|'in'
name|'xrange'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'_response_headers'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'_response_headers'
op|'['
name|'i'
op|']'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'etag'"
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_response_headers'
op|'['
name|'i'
op|']'
op|'='
op|'('
string|"'Etag'"
op|','
name|'self'
op|'.'
name|'slo_etag'
op|')'
newline|'\n'
name|'break'
newline|'\n'
nl|'\n'
dedent|''
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
DECL|class|StaticLargeObject
dedent|''
dedent|''
name|'class'
name|'StaticLargeObject'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    StaticLargeObject Middleware\n\n    See above for a full description.\n\n    The proxy logs created for any subrequests made will have swift.source set\n    to "SLO".\n\n    :param app: The next WSGI filter or app in the paste.deploy chain.\n    :param conf: The configuration dict for the middleware.\n    """'
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
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
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
string|"'slo'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_manifest_segments'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_manifest_segments'"
op|','
nl|'\n'
number|'1000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_manifest_size'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_manifest_size'"
op|','
nl|'\n'
number|'1024'
op|'*'
number|'1024'
op|'*'
number|'2'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'min_segment_size'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'min_segment_size'"
op|','
nl|'\n'
number|'1024'
op|'*'
number|'1024'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'bulk_deleter'
op|'='
name|'Bulk'
op|'('
nl|'\n'
name|'app'
op|','
op|'{'
string|"'max_deletes_per_request'"
op|':'
name|'self'
op|'.'
name|'max_manifest_segments'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handle_multipart_put
dedent|''
name|'def'
name|'handle_multipart_put'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Will handle the PUT of a SLO manifest.\n        Heads every object in manifest to check if is valid and if so will\n        save a manifest generated from the user input. Uses WSGIContext to\n        call self.app and start_response and returns a WSGI iterator.\n\n        :params req: a swob.Request with an obj in path\n        :raises: HttpException on errors\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'vrs'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'1'
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
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'content_length'
op|'>'
name|'self'
op|'.'
name|'max_manifest_size'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPRequestEntityTooLarge'
op|'('
nl|'\n'
string|'"Manifest File > %d bytes"'
op|'%'
name|'self'
op|'.'
name|'max_manifest_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Copy-From'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPMethodNotAllowed'
op|'('
nl|'\n'
string|"'Multipart Manifest PUTs cannot be Copy requests'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'content_length'
name|'is'
name|'None'
name|'and'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'transfer-encoding'"
op|','
string|"''"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
op|'!='
string|"'chunked'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPLengthRequired'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'parsed_data'
op|'='
name|'parse_input'
op|'('
name|'req'
op|'.'
name|'body_file'
op|'.'
name|'read'
op|'('
name|'self'
op|'.'
name|'max_manifest_size'
op|')'
op|')'
newline|'\n'
name|'problem_segments'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
name|'if'
name|'len'
op|'('
name|'parsed_data'
op|')'
op|'>'
name|'self'
op|'.'
name|'max_manifest_segments'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPRequestEntityTooLarge'
op|'('
nl|'\n'
string|"'Number segments must be <= %d'"
op|'%'
name|'self'
op|'.'
name|'max_manifest_segments'
op|')'
newline|'\n'
dedent|''
name|'total_size'
op|'='
number|'0'
newline|'\n'
name|'out_content_type'
op|'='
name|'req'
op|'.'
name|'accept'
op|'.'
name|'best_match'
op|'('
name|'ACCEPTABLE_FORMATS'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'out_content_type'
op|':'
newline|'\n'
indent|'            '
name|'out_content_type'
op|'='
string|"'text/plain'"
newline|'\n'
dedent|''
name|'data_for_storage'
op|'='
op|'['
op|']'
newline|'\n'
name|'slo_etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'index'
op|','
name|'seg_dict'
name|'in'
name|'enumerate'
op|'('
name|'parsed_data'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'obj_path'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
nl|'\n'
op|'['
string|"''"
op|','
name|'vrs'
op|','
name|'account'
op|','
name|'seg_dict'
op|'['
string|"'path'"
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
op|']'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'seg_size'
op|'='
name|'int'
op|'('
name|'seg_dict'
op|'['
string|"'size_bytes'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'ValueError'
op|','
name|'TypeError'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPBadRequest'
op|'('
string|"'Invalid Manifest File'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'seg_size'
op|'<'
name|'self'
op|'.'
name|'min_segment_size'
name|'and'
op|'('
name|'index'
op|'=='
number|'0'
name|'or'
name|'index'
op|'<'
name|'len'
op|'('
name|'parsed_data'
op|')'
op|'-'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
string|"'Each segment, except the last, must be larger than '"
nl|'\n'
string|"'%d bytes.'"
op|'%'
name|'self'
op|'.'
name|'min_segment_size'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'new_env'
op|'='
name|'req'
op|'.'
name|'environ'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'obj_path'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'obj_path'
op|'='
name|'obj_path'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'new_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
name|'obj_path'
newline|'\n'
name|'new_env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'='
string|"'HEAD'"
newline|'\n'
name|'new_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'SLO'"
newline|'\n'
name|'del'
op|'('
name|'new_env'
op|'['
string|"'wsgi.input'"
op|']'
op|')'
newline|'\n'
name|'del'
op|'('
name|'new_env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|')'
newline|'\n'
name|'new_env'
op|'['
string|"'CONTENT_LENGTH'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'new_env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
string|"'%s MultipartPUT'"
op|'%'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
newline|'\n'
name|'head_seg_resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'obj_path'
op|','
name|'new_env'
op|')'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'head_seg_resp'
op|'.'
name|'is_success'
op|':'
newline|'\n'
indent|'                '
name|'total_size'
op|'+='
name|'seg_size'
newline|'\n'
name|'if'
name|'seg_size'
op|'!='
name|'head_seg_resp'
op|'.'
name|'content_length'
op|':'
newline|'\n'
indent|'                    '
name|'problem_segments'
op|'.'
name|'append'
op|'('
op|'['
name|'quote'
op|'('
name|'obj_path'
op|')'
op|','
string|"'Size Mismatch'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'seg_dict'
op|'['
string|"'etag'"
op|']'
op|'=='
name|'head_seg_resp'
op|'.'
name|'etag'
op|':'
newline|'\n'
indent|'                    '
name|'slo_etag'
op|'.'
name|'update'
op|'('
name|'seg_dict'
op|'['
string|"'etag'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'problem_segments'
op|'.'
name|'append'
op|'('
op|'['
name|'quote'
op|'('
name|'obj_path'
op|')'
op|','
string|"'Etag Mismatch'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'head_seg_resp'
op|'.'
name|'last_modified'
op|':'
newline|'\n'
indent|'                    '
name|'last_modified'
op|'='
name|'head_seg_resp'
op|'.'
name|'last_modified'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|"# shouldn't happen"
nl|'\n'
indent|'                    '
name|'last_modified'
op|'='
name|'datetime'
op|'.'
name|'now'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'last_modified_formatted'
op|'='
name|'last_modified'
op|'.'
name|'strftime'
op|'('
string|"'%Y-%m-%dT%H:%M:%S.%f'"
op|')'
newline|'\n'
name|'seg_data'
op|'='
op|'{'
string|"'name'"
op|':'
string|"'/'"
op|'+'
name|'seg_dict'
op|'['
string|"'path'"
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
op|','
nl|'\n'
string|"'bytes'"
op|':'
name|'seg_size'
op|','
nl|'\n'
string|"'hash'"
op|':'
name|'seg_dict'
op|'['
string|"'etag'"
op|']'
op|','
nl|'\n'
string|"'content_type'"
op|':'
name|'head_seg_resp'
op|'.'
name|'content_type'
op|','
nl|'\n'
string|"'last_modified'"
op|':'
name|'last_modified_formatted'
op|'}'
newline|'\n'
name|'if'
name|'config_true_value'
op|'('
nl|'\n'
name|'head_seg_resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Static-Large-Object'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'seg_data'
op|'['
string|"'sub_slo'"
op|']'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'data_for_storage'
op|'.'
name|'append'
op|'('
name|'seg_data'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'problem_segments'
op|'.'
name|'append'
op|'('
op|'['
name|'quote'
op|'('
name|'obj_path'
op|')'
op|','
nl|'\n'
name|'head_seg_resp'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'problem_segments'
op|':'
newline|'\n'
indent|'            '
name|'resp_body'
op|'='
name|'get_response_body'
op|'('
nl|'\n'
name|'out_content_type'
op|','
op|'{'
op|'}'
op|','
name|'problem_segments'
op|')'
newline|'\n'
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'resp_body'
op|','
name|'content_type'
op|'='
name|'out_content_type'
op|')'
newline|'\n'
dedent|''
name|'env'
op|'='
name|'req'
op|'.'
name|'environ'
newline|'\n'
nl|'\n'
name|'if'
name|'not'
name|'env'
op|'.'
name|'get'
op|'('
string|"'CONTENT_TYPE'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'guessed_type'
op|','
name|'_junk'
op|'='
name|'mimetypes'
op|'.'
name|'guess_type'
op|'('
name|'req'
op|'.'
name|'path_info'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'CONTENT_TYPE'"
op|']'
op|'='
name|'guessed_type'
name|'or'
string|"'application/octet-stream'"
newline|'\n'
dedent|''
name|'env'
op|'['
string|"'swift.content_type_overriden'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'env'
op|'['
string|"'CONTENT_TYPE'"
op|']'
op|'+='
string|'";swift_bytes=%d"'
op|'%'
name|'total_size'
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_STATIC_LARGE_OBJECT'"
op|']'
op|'='
string|"'True'"
newline|'\n'
name|'json_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'data_for_storage'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'CONTENT_LENGTH'"
op|']'
op|'='
name|'str'
op|'('
name|'len'
op|'('
name|'json_data'
op|')'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|'='
name|'StringIO'
op|'('
name|'json_data'
op|')'
newline|'\n'
nl|'\n'
name|'slo_context'
op|'='
name|'SloContext'
op|'('
name|'self'
op|','
name|'slo_etag'
op|')'
newline|'\n'
name|'return'
name|'slo_context'
op|'.'
name|'handle_slo_put'
op|'('
name|'req'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_segments_to_delete_iter
dedent|''
name|'def'
name|'get_segments_to_delete_iter'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        A generator function to be used to delete all the segments and\n        sub-segments referenced in a manifest.\n\n        :raises HTTPBadRequest: on sub manifest not manifest anymore or\n                                on too many buffered sub segments\n        :raises HTTPServerError: on unable to load manifest\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'vrs'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'4'
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
name|'raise'
name|'HTTPBadRequest'
op|'('
string|"'Not a SLO manifest'"
op|')'
newline|'\n'
dedent|''
name|'sub_segments'
op|'='
op|'['
op|'{'
nl|'\n'
string|"'sub_slo'"
op|':'
name|'True'
op|','
nl|'\n'
string|"'name'"
op|':'
op|'('
string|"'/%s/%s'"
op|'%'
op|'('
name|'container'
op|','
name|'obj'
op|')'
op|')'
op|'.'
name|'decode'
op|'('
string|"'utf-8'"
op|')'
op|'}'
op|']'
newline|'\n'
name|'while'
name|'sub_segments'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'len'
op|'('
name|'sub_segments'
op|')'
op|'>'
name|'MAX_BUFFERED_SLO_SEGMENTS'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
string|"'Too many buffered slo segments to delete.'"
op|')'
newline|'\n'
dedent|''
name|'seg_data'
op|'='
name|'sub_segments'
op|'.'
name|'pop'
op|'('
number|'0'
op|')'
newline|'\n'
name|'if'
name|'seg_data'
op|'.'
name|'get'
op|'('
string|"'sub_slo'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'new_env'
op|'='
name|'req'
op|'.'
name|'environ'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'new_env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'='
string|"'GET'"
newline|'\n'
name|'del'
op|'('
name|'new_env'
op|'['
string|"'wsgi.input'"
op|']'
op|')'
newline|'\n'
name|'new_env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'multipart-manifest=get'"
newline|'\n'
name|'new_env'
op|'['
string|"'CONTENT_LENGTH'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'new_env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
string|"'%s MultipartDELETE'"
op|'%'
name|'new_env'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
newline|'\n'
name|'new_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'SLO'"
newline|'\n'
name|'new_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
op|'('
nl|'\n'
string|"'/%s/%s/%s'"
op|'%'
op|'('
nl|'\n'
name|'vrs'
op|','
name|'account'
op|','
nl|'\n'
name|'seg_data'
op|'['
string|"'name'"
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
op|')'
op|')'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
name|'sub_resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"''"
op|','
name|'new_env'
op|')'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'sub_resp'
op|'.'
name|'is_success'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
comment|'# if its still a SLO, load its segments'
nl|'\n'
indent|'                        '
name|'if'
name|'config_true_value'
op|'('
nl|'\n'
name|'sub_resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Static-Large-Object'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'sub_segments'
op|'.'
name|'extend'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'sub_resp'
op|'.'
name|'body'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
name|'HTTPServerError'
op|'('
string|"'Unable to load SLO manifest'"
op|')'
newline|'\n'
comment|'# add sub-manifest back to be deleted after sub segments'
nl|'\n'
comment|'# (even if obj is not a SLO)'
nl|'\n'
dedent|''
name|'seg_data'
op|'['
string|"'sub_slo'"
op|']'
op|'='
name|'False'
newline|'\n'
name|'sub_segments'
op|'.'
name|'append'
op|'('
name|'seg_data'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'sub_resp'
op|'.'
name|'status_int'
op|'!='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
comment|'# on deletes treat not found as success'
nl|'\n'
indent|'                    '
name|'raise'
name|'HTTPServerError'
op|'('
string|"'Sub SLO unable to load.'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'seg_data'
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
DECL|member|handle_multipart_delete
dedent|''
dedent|''
dedent|''
name|'def'
name|'handle_multipart_delete'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Will delete all the segments in the SLO manifest and then, if\n        successful, will delete the manifest file.\n        :params req: a swob.Request with an obj in path\n        :raises HTTPServerError: on invalid manifest\n        :returns: swob.Response whose app_iter set to Bulk.handle_delete_iter\n        """'
newline|'\n'
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'req'
op|'.'
name|'path_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid UTF8 or contains NULL'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'HTTPOk'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'out_content_type'
op|'='
name|'req'
op|'.'
name|'accept'
op|'.'
name|'best_match'
op|'('
name|'ACCEPTABLE_FORMATS'
op|')'
newline|'\n'
name|'if'
name|'out_content_type'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'.'
name|'content_type'
op|'='
name|'out_content_type'
newline|'\n'
dedent|''
name|'resp'
op|'.'
name|'app_iter'
op|'='
name|'self'
op|'.'
name|'bulk_deleter'
op|'.'
name|'handle_delete_iter'
op|'('
nl|'\n'
name|'req'
op|','
name|'objs_to_delete'
op|'='
name|'self'
op|'.'
name|'get_segments_to_delete_iter'
op|'('
name|'req'
op|')'
op|','
nl|'\n'
name|'user_agent'
op|'='
string|"'MultipartDELETE'"
op|','
name|'swift_source'
op|'='
string|"'SLO'"
op|','
nl|'\n'
name|'out_content_type'
op|'='
name|'out_content_type'
op|')'
newline|'\n'
name|'return'
name|'resp'
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
string|'"""\n        WSGI entry point\n        """'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'vrs'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'1'
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
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'PUT'"
name|'and'
name|'req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
string|"'multipart-manifest'"
op|')'
op|'=='
string|"'put'"
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'self'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'DELETE'"
name|'and'
name|'req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
string|"'multipart-manifest'"
op|')'
op|'=='
string|"'delete'"
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'self'
op|'.'
name|'handle_multipart_delete'
op|'('
name|'req'
op|')'
op|'('
name|'env'
op|','
nl|'\n'
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'X-Static-Large-Object'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'X-Static-Large-Object is a reserved header. '"
nl|'\n'
string|"'To create a static large object add query param '"
nl|'\n'
string|"'multipart-manifest=put.'"
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
name|'HTTPException'
name|'as'
name|'err_resp'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'err_resp'
op|'('
name|'env'
op|','
name|'start_response'
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
DECL|function|slo_filter
name|'def'
name|'slo_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'StaticLargeObject'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'slo_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
