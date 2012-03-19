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
string|'"""\nMonkey Patch httplib.HTTPResponse to buffer reads of headers. This can improve\nperformance when making large numbers of small HTTP requests.  This module\nalso provides helper functions to make HTTP connections using\nBufferedHTTPResponse.\n\n.. warning::\n\n    If you use this, be sure that the libraries you are using do not access\n    the socket directly (xmlrpclib, I\'m looking at you :/), and instead\n    make all calls through httplib.\n"""'
newline|'\n'
nl|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
op|'.'
name|'httplib'
name|'import'
name|'CONTINUE'
op|','
name|'HTTPConnection'
op|','
name|'HTTPMessage'
op|','
name|'HTTPResponse'
op|','
name|'HTTPSConnection'
op|','
name|'_UNKNOWN'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BufferedHTTPResponse
name|'class'
name|'BufferedHTTPResponse'
op|'('
name|'HTTPResponse'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""HTTPResponse class that buffers reading of headers"""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'sock'
op|','
name|'debuglevel'
op|'='
number|'0'
op|','
name|'strict'
op|'='
number|'0'
op|','
nl|'\n'
name|'method'
op|'='
name|'None'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'sock'
op|'='
name|'sock'
newline|'\n'
name|'self'
op|'.'
name|'fp'
op|'='
name|'sock'
op|'.'
name|'makefile'
op|'('
string|"'rb'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'debuglevel'
op|'='
name|'debuglevel'
newline|'\n'
name|'self'
op|'.'
name|'strict'
op|'='
name|'strict'
newline|'\n'
name|'self'
op|'.'
name|'_method'
op|'='
name|'method'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
name|'None'
newline|'\n'
nl|'\n'
comment|'# from the Status-Line of the response'
nl|'\n'
name|'self'
op|'.'
name|'version'
op|'='
name|'_UNKNOWN'
comment|'# HTTP-Version'
newline|'\n'
name|'self'
op|'.'
name|'status'
op|'='
name|'_UNKNOWN'
comment|'# Status-Code'
newline|'\n'
name|'self'
op|'.'
name|'reason'
op|'='
name|'_UNKNOWN'
comment|'# Reason-Phrase'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'chunked'
op|'='
name|'_UNKNOWN'
comment|'# is "chunked" being used?'
newline|'\n'
name|'self'
op|'.'
name|'chunk_left'
op|'='
name|'_UNKNOWN'
comment|'# bytes left to read in current chunk'
newline|'\n'
name|'self'
op|'.'
name|'length'
op|'='
name|'_UNKNOWN'
comment|'# number of bytes left in response'
newline|'\n'
name|'self'
op|'.'
name|'will_close'
op|'='
name|'_UNKNOWN'
comment|'# conn will close at end of response'
newline|'\n'
nl|'\n'
DECL|member|expect_response
dedent|''
name|'def'
name|'expect_response'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'fp'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fp'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'fp'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'fp'
op|'='
name|'self'
op|'.'
name|'sock'
op|'.'
name|'makefile'
op|'('
string|"'rb'"
op|','
number|'0'
op|')'
newline|'\n'
name|'version'
op|','
name|'status'
op|','
name|'reason'
op|'='
name|'self'
op|'.'
name|'_read_status'
op|'('
op|')'
newline|'\n'
name|'if'
name|'status'
op|'!='
name|'CONTINUE'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_read_status'
op|'='
name|'lambda'
op|':'
op|'('
name|'version'
op|','
name|'status'
op|','
name|'reason'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'begin'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'status'
op|'='
name|'status'
newline|'\n'
name|'self'
op|'.'
name|'reason'
op|'='
name|'reason'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'='
number|'11'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
name|'HTTPMessage'
op|'('
name|'self'
op|'.'
name|'fp'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'.'
name|'fp'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'HTTPResponse'
op|'.'
name|'close'
op|'('
name|'self'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'sock'
op|'='
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BufferedHTTPConnection
dedent|''
dedent|''
name|'class'
name|'BufferedHTTPConnection'
op|'('
name|'HTTPConnection'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""HTTPConnection class that uses BufferedHTTPResponse"""'
newline|'\n'
DECL|variable|response_class
name|'response_class'
op|'='
name|'BufferedHTTPResponse'
newline|'\n'
nl|'\n'
DECL|member|connect
name|'def'
name|'connect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_connected_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'return'
name|'HTTPConnection'
op|'.'
name|'connect'
op|'('
name|'self'
op|')'
newline|'\n'
nl|'\n'
DECL|member|putrequest
dedent|''
name|'def'
name|'putrequest'
op|'('
name|'self'
op|','
name|'method'
op|','
name|'url'
op|','
name|'skip_host'
op|'='
number|'0'
op|','
name|'skip_accept_encoding'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_method'
op|'='
name|'method'
newline|'\n'
name|'self'
op|'.'
name|'_path'
op|'='
name|'url'
newline|'\n'
name|'return'
name|'HTTPConnection'
op|'.'
name|'putrequest'
op|'('
name|'self'
op|','
name|'method'
op|','
name|'url'
op|','
name|'skip_host'
op|','
nl|'\n'
name|'skip_accept_encoding'
op|')'
newline|'\n'
nl|'\n'
DECL|member|getexpect
dedent|''
name|'def'
name|'getexpect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'response'
op|'='
name|'BufferedHTTPResponse'
op|'('
name|'self'
op|'.'
name|'sock'
op|','
name|'strict'
op|'='
name|'self'
op|'.'
name|'strict'
op|','
nl|'\n'
name|'method'
op|'='
name|'self'
op|'.'
name|'_method'
op|')'
newline|'\n'
name|'response'
op|'.'
name|'expect_response'
op|'('
op|')'
newline|'\n'
name|'return'
name|'response'
newline|'\n'
nl|'\n'
DECL|member|getresponse
dedent|''
name|'def'
name|'getresponse'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'response'
op|'='
name|'HTTPConnection'
op|'.'
name|'getresponse'
op|'('
name|'self'
op|')'
newline|'\n'
name|'logging'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"HTTP PERF: %(time).5f seconds to %(method)s "'
nl|'\n'
string|'"%(host)s:%(port)s %(path)s)"'
op|')'
op|','
nl|'\n'
op|'{'
string|"'time'"
op|':'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'_connected_time'
op|','
string|"'method'"
op|':'
name|'self'
op|'.'
name|'_method'
op|','
nl|'\n'
string|"'host'"
op|':'
name|'self'
op|'.'
name|'host'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'path'"
op|':'
name|'self'
op|'.'
name|'_path'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'response'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|http_connect
dedent|''
dedent|''
name|'def'
name|'http_connect'
op|'('
name|'ipaddr'
op|','
name|'port'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'method'
op|','
name|'path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'None'
op|','
name|'query_string'
op|'='
name|'None'
op|','
name|'ssl'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function to create an HTTPConnection object. If ssl is set True,\n    HTTPSConnection will be used. However, if ssl=False, BufferedHTTPConnection\n    will be used, which is buffered for backend Swift services.\n\n    :param ipaddr: IPv4 address to connect to\n    :param port: port to connect to\n    :param device: device of the node to query\n    :param partition: partition on the device\n    :param method: HTTP method to request (\'GET\', \'PUT\', \'POST\', etc.)\n    :param path: request path\n    :param headers: dictionary of headers\n    :param query_string: request query string\n    :param ssl: set True if SSL should be used (default: False)\n    :returns: HTTPConnection object\n    """'
newline|'\n'
name|'if'
name|'not'
name|'port'
op|':'
newline|'\n'
indent|'        '
name|'port'
op|'='
number|'443'
name|'if'
name|'ssl'
name|'else'
number|'80'
newline|'\n'
dedent|''
name|'if'
name|'ssl'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'HTTPSConnection'
op|'('
string|"'%s:%s'"
op|'%'
op|'('
name|'ipaddr'
op|','
name|'port'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'BufferedHTTPConnection'
op|'('
string|"'%s:%s'"
op|'%'
op|'('
name|'ipaddr'
op|','
name|'port'
op|')'
op|')'
newline|'\n'
dedent|''
name|'path'
op|'='
name|'quote'
op|'('
string|"'/'"
op|'+'
name|'device'
op|'+'
string|"'/'"
op|'+'
name|'str'
op|'('
name|'partition'
op|')'
op|'+'
name|'path'
op|')'
newline|'\n'
name|'if'
name|'query_string'
op|':'
newline|'\n'
indent|'        '
name|'path'
op|'+='
string|"'?'"
op|'+'
name|'query_string'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'path'
op|'='
name|'path'
newline|'\n'
name|'conn'
op|'.'
name|'putrequest'
op|'('
name|'method'
op|','
name|'path'
op|','
name|'skip_host'
op|'='
op|'('
name|'headers'
name|'and'
string|"'Host'"
name|'in'
name|'headers'
op|')'
op|')'
newline|'\n'
name|'if'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'headers'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'putheader'
op|'('
name|'header'
op|','
name|'str'
op|'('
name|'value'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'conn'
op|'.'
name|'endheaders'
op|'('
op|')'
newline|'\n'
name|'return'
name|'conn'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|http_connect_raw
dedent|''
name|'def'
name|'http_connect_raw'
op|'('
name|'ipaddr'
op|','
name|'port'
op|','
name|'method'
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'None'
op|','
nl|'\n'
name|'query_string'
op|'='
name|'None'
op|','
name|'ssl'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function to create an HTTPConnection object. If ssl is set True,\n    HTTPSConnection will be used. However, if ssl=False, BufferedHTTPConnection\n    will be used, which is buffered for backend Swift services.\n\n    :param ipaddr: IPv4 address to connect to\n    :param port: port to connect to\n    :param method: HTTP method to request (\'GET\', \'PUT\', \'POST\', etc.)\n    :param path: request path\n    :param headers: dictionary of headers\n    :param query_string: request query string\n    :param ssl: set True if SSL should be used (default: False)\n    :returns: HTTPConnection object\n    """'
newline|'\n'
name|'if'
name|'not'
name|'port'
op|':'
newline|'\n'
indent|'        '
name|'port'
op|'='
number|'443'
name|'if'
name|'ssl'
name|'else'
number|'80'
newline|'\n'
dedent|''
name|'if'
name|'ssl'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'HTTPSConnection'
op|'('
string|"'%s:%s'"
op|'%'
op|'('
name|'ipaddr'
op|','
name|'port'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'BufferedHTTPConnection'
op|'('
string|"'%s:%s'"
op|'%'
op|'('
name|'ipaddr'
op|','
name|'port'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'query_string'
op|':'
newline|'\n'
indent|'        '
name|'path'
op|'+='
string|"'?'"
op|'+'
name|'query_string'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'path'
op|'='
name|'path'
newline|'\n'
name|'conn'
op|'.'
name|'putrequest'
op|'('
name|'method'
op|','
name|'path'
op|','
name|'skip_host'
op|'='
op|'('
name|'headers'
name|'and'
string|"'Host'"
name|'in'
name|'headers'
op|')'
op|')'
newline|'\n'
name|'if'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'headers'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'putheader'
op|'('
name|'header'
op|','
name|'str'
op|'('
name|'value'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'conn'
op|'.'
name|'endheaders'
op|'('
op|')'
newline|'\n'
name|'return'
name|'conn'
newline|'\n'
dedent|''
endmarker|''
end_unit
