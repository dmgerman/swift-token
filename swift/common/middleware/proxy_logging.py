begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
string|'"""\nLogging middleware for the Swift proxy.\n\nThis serves as both the default logging implementation and an example of how\nto plug in your own logging format/method.\n\nThe logging format implemented below is as follows:\n\nclient_ip remote_addr datetime request_method request_path protocol\n    status_int referer user_agent auth_token bytes_recvd bytes_sent\n    client_etag transaction_id headers request_time source\n\nThese values are space-separated, and each is url-encoded, so that they can\nbe separated with a simple .split()\n\n* remote_addr is the contents of the REMOTE_ADDR environment variable, while\n  client_ip is swift\'s best guess at the end-user IP, extracted variously\n  from the X-Forwarded-For header, X-Cluster-Ip header, or the REMOTE_ADDR\n  environment variable.\n\n* Values that are missing (e.g. due to a header not being present) or zero\n  are generally represented by a single hyphen (\'-\').\n"""'
newline|'\n'
nl|'\n'
name|'import'
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
name|'webob'
name|'import'
name|'Request'
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
op|','
name|'get_remote_client'
op|','
name|'TRUE_VALUES'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|InputProxy
name|'class'
name|'InputProxy'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    File-like object that counts bytes read.\n    To be swapped in for wsgi.input for accounting purposes.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'wsgi_input'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        :param wsgi_input: file-like object to wrap the functionality of\n        """'
newline|'\n'
name|'self'
op|'.'
name|'wsgi_input'
op|'='
name|'wsgi_input'
newline|'\n'
name|'self'
op|'.'
name|'bytes_received'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'client_disconnect'
op|'='
name|'False'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
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
string|'"""\n        Pass read request to the underlying file-like object and\n        add bytes read to total.\n        """'
newline|'\n'
name|'try'
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
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'client_disconnect'
op|'='
name|'True'
newline|'\n'
name|'raise'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'bytes_received'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'return'
name|'chunk'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
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
string|'"""\n        Pass readline request to the underlying file-like object and\n        add bytes read to total.\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'line'
op|'='
name|'self'
op|'.'
name|'wsgi_input'
op|'.'
name|'readline'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'client_disconnect'
op|'='
name|'True'
newline|'\n'
name|'raise'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'bytes_received'
op|'+='
name|'len'
op|'('
name|'line'
op|')'
newline|'\n'
name|'return'
name|'line'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ProxyLoggingMiddleware
dedent|''
dedent|''
name|'class'
name|'ProxyLoggingMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Middleware that logs Swift proxy requests in the swift log format.\n    """'
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
name|'log_hdrs'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_headers'"
op|','
string|"'no'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
name|'TRUE_VALUES'
newline|'\n'
name|'access_log_conf'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'key'
name|'in'
op|'('
string|"'log_facility'"
op|','
string|"'log_name'"
op|','
string|"'log_level'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'access_'"
op|'+'
name|'key'
op|','
name|'conf'
op|'.'
name|'get'
op|'('
name|'key'
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'if'
name|'value'
op|':'
newline|'\n'
indent|'                '
name|'access_log_conf'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'access_logger'
op|'='
name|'get_logger'
op|'('
name|'access_log_conf'
op|','
nl|'\n'
name|'log_route'
op|'='
string|"'proxy-access'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|log_request
dedent|''
name|'def'
name|'log_request'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'status_int'
op|','
name|'bytes_received'
op|','
name|'bytes_sent'
op|','
nl|'\n'
name|'request_time'
op|','
name|'client_disconnect'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Log a request.\n\n        :param env: WSGI environment\n        :param status_int: integer code for the response status\n        :param bytes_received: bytes successfully read from the request body\n        :param bytes_sent: bytes yielded to the WSGI server\n        :param request_time: time taken to satisfy the request, in seconds\n        """'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'client_disconnect'
op|':'
comment|"# log disconnected clients as '499' status code"
newline|'\n'
indent|'            '
name|'status_int'
op|'='
number|'499'
newline|'\n'
dedent|''
name|'the_request'
op|'='
name|'quote'
op|'('
name|'unquote'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'query_string'
op|':'
newline|'\n'
indent|'            '
name|'the_request'
op|'='
name|'the_request'
op|'+'
string|"'?'"
op|'+'
name|'req'
op|'.'
name|'query_string'
newline|'\n'
dedent|''
name|'logged_headers'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'log_hdrs'
op|':'
newline|'\n'
indent|'            '
name|'logged_headers'
op|'='
string|"'\\n'"
op|'.'
name|'join'
op|'('
string|"'%s: %s'"
op|'%'
op|'('
name|'k'
op|','
name|'v'
op|')'
nl|'\n'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'access_logger'
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
name|'if'
name|'x'
name|'else'
string|"'-'"
op|')'
nl|'\n'
name|'for'
name|'x'
name|'in'
op|'('
nl|'\n'
name|'get_remote_client'
op|'('
name|'req'
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'remote_addr'
op|','
nl|'\n'
name|'time'
op|'.'
name|'strftime'
op|'('
string|"'%d/%b/%Y/%H/%M/%S'"
op|','
name|'time'
op|'.'
name|'gmtime'
op|'('
op|')'
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'method'
op|','
nl|'\n'
name|'the_request'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SERVER_PROTOCOL'"
op|')'
op|','
nl|'\n'
name|'status_int'
op|','
nl|'\n'
name|'req'
op|'.'
name|'referer'
op|','
nl|'\n'
name|'req'
op|'.'
name|'user_agent'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-token'"
op|')'
op|','
nl|'\n'
name|'bytes_received'
op|','
nl|'\n'
name|'bytes_sent'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'etag'"
op|','
name|'None'
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.trans_id'"
op|')'
op|','
nl|'\n'
name|'logged_headers'
op|','
nl|'\n'
string|"'%.4f'"
op|'%'
name|'request_time'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.source'"
op|')'
op|','
nl|'\n'
op|')'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'access_logger'
op|'.'
name|'txn_id'
op|'='
name|'None'
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
name|'status_int'
op|'='
op|'['
number|'500'
op|']'
newline|'\n'
name|'input_proxy'
op|'='
name|'InputProxy'
op|'('
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|'='
name|'input_proxy'
newline|'\n'
name|'start_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_start_response
name|'def'
name|'my_start_response'
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
name|'status_int'
op|'['
number|'0'
op|']'
op|'='
name|'int'
op|'('
name|'status'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
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
DECL|function|iter_response
dedent|''
name|'def'
name|'iter_response'
op|'('
name|'iterator'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'bytes_sent'
op|'='
number|'0'
newline|'\n'
name|'client_disconnect'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'chunk'
name|'in'
name|'iterator'
op|':'
newline|'\n'
indent|'                    '
name|'bytes_sent'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'yield'
name|'chunk'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'GeneratorExit'
op|':'
comment|'# generator was closed before we finished'
newline|'\n'
indent|'                '
name|'client_disconnect'
op|'='
name|'True'
newline|'\n'
name|'raise'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'log_request'
op|'('
name|'env'
op|','
name|'status_int'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'input_proxy'
op|'.'
name|'bytes_received'
op|','
name|'bytes_sent'
op|','
nl|'\n'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start_time'
op|','
nl|'\n'
name|'client_disconnect'
name|'or'
name|'input_proxy'
op|'.'
name|'client_disconnect'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'iterator'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'my_start_response'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'log_request'
op|'('
name|'env'
op|','
number|'500'
op|','
name|'input_proxy'
op|'.'
name|'bytes_received'
op|','
number|'0'
op|','
nl|'\n'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start_time'
op|','
name|'input_proxy'
op|'.'
name|'client_disconnect'
op|')'
newline|'\n'
name|'raise'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'iter_response'
op|'('
name|'iterator'
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
nl|'\n'
DECL|function|proxy_logger
name|'def'
name|'proxy_logger'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ProxyLoggingMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'proxy_logger'
newline|'\n'
dedent|''
endmarker|''
end_unit
