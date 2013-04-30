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
name|'import'
name|'tarfile'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
op|','
name|'unquote'
newline|'\n'
name|'from'
name|'xml'
op|'.'
name|'sax'
name|'import'
name|'saxutils'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
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
name|'HTTPBadGateway'
op|','
name|'HTTPCreated'
op|','
name|'HTTPBadRequest'
op|','
name|'HTTPNotFound'
op|','
name|'HTTPUnauthorized'
op|','
name|'HTTPOk'
op|','
name|'HTTPPreconditionFailed'
op|','
name|'HTTPRequestEntityTooLarge'
op|','
name|'HTTPNotAcceptable'
op|','
name|'HTTPLengthRequired'
op|','
name|'HTTPException'
op|','
name|'HTTPServerError'
op|','
name|'wsgify'
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
name|'MAX_FILE_SIZE'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_BAD_REQUEST'
op|','
name|'HTTP_UNAUTHORIZED'
op|','
name|'HTTP_NOT_FOUND'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'MAX_OBJECT_NAME_LENGTH'
op|','
name|'MAX_CONTAINER_NAME_LENGTH'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|MAX_PATH_LENGTH
name|'MAX_PATH_LENGTH'
op|'='
name|'MAX_OBJECT_NAME_LENGTH'
op|'+'
name|'MAX_CONTAINER_NAME_LENGTH'
op|'+'
number|'2'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|CreateContainerError
name|'class'
name|'CreateContainerError'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'msg'
op|','
name|'status_int'
op|','
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'status_int'
op|'='
name|'status_int'
newline|'\n'
name|'self'
op|'.'
name|'status'
op|'='
name|'status'
newline|'\n'
name|'Exception'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'msg'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|ACCEPTABLE_FORMATS
dedent|''
dedent|''
name|'ACCEPTABLE_FORMATS'
op|'='
op|'['
string|"'text/plain'"
op|','
string|"'application/json'"
op|','
string|"'application/xml'"
op|','
nl|'\n'
string|"'text/xml'"
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_response_body
name|'def'
name|'get_response_body'
op|'('
name|'data_format'
op|','
name|'data_dict'
op|','
name|'error_list'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns a properly formatted response body according to format. Handles\n    json and xml, otherwise will return text/plain. Note: xml response does not\n    include xml declaration.\n    :params data_format: resulting format\n    :params data_dict: generated data about results.\n    :params error_list: list of quoted filenames that failed\n    """'
newline|'\n'
name|'if'
name|'data_format'
op|'=='
string|"'application/json'"
op|':'
newline|'\n'
indent|'        '
name|'data_dict'
op|'['
string|"'Errors'"
op|']'
op|'='
name|'error_list'
newline|'\n'
name|'return'
name|'json'
op|'.'
name|'dumps'
op|'('
name|'data_dict'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'data_format'
name|'and'
name|'data_format'
op|'.'
name|'endswith'
op|'('
string|"'/xml'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'output'
op|'='
string|"'<delete>\\n'"
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'sorted'
op|'('
name|'data_dict'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'xml_key'
op|'='
name|'key'
op|'.'
name|'replace'
op|'('
string|"' '"
op|','
string|"'_'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'output'
op|'+='
string|"'<%s>%s</%s>\\n'"
op|'%'
op|'('
name|'xml_key'
op|','
name|'data_dict'
op|'['
name|'key'
op|']'
op|','
name|'xml_key'
op|')'
newline|'\n'
dedent|''
name|'output'
op|'+='
string|"'<errors>\\n'"
newline|'\n'
name|'output'
op|'+='
string|"'\\n'"
op|'.'
name|'join'
op|'('
nl|'\n'
op|'['
string|"'<object>'"
nl|'\n'
string|"'<name>%s</name><status>%s</status>'"
nl|'\n'
string|"'</object>'"
op|'%'
op|'('
name|'saxutils'
op|'.'
name|'escape'
op|'('
name|'name'
op|')'
op|','
name|'status'
op|')'
name|'for'
nl|'\n'
name|'name'
op|','
name|'status'
name|'in'
name|'error_list'
op|']'
op|')'
newline|'\n'
name|'output'
op|'+='
string|"'</errors>\\n</delete>\\n'"
newline|'\n'
name|'return'
name|'output'
newline|'\n'
nl|'\n'
dedent|''
name|'output'
op|'='
string|"''"
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'sorted'
op|'('
name|'data_dict'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'output'
op|'+='
string|"'%s: %s\\n'"
op|'%'
op|'('
name|'key'
op|','
name|'data_dict'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'output'
op|'+='
string|"'Errors:\\n'"
newline|'\n'
name|'output'
op|'+='
string|"'\\n'"
op|'.'
name|'join'
op|'('
nl|'\n'
op|'['
string|"'%s, %s'"
op|'%'
op|'('
name|'name'
op|','
name|'status'
op|')'
nl|'\n'
name|'for'
name|'name'
op|','
name|'status'
name|'in'
name|'error_list'
op|']'
op|')'
newline|'\n'
name|'return'
name|'output'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Bulk
dedent|''
name|'class'
name|'Bulk'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Middleware that will do many operations on a single request.\n\n    Extract Archive:\n\n    Expand tar files into a swift account. Request must be a PUT with the\n    query parameter ?extract-archive=format specifying the format of archive\n    file. Accepted formats are tar, tar.gz, and tar.bz2.\n\n    For a PUT to the following url:\n\n    /v1/AUTH_Account/$UPLOAD_PATH?extract-archive=tar.gz\n\n    UPLOAD_PATH is where the files will be expanded to. UPLOAD_PATH can be a\n    container, a pseudo-directory within a container, or an empty string. The\n    destination of a file in the archive will be built as follows:\n\n    /v1/AUTH_Account/$UPLOAD_PATH/$FILE_PATH\n\n    Where FILE_PATH is the file name from the listing in the tar file.\n\n    If the UPLOAD_PATH is an empty string, containers will be auto created\n    accordingly and files in the tar that would not map to any container (files\n    in the base directory) will be ignored.\n\n    Only regular files will be uploaded. Empty directories, symlinks, etc will\n    not be uploaded.\n\n    The response from bulk operations functions differently from other swift\n    responses. This is because a short request body sent from the client could\n    result in many operations on the proxy server and precautions need to be\n    made to prevent the request from timing out due to lack of activity. To\n    this end, the client will always receive a 200 Ok response, regardless of\n    the actual success of the call.  The body of the response must be parsed to\n    determine the actual success of the operation. In addition to this the\n    client may receive zero or more whitespace characters prepended to the\n    actual response body while the proxy server is completing the request.\n\n    The format of the response body defaults to text/plain but can be either\n    json or xml depending on the Accept header. Acceptable formats are\n    text/plain, application/json, application/xml, and text/xml. An example\n    body is as follows:\n\n    {"Response Code": "201 Created",\n     "Response Body": "",\n     "Errors": [],\n     "Number Files Created": 10}\n\n    If all valid files were uploaded successfully the Response Code will be a\n    201 Created.  If any files failed to be created the response code\n    corresponds to the subrequest\'s error. Possible codes are 400, 401, 502 (on\n    server errors), etc. In both cases the response body will specify the\n    number of files successfully uploaded and a list of the files that failed.\n\n    There are proxy logs created for each file (which becomes a subrequest) in\n    the tar. The subrequest\'s proxy log will have a swift.source set to "EA"\n    the log\'s content length will reflect the unzipped size of the file. If\n    double proxy-logging is used the leftmost logger will not have a\n    swift.source set and the content length will reflect the size of the\n    payload sent to the proxy (the unexpanded size of the tar.gz).\n\n    Bulk Delete:\n\n    Will delete multiple objects or containers from their account with a\n    single request. Responds to DELETE requests with query parameter\n    ?bulk-delete set. The Content-Type should be set to text/plain.\n    The body of the DELETE request will be a newline separated list of url\n    encoded objects to delete. You can delete 10,000 (configurable) objects\n    per request. The objects specified in the DELETE request body must be URL\n    encoded and in the form:\n\n    /container_name/obj_name\n\n    or for a container (which must be empty at time of delete)\n\n    /container_name\n\n    The response is similar to bulk deletes as in every response will be a 200\n    Ok and you must parse the response body for acutal results. An example\n    response is:\n\n    {"Number Not Found": 0,\n     "Response Code": "200 OK",\n     "Response Body": "",\n     "Errors": [],\n     "Number Deleted": 6}\n\n    If all items were successfully deleted (or did not exist), the Response\n    Code will be a 200 Ok. If any failed to delete, the response code\n    corresponds to the subrequest\'s error. Possible codes are 400, 401, 502 (on\n    server errors), etc. In all cases the response body will specify the number\n    of items successfully deleted, not found, and a list of those that failed.\n    The return body will be formatted in the way specified in the request\'s\n    Accept header. Acceptable formats are text/plain, application/json,\n    application/xml, and text/xml.\n\n    There are proxy logs created for each object or container (which becomes a\n    subrequest) that is deleted. The subrequest\'s proxy log will have a\n    swift.source set to "BD" the log\'s content length of 0. If double\n    proxy-logging is used the leftmost logger will not have a\n    swift.source set and the content length will reflect the size of the\n    payload sent to the proxy (the list of objects/containers to be deleted).\n    """'
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
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'bulk'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_containers'
op|'='
name|'int'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_containers_per_extraction'"
op|','
number|'10000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_failed_extractions'
op|'='
name|'int'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_failed_extractions'"
op|','
number|'1000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_deletes_per_request'
op|'='
name|'int'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_deletes_per_request'"
op|','
number|'10000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'yield_frequency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'yield_frequency'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_container
dedent|''
name|'def'
name|'create_container'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'container_path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Makes a subrequest to create a new container.\n        :params container_path: an unquoted path to a container to be created\n        :returns: None on success\n        :raises: CreateContainerError on creation error\n        """'
newline|'\n'
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
string|"'PATH_INFO'"
op|']'
op|'='
name|'container_path'
newline|'\n'
name|'new_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'EA'"
newline|'\n'
name|'create_cont_req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'container_path'
op|','
name|'environ'
op|'='
name|'new_env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'create_cont_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|'!='
number|'2'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'CreateContainerError'
op|'('
nl|'\n'
string|'"Create Container Failed: "'
op|'+'
name|'container_path'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status_int'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_objs_to_delete
dedent|''
dedent|''
name|'def'
name|'get_objs_to_delete'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Will populate objs_to_delete with data from request input.\n        :params req: a Swob request\n        :returns: a list of the contents of req.body when separated by newline.\n        :raises: HTTPException on failures\n        """'
newline|'\n'
name|'line'
op|'='
string|"''"
newline|'\n'
name|'data_remaining'
op|'='
name|'True'
newline|'\n'
name|'objs_to_delete'
op|'='
op|'['
op|']'
newline|'\n'
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
nl|'\n'
dedent|''
name|'while'
name|'data_remaining'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'\\n'"
name|'in'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'obj_to_delete'
op|','
name|'line'
op|'='
name|'line'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|','
number|'1'
op|')'
newline|'\n'
name|'objs_to_delete'
op|'.'
name|'append'
op|'('
name|'unquote'
op|'('
name|'obj_to_delete'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'='
name|'req'
op|'.'
name|'body_file'
op|'.'
name|'read'
op|'('
name|'MAX_PATH_LENGTH'
op|')'
newline|'\n'
name|'if'
name|'data'
op|':'
newline|'\n'
indent|'                    '
name|'line'
op|'+='
name|'data'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'data_remaining'
op|'='
name|'False'
newline|'\n'
name|'if'
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'objs_to_delete'
op|'.'
name|'append'
op|'('
name|'unquote'
op|'('
name|'line'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'len'
op|'('
name|'objs_to_delete'
op|')'
op|'>'
name|'self'
op|'.'
name|'max_deletes_per_request'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPRequestEntityTooLarge'
op|'('
nl|'\n'
string|"'Maximum Bulk Deletes: %d per request'"
op|'%'
nl|'\n'
name|'self'
op|'.'
name|'max_deletes_per_request'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'line'
op|')'
op|'>'
name|'MAX_PATH_LENGTH'
op|'*'
number|'2'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPBadRequest'
op|'('
string|"'Invalid File Name'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'objs_to_delete'
newline|'\n'
nl|'\n'
DECL|member|handle_delete_iter
dedent|''
name|'def'
name|'handle_delete_iter'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'objs_to_delete'
op|'='
name|'None'
op|','
nl|'\n'
name|'user_agent'
op|'='
string|"'BulkDelete'"
op|','
name|'swift_source'
op|'='
string|"'BD'"
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        A generator that can be assigned to a swob Response\'s app_iter which,\n        when iterated over, will delete the objects specified in request body.\n        Will occasionally yield whitespace while request is being processed.\n        When the request is completed will yield a response body that can be\n        parsed to determine success. See above documentation for details.\n        :params req: a swob Request\n        :params objs_to_delete: a list of dictionaries that specifies the\n                                objects to be deleted. If None, uses\n                                self.get_objs_to_delete to query request.\n        """'
newline|'\n'
name|'last_yield'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'separator'
op|'='
string|"''"
newline|'\n'
name|'failed_files'
op|'='
op|'['
op|']'
newline|'\n'
name|'resp_dict'
op|'='
op|'{'
string|"'Response Status'"
op|':'
name|'HTTPOk'
op|'('
op|')'
op|'.'
name|'status'
op|','
nl|'\n'
string|"'Response Body'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'Number Deleted'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'Number Not Found'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
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
indent|'                '
name|'raise'
name|'HTTPNotAcceptable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'out_content_type'
op|'.'
name|'endswith'
op|'('
string|"'/xml'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'yield'
string|'\'<?xml version="1.0" encoding="UTF-8"?>\\n\''
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'vrs'
op|','
name|'account'
op|','
name|'_junk'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'2'
op|','
number|'3'
op|','
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'incoming_format'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'Content-Type'"
op|')'
newline|'\n'
name|'if'
name|'incoming_format'
name|'and'
name|'not'
name|'incoming_format'
op|'.'
name|'startswith'
op|'('
string|"'text/plain'"
op|')'
op|':'
newline|'\n'
comment|'# For now only accept newline separated object names'
nl|'\n'
indent|'                '
name|'raise'
name|'HTTPNotAcceptable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'objs_to_delete'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'objs_to_delete'
op|'='
name|'self'
op|'.'
name|'get_objs_to_delete'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'failed_file_response_type'
op|'='
name|'HTTPBadRequest'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'eventlet.minimum_write_chunk_size'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'obj_to_delete'
name|'in'
name|'objs_to_delete'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'last_yield'
op|'+'
name|'self'
op|'.'
name|'yield_frequency'
op|'<'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'separator'
op|'='
string|"'\\r\\n\\r\\n'"
newline|'\n'
name|'last_yield'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'yield'
string|"' '"
newline|'\n'
dedent|''
name|'obj_to_delete'
op|'='
name|'obj_to_delete'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'obj_to_delete'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'delete_path'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
string|"''"
op|','
name|'vrs'
op|','
name|'account'
op|','
name|'obj_to_delete'
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'delete_path'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
name|'quote'
op|'('
name|'delete_path'
op|')'
op|','
nl|'\n'
name|'HTTPPreconditionFailed'
op|'('
op|')'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
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
name|'new_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
name|'delete_path'
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
string|"'%s %s'"
op|'%'
op|'('
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|')'
op|','
name|'user_agent'
op|')'
newline|'\n'
name|'new_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
name|'swift_source'
newline|'\n'
name|'delete_obj_req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'delete_path'
op|','
name|'new_env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'delete_obj_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|'=='
number|'2'
op|':'
newline|'\n'
indent|'                    '
name|'resp_dict'
op|'['
string|"'Number Deleted'"
op|']'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'elif'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                    '
name|'resp_dict'
op|'['
string|"'Number Not Found'"
op|']'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'elif'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_UNAUTHORIZED'
op|':'
newline|'\n'
indent|'                    '
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
name|'quote'
op|'('
name|'delete_path'
op|')'
op|','
nl|'\n'
name|'HTTP_UNAUTHORIZED'
op|']'
op|')'
newline|'\n'
name|'raise'
name|'HTTPUnauthorized'
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
indent|'                    '
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|'=='
number|'5'
op|':'
newline|'\n'
indent|'                        '
name|'failed_file_response_type'
op|'='
name|'HTTPBadGateway'
newline|'\n'
dedent|''
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
name|'quote'
op|'('
name|'delete_path'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'failed_files'
op|':'
newline|'\n'
indent|'                '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'failed_file_response_type'
op|'('
op|')'
op|'.'
name|'status'
newline|'\n'
dedent|''
name|'elif'
name|'not'
op|'('
name|'resp_dict'
op|'['
string|"'Number Deleted'"
op|']'
name|'or'
nl|'\n'
name|'resp_dict'
op|'['
string|"'Number Not Found'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'HTTPBadRequest'
op|'('
op|')'
op|'.'
name|'status'
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Body'"
op|']'
op|'='
string|"'Invalid bulk delete.'"
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'err'
op|'.'
name|'status'
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Body'"
op|']'
op|'='
name|'err'
op|'.'
name|'body'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'Error in bulk delete.'"
op|')'
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'HTTPServerError'
op|'('
op|')'
op|'.'
name|'status'
newline|'\n'
nl|'\n'
dedent|''
name|'yield'
name|'separator'
op|'+'
name|'get_response_body'
op|'('
name|'out_content_type'
op|','
nl|'\n'
name|'resp_dict'
op|','
name|'failed_files'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handle_extract_iter
dedent|''
name|'def'
name|'handle_extract_iter'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'compress_type'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        A generator that can be assigned to a swob Response\'s app_iter which,\n        when iterated over, will extract and PUT the objects pulled from the\n        request body. Will occasionally yield whitespace while request is being\n        processed. When the request is completed will yield a response body\n        that can be parsed to determine success. See above documentation for\n        details.\n        :params req: a swob Request\n        :params compress_type: specifying the compression type of the tar.\n                               Accepts \'\', \'gz, or \'bz2\'\n        """'
newline|'\n'
name|'resp_dict'
op|'='
op|'{'
string|"'Response Status'"
op|':'
name|'HTTPCreated'
op|'('
op|')'
op|'.'
name|'status'
op|','
nl|'\n'
string|"'Response Body'"
op|':'
string|"''"
op|','
string|"'Number Files Created'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'failed_files'
op|'='
op|'['
op|']'
newline|'\n'
name|'last_yield'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'separator'
op|'='
string|"''"
newline|'\n'
name|'existing_containers'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
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
indent|'                '
name|'raise'
name|'HTTPNotAcceptable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'out_content_type'
op|'.'
name|'endswith'
op|'('
string|"'/xml'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'yield'
string|'\'<?xml version="1.0" encoding="UTF-8"?>\\n\''
newline|'\n'
nl|'\n'
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
nl|'\n'
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
indent|'                '
name|'raise'
name|'HTTPLengthRequired'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'vrs'
op|','
name|'account'
op|','
name|'extract_base'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'2'
op|','
number|'3'
op|','
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'extract_base'
op|'='
name|'extract_base'
name|'or'
string|"''"
newline|'\n'
name|'extract_base'
op|'='
name|'extract_base'
op|'.'
name|'rstrip'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'tar'
op|'='
name|'tarfile'
op|'.'
name|'open'
op|'('
name|'mode'
op|'='
string|"'r|'"
op|'+'
name|'compress_type'
op|','
nl|'\n'
name|'fileobj'
op|'='
name|'req'
op|'.'
name|'body_file'
op|')'
newline|'\n'
name|'failed_response_type'
op|'='
name|'HTTPBadRequest'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'eventlet.minimum_write_chunk_size'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'last_yield'
op|'+'
name|'self'
op|'.'
name|'yield_frequency'
op|'<'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'separator'
op|'='
string|"'\\r\\n\\r\\n'"
newline|'\n'
name|'last_yield'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'yield'
string|"' '"
newline|'\n'
dedent|''
name|'tar_info'
op|'='
name|'tar'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'if'
name|'tar_info'
name|'is'
name|'None'
name|'or'
name|'len'
op|'('
name|'failed_files'
op|')'
op|'>='
name|'self'
op|'.'
name|'max_failed_extractions'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'tar_info'
op|'.'
name|'isfile'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'obj_path'
op|'='
name|'tar_info'
op|'.'
name|'name'
newline|'\n'
name|'if'
name|'obj_path'
op|'.'
name|'startswith'
op|'('
string|"'./'"
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'obj_path'
op|'='
name|'obj_path'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
dedent|''
name|'obj_path'
op|'='
name|'obj_path'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'if'
name|'extract_base'
op|':'
newline|'\n'
indent|'                        '
name|'obj_path'
op|'='
name|'extract_base'
op|'+'
string|"'/'"
op|'+'
name|'obj_path'
newline|'\n'
dedent|''
name|'if'
string|"'/'"
name|'not'
name|'in'
name|'obj_path'
op|':'
newline|'\n'
indent|'                        '
name|'continue'
comment|'# ignore base level file'
newline|'\n'
nl|'\n'
dedent|''
name|'destination'
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
name|'obj_path'
op|']'
op|')'
newline|'\n'
name|'container'
op|'='
name|'obj_path'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'destination'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'failed_files'
op|'.'
name|'append'
op|'('
nl|'\n'
op|'['
name|'quote'
op|'('
name|'destination'
op|'['
op|':'
name|'MAX_PATH_LENGTH'
op|']'
op|')'
op|','
nl|'\n'
name|'HTTPPreconditionFailed'
op|'('
op|')'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'tar_info'
op|'.'
name|'size'
op|'>'
name|'MAX_FILE_SIZE'
op|':'
newline|'\n'
indent|'                        '
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
nl|'\n'
name|'quote'
op|'('
name|'destination'
op|'['
op|':'
name|'MAX_PATH_LENGTH'
op|']'
op|')'
op|','
nl|'\n'
name|'HTTPRequestEntityTooLarge'
op|'('
op|')'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'container'
name|'not'
name|'in'
name|'existing_containers'
op|':'
newline|'\n'
indent|'                        '
name|'try'
op|':'
newline|'\n'
indent|'                            '
name|'self'
op|'.'
name|'create_container'
op|'('
nl|'\n'
name|'req'
op|','
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
string|"''"
op|','
name|'vrs'
op|','
name|'account'
op|','
name|'container'
op|']'
op|')'
op|')'
newline|'\n'
name|'existing_containers'
op|'.'
name|'add'
op|'('
name|'container'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'CreateContainerError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                            '
name|'if'
name|'err'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_UNAUTHORIZED'
op|':'
newline|'\n'
indent|'                                '
name|'raise'
name|'HTTPUnauthorized'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
nl|'\n'
name|'quote'
op|'('
name|'destination'
op|'['
op|':'
name|'MAX_PATH_LENGTH'
op|']'
op|')'
op|','
nl|'\n'
name|'err'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                            '
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
nl|'\n'
name|'quote'
op|'('
name|'destination'
op|'['
op|':'
name|'MAX_PATH_LENGTH'
op|']'
op|')'
op|','
nl|'\n'
name|'HTTP_BAD_REQUEST'
op|']'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'existing_containers'
op|')'
op|'>'
name|'self'
op|'.'
name|'max_containers'
op|':'
newline|'\n'
indent|'                            '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
string|"'More than %d base level containers in tar.'"
op|'%'
nl|'\n'
name|'self'
op|'.'
name|'max_containers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'tar_file'
op|'='
name|'tar'
op|'.'
name|'extractfile'
op|'('
name|'tar_info'
op|')'
newline|'\n'
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
string|"'wsgi.input'"
op|']'
op|'='
name|'tar_file'
newline|'\n'
name|'new_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
name|'destination'
newline|'\n'
name|'new_env'
op|'['
string|"'CONTENT_LENGTH'"
op|']'
op|'='
name|'tar_info'
op|'.'
name|'size'
newline|'\n'
name|'new_env'
op|'['
string|"'swift.source'"
op|']'
op|'='
string|"'EA'"
newline|'\n'
name|'new_env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
string|"'%s BulkExpand'"
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
name|'create_obj_req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'destination'
op|','
name|'new_env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'create_obj_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|'=='
number|'2'
op|':'
newline|'\n'
indent|'                        '
name|'resp_dict'
op|'['
string|"'Number Files Created'"
op|']'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_UNAUTHORIZED'
op|':'
newline|'\n'
indent|'                            '
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
nl|'\n'
name|'quote'
op|'('
name|'destination'
op|'['
op|':'
name|'MAX_PATH_LENGTH'
op|']'
op|')'
op|','
nl|'\n'
name|'HTTP_UNAUTHORIZED'
op|']'
op|')'
newline|'\n'
name|'raise'
name|'HTTPUnauthorized'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|'=='
number|'5'
op|':'
newline|'\n'
indent|'                            '
name|'failed_response_type'
op|'='
name|'HTTPBadGateway'
newline|'\n'
dedent|''
name|'failed_files'
op|'.'
name|'append'
op|'('
op|'['
nl|'\n'
name|'quote'
op|'('
name|'destination'
op|'['
op|':'
name|'MAX_PATH_LENGTH'
op|']'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'failed_files'
op|':'
newline|'\n'
indent|'                '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'failed_response_type'
op|'('
op|')'
op|'.'
name|'status'
newline|'\n'
dedent|''
name|'elif'
name|'not'
name|'resp_dict'
op|'['
string|"'Number Files Created'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'HTTPBadRequest'
op|'('
op|')'
op|'.'
name|'status'
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Body'"
op|']'
op|'='
string|"'Invalid Tar File: No Valid Files'"
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'err'
op|'.'
name|'status'
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Body'"
op|']'
op|'='
name|'err'
op|'.'
name|'body'
newline|'\n'
dedent|''
name|'except'
name|'tarfile'
op|'.'
name|'TarError'
op|','
name|'tar_error'
op|':'
newline|'\n'
indent|'            '
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'HTTPBadRequest'
op|'('
op|')'
op|'.'
name|'status'
op|','
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Body'"
op|']'
op|'='
string|"'Invalid Tar File: %s'"
op|'%'
name|'tar_error'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'Error in extract archive.'"
op|')'
newline|'\n'
name|'resp_dict'
op|'['
string|"'Response Status'"
op|']'
op|'='
name|'HTTPServerError'
op|'('
op|')'
op|'.'
name|'status'
newline|'\n'
nl|'\n'
dedent|''
name|'yield'
name|'separator'
op|'+'
name|'get_response_body'
op|'('
nl|'\n'
name|'out_content_type'
op|','
name|'resp_dict'
op|','
name|'failed_files'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'wsgify'
newline|'\n'
DECL|member|__call__
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'extract_type'
op|'='
name|'req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
string|"'extract-archive'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'extract_type'
name|'is'
name|'not'
name|'None'
name|'and'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'PUT'"
op|':'
newline|'\n'
indent|'            '
name|'archive_type'
op|'='
op|'{'
nl|'\n'
string|"'tar'"
op|':'
string|"''"
op|','
string|"'tar.gz'"
op|':'
string|"'gz'"
op|','
nl|'\n'
string|"'tar.bz2'"
op|':'
string|"'bz2'"
op|'}'
op|'.'
name|'get'
op|'('
name|'extract_type'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
string|"'.'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'archive_type'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'HTTPOk'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'app_iter'
op|'='
name|'self'
op|'.'
name|'handle_extract_iter'
op|'('
name|'req'
op|','
name|'archive_type'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
string|'"Unsupported archive format"'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
string|"'bulk-delete'"
name|'in'
name|'req'
op|'.'
name|'params'
name|'and'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'DELETE'"
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPOk'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'app_iter'
op|'='
name|'self'
op|'.'
name|'handle_delete_iter'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'resp'
name|'or'
name|'self'
op|'.'
name|'app'
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
DECL|function|bulk_filter
name|'def'
name|'bulk_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'Bulk'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'bulk_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
