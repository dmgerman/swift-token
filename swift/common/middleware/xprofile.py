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
string|'"""\nProfiling middleware for Swift Servers.\n\nThe current implementation is based on eventlet aware profiler.(For the\nfuture, more profilers could be added in to collect more data for analysis.)\nProfiling all incoming requests and accumulating cpu timing statistics\ninformation for performance tuning and optimization. An mini web UI is also\nprovided for profiling data analysis. It can be accessed from the URL as\nbelow.\n\nIndex page for browse profile data::\n\n    http://SERVER_IP:PORT/__profile__\n\nList all profiles to return profile ids in json format::\n\n    http://SERVER_IP:PORT/__profile__/\n    http://SERVER_IP:PORT/__profile__/all\n\nRetrieve specific profile data in different formats::\n\n    http://SERVER_IP:PORT/__profile__/PROFILE_ID?format=[default|json|csv|ods]\n    http://SERVER_IP:PORT/__profile__/current?format=[default|json|csv|ods]\n    http://SERVER_IP:PORT/__profile__/all?format=[default|json|csv|ods]\n\nRetrieve metrics from specific function in json format::\n\n    http://SERVER_IP:PORT/__profile__/PROFILE_ID/NFL?format=json\n    http://SERVER_IP:PORT/__profile__/current/NFL?format=json\n    http://SERVER_IP:PORT/__profile__/all/NFL?format=json\n\n    NFL is defined by concatenation of file name, function name and the first\n    line number.\n    e.g.::\n        account.py:50(GETorHEAD)\n    or with full path:\n        opt/stack/swift/swift/proxy/controllers/account.py:50(GETorHEAD)\n\n    A list of URL examples:\n\n    http://localhost:8080/__profile__    (proxy server)\n    http://localhost:6200/__profile__/all    (object server)\n    http://localhost:6201/__profile__/current    (container server)\n    http://localhost:6202/__profile__/12345?format=json    (account server)\n\nThe profiling middleware can be configured in paste file for WSGI servers such\nas proxy, account, container and object servers. Please refer to the sample\nconfiguration files in etc directory.\n\nThe profiling data is provided with four formats such as binary(by default),\njson, csv and odf spreadsheet which requires installing odfpy library.\n\n    sudo pip install odfpy\n\nThere\'s also a simple visualization capability which is enabled by using\nmatplotlib toolkit. it is also required to be installed if you want to use\nit to visualize statistic data.\n\n    sudo apt-get install python-matplotlib\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'greenthread'
op|','
name|'GreenPool'
op|','
name|'patcher'
newline|'\n'
name|'import'
name|'eventlet'
op|'.'
name|'green'
op|'.'
name|'profile'
name|'as'
name|'eprofile'
newline|'\n'
name|'import'
name|'six'
newline|'\n'
name|'from'
name|'six'
op|'.'
name|'moves'
name|'import'
name|'urllib'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
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
name|'config_true_value'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'x_profile'
op|'.'
name|'exceptions'
name|'import'
name|'NotFoundException'
op|','
name|'MethodNotAllowed'
op|','
name|'ProfileException'
newline|'\n'
name|'from'
name|'x_profile'
op|'.'
name|'html_viewer'
name|'import'
name|'HTMLViewer'
newline|'\n'
name|'from'
name|'x_profile'
op|'.'
name|'profile_model'
name|'import'
name|'ProfileLog'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|DEFAULT_PROFILE_PREFIX
name|'DEFAULT_PROFILE_PREFIX'
op|'='
string|"'/tmp/log/swift/profile/default.profile'"
newline|'\n'
nl|'\n'
comment|'# unwind the iterator; it may call start_response, do lots of work, etc'
nl|'\n'
name|'PROFILE_EXEC_EAGER'
op|'='
string|'"""\napp_iter = self.app(environ, start_response)\napp_iter_ = list(app_iter)\nif hasattr(app_iter, \'close\'):\n    app_iter.close()\n"""'
newline|'\n'
nl|'\n'
comment|"# don't unwind the iterator (don't consume resources)"
nl|'\n'
name|'PROFILE_EXEC_LAZY'
op|'='
string|'"""\napp_iter_ = self.app(environ, start_response)\n"""'
newline|'\n'
nl|'\n'
DECL|variable|thread
name|'thread'
op|'='
name|'patcher'
op|'.'
name|'original'
op|'('
string|"'thread'"
op|')'
comment|'# non-monkeypatched module needed'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'# This monkey patch code fix the problem of eventlet profile tool'
nl|'\n'
comment|'# which can not accumulate profiling results across multiple calls'
nl|'\n'
comment|'# of runcalls and runctx.'
nl|'\n'
DECL|function|new_setup
name|'def'
name|'new_setup'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'self'
op|'.'
name|'_has_setup'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'cur'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'timings'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'current_tasklet'
op|'='
name|'greenthread'
op|'.'
name|'getcurrent'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'thread_id'
op|'='
name|'thread'
op|'.'
name|'get_ident'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'simulate_call'
op|'('
string|'"profiler"'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|new_runctx
dedent|''
name|'def'
name|'new_runctx'
op|'('
name|'self'
op|','
name|'cmd'
op|','
name|'globals'
op|','
name|'locals'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'not'
name|'getattr'
op|'('
name|'self'
op|','
string|"'_has_setup'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_setup'
op|'('
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'base'
op|'.'
name|'runctx'
op|'('
name|'self'
op|','
name|'cmd'
op|','
name|'globals'
op|','
name|'locals'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'TallyTimings'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|new_runcall
dedent|''
dedent|''
name|'def'
name|'new_runcall'
op|'('
name|'self'
op|','
name|'func'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'not'
name|'getattr'
op|'('
name|'self'
op|','
string|"'_has_setup'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_setup'
op|'('
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'base'
op|'.'
name|'runcall'
op|'('
name|'self'
op|','
name|'func'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kw'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'TallyTimings'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ProfileMiddleware
dedent|''
dedent|''
name|'class'
name|'ProfileMiddleware'
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
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'profile'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_filename_prefix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_filename_prefix'"
op|','
nl|'\n'
name|'DEFAULT_PROFILE_PREFIX'
op|')'
newline|'\n'
name|'dirname'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'self'
op|'.'
name|'log_filename_prefix'
op|')'
newline|'\n'
comment|'# Notes: this effort may fail due to permission denied.'
nl|'\n'
comment|'# it is better to be created and authorized to current'
nl|'\n'
comment|'# user in advance.'
nl|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'dirname'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'makedirs'
op|'('
name|'dirname'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'dump_interval'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'dump_interval'"
op|','
number|'5.0'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'dump_timestamp'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'dump_timestamp'"
op|','
string|"'no'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'flush_at_shutdown'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'flush_at_shutdown'"
op|','
string|"'no'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'path'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'path'"
op|','
string|"'__profile__'"
op|')'
op|'.'
name|'replace'
op|'('
string|"'/'"
op|','
string|"''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'unwind'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'unwind'"
op|','
string|"'no'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'profile_module'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'profile_module'"
op|','
nl|'\n'
string|"'eventlet.green.profile'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'profiler'
op|'='
name|'get_profiler'
op|'('
name|'self'
op|'.'
name|'profile_module'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'profile_log'
op|'='
name|'ProfileLog'
op|'('
name|'self'
op|'.'
name|'log_filename_prefix'
op|','
nl|'\n'
name|'self'
op|'.'
name|'dump_timestamp'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'viewer'
op|'='
name|'HTMLViewer'
op|'('
name|'self'
op|'.'
name|'path'
op|','
name|'self'
op|'.'
name|'profile_module'
op|','
nl|'\n'
name|'self'
op|'.'
name|'profile_log'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'dump_pool'
op|'='
name|'GreenPool'
op|'('
number|'1000'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'last_dump_at'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|__del__
dedent|''
name|'def'
name|'__del__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'flush_at_shutdown'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'clear'
op|'('
name|'str'
op|'('
name|'os'
op|'.'
name|'getpid'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_combine_body_qs
dedent|''
dedent|''
name|'def'
name|'_combine_body_qs'
op|'('
name|'self'
op|','
name|'request'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'wsgi_input'
op|'='
name|'request'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
newline|'\n'
name|'query_dict'
op|'='
name|'request'
op|'.'
name|'params'
newline|'\n'
name|'qs_in_body'
op|'='
name|'wsgi_input'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'query_dict'
op|'.'
name|'update'
op|'('
name|'urllib'
op|'.'
name|'parse'
op|'.'
name|'parse_qs'
op|'('
name|'qs_in_body'
op|','
nl|'\n'
name|'keep_blank_values'
op|'='
name|'True'
op|','
nl|'\n'
name|'strict_parsing'
op|'='
name|'False'
op|')'
op|')'
newline|'\n'
name|'return'
name|'query_dict'
newline|'\n'
nl|'\n'
DECL|member|dump_checkpoint
dedent|''
name|'def'
name|'dump_checkpoint'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'current_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'last_dump_at'
name|'is'
name|'None'
name|'or'
name|'self'
op|'.'
name|'last_dump_at'
op|'+'
name|'self'
op|'.'
name|'dump_interval'
op|'<'
name|'current_time'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'dump_pool'
op|'.'
name|'spawn_n'
op|'('
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'dump_profile'
op|','
nl|'\n'
name|'self'
op|'.'
name|'profiler'
op|','
name|'os'
op|'.'
name|'getpid'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'last_dump_at'
op|'='
name|'current_time'
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
name|'environ'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'request'
op|'='
name|'Request'
op|'('
name|'environ'
op|')'
newline|'\n'
name|'path_entry'
op|'='
name|'request'
op|'.'
name|'path_info'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
newline|'\n'
comment|"# hijack favicon request sent by browser so that it doesn't"
nl|'\n'
comment|'# invoke profiling hook and contaminate the data.'
nl|'\n'
name|'if'
name|'path_entry'
op|'['
number|'1'
op|']'
op|'=='
string|"'favicon.ico'"
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
string|"'200 OK'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
string|"''"
newline|'\n'
dedent|''
name|'elif'
name|'path_entry'
op|'['
number|'1'
op|']'
op|'=='
name|'self'
op|'.'
name|'path'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'dump_checkpoint'
op|'('
op|')'
newline|'\n'
name|'query_dict'
op|'='
name|'self'
op|'.'
name|'_combine_body_qs'
op|'('
name|'request'
op|')'
newline|'\n'
name|'content'
op|','
name|'headers'
op|'='
name|'self'
op|'.'
name|'viewer'
op|'.'
name|'render'
op|'('
name|'request'
op|'.'
name|'url'
op|','
nl|'\n'
name|'request'
op|'.'
name|'method'
op|','
nl|'\n'
name|'path_entry'
op|','
nl|'\n'
name|'query_dict'
op|','
nl|'\n'
name|'self'
op|'.'
name|'renew_profile'
op|')'
newline|'\n'
name|'start_response'
op|'('
string|"'200 OK'"
op|','
name|'headers'
op|')'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'content'
op|','
name|'six'
op|'.'
name|'text_type'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'content'
op|'='
name|'content'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'return'
op|'['
name|'content'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'MethodNotAllowed'
name|'as'
name|'mx'
op|':'
newline|'\n'
indent|'                '
name|'start_response'
op|'('
string|"'405 Method Not Allowed'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
string|"'%s'"
op|'%'
name|'mx'
newline|'\n'
dedent|''
name|'except'
name|'NotFoundException'
name|'as'
name|'nx'
op|':'
newline|'\n'
indent|'                '
name|'start_response'
op|'('
string|"'404 Not Found'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
string|"'%s'"
op|'%'
name|'nx'
newline|'\n'
dedent|''
name|'except'
name|'ProfileException'
name|'as'
name|'pf'
op|':'
newline|'\n'
indent|'                '
name|'start_response'
op|'('
string|"'500 Internal Server Error'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
string|"'%s'"
op|'%'
name|'pf'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'ex'
op|':'
newline|'\n'
indent|'                '
name|'start_response'
op|'('
string|"'500 Internal Server Error'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
name|'_'
op|'('
string|"'Error on render profiling results: %s'"
op|')'
op|'%'
name|'ex'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'_locals'
op|'='
name|'locals'
op|'('
op|')'
newline|'\n'
name|'code'
op|'='
name|'self'
op|'.'
name|'unwind'
name|'and'
name|'PROFILE_EXEC_EAGER'
name|'or'
name|'PROFILE_EXEC_LAZY'
newline|'\n'
name|'self'
op|'.'
name|'profiler'
op|'.'
name|'runctx'
op|'('
name|'code'
op|','
name|'globals'
op|'('
op|')'
op|','
name|'_locals'
op|')'
newline|'\n'
name|'app_iter'
op|'='
name|'_locals'
op|'['
string|"'app_iter_'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'dump_checkpoint'
op|'('
op|')'
newline|'\n'
name|'return'
name|'app_iter'
newline|'\n'
nl|'\n'
DECL|member|renew_profile
dedent|''
dedent|''
name|'def'
name|'renew_profile'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'profiler'
op|'='
name|'get_profiler'
op|'('
name|'self'
op|'.'
name|'profile_module'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_profiler
dedent|''
dedent|''
name|'def'
name|'get_profiler'
op|'('
name|'profile_module'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'profile_module'
op|'=='
string|"'eventlet.green.profile'"
op|':'
newline|'\n'
indent|'        '
name|'eprofile'
op|'.'
name|'Profile'
op|'.'
name|'_setup'
op|'='
name|'new_setup'
newline|'\n'
name|'eprofile'
op|'.'
name|'Profile'
op|'.'
name|'runctx'
op|'='
name|'new_runctx'
newline|'\n'
name|'eprofile'
op|'.'
name|'Profile'
op|'.'
name|'runcall'
op|'='
name|'new_runcall'
newline|'\n'
comment|'# hacked method to import profile module supported in python 2.6'
nl|'\n'
dedent|''
name|'__import__'
op|'('
name|'profile_module'
op|')'
newline|'\n'
name|'return'
name|'sys'
op|'.'
name|'modules'
op|'['
name|'profile_module'
op|']'
op|'.'
name|'Profile'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
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
DECL|function|profile_filter
name|'def'
name|'profile_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ProfileMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'profile_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
