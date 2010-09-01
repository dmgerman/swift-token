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
name|'ConfigParser'
name|'import'
name|'ConfigParser'
newline|'\n'
name|'import'
name|'zlib'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'internal_proxy'
name|'import'
name|'InternalProxy'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'ChunkReadTimeout'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
newline|'\n'
nl|'\n'
DECL|class|ConfigError
name|'class'
name|'ConfigError'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|MissingProxyConfig
dedent|''
name|'class'
name|'MissingProxyConfig'
op|'('
name|'ConfigError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|LogProcessor
dedent|''
name|'class'
name|'LogProcessor'
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
name|'conf'
op|','
name|'logger'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'stats_conf'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log-processor'"
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
nl|'\n'
name|'working_dir'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'working_dir'"
op|','
string|"'/tmp/swift/'"
op|')'
newline|'\n'
name|'if'
name|'working_dir'
op|'.'
name|'endswith'
op|'('
string|"'/'"
op|')'
name|'and'
name|'len'
op|'('
name|'working_dir'
op|')'
op|'>'
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'working_dir'
op|'='
name|'working_dir'
op|'['
op|':'
op|'-'
number|'1'
op|']'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'working_dir'
op|'='
name|'working_dir'
newline|'\n'
name|'proxy_server_conf_loc'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'proxy_server_conf'"
op|','
nl|'\n'
string|"'/etc/swift/proxy-server.conf'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'c'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'c'
op|'.'
name|'read'
op|'('
name|'proxy_server_conf_loc'
op|')'
newline|'\n'
name|'proxy_server_conf'
op|'='
name|'dict'
op|'('
name|'c'
op|'.'
name|'items'
op|'('
string|"'proxy-server'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'raise'
newline|'\n'
name|'raise'
name|'MissingProxyConfig'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'proxy_server_conf'
op|'='
name|'proxy_server_conf'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'logger'
op|','
name|'tuple'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
op|'*'
name|'logger'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'internal_proxy'
op|'='
name|'InternalProxy'
op|'('
name|'self'
op|'.'
name|'proxy_server_conf'
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'retries'
op|'='
number|'3'
op|')'
newline|'\n'
nl|'\n'
comment|'# load the processing plugins'
nl|'\n'
name|'self'
op|'.'
name|'plugins'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'plugin_prefix'
op|'='
string|"'log-processor-'"
newline|'\n'
name|'for'
name|'section'
name|'in'
op|'('
name|'x'
name|'for'
name|'x'
name|'in'
name|'conf'
name|'if'
name|'x'
op|'.'
name|'startswith'
op|'('
name|'plugin_prefix'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'plugin_name'
op|'='
name|'section'
op|'['
name|'len'
op|'('
name|'plugin_prefix'
op|')'
op|':'
op|']'
newline|'\n'
name|'plugin_conf'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
name|'section'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'='
name|'plugin_conf'
newline|'\n'
name|'import_target'
op|','
name|'class_name'
op|'='
name|'plugin_conf'
op|'['
string|"'class_path'"
op|']'
op|'.'
name|'rsplit'
op|'('
string|"'.'"
op|','
number|'1'
op|')'
newline|'\n'
name|'module'
op|'='
name|'__import__'
op|'('
name|'import_target'
op|','
name|'fromlist'
op|'='
op|'['
name|'import_target'
op|']'
op|')'
newline|'\n'
name|'klass'
op|'='
name|'getattr'
op|'('
name|'module'
op|','
name|'class_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'['
string|"'instance'"
op|']'
op|'='
name|'klass'
op|'('
name|'plugin_conf'
op|')'
newline|'\n'
nl|'\n'
DECL|member|process_one_file
dedent|''
dedent|''
name|'def'
name|'process_one_file'
op|'('
name|'self'
op|','
name|'plugin_name'
op|','
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
op|':'
newline|'\n'
comment|'# get an iter of the object data'
nl|'\n'
indent|'        '
name|'compressed'
op|'='
name|'object_name'
op|'.'
name|'endswith'
op|'('
string|"'.gz'"
op|')'
newline|'\n'
name|'stream'
op|'='
name|'self'
op|'.'
name|'get_object_data'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|','
nl|'\n'
name|'compressed'
op|'='
name|'compressed'
op|')'
newline|'\n'
comment|'# look up the correct plugin and send the stream to it'
nl|'\n'
name|'return'
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'['
string|"'instance'"
op|']'
op|'.'
name|'process'
op|'('
name|'stream'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_data_list
dedent|''
name|'def'
name|'get_data_list'
op|'('
name|'self'
op|','
name|'start_date'
op|'='
name|'None'
op|','
name|'end_date'
op|'='
name|'None'
op|','
name|'listing_filter'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'total_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'plugins'
op|':'
newline|'\n'
indent|'            '
name|'account'
op|'='
name|'p'
op|'['
string|"'swift_account'"
op|']'
newline|'\n'
name|'container'
op|'='
name|'p'
op|'['
string|"'container_name'"
op|']'
newline|'\n'
name|'l'
op|'='
name|'self'
op|'.'
name|'get_container_listing'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'start_date'
op|','
nl|'\n'
name|'end_date'
op|','
name|'listing_filter'
op|')'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'l'
op|':'
newline|'\n'
indent|'                '
name|'total_list'
op|'.'
name|'append'
op|'('
op|'('
name|'p'
op|','
name|'account'
op|','
name|'container'
op|','
name|'i'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'total_list'
newline|'\n'
nl|'\n'
DECL|member|get_container_listing
dedent|''
name|'def'
name|'get_container_listing'
op|'('
name|'self'
op|','
name|'swift_account'
op|','
name|'container_name'
op|','
name|'start_date'
op|'='
name|'None'
op|','
nl|'\n'
name|'end_date'
op|'='
name|'None'
op|','
name|'listing_filter'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Get a container listing, filtered by start_date, end_date, and\n        listing_filter. Dates, if given, should be in YYYYMMDDHH format\n        '''"
newline|'\n'
name|'search_key'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'start_date'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'date_parts'
op|'='
op|'['
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'year'
op|','
name|'start_date'
op|'='
name|'start_date'
op|'['
op|':'
number|'4'
op|']'
op|','
name|'start_date'
op|'['
number|'4'
op|':'
op|']'
newline|'\n'
name|'if'
name|'year'
op|':'
newline|'\n'
indent|'                    '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'year'
op|')'
newline|'\n'
name|'month'
op|','
name|'start_date'
op|'='
name|'start_date'
op|'['
op|':'
number|'2'
op|']'
op|','
name|'start_date'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'month'
op|':'
newline|'\n'
indent|'                        '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'month'
op|')'
newline|'\n'
name|'day'
op|','
name|'start_date'
op|'='
name|'start_date'
op|'['
op|':'
number|'2'
op|']'
op|','
name|'start_date'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'day'
op|':'
newline|'\n'
indent|'                            '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'day'
op|')'
newline|'\n'
name|'hour'
op|','
name|'start_date'
op|'='
name|'start_date'
op|'['
op|':'
number|'2'
op|']'
op|','
name|'start_date'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'hour'
op|':'
newline|'\n'
indent|'                                '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'hour'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'IndexError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'search_key'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
name|'date_parts'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'end_key'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'end_date'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'date_parts'
op|'='
op|'['
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'year'
op|','
name|'end_date'
op|'='
name|'end_date'
op|'['
op|':'
number|'4'
op|']'
op|','
name|'end_date'
op|'['
number|'4'
op|':'
op|']'
newline|'\n'
name|'if'
name|'year'
op|':'
newline|'\n'
indent|'                    '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'year'
op|')'
newline|'\n'
name|'month'
op|','
name|'end_date'
op|'='
name|'end_date'
op|'['
op|':'
number|'2'
op|']'
op|','
name|'end_date'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'month'
op|':'
newline|'\n'
indent|'                        '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'month'
op|')'
newline|'\n'
name|'day'
op|','
name|'end_date'
op|'='
name|'end_date'
op|'['
op|':'
number|'2'
op|']'
op|','
name|'end_date'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'day'
op|':'
newline|'\n'
indent|'                            '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'day'
op|')'
newline|'\n'
name|'hour'
op|','
name|'end_date'
op|'='
name|'end_date'
op|'['
op|':'
number|'2'
op|']'
op|','
name|'end_date'
op|'['
number|'2'
op|':'
op|']'
newline|'\n'
name|'if'
name|'hour'
op|':'
newline|'\n'
indent|'                                '
name|'date_parts'
op|'.'
name|'append'
op|'('
name|'hour'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'IndexError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'end_key'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
name|'date_parts'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'container_listing'
op|'='
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'get_container_list'
op|'('
nl|'\n'
name|'swift_account'
op|','
nl|'\n'
name|'container_name'
op|','
nl|'\n'
name|'marker'
op|'='
name|'search_key'
op|')'
newline|'\n'
name|'results'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
name|'container_listing'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'listing_filter'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'listing_filter'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
dedent|''
name|'for'
name|'item'
name|'in'
name|'container_listing'
op|':'
newline|'\n'
indent|'                '
name|'name'
op|'='
name|'item'
op|'['
string|"'name'"
op|']'
newline|'\n'
name|'if'
name|'end_key'
name|'and'
name|'name'
op|'>'
name|'end_key'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'name'
name|'not'
name|'in'
name|'listing_filter'
op|':'
newline|'\n'
indent|'                    '
name|'results'
op|'.'
name|'append'
op|'('
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'results'
newline|'\n'
nl|'\n'
DECL|member|get_object_data
dedent|''
name|'def'
name|'get_object_data'
op|'('
name|'self'
op|','
name|'swift_account'
op|','
name|'container_name'
op|','
name|'object_name'
op|','
nl|'\n'
name|'compressed'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''reads an object and yields its lines'''"
newline|'\n'
name|'o'
op|'='
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'get_object'
op|'('
name|'swift_account'
op|','
nl|'\n'
name|'container_name'
op|','
nl|'\n'
name|'object_name'
op|')'
newline|'\n'
name|'last_part'
op|'='
string|"''"
newline|'\n'
name|'last_compressed_part'
op|'='
string|"''"
newline|'\n'
comment|'# magic in the following zlib.decompressobj argument is courtesy of'
nl|'\n'
comment|'# http://stackoverflow.com/questions/2423866/python-decompressing-gzip-chunk-by-chunk'
nl|'\n'
name|'d'
op|'='
name|'zlib'
op|'.'
name|'decompressobj'
op|'('
number|'16'
op|'+'
name|'zlib'
op|'.'
name|'MAX_WBITS'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'chunk'
name|'in'
name|'o'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'compressed'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'chunk'
op|'='
name|'d'
op|'.'
name|'decompress'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'zlib'
op|'.'
name|'error'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
name|'BadFileDownload'
op|'('
op|')'
comment|'# bad compressed data'
newline|'\n'
dedent|''
dedent|''
name|'parts'
op|'='
name|'chunk'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
newline|'\n'
name|'parts'
op|'['
number|'0'
op|']'
op|'='
name|'last_part'
op|'+'
name|'parts'
op|'['
number|'0'
op|']'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'parts'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'yield'
name|'part'
newline|'\n'
dedent|''
name|'last_part'
op|'='
name|'parts'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'last_part'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'last_part'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ChunkReadTimeout'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'BadFileDownload'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|function|multiprocess_collate
dedent|''
dedent|''
dedent|''
name|'def'
name|'multiprocess_collate'
op|'('
name|'processor_args'
op|','
nl|'\n'
name|'start_date'
op|'='
name|'None'
op|','
nl|'\n'
name|'end_date'
op|'='
name|'None'
op|','
nl|'\n'
name|'listing_filter'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''get listing of files and yield hourly data from them'''"
newline|'\n'
name|'p'
op|'='
name|'LogProcessor'
op|'('
op|'*'
name|'processor_args'
op|')'
newline|'\n'
name|'all_files'
op|'='
name|'p'
op|'.'
name|'get_data_list'
op|'('
name|'start_date'
op|','
name|'end_date'
op|','
name|'listing_filter'
op|')'
newline|'\n'
nl|'\n'
name|'p'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'loaded %d files to process'"
op|'%'
name|'len'
op|'('
name|'all_files'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'not'
name|'all_files'
op|':'
newline|'\n'
comment|'# no work to do'
nl|'\n'
indent|'        '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'worker_count'
op|'='
name|'multiprocessing'
op|'.'
name|'cpu_count'
op|'('
op|')'
op|'-'
number|'1'
newline|'\n'
name|'results'
op|'='
op|'['
op|']'
newline|'\n'
name|'in_queue'
op|'='
name|'multiprocessing'
op|'.'
name|'Queue'
op|'('
op|')'
newline|'\n'
name|'out_queue'
op|'='
name|'multiprocessing'
op|'.'
name|'Queue'
op|'('
op|')'
newline|'\n'
name|'for'
name|'_'
name|'in'
name|'range'
op|'('
name|'worker_count'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'='
name|'multiprocessing'
op|'.'
name|'Process'
op|'('
name|'target'
op|'='
name|'collate_worker'
op|','
nl|'\n'
name|'args'
op|'='
op|'('
name|'processor_args'
op|','
nl|'\n'
name|'in_queue'
op|','
nl|'\n'
name|'out_queue'
op|')'
op|')'
newline|'\n'
name|'p'
op|'.'
name|'start'
op|'('
op|')'
newline|'\n'
name|'results'
op|'.'
name|'append'
op|'('
name|'p'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'x'
name|'in'
name|'all_files'
op|':'
newline|'\n'
indent|'        '
name|'in_queue'
op|'.'
name|'put'
op|'('
name|'x'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'_'
name|'in'
name|'range'
op|'('
name|'worker_count'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'in_queue'
op|'.'
name|'put'
op|'('
name|'None'
op|')'
newline|'\n'
dedent|''
name|'count'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'item'
op|','
name|'data'
op|'='
name|'out_queue'
op|'.'
name|'get_nowait'
op|'('
op|')'
newline|'\n'
name|'count'
op|'+='
number|'1'
newline|'\n'
name|'if'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'item'
op|','
name|'data'
newline|'\n'
dedent|''
name|'if'
name|'count'
op|'>='
name|'len'
op|'('
name|'all_files'
op|')'
op|':'
newline|'\n'
comment|'# this implies that one result will come from every request'
nl|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Queue'
op|'.'
name|'Empty'
op|':'
newline|'\n'
indent|'            '
name|'time'
op|'.'
name|'sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'r'
name|'in'
name|'results'
op|':'
newline|'\n'
indent|'        '
name|'r'
op|'.'
name|'join'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|function|collate_worker
dedent|''
dedent|''
name|'def'
name|'collate_worker'
op|'('
name|'processor_args'
op|','
name|'in_queue'
op|','
name|'out_queue'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''worker process for multiprocess_collate'''"
newline|'\n'
name|'p'
op|'='
name|'LogProcessor'
op|'('
op|'*'
name|'processor_args'
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'item'
op|'='
name|'in_queue'
op|'.'
name|'get_nowait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'item'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Queue'
op|'.'
name|'Empty'
op|':'
newline|'\n'
indent|'            '
name|'time'
op|'.'
name|'sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'ret'
op|'='
name|'None'
newline|'\n'
name|'ret'
op|'='
name|'p'
op|'.'
name|'process_one_file'
op|'('
name|'item'
op|')'
newline|'\n'
name|'out_queue'
op|'.'
name|'put'
op|'('
op|'('
name|'item'
op|','
name|'ret'
op|')'
op|')'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
