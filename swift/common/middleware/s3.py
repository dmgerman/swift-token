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
name|'webob'
name|'import'
name|'Request'
op|','
name|'Response'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPNotFound'
newline|'\n'
name|'from'
name|'simplejson'
name|'import'
name|'loads'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
op|','
name|'sha1'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
op|','
name|'quote'
newline|'\n'
name|'import'
name|'rfc822'
newline|'\n'
name|'import'
name|'hmac'
newline|'\n'
name|'import'
name|'base64'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
nl|'\n'
DECL|function|get_err_response
name|'def'
name|'get_err_response'
op|'('
name|'code'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'error_table'
op|'='
op|'{'
string|"'AccessDenied'"
op|':'
nl|'\n'
op|'('
number|'403'
op|','
string|"'Access denied'"
op|')'
op|','
nl|'\n'
string|"'BucketAlreadyExists'"
op|':'
nl|'\n'
op|'('
number|'409'
op|','
string|"'The requested bucket name is not available'"
op|')'
op|','
nl|'\n'
string|"'BucketNotEmpty'"
op|':'
nl|'\n'
op|'('
number|'409'
op|','
string|"'The bucket you tried to delete is not empty'"
op|')'
op|','
nl|'\n'
string|"'InvalidArgument'"
op|':'
nl|'\n'
op|'('
number|'400'
op|','
string|"'Invalid Argument'"
op|')'
op|','
nl|'\n'
string|"'InvalidBucketName'"
op|':'
nl|'\n'
op|'('
number|'400'
op|','
string|"'The specified bucket is not valid'"
op|')'
op|','
nl|'\n'
string|"'InvalidURI'"
op|':'
nl|'\n'
op|'('
number|'400'
op|','
string|"'Could not parse the specified URI'"
op|')'
op|','
nl|'\n'
string|"'NoSuchBucket'"
op|':'
nl|'\n'
op|'('
number|'404'
op|','
string|"'The specified bucket does not exist'"
op|')'
op|','
nl|'\n'
string|"'SignatureDoesNotMatch'"
op|':'
nl|'\n'
op|'('
number|'403'
op|','
string|"'The calculated request signature does not match your provided one'"
op|')'
op|','
nl|'\n'
string|"'NoSuchKey'"
op|':'
nl|'\n'
op|'('
number|'404'
op|','
string|"'The resource you requested does not exist'"
op|')'
op|'}'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Response'
op|'('
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
name|'error_table'
op|'['
name|'code'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
name|'error_table'
op|'['
name|'code'
op|']'
op|'['
number|'1'
op|']'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|'"""<?xml version="1.0" encoding="UTF-8"?>\\r\\n<Error>\\r\\n  <Code>%s</Code>\\r\\n  <Message>%s</Message>\\r\\n</Error>\\r\\n"""'
op|'%'
op|'('
name|'code'
op|','
name|'error_table'
op|'['
name|'code'
op|']'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|class|Controller
dedent|''
name|'class'
name|'Controller'
op|'('
name|'object'
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
name|'app'
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
nl|'\n'
DECL|class|ServiceController
dedent|''
dedent|''
name|'class'
name|'ServiceController'
op|'('
name|'Controller'
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
name|'env'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'token'
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
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
name|'token'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/v1/%s'"
op|'%'
name|'account_name'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'format=json'"
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'containers'
op|'='
name|'loads'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'list'
op|'('
name|'resp'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
comment|"# we don't keep the creation time of a backet (s3cmd doesn't"
nl|'\n'
comment|'# work without that) so we use something bogus.'
nl|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|'"""<?xml version="1.0" encoding="UTF-8"?><ListAllMyBucketsResult xmlns="http://doc.s3.amazonaws.com/2006-03-01"><Buckets>%s</Buckets></ListAllMyBucketsResult>"""'
op|'%'
op|'('
string|'""'
op|'.'
name|'join'
op|'('
op|'['
string|"'<Bucket><Name>%s</Name><CreationDate>2009-02-03T16:45:09.000Z</CreationDate></Bucket>'"
op|'%'
name|'i'
op|'['
string|"'name'"
op|']'
name|'for'
name|'i'
name|'in'
name|'containers'
op|']'
op|')'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|class|BucketController
dedent|''
dedent|''
name|'class'
name|'BucketController'
op|'('
name|'Controller'
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
name|'env'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'token'
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
name|'container_name'
op|'='
name|'unquote'
op|'('
name|'container_name'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
name|'token'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/v1/%s/%s'"
op|'%'
op|'('
name|'account_name'
op|','
name|'container_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'format=json'"
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'objects'
op|'='
name|'loads'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'list'
op|'('
name|'resp'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'status'
op|'='
name|'int'
op|'('
name|'resp'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'Response'
op|'('
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidBucketName'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'print'
name|'resp'
newline|'\n'
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|'"""<?xml version="1.0" encoding="UTF-8"?><ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01"><Name>%s</Name>%s</ListBucketResult>"""'
op|'%'
op|'('
name|'self'
op|'.'
name|'container_name'
op|','
string|'""'
op|'.'
name|'join'
op|'('
op|'['
string|"'<Contents><Key>%s</Key><LastModified>%s</LastModified><ETag>%s</ETag><Size>%s</Size><StorageClass>STANDARD</StorageClass></Contents>'"
op|'%'
op|'('
name|'i'
op|'['
string|"'name'"
op|']'
op|','
name|'i'
op|'['
string|"'last_modified'"
op|']'
op|','
name|'i'
op|'['
string|"'hash'"
op|']'
op|','
name|'i'
op|'['
string|"'bytes'"
op|']'
op|')'
name|'for'
name|'i'
name|'in'
name|'objects'
op|']'
op|')'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|PUT
dedent|''
name|'def'
name|'PUT'
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'resp'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'202'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'BucketAlreadyExists'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'print'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'add'
op|'('
string|"'Location'"
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|DELETE
dedent|''
name|'def'
name|'DELETE'
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'status'
op|'='
name|'int'
op|'('
name|'resp'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'204'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidBucketName'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'409'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'BucketNotEmpty'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'print'
name|'resp'
newline|'\n'
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
DECL|class|ObjectController
dedent|''
dedent|''
dedent|''
name|'class'
name|'ObjectController'
op|'('
name|'Controller'
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
name|'env'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'token'
op|','
name|'container_name'
op|','
name|'object_name'
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
name|'container_name'
op|'='
name|'unquote'
op|'('
name|'container_name'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
name|'token'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/v1/%s/%s/%s'"
op|'%'
op|'('
name|'account_name'
op|','
name|'container_name'
op|','
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GETorHEAD
dedent|''
name|'def'
name|'GETorHEAD'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
comment|'# there should be better ways.'
nl|'\n'
comment|'# TODO:'
nl|'\n'
comment|"# - we can't handle various errors properly (autorization, etc)"
nl|'\n'
comment|'# - hide GETorHEAD'
nl|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'method'
op|'='
name|'req'
op|'.'
name|'method'
newline|'\n'
name|'req'
op|'.'
name|'method'
op|'='
string|"'GET'"
newline|'\n'
name|'data'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'if'
name|'type'
op|'('
name|'data'
op|')'
op|'=='
name|'list'
op|':'
newline|'\n'
indent|'            '
name|'status'
op|'='
name|'int'
op|'('
name|'data'
op|'['
number|'0'
op|']'
op|'['
name|'data'
op|'['
number|'0'
op|']'
op|'.'
name|'find'
op|'('
string|"'<title>'"
op|')'
op|'+'
number|'7'
op|':'
op|']'
op|'.'
name|'split'
op|'('
string|"' '"
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'if'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'NoSuchKey'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'method'
op|'=='
string|"'GET'"
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'Response'
op|'('
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'list'
op|'('
name|'data'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'list'
op|'('
name|'data'
op|')'
op|')'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'etag'
op|'='
name|'etag'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
dedent|''
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|HEAD
dedent|''
name|'def'
name|'HEAD'
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
name|'return'
name|'self'
op|'.'
name|'GETorHEAD'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
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
name|'return'
name|'self'
op|'.'
name|'GETorHEAD'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|PUT
dedent|''
name|'def'
name|'PUT'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
comment|'# TODO: how can we get etag from the response header?'
nl|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'req'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'resp'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidBucketName'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'201'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'etag'
op|'='
name|'etag'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'print'
name|'resp'
newline|'\n'
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|DELETE
dedent|''
dedent|''
name|'def'
name|'DELETE'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
comment|'# TODO: how can we get the response result?'
nl|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'status'
op|'='
name|'int'
op|'('
name|'resp'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'204'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
name|'print'
name|'resp'
newline|'\n'
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'NoSuchKey'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
nl|'\n'
DECL|class|Swift3Middleware
dedent|''
dedent|''
dedent|''
name|'class'
name|'Swift3Middleware'
op|'('
name|'object'
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
name|'app'
op|','
name|'conf'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
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
nl|'\n'
DECL|member|get_controller
dedent|''
name|'def'
name|'get_controller'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'path'
op|','
number|'0'
op|','
number|'2'
op|')'
newline|'\n'
name|'d'
op|'='
name|'dict'
op|'('
name|'container_name'
op|'='
name|'container'
op|','
name|'object_name'
op|'='
name|'obj'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'container'
name|'and'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'ObjectController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'BucketController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'return'
name|'ServiceController'
op|','
name|'d'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|'"content-md5"'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'md5'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|'"content-md5"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'md5'
op|'='
string|'""'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|'"content-type"'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'content_type'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|'"content-type"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'content_type'
op|'='
string|'""'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|'"date"'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'date'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|'"date"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'date'
op|'='
string|'""'
newline|'\n'
nl|'\n'
dedent|''
name|'h'
op|'='
name|'req'
op|'.'
name|'method'
op|'+'
string|'"\\n"'
op|'+'
name|'md5'
op|'+'
string|'"\\n"'
op|'+'
name|'content_type'
op|'+'
string|'"\\n"'
op|'+'
name|'date'
op|'+'
string|'"\\n"'
newline|'\n'
name|'for'
name|'header'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'header'
op|'.'
name|'startswith'
op|'('
string|'"X-Amz-"'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'h'
op|'+='
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|'+'
string|'":"'
op|'+'
name|'str'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
op|')'
op|'+'
string|'"\\n"'
newline|'\n'
dedent|''
dedent|''
name|'h'
op|'+='
name|'req'
op|'.'
name|'path'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'account'
op|','
name|'_'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'Authorization'"
op|']'
op|'.'
name|'split'
op|'('
string|"' '"
op|')'
op|'['
op|'-'
number|'1'
op|']'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
op|','
name|'None'
newline|'\n'
dedent|''
name|'token'
op|'='
name|'base64'
op|'.'
name|'urlsafe_b64encode'
op|'('
name|'h'
op|')'
newline|'\n'
name|'return'
name|'account'
op|','
name|'token'
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
comment|'#        print req.method'
nl|'\n'
comment|'#        print req.path'
nl|'\n'
name|'if'
name|'not'
string|"'Authorization'"
name|'in'
name|'req'
op|'.'
name|'headers'
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
name|'controller'
op|','
name|'path_parts'
op|'='
name|'self'
op|'.'
name|'get_controller'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'account_name'
op|','
name|'token'
op|'='
name|'self'
op|'.'
name|'get_account_info'
op|'('
name|'env'
op|','
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'account_name'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidArgument'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'controller'
op|'='
name|'controller'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'app'
op|','
name|'account_name'
op|','
name|'token'
op|','
op|'**'
name|'path_parts'
op|')'
newline|'\n'
name|'if'
name|'hasattr'
op|'('
name|'controller'
op|','
name|'req'
op|'.'
name|'method'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'res'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
name|'req'
op|'.'
name|'method'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'res'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
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
DECL|function|swift3_filter
name|'def'
name|'swift3_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'Swift3Middleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'swift3_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
