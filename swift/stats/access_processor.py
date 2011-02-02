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
name|'import'
name|'collections'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
newline|'\n'
name|'import'
name|'copy'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
op|','
name|'get_logger'
newline|'\n'
nl|'\n'
DECL|variable|month_map
name|'month_map'
op|'='
string|"'_ Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'"
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccessLogProcessor
name|'class'
name|'AccessLogProcessor'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Transform proxy server access logs"""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'server_name'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'server_name'"
op|','
string|"'proxy-server'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'lb_private_ips'
op|'='
op|'['
name|'x'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'x'
name|'in'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'lb_private_ips'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
name|'if'
name|'x'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'service_ips'
op|'='
op|'['
name|'x'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'x'
name|'in'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'service_ips'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
name|'if'
name|'x'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'warn_percent'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'warn_percent'"
op|','
string|"'0.8'"
op|')'
op|')'
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
string|"'access-processor'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|log_line_parser
dedent|''
name|'def'
name|'log_line_parser'
op|'('
name|'self'
op|','
name|'raw_log'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''given a raw access log line, return a dict of the good parts'''"
newline|'\n'
name|'d'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
op|'('
name|'unused'
op|','
nl|'\n'
name|'server'
op|','
nl|'\n'
name|'client_ip'
op|','
nl|'\n'
name|'lb_ip'
op|','
nl|'\n'
name|'timestamp'
op|','
nl|'\n'
name|'method'
op|','
nl|'\n'
name|'request'
op|','
nl|'\n'
name|'http_version'
op|','
nl|'\n'
name|'code'
op|','
nl|'\n'
name|'referrer'
op|','
nl|'\n'
name|'user_agent'
op|','
nl|'\n'
name|'auth_token'
op|','
nl|'\n'
name|'bytes_in'
op|','
nl|'\n'
name|'bytes_out'
op|','
nl|'\n'
name|'etag'
op|','
nl|'\n'
name|'trans_id'
op|','
nl|'\n'
name|'headers'
op|','
nl|'\n'
name|'processing_time'
op|')'
op|'='
op|'('
name|'unquote'
op|'('
name|'x'
op|')'
name|'for'
name|'x'
name|'in'
nl|'\n'
name|'raw_log'
op|'['
number|'16'
op|':'
op|']'
op|'.'
name|'split'
op|'('
string|"' '"
op|')'
op|'['
op|':'
number|'18'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Bad line data: %s'"
op|')'
op|'%'
name|'repr'
op|'('
name|'raw_log'
op|')'
op|')'
newline|'\n'
name|'return'
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'if'
name|'server'
op|'!='
name|'self'
op|'.'
name|'server_name'
op|':'
newline|'\n'
comment|'# incorrect server name in log line'
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'\'Bad server name: found "%(found)s" \''
string|'\'expected "%(expected)s"\''
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'found'"
op|':'
name|'server'
op|','
string|"'expected'"
op|':'
name|'self'
op|'.'
name|'server_name'
op|'}'
op|')'
newline|'\n'
name|'return'
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
op|'('
name|'version'
op|','
name|'account'
op|','
name|'container_name'
op|','
name|'object_name'
op|')'
op|'='
name|'split_path'
op|'('
name|'request'
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
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Invalid path: %(error)s from data: %(log)s'"
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'error'"
op|':'
name|'e'
op|','
string|"'log'"
op|':'
name|'repr'
op|'('
name|'raw_log'
op|')'
op|'}'
op|')'
newline|'\n'
name|'return'
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'if'
name|'container_name'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'container_name'
op|'='
name|'container_name'
op|'.'
name|'split'
op|'('
string|"'?'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'object_name'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'object_name'
op|'='
name|'object_name'
op|'.'
name|'split'
op|'('
string|"'?'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'account'
op|'.'
name|'split'
op|'('
string|"'?'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'query'
op|'='
name|'None'
newline|'\n'
name|'if'
string|"'?'"
name|'in'
name|'request'
op|':'
newline|'\n'
indent|'            '
name|'request'
op|','
name|'query'
op|'='
name|'request'
op|'.'
name|'split'
op|'('
string|"'?'"
op|','
number|'1'
op|')'
newline|'\n'
name|'args'
op|'='
name|'query'
op|'.'
name|'split'
op|'('
string|"'&'"
op|')'
newline|'\n'
comment|'# Count each query argument. This is used later to aggregate'
nl|'\n'
comment|'# the number of format, prefix, etc. queries.'
nl|'\n'
name|'for'
name|'q'
name|'in'
name|'args'
op|':'
newline|'\n'
indent|'                '
name|'if'
string|"'='"
name|'in'
name|'q'
op|':'
newline|'\n'
indent|'                    '
name|'k'
op|','
name|'v'
op|'='
name|'q'
op|'.'
name|'split'
op|'('
string|"'='"
op|','
number|'1'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'k'
op|'='
name|'q'
newline|'\n'
comment|'# Certain keys will get summmed in stats reporting'
nl|'\n'
comment|'# (format, path, delimiter, etc.). Save a "1" here'
nl|'\n'
comment|'# to indicate that this request is 1 request for'
nl|'\n'
comment|'# its respective key.'
nl|'\n'
dedent|''
name|'d'
op|'['
name|'k'
op|']'
op|'='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'d'
op|'['
string|"'client_ip'"
op|']'
op|'='
name|'client_ip'
newline|'\n'
name|'d'
op|'['
string|"'lb_ip'"
op|']'
op|'='
name|'lb_ip'
newline|'\n'
name|'d'
op|'['
string|"'method'"
op|']'
op|'='
name|'method'
newline|'\n'
name|'d'
op|'['
string|"'request'"
op|']'
op|'='
name|'request'
newline|'\n'
name|'if'
name|'query'
op|':'
newline|'\n'
indent|'            '
name|'d'
op|'['
string|"'query'"
op|']'
op|'='
name|'query'
newline|'\n'
dedent|''
name|'d'
op|'['
string|"'http_version'"
op|']'
op|'='
name|'http_version'
newline|'\n'
name|'d'
op|'['
string|"'code'"
op|']'
op|'='
name|'code'
newline|'\n'
name|'d'
op|'['
string|"'referrer'"
op|']'
op|'='
name|'referrer'
newline|'\n'
name|'d'
op|'['
string|"'user_agent'"
op|']'
op|'='
name|'user_agent'
newline|'\n'
name|'d'
op|'['
string|"'auth_token'"
op|']'
op|'='
name|'auth_token'
newline|'\n'
name|'d'
op|'['
string|"'bytes_in'"
op|']'
op|'='
name|'bytes_in'
newline|'\n'
name|'d'
op|'['
string|"'bytes_out'"
op|']'
op|'='
name|'bytes_out'
newline|'\n'
name|'d'
op|'['
string|"'etag'"
op|']'
op|'='
name|'etag'
newline|'\n'
name|'d'
op|'['
string|"'trans_id'"
op|']'
op|'='
name|'trans_id'
newline|'\n'
name|'d'
op|'['
string|"'processing_time'"
op|']'
op|'='
name|'processing_time'
newline|'\n'
name|'day'
op|','
name|'month'
op|','
name|'year'
op|','
name|'hour'
op|','
name|'minute'
op|','
name|'second'
op|'='
name|'timestamp'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'d'
op|'['
string|"'day'"
op|']'
op|'='
name|'day'
newline|'\n'
name|'month'
op|'='
op|'('
string|"'%02s'"
op|'%'
name|'month_map'
op|'.'
name|'index'
op|'('
name|'month'
op|')'
op|')'
op|'.'
name|'replace'
op|'('
string|"' '"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'d'
op|'['
string|"'month'"
op|']'
op|'='
name|'month'
newline|'\n'
name|'d'
op|'['
string|"'year'"
op|']'
op|'='
name|'year'
newline|'\n'
name|'d'
op|'['
string|"'hour'"
op|']'
op|'='
name|'hour'
newline|'\n'
name|'d'
op|'['
string|"'minute'"
op|']'
op|'='
name|'minute'
newline|'\n'
name|'d'
op|'['
string|"'second'"
op|']'
op|'='
name|'second'
newline|'\n'
name|'d'
op|'['
string|"'tz'"
op|']'
op|'='
string|"'+0000'"
newline|'\n'
name|'d'
op|'['
string|"'account'"
op|']'
op|'='
name|'account'
newline|'\n'
name|'d'
op|'['
string|"'container_name'"
op|']'
op|'='
name|'container_name'
newline|'\n'
name|'d'
op|'['
string|"'object_name'"
op|']'
op|'='
name|'object_name'
newline|'\n'
name|'d'
op|'['
string|"'bytes_out'"
op|']'
op|'='
name|'int'
op|'('
name|'d'
op|'['
string|"'bytes_out'"
op|']'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'0'"
op|')'
op|')'
newline|'\n'
name|'d'
op|'['
string|"'bytes_in'"
op|']'
op|'='
name|'int'
op|'('
name|'d'
op|'['
string|"'bytes_in'"
op|']'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'0'"
op|')'
op|')'
newline|'\n'
name|'d'
op|'['
string|"'code'"
op|']'
op|'='
name|'int'
op|'('
name|'d'
op|'['
string|"'code'"
op|']'
op|')'
newline|'\n'
name|'return'
name|'d'
newline|'\n'
nl|'\n'
DECL|member|process
dedent|''
name|'def'
name|'process'
op|'('
name|'self'
op|','
name|'obj_stream'
op|','
name|'data_object_account'
op|','
name|'data_object_container'
op|','
nl|'\n'
name|'data_object_name'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''generate hourly groupings of data from one access log file'''"
newline|'\n'
name|'hourly_aggr_info'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'total_lines'
op|'='
number|'0'
newline|'\n'
name|'bad_lines'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'line'
name|'in'
name|'obj_stream'
op|':'
newline|'\n'
indent|'            '
name|'line_data'
op|'='
name|'self'
op|'.'
name|'log_line_parser'
op|'('
name|'line'
op|')'
newline|'\n'
name|'total_lines'
op|'+='
number|'1'
newline|'\n'
name|'if'
name|'not'
name|'line_data'
op|':'
newline|'\n'
indent|'                '
name|'bad_lines'
op|'+='
number|'1'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'line_data'
op|'['
string|"'account'"
op|']'
newline|'\n'
name|'container_name'
op|'='
name|'line_data'
op|'['
string|"'container_name'"
op|']'
newline|'\n'
name|'year'
op|'='
name|'line_data'
op|'['
string|"'year'"
op|']'
newline|'\n'
name|'month'
op|'='
name|'line_data'
op|'['
string|"'month'"
op|']'
newline|'\n'
name|'day'
op|'='
name|'line_data'
op|'['
string|"'day'"
op|']'
newline|'\n'
name|'hour'
op|'='
name|'line_data'
op|'['
string|"'hour'"
op|']'
newline|'\n'
name|'bytes_out'
op|'='
name|'line_data'
op|'['
string|"'bytes_out'"
op|']'
newline|'\n'
name|'bytes_in'
op|'='
name|'line_data'
op|'['
string|"'bytes_in'"
op|']'
newline|'\n'
name|'method'
op|'='
name|'line_data'
op|'['
string|"'method'"
op|']'
newline|'\n'
name|'code'
op|'='
name|'int'
op|'('
name|'line_data'
op|'['
string|"'code'"
op|']'
op|')'
newline|'\n'
name|'object_name'
op|'='
name|'line_data'
op|'['
string|"'object_name'"
op|']'
newline|'\n'
name|'client_ip'
op|'='
name|'line_data'
op|'['
string|"'client_ip'"
op|']'
newline|'\n'
nl|'\n'
name|'op_level'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'not'
name|'container_name'
op|':'
newline|'\n'
indent|'                '
name|'op_level'
op|'='
string|"'account'"
newline|'\n'
dedent|''
name|'elif'
name|'container_name'
name|'and'
name|'not'
name|'object_name'
op|':'
newline|'\n'
indent|'                '
name|'op_level'
op|'='
string|"'container'"
newline|'\n'
dedent|''
name|'elif'
name|'object_name'
op|':'
newline|'\n'
indent|'                '
name|'op_level'
op|'='
string|"'object'"
newline|'\n'
nl|'\n'
dedent|''
name|'aggr_key'
op|'='
op|'('
name|'account'
op|','
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|')'
newline|'\n'
name|'d'
op|'='
name|'hourly_aggr_info'
op|'.'
name|'get'
op|'('
name|'aggr_key'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'line_data'
op|'['
string|"'lb_ip'"
op|']'
name|'in'
name|'self'
op|'.'
name|'lb_private_ips'
op|':'
newline|'\n'
indent|'                '
name|'source'
op|'='
string|"'service'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'source'
op|'='
string|"'public'"
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'line_data'
op|'['
string|"'client_ip'"
op|']'
name|'in'
name|'self'
op|'.'
name|'service_ips'
op|':'
newline|'\n'
indent|'                '
name|'source'
op|'='
string|"'service'"
newline|'\n'
nl|'\n'
dedent|''
name|'d'
op|'['
op|'('
name|'source'
op|','
string|"'bytes_out'"
op|')'
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
op|'('
nl|'\n'
name|'source'
op|','
string|"'bytes_out'"
op|')'
op|','
number|'0'
op|')'
op|'+'
name|'bytes_out'
newline|'\n'
name|'d'
op|'['
op|'('
name|'source'
op|','
string|"'bytes_in'"
op|')'
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
op|'('
name|'source'
op|','
string|"'bytes_in'"
op|')'
op|','
number|'0'
op|')'
op|'+'
name|'bytes_in'
newline|'\n'
nl|'\n'
name|'d'
op|'['
string|"'format_query'"
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
string|"'format_query'"
op|','
number|'0'
op|')'
op|'+'
name|'line_data'
op|'.'
name|'get'
op|'('
string|"'format'"
op|','
number|'0'
op|')'
newline|'\n'
name|'d'
op|'['
string|"'marker_query'"
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
string|"'marker_query'"
op|','
number|'0'
op|')'
op|'+'
name|'line_data'
op|'.'
name|'get'
op|'('
string|"'marker'"
op|','
number|'0'
op|')'
newline|'\n'
name|'d'
op|'['
string|"'prefix_query'"
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
string|"'prefix_query'"
op|','
number|'0'
op|')'
op|'+'
name|'line_data'
op|'.'
name|'get'
op|'('
string|"'prefix'"
op|','
number|'0'
op|')'
newline|'\n'
name|'d'
op|'['
string|"'delimiter_query'"
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
string|"'delimiter_query'"
op|','
number|'0'
op|')'
op|'+'
name|'line_data'
op|'.'
name|'get'
op|'('
string|"'delimiter'"
op|','
number|'0'
op|')'
newline|'\n'
name|'path'
op|'='
name|'line_data'
op|'.'
name|'get'
op|'('
string|"'path'"
op|','
number|'0'
op|')'
newline|'\n'
name|'d'
op|'['
string|"'path_query'"
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
string|"'path_query'"
op|','
number|'0'
op|')'
op|'+'
name|'path'
newline|'\n'
nl|'\n'
name|'code'
op|'='
string|"'%dxx'"
op|'%'
op|'('
name|'code'
op|'/'
number|'100'
op|')'
newline|'\n'
name|'key'
op|'='
op|'('
name|'source'
op|','
name|'op_level'
op|','
name|'method'
op|','
name|'code'
op|')'
newline|'\n'
name|'d'
op|'['
name|'key'
op|']'
op|'='
name|'d'
op|'.'
name|'setdefault'
op|'('
name|'key'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
nl|'\n'
name|'hourly_aggr_info'
op|'['
name|'aggr_key'
op|']'
op|'='
name|'d'
newline|'\n'
dedent|''
name|'if'
name|'bad_lines'
op|'>'
op|'('
name|'total_lines'
op|'*'
name|'self'
op|'.'
name|'warn_percent'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'name'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
name|'data_object_account'
op|','
name|'data_object_container'
op|','
nl|'\n'
name|'data_object_name'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warning'
op|'('
name|'_'
op|'('
string|"'I found a bunch of bad lines in %(name)s '"
string|"'(%(bad)d bad, %(total)d total)'"
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'name'"
op|':'
name|'name'
op|','
string|"'bad'"
op|':'
name|'bad_lines'
op|','
string|"'total'"
op|':'
name|'total_lines'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'hourly_aggr_info'
newline|'\n'
nl|'\n'
DECL|member|keylist_mapping
dedent|''
name|'def'
name|'keylist_mapping'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'source_keys'
op|'='
string|"'service public'"
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'level_keys'
op|'='
string|"'account container object'"
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'verb_keys'
op|'='
string|"'GET PUT POST DELETE HEAD COPY'"
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'code_keys'
op|'='
string|"'2xx 4xx 5xx'"
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'keylist_mapping'
op|'='
op|'{'
nl|'\n'
comment|'#   <db key> : <row key> or <set of row keys>'
nl|'\n'
string|"'service_bw_in'"
op|':'
op|'('
string|"'service'"
op|','
string|"'bytes_in'"
op|')'
op|','
nl|'\n'
string|"'service_bw_out'"
op|':'
op|'('
string|"'service'"
op|','
string|"'bytes_out'"
op|')'
op|','
nl|'\n'
string|"'public_bw_in'"
op|':'
op|'('
string|"'public'"
op|','
string|"'bytes_in'"
op|')'
op|','
nl|'\n'
string|"'public_bw_out'"
op|':'
op|'('
string|"'public'"
op|','
string|"'bytes_out'"
op|')'
op|','
nl|'\n'
string|"'account_requests'"
op|':'
name|'set'
op|'('
op|')'
op|','
nl|'\n'
string|"'container_requests'"
op|':'
name|'set'
op|'('
op|')'
op|','
nl|'\n'
string|"'object_requests'"
op|':'
name|'set'
op|'('
op|')'
op|','
nl|'\n'
string|"'service_request'"
op|':'
name|'set'
op|'('
op|')'
op|','
nl|'\n'
string|"'public_request'"
op|':'
name|'set'
op|'('
op|')'
op|','
nl|'\n'
string|"'ops_count'"
op|':'
name|'set'
op|'('
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'for'
name|'verb'
name|'in'
name|'verb_keys'
op|':'
newline|'\n'
indent|'            '
name|'keylist_mapping'
op|'['
name|'verb'
op|']'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
dedent|''
name|'for'
name|'code'
name|'in'
name|'code_keys'
op|':'
newline|'\n'
indent|'            '
name|'keylist_mapping'
op|'['
name|'code'
op|']'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
dedent|''
name|'for'
name|'source'
name|'in'
name|'source_keys'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'level'
name|'in'
name|'level_keys'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'verb'
name|'in'
name|'verb_keys'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'code'
name|'in'
name|'code_keys'
op|':'
newline|'\n'
indent|'                        '
name|'keylist_mapping'
op|'['
string|"'account_requests'"
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
name|'source'
op|','
string|"'account'"
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
string|"'container_requests'"
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
name|'source'
op|','
string|"'container'"
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
string|"'object_requests'"
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
name|'source'
op|','
string|"'object'"
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
string|"'service_request'"
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
string|"'service'"
op|','
name|'level'
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
string|"'public_request'"
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
string|"'public'"
op|','
name|'level'
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
name|'verb'
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
name|'source'
op|','
name|'level'
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
name|'code'
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
name|'source'
op|','
name|'level'
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
name|'keylist_mapping'
op|'['
string|"'ops_count'"
op|']'
op|'.'
name|'add'
op|'('
nl|'\n'
op|'('
name|'source'
op|','
name|'level'
op|','
name|'verb'
op|','
name|'code'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'return'
name|'keylist_mapping'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
