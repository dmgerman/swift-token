begin_unit
comment|'# Copyright (c) 2011 OpenStack, LLC.'
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
string|'"""\nFormPost Middleware\n\nTranslates a browser form post into a regular Swift object PUT.\n\nThe format of the form is::\n\n    <form action="<swift-url>" method="POST"\n          enctype="multipart/form-data">\n      <input type="hidden" name="redirect" value="<redirect-url>" />\n      <input type="hidden" name="max_file_size" value="<bytes>" />\n      <input type="hidden" name="max_file_count" value="<count>" />\n      <input type="hidden" name="expires" value="<unix-timestamp>" />\n      <input type="hidden" name="signature" value="<hmac>" />\n      <input type="file" name="file1" /><br />\n      <input type="submit" />\n    </form>\n\nThe <swift-url> is the URL to the Swift desination, such as::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/object_prefix\n\nThe name of each file uploaded will be appended to the <swift-url>\ngiven. So, you can upload directly to the root of container with a\nurl like::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/\n\nOptionally, you can include an object prefix to better separate\ndifferent users\' uploads, such as::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/object_prefix\n\nNote the form method must be POST and the enctype must be set as\n"multipart/form-data".\n\nThe redirect attribute is the URL to redirect the browser to after\nthe upload completes. The URL will have status and message query\nparameters added to it, indicating the HTTP status code for the\nupload (2xx is success) and a possible message for further\ninformation if there was an error (such as "max_file_size exceeded").\n\nThe max_file_size attribute must be included and indicates the\nlargest single file upload that can be done, in bytes.\n\nThe max_file_count attribute must be included and indicates the\nmaximum number of files that can be uploaded with the form. Include\nadditional ``<input type="file" name="filexx" />`` attributes if\ndesired.\n\nThe expires attribute is the Unix timestamp before which the form\nmust be submitted before it is invalidated.\n\nThe signature attribute is the HMAC-SHA1 signature of the form. Here is\nsample code for computing the signature::\n\n    import hmac\n    from hashlib import sha1\n    from time import time\n    path = \'/v1/account/container/object_prefix\'\n    redirect = \'https://myserver.com/some-page\'\n    max_file_size = 104857600\n    max_file_count = 10\n    expires = int(time() + 600)\n    key = \'mykey\'\n    hmac_body = \'%s\\\\n%s\\\\n%s\\\\n%s\\\\n%s\' % (path, redirect,\n        max_file_size, max_file_count, expires)\n    signature = hmac.new(key, hmac_body, sha1).hexdigest()\n\nThe key is the value of the X-Account-Meta-Temp-URL-Key header on the\naccount.\n\nBe certain to use the full path, from the /v1/ onward.\n\nThe command line tool ``swift-form-signature`` may be used (mostly\njust when testing) to compute expires and signature.\n\nAlso note that the file attributes must be after the other attributes\nin order to be processed correctly. If attributes come after the\nfile, they won\'t be sent with the subrequest (there is no way to\nparse all the attributes on the server-side without reading the whole\nthing into memory -- to service many requests, some with large files,\nthere just isn\'t enough memory on the server, so attributes following\nthe file are simply ignored).\n"""'
newline|'\n'
nl|'\n'
DECL|variable|__all__
name|'__all__'
op|'='
op|'['
string|"'FormPost'"
op|','
string|"'filter_factory'"
op|','
string|"'READ_CHUNK_SIZE'"
op|','
string|"'MAX_VALUE_LENGTH'"
op|']'
newline|'\n'
nl|'\n'
name|'import'
name|'hmac'
newline|'\n'
name|'import'
name|'re'
newline|'\n'
name|'import'
name|'rfc822'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'sha1'
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
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'streq_const_time'
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
name|'HTTP_BAD_REQUEST'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#: The size of data to read from the form at any given time.'
nl|'\n'
DECL|variable|READ_CHUNK_SIZE
name|'READ_CHUNK_SIZE'
op|'='
number|'4096'
newline|'\n'
nl|'\n'
comment|"#: The maximum size of any attribute's value. Any additional data will be"
nl|'\n'
comment|'#: truncated.'
nl|'\n'
DECL|variable|MAX_VALUE_LENGTH
name|'MAX_VALUE_LENGTH'
op|'='
number|'4096'
newline|'\n'
nl|'\n'
comment|'#: Regular expression to match form attributes.'
nl|'\n'
DECL|variable|ATTRIBUTES_RE
name|'ATTRIBUTES_RE'
op|'='
name|'re'
op|'.'
name|'compile'
op|'('
string|'r\'(\\w+)=(".*?"|[^";]+)(; ?|$)\''
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FormInvalid
name|'class'
name|'FormInvalid'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_parse_attrs
dedent|''
name|'def'
name|'_parse_attrs'
op|'('
name|'header'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Given the value of a header like:\n    Content-Disposition: form-data; name="somefile"; filename="test.html"\n\n    Return data like\n    ("form-data", {"name": "somefile", "filename": "test.html"})\n\n    :param header: Value of a header (the part after the \': \').\n    :returns: (value name, dict) of the attribute data parsed (see above).\n    """'
newline|'\n'
name|'attributes'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'attrs'
op|'='
string|"''"
newline|'\n'
name|'if'
string|"'; '"
name|'in'
name|'header'
op|':'
newline|'\n'
indent|'        '
name|'header'
op|','
name|'attrs'
op|'='
name|'header'
op|'.'
name|'split'
op|'('
string|"'; '"
op|','
number|'1'
op|')'
newline|'\n'
dedent|''
name|'m'
op|'='
name|'True'
newline|'\n'
name|'while'
name|'m'
op|':'
newline|'\n'
indent|'        '
name|'m'
op|'='
name|'ATTRIBUTES_RE'
op|'.'
name|'match'
op|'('
name|'attrs'
op|')'
newline|'\n'
name|'if'
name|'m'
op|':'
newline|'\n'
indent|'            '
name|'attrs'
op|'='
name|'attrs'
op|'['
name|'len'
op|'('
name|'m'
op|'.'
name|'group'
op|'('
number|'0'
op|')'
op|')'
op|':'
op|']'
newline|'\n'
name|'attributes'
op|'['
name|'m'
op|'.'
name|'group'
op|'('
number|'1'
op|')'
op|']'
op|'='
name|'m'
op|'.'
name|'group'
op|'('
number|'2'
op|')'
op|'.'
name|'strip'
op|'('
string|'\'"\''
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'header'
op|','
name|'attributes'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|_IterRequestsFileLikeObject
dedent|''
name|'class'
name|'_IterRequestsFileLikeObject'
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
name|'wsgi_input'
op|','
name|'boundary'
op|','
name|'input_buffer'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'no_more_data_for_this_file'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'no_more_files'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'wsgi_input'
op|'='
name|'wsgi_input'
newline|'\n'
name|'self'
op|'.'
name|'boundary'
op|'='
name|'boundary'
newline|'\n'
name|'self'
op|'.'
name|'input_buffer'
op|'='
name|'input_buffer'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'length'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'length'
op|':'
newline|'\n'
indent|'            '
name|'length'
op|'='
name|'READ_CHUNK_SIZE'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'no_more_data_for_this_file'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"''"
newline|'\n'
nl|'\n'
comment|"# read enough data to know whether we're going to run"
nl|'\n'
comment|'# into a boundary in next [length] bytes'
nl|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'input_buffer'
op|')'
op|'<'
name|'length'
op|'+'
name|'len'
op|'('
name|'self'
op|'.'
name|'boundary'
op|')'
op|'+'
number|'2'
op|':'
newline|'\n'
indent|'            '
name|'to_read'
op|'='
name|'length'
op|'+'
name|'len'
op|'('
name|'self'
op|'.'
name|'boundary'
op|')'
op|'+'
number|'2'
newline|'\n'
name|'while'
name|'to_read'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'chunk'
op|'='
name|'self'
op|'.'
name|'wsgi_input'
op|'.'
name|'read'
op|'('
name|'to_read'
op|')'
newline|'\n'
name|'to_read'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'input_buffer'
op|'+='
name|'chunk'
newline|'\n'
name|'if'
name|'not'
name|'chunk'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'no_more_files'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'boundary_pos'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'.'
name|'find'
op|'('
name|'self'
op|'.'
name|'boundary'
op|')'
newline|'\n'
nl|'\n'
comment|'# boundary does not exist in the next (length) bytes'
nl|'\n'
name|'if'
name|'boundary_pos'
op|'=='
op|'-'
number|'1'
name|'or'
name|'boundary_pos'
op|'>'
name|'length'
op|':'
newline|'\n'
indent|'            '
name|'ret'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'['
op|':'
name|'length'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'input_buffer'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'['
name|'length'
op|':'
op|']'
newline|'\n'
comment|'# if it does, just return data up to the boundary'
nl|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'ret'
op|','
name|'self'
op|'.'
name|'input_buffer'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'.'
name|'split'
op|'('
name|'self'
op|'.'
name|'boundary'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'no_more_files'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'.'
name|'startswith'
op|'('
string|"'--'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'no_more_data_for_this_file'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'input_buffer'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
dedent|''
name|'return'
name|'ret'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'no_more_data_for_this_file'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"''"
newline|'\n'
dedent|''
name|'boundary_pos'
op|'='
name|'newline_pos'
op|'='
op|'-'
number|'1'
newline|'\n'
name|'while'
name|'newline_pos'
op|'<'
number|'0'
name|'and'
name|'boundary_pos'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'chunk'
op|'='
name|'self'
op|'.'
name|'wsgi_input'
op|'.'
name|'read'
op|'('
name|'READ_CHUNK_SIZE'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'input_buffer'
op|'+='
name|'chunk'
newline|'\n'
name|'newline_pos'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'.'
name|'find'
op|'('
string|"'\\r\\n'"
op|')'
newline|'\n'
name|'boundary_pos'
op|'='
name|'self'
op|'.'
name|'input_buffer'
op|'.'
name|'find'
op|'('
name|'self'
op|'.'
name|'boundary'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'chunk'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'no_more_files'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
comment|'# found a newline'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'newline_pos'
op|'>='
number|'0'
name|'and'
op|'('
name|'boundary_pos'
op|'<'
number|'0'
name|'or'
name|'newline_pos'
op|'<'
name|'boundary_pos'
op|')'
op|':'
newline|'\n'
comment|'# Use self.read to ensure any logic there happens...'
nl|'\n'
indent|'            '
name|'ret'
op|'='
string|"''"
newline|'\n'
name|'to_read'
op|'='
name|'newline_pos'
op|'+'
number|'2'
newline|'\n'
name|'while'
name|'to_read'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'chunk'
op|'='
name|'self'
op|'.'
name|'read'
op|'('
name|'to_read'
op|')'
newline|'\n'
comment|"# Should never happen since we're reading from input_buffer,"
nl|'\n'
comment|'# but just for completeness...'
nl|'\n'
name|'if'
name|'not'
name|'chunk'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'to_read'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'ret'
op|'+='
name|'chunk'
newline|'\n'
dedent|''
name|'return'
name|'ret'
newline|'\n'
dedent|''
name|'else'
op|':'
comment|'# no newlines, just return up to next boundary'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'read'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'input_buffer'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_iter_requests
dedent|''
dedent|''
dedent|''
name|'def'
name|'_iter_requests'
op|'('
name|'wsgi_input'
op|','
name|'boundary'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Given a multi-part mime encoded input file object and boundary,\n    yield file-like objects for each part.\n\n    :param wsgi_input: The file-like object to read from.\n    :param boundary: The mime boundary to separate new file-like\n                     objects on.\n    :returns: A generator of file-like objects for each part.\n    """'
newline|'\n'
name|'boundary'
op|'='
string|"'--'"
op|'+'
name|'boundary'
newline|'\n'
name|'if'
name|'wsgi_input'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'!='
name|'boundary'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'FormInvalid'
op|'('
string|"'invalid starting boundary'"
op|')'
newline|'\n'
dedent|''
name|'boundary'
op|'='
string|"'\\r\\n'"
op|'+'
name|'boundary'
newline|'\n'
name|'input_buffer'
op|'='
string|"''"
newline|'\n'
name|'done'
op|'='
name|'False'
newline|'\n'
name|'while'
name|'not'
name|'done'
op|':'
newline|'\n'
indent|'        '
name|'it'
op|'='
name|'_IterRequestsFileLikeObject'
op|'('
name|'wsgi_input'
op|','
name|'boundary'
op|','
name|'input_buffer'
op|')'
newline|'\n'
name|'yield'
name|'it'
newline|'\n'
name|'done'
op|'='
name|'it'
op|'.'
name|'no_more_files'
newline|'\n'
name|'input_buffer'
op|'='
name|'it'
op|'.'
name|'input_buffer'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|_CappedFileLikeObject
dedent|''
dedent|''
name|'class'
name|'_CappedFileLikeObject'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    A file-like object wrapping another file-like object that raises\n    an EOFError if the amount of data read exceeds a given\n    max_file_size.\n\n    :param fp: The file-like object to wrap.\n    :param max_file_size: The maximum bytes to read before raising an\n                          EOFError.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'fp'
op|','
name|'max_file_size'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'fp'
op|'='
name|'fp'
newline|'\n'
name|'self'
op|'.'
name|'max_file_size'
op|'='
name|'max_file_size'
newline|'\n'
name|'self'
op|'.'
name|'amount_read'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'size'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'ret'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'read'
op|'('
name|'size'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'amount_read'
op|'+='
name|'len'
op|'('
name|'ret'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'amount_read'
op|'>'
name|'self'
op|'.'
name|'max_file_size'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'EOFError'
op|'('
string|"'max_file_size exceeded'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'ret'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'ret'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'amount_read'
op|'+='
name|'len'
op|'('
name|'ret'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'amount_read'
op|'>'
name|'self'
op|'.'
name|'max_file_size'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'EOFError'
op|'('
string|"'max_file_size exceeded'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'ret'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FormPost
dedent|''
dedent|''
name|'class'
name|'FormPost'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    FormPost Middleware\n\n    See above for a full description.\n\n    The proxy logs created for any subrequests made will have swift.source set\n    to "FP".\n\n    :param app: The next WSGI filter or app in the paste.deploy\n                chain.\n    :param conf: The configuration dict for the middleware.\n    """'
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
string|'"""\n        Main hook into the WSGI paste.deploy filter/app pipeline.\n\n        :param env: The WSGI environment dict.\n        :param start_response: The WSGI start_response hook.\n        :returns: Response as per WSGI.\n        """'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'POST'"
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'content_type'
op|','
name|'attrs'
op|'='
name|'_parse_attrs'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'CONTENT_TYPE'"
op|')'
name|'or'
string|"''"
op|')'
newline|'\n'
name|'if'
name|'content_type'
op|'=='
string|"'multipart/form-data'"
name|'and'
string|"'boundary'"
name|'in'
name|'attrs'
op|':'
newline|'\n'
indent|'                    '
name|'env'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'+='
string|"' FormPost'"
newline|'\n'
name|'status'
op|','
name|'headers'
op|','
name|'body'
op|'='
name|'self'
op|'.'
name|'_translate_form'
op|'('
nl|'\n'
name|'env'
op|','
name|'attrs'
op|'['
string|"'boundary'"
op|']'
op|')'
newline|'\n'
name|'start_response'
op|'('
name|'status'
op|','
name|'headers'
op|')'
newline|'\n'
name|'return'
name|'body'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'FormInvalid'
op|','
name|'EOFError'
op|')'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'body'
op|'='
string|"'FormPost: %s'"
op|'%'
name|'err'
newline|'\n'
name|'start_response'
op|'('
nl|'\n'
string|"'400 Bad Request'"
op|','
nl|'\n'
op|'('
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
op|')'
op|')'
newline|'\n'
name|'return'
op|'['
name|'body'
op|']'
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
DECL|member|_translate_form
dedent|''
name|'def'
name|'_translate_form'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'boundary'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Translates the form data into subrequests and issues a\n        response.\n\n        :param env: The WSGI environment dict.\n        :param boundary: The MIME type boundary to look for.\n        :returns: status_line, headers_list, body\n        """'
newline|'\n'
name|'key'
op|'='
name|'self'
op|'.'
name|'_get_key'
op|'('
name|'env'
op|')'
newline|'\n'
name|'status'
op|'='
name|'message'
op|'='
string|"''"
newline|'\n'
name|'attributes'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'file_count'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'fp'
name|'in'
name|'_iter_requests'
op|'('
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|','
name|'boundary'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'hdrs'
op|'='
name|'rfc822'
op|'.'
name|'Message'
op|'('
name|'fp'
op|','
number|'0'
op|')'
newline|'\n'
name|'disp'
op|','
name|'attrs'
op|'='
name|'_parse_attrs'
op|'('
name|'hdrs'
op|'.'
name|'getheader'
op|'('
string|"'Content-Disposition'"
op|','
string|"''"
op|')'
op|')'
newline|'\n'
name|'if'
name|'disp'
op|'=='
string|"'form-data'"
name|'and'
name|'attrs'
op|'.'
name|'get'
op|'('
string|"'filename'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'file_count'
op|'+='
number|'1'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'file_count'
op|'>'
name|'int'
op|'('
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'max_file_count'"
op|')'
name|'or'
number|'0'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'status'
op|'='
string|"'400 Bad Request'"
newline|'\n'
name|'message'
op|'='
string|"'max file count exceeded'"
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'FormInvalid'
op|'('
string|"'max_file_count not an integer'"
op|')'
newline|'\n'
dedent|''
name|'attributes'
op|'['
string|"'filename'"
op|']'
op|'='
name|'attrs'
op|'['
string|"'filename'"
op|']'
name|'or'
string|"'filename'"
newline|'\n'
name|'if'
string|"'content-type'"
name|'not'
name|'in'
name|'attributes'
name|'and'
string|"'content-type'"
name|'in'
name|'hdrs'
op|':'
newline|'\n'
indent|'                    '
name|'attributes'
op|'['
string|"'content-type'"
op|']'
op|'='
name|'hdrs'
op|'['
string|"'Content-Type'"
op|']'
name|'or'
string|"'application/octet-stream'"
newline|'\n'
dedent|''
name|'status'
op|','
name|'message'
op|'='
name|'self'
op|'.'
name|'_perform_subrequest'
op|'('
name|'env'
op|','
name|'attributes'
op|','
name|'fp'
op|','
nl|'\n'
name|'key'
op|')'
newline|'\n'
name|'if'
name|'status'
op|'['
op|':'
number|'1'
op|']'
op|'!='
string|"'2'"
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'='
string|"''"
newline|'\n'
name|'mxln'
op|'='
name|'MAX_VALUE_LENGTH'
newline|'\n'
name|'while'
name|'mxln'
op|':'
newline|'\n'
indent|'                    '
name|'chunk'
op|'='
name|'fp'
op|'.'
name|'read'
op|'('
name|'mxln'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'chunk'
op|':'
newline|'\n'
indent|'                        '
name|'break'
newline|'\n'
dedent|''
name|'mxln'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'data'
op|'+='
name|'chunk'
newline|'\n'
dedent|''
name|'while'
name|'fp'
op|'.'
name|'read'
op|'('
name|'READ_CHUNK_SIZE'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
dedent|''
name|'if'
string|"'name'"
name|'in'
name|'attrs'
op|':'
newline|'\n'
indent|'                    '
name|'attributes'
op|'['
name|'attrs'
op|'['
string|"'name'"
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'data'
op|'.'
name|'rstrip'
op|'('
string|"'\\r\\n--'"
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'not'
name|'status'
op|':'
newline|'\n'
indent|'            '
name|'status'
op|'='
string|"'400 Bad Request'"
newline|'\n'
name|'message'
op|'='
string|"'no files to process'"
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'redirect'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
name|'status'
newline|'\n'
name|'if'
name|'message'
op|':'
newline|'\n'
indent|'                '
name|'body'
op|'='
name|'status'
op|'+'
string|"'\\r\\nFormPost: '"
op|'+'
name|'message'
op|'.'
name|'title'
op|'('
op|')'
newline|'\n'
dedent|''
name|'headers'
op|'='
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
name|'len'
op|'('
name|'body'
op|')'
op|')'
op|']'
newline|'\n'
name|'return'
name|'status'
op|','
name|'headers'
op|','
name|'body'
newline|'\n'
dedent|''
name|'status'
op|'='
name|'status'
op|'.'
name|'split'
op|'('
string|"' '"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'body'
op|'='
string|'\'<html><body><p><a href="%s?status=%s&message=%s">Click to \''
string|"'continue...</a></p></body></html>'"
op|'%'
op|'('
name|'attributes'
op|'['
string|"'redirect'"
op|']'
op|','
name|'quote'
op|'('
name|'status'
op|')'
op|','
name|'quote'
op|'('
name|'message'
op|')'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'['
nl|'\n'
op|'('
string|"'Location'"
op|','
string|"'%s?status=%s&message=%s'"
op|'%'
op|'('
nl|'\n'
name|'attributes'
op|'['
string|"'redirect'"
op|']'
op|','
name|'quote'
op|'('
name|'status'
op|')'
op|','
name|'quote'
op|'('
name|'message'
op|')'
op|')'
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
newline|'\n'
name|'return'
string|"'303 See Other'"
op|','
name|'headers'
op|','
name|'body'
newline|'\n'
nl|'\n'
DECL|member|_perform_subrequest
dedent|''
name|'def'
name|'_perform_subrequest'
op|'('
name|'self'
op|','
name|'orig_env'
op|','
name|'attributes'
op|','
name|'fp'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Performs the subrequest and returns the response.\n\n        :param orig_env: The WSGI environment dict; will only be used\n                         to form a new env for the subrequest.\n        :param attributes: dict of the attributes of the form so far.\n        :param fp: The file-like object containing the request body.\n        :param key: The account key to validate the signature with.\n        :returns: (status_line, message)\n        """'
newline|'\n'
name|'if'
name|'not'
name|'key'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"'401 Unauthorized'"
op|','
string|"'invalid signature'"
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'max_file_size'
op|'='
name|'int'
op|'('
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'max_file_size'"
op|')'
name|'or'
number|'0'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'FormInvalid'
op|'('
string|"'max_file_size not an integer'"
op|')'
newline|'\n'
dedent|''
name|'subenv'
op|'='
name|'make_pre_authed_env'
op|'('
name|'orig_env'
op|','
string|"'PUT'"
op|','
name|'agent'
op|'='
name|'None'
op|','
nl|'\n'
name|'swift_source'
op|'='
string|"'FP'"
op|')'
newline|'\n'
name|'subenv'
op|'['
string|"'HTTP_TRANSFER_ENCODING'"
op|']'
op|'='
string|"'chunked'"
newline|'\n'
name|'subenv'
op|'['
string|"'wsgi.input'"
op|']'
op|'='
name|'_CappedFileLikeObject'
op|'('
name|'fp'
op|','
name|'max_file_size'
op|')'
newline|'\n'
name|'if'
name|'subenv'
op|'['
string|"'PATH_INFO'"
op|']'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'/'"
name|'and'
name|'subenv'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'count'
op|'('
string|"'/'"
op|')'
op|'<'
number|'4'
op|':'
newline|'\n'
indent|'            '
name|'subenv'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+='
string|"'/'"
newline|'\n'
dedent|''
name|'subenv'
op|'['
string|"'PATH_INFO'"
op|']'
op|'+='
name|'attributes'
op|'['
string|"'filename'"
op|']'
name|'or'
string|"'filename'"
newline|'\n'
name|'if'
string|"'content-type'"
name|'in'
name|'attributes'
op|':'
newline|'\n'
indent|'            '
name|'subenv'
op|'['
string|"'CONTENT_TYPE'"
op|']'
op|'='
name|'attributes'
op|'['
string|"'content-type'"
op|']'
name|'or'
string|"'application/octet-stream'"
newline|'\n'
dedent|''
name|'elif'
string|"'CONTENT_TYPE'"
name|'in'
name|'subenv'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'subenv'
op|'['
string|"'CONTENT_TYPE'"
op|']'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'int'
op|'('
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'expires'"
op|')'
name|'or'
number|'0'
op|')'
op|'<'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
string|"'401 Unauthorized'"
op|','
string|"'form expired'"
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'FormInvalid'
op|'('
string|"'expired not an integer'"
op|')'
newline|'\n'
dedent|''
name|'hmac_body'
op|'='
string|"'%s\\n%s\\n%s\\n%s\\n%s'"
op|'%'
op|'('
nl|'\n'
name|'orig_env'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
nl|'\n'
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'redirect'"
op|')'
name|'or'
string|"''"
op|','
nl|'\n'
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'max_file_size'"
op|')'
name|'or'
string|"'0'"
op|','
nl|'\n'
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'max_file_count'"
op|')'
name|'or'
string|"'0'"
op|','
nl|'\n'
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'expires'"
op|')'
name|'or'
string|"'0'"
op|')'
newline|'\n'
name|'sig'
op|'='
name|'hmac'
op|'.'
name|'new'
op|'('
name|'key'
op|','
name|'hmac_body'
op|','
name|'sha1'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'streq_const_time'
op|'('
name|'sig'
op|','
op|'('
name|'attributes'
op|'.'
name|'get'
op|'('
string|"'signature'"
op|')'
name|'or'
nl|'\n'
string|"'invalid'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"'401 Unauthorized'"
op|','
string|"'invalid signature'"
newline|'\n'
dedent|''
name|'substatus'
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
name|'headers'
op|','
name|'exc_info'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'substatus'
op|'['
number|'0'
op|']'
op|'='
name|'status'
newline|'\n'
nl|'\n'
dedent|''
name|'i'
op|'='
name|'iter'
op|'('
name|'self'
op|'.'
name|'app'
op|'('
name|'subenv'
op|','
name|'_start_response'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
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
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'substatus'
op|'['
number|'0'
op|']'
op|','
string|"''"
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
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the X-Account-Meta-Temp-URL-Key header value for the\n        account, or None if none is set.\n\n        :param env: The WSGI environment for the request.\n        :returns: X-Account-Meta-Temp-URL-Key str value, or None.\n        """'
newline|'\n'
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
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'<'
number|'4'
name|'or'
name|'parts'
op|'['
number|'0'
op|']'
name|'or'
name|'parts'
op|'['
number|'1'
op|']'
op|'!='
string|"'v1'"
name|'or'
name|'not'
name|'parts'
op|'['
number|'2'
op|']'
name|'or'
name|'not'
name|'parts'
op|'['
number|'3'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'parts'
op|'['
number|'2'
op|']'
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
name|'agent'
op|'='
name|'None'
op|','
name|'swift_source'
op|'='
string|"'FP'"
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
name|'FormPost'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
