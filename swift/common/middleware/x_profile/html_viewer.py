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
name|'import'
name|'cgi'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'random'
newline|'\n'
name|'import'
name|'re'
newline|'\n'
name|'import'
name|'string'
newline|'\n'
name|'import'
name|'tempfile'
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
name|'exceptions'
name|'import'
name|'PLOTLIBNotInstalled'
op|','
name|'ODFLIBNotInstalled'
op|','
name|'NotFoundException'
op|','
name|'MethodNotAllowed'
op|','
name|'DataLoadFailure'
op|','
name|'ProfileException'
newline|'\n'
name|'from'
name|'profile_model'
name|'import'
name|'Stats2'
newline|'\n'
nl|'\n'
DECL|variable|PLOTLIB_INSTALLED
name|'PLOTLIB_INSTALLED'
op|'='
name|'True'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'matplotlib'
newline|'\n'
comment|'# use agg backend for writing to file, not for rendering in a window.'
nl|'\n'
comment|'# otherwise some platform will complain "no display name and $DISPLAY'
nl|'\n'
comment|'# environment variable"'
nl|'\n'
name|'matplotlib'
op|'.'
name|'use'
op|'('
string|"'agg'"
op|')'
newline|'\n'
name|'import'
name|'matplotlib'
op|'.'
name|'pyplot'
name|'as'
name|'plt'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
DECL|variable|PLOTLIB_INSTALLED
indent|'    '
name|'PLOTLIB_INSTALLED'
op|'='
name|'False'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
name|'empty_description'
op|'='
string|'"""\n        The default profile of current process or the profile you requested is\n        empty. <input type="submit" name="refresh" value="Refresh"/>\n"""'
newline|'\n'
nl|'\n'
name|'profile_tmpl'
op|'='
string|'"""\n              <select name="profile">\n                <option value="current">current</option>\n                <option value="all">all</option>\n                ${profile_list}\n              </select>\n"""'
newline|'\n'
nl|'\n'
name|'sort_tmpl'
op|'='
string|'"""\n              <select name="sort">\n                <option value="time">time</option>\n                <option value="cumulative">cumulative</option>\n                <option value="calls">calls</option>\n                <option value="pcalls">pcalls</option>\n                <option value="name">name</option>\n                <option value="file">file</option>\n                <option value="module">module</option>\n                <option value="line">line</option>\n                <option value="nfl">nfl</option>\n                <option value="stdname">stdname</option>\n              </select>\n"""'
newline|'\n'
nl|'\n'
name|'limit_tmpl'
op|'='
string|'"""\n              <select name="limit">\n                <option value="-1">all</option>\n                <option value="0.1">10%</option>\n                <option value="0.2">20%</option>\n                <option value="0.3">30%</option>\n                <option value="10">10</option>\n                <option value="20">20</option>\n                <option value="30">30</option>\n                <option value="50">50</option>\n                <option value="100">100</option>\n                <option value="200">200</option>\n                <option value="300">300</option>\n                <option value="400">400</option>\n                <option value="500">500</option>\n              </select>\n"""'
newline|'\n'
nl|'\n'
name|'fulldirs_tmpl'
op|'='
string|'"""\n              <input type="checkbox" name="fulldirs" value="1"\n              ${fulldir_checked}/>\n"""'
newline|'\n'
nl|'\n'
name|'mode_tmpl'
op|'='
string|'"""\n              <select name="mode">\n                <option value="stats">stats</option>\n                <option value="callees">callees</option>\n                <option value="callers">callers</option>\n              </select>\n"""'
newline|'\n'
nl|'\n'
name|'nfl_filter_tmpl'
op|'='
string|'"""\n              <input type="text" name="nfl_filter" value="${nfl_filter}"\n              placeholder="filename part" />\n"""'
newline|'\n'
nl|'\n'
name|'formelements_tmpl'
op|'='
string|'"""\n      <div>\n        <table>\n          <tr>\n            <td>\n              <strong>Profile</strong>\n            <td>\n              <strong>Sort</strong>\n            </td>\n            <td>\n              <strong>Limit</strong>\n            </td>\n            <td>\n              <strong>Full Path</strong>\n            </td>\n            <td>\n              <strong>Filter</strong>\n            </td>\n            <td>\n            </td>\n            <td>\n              <strong>Plot Metric</strong>\n            </td>\n            <td>\n              <strong>Plot Type</strong>\n            <td>\n            </td>\n            <td>\n              <strong>Format</strong>\n            </td>\n            <td>\n            <td>\n            </td>\n            <td>\n            </td>\n\n          </tr>\n          <tr>\n            <td>\n               ${profile}\n            <td>\n               ${sort}\n            </td>\n            <td>\n               ${limit}\n            </td>\n            <td>\n              ${fulldirs}\n            </td>\n            <td>\n              ${nfl_filter}\n            </td>\n            <td>\n              <input type="submit" name="query" value="query"/>\n            </td>\n            <td>\n              <select name=\'metric\'>\n                <option value=\'nc\'>call count</option>\n                <option value=\'cc\'>primitive call count</option>\n                <option value=\'tt\'>total time</option>\n                <option value=\'ct\'>cumulative time</option>\n              </select>\n            </td>\n            <td>\n              <select name=\'plottype\'>\n                <option value=\'bar\'>bar</option>\n                <option value=\'pie\'>pie</option>\n              </select>\n            <td>\n              <input type="submit" name="plot" value="plot"/>\n            </td>\n            <td>\n              <select name=\'format\'>\n                <option value=\'default\'>binary</option>\n                <option value=\'json\'>json</option>\n                <option value=\'csv\'>csv</option>\n                <option value=\'ods\'>ODF.ods</option>\n              </select>\n            </td>\n            <td>\n              <input type="submit" name="download" value="download"/>\n            </td>\n            <td>\n              <input type="submit" name="clear" value="clear"/>\n            </td>\n          </tr>\n        </table>\n      </div>\n"""'
newline|'\n'
nl|'\n'
name|'index_tmpl'
op|'='
string|'"""\n<html>\n  <head>\n    <title>profile results</title>\n    <style>\n    <!--\n      tr.normal { background-color: #ffffff }\n      tr.hover { background-color: #88eeee }\n    //-->\n    </style>\n  </head>\n  <body>\n\n    <form action="${action}" method="POST">\n\n      <div class="form-text">\n        ${description}\n      </div>\n      <hr />\n      ${formelements}\n\n    </form>\n    <pre>\n${profilehtml}\n    </pre>\n\n  </body>\n</html>\n"""'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|HTMLViewer
name|'class'
name|'HTMLViewer'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|variable|format_dict
indent|'    '
name|'format_dict'
op|'='
op|'{'
string|"'default'"
op|':'
string|"'application/octet-stream'"
op|','
nl|'\n'
string|"'json'"
op|':'
string|"'application/json'"
op|','
nl|'\n'
string|"'csv'"
op|':'
string|"'text/csv'"
op|','
nl|'\n'
string|"'ods'"
op|':'
string|"'application/vnd.oasis.opendocument.spreadsheet'"
op|','
nl|'\n'
string|"'python'"
op|':'
string|"'text/html'"
op|'}'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app_path'
op|','
name|'profile_module'
op|','
name|'profile_log'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app_path'
op|'='
name|'app_path'
newline|'\n'
name|'self'
op|'.'
name|'profile_module'
op|'='
name|'profile_module'
newline|'\n'
name|'self'
op|'.'
name|'profile_log'
op|'='
name|'profile_log'
newline|'\n'
nl|'\n'
DECL|member|_get_param
dedent|''
name|'def'
name|'_get_param'
op|'('
name|'self'
op|','
name|'query_dict'
op|','
name|'key'
op|','
name|'default'
op|'='
name|'None'
op|','
name|'multiple'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'query_dict'
op|'.'
name|'get'
op|'('
name|'key'
op|','
name|'default'
op|')'
newline|'\n'
name|'if'
name|'value'
name|'is'
name|'None'
name|'or'
name|'value'
op|'=='
string|"''"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'default'
newline|'\n'
dedent|''
name|'if'
name|'multiple'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'value'
newline|'\n'
dedent|''
name|'if'
name|'isinstance'
op|'('
name|'value'
op|','
name|'list'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'eval'
op|'('
name|'value'
op|'['
number|'0'
op|']'
op|')'
name|'if'
name|'isinstance'
op|'('
name|'default'
op|','
name|'int'
op|')'
name|'else'
name|'value'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'value'
newline|'\n'
nl|'\n'
DECL|member|render
dedent|''
dedent|''
name|'def'
name|'render'
op|'('
name|'self'
op|','
name|'url'
op|','
name|'method'
op|','
name|'path_entry'
op|','
name|'query_dict'
op|','
name|'clear_callback'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'plot'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'plot'"
op|','
name|'None'
op|')'
newline|'\n'
name|'download'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'download'"
op|','
name|'None'
op|')'
newline|'\n'
name|'clear'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'clear'"
op|','
name|'None'
op|')'
newline|'\n'
name|'action'
op|'='
name|'plot'
name|'or'
name|'download'
name|'or'
name|'clear'
newline|'\n'
name|'profile_id'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'profile'"
op|','
string|"'current'"
op|')'
newline|'\n'
name|'sort'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'sort'"
op|','
string|"'time'"
op|')'
newline|'\n'
name|'limit'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'limit'"
op|','
op|'-'
number|'1'
op|')'
newline|'\n'
name|'fulldirs'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'fulldirs'"
op|','
number|'0'
op|')'
newline|'\n'
name|'nfl_filter'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'nfl_filter'"
op|','
string|"''"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'metric_selected'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'metric'"
op|','
string|"'cc'"
op|')'
newline|'\n'
name|'plot_type'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'plottype'"
op|','
string|"'bar'"
op|')'
newline|'\n'
name|'download_format'
op|'='
name|'self'
op|'.'
name|'_get_param'
op|'('
name|'query_dict'
op|','
string|"'format'"
op|','
string|"'default'"
op|')'
newline|'\n'
name|'content'
op|'='
string|"''"
newline|'\n'
comment|'# GET  /__profile, POST /__profile'
nl|'\n'
name|'if'
name|'len'
op|'('
name|'path_entry'
op|')'
op|'=='
number|'2'
name|'and'
name|'method'
name|'in'
op|'['
string|"'GET'"
op|','
string|"'POST'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'log_files'
op|'='
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'get_logfiles'
op|'('
name|'profile_id'
op|')'
newline|'\n'
name|'if'
name|'action'
op|'=='
string|"'plot'"
op|':'
newline|'\n'
indent|'                '
name|'content'
op|','
name|'headers'
op|'='
name|'self'
op|'.'
name|'plot'
op|'('
name|'log_files'
op|','
name|'sort'
op|','
name|'limit'
op|','
nl|'\n'
name|'nfl_filter'
op|','
name|'metric_selected'
op|','
nl|'\n'
name|'plot_type'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'action'
op|'=='
string|"'download'"
op|':'
newline|'\n'
indent|'                '
name|'content'
op|','
name|'headers'
op|'='
name|'self'
op|'.'
name|'download'
op|'('
name|'log_files'
op|','
name|'sort'
op|','
name|'limit'
op|','
nl|'\n'
name|'nfl_filter'
op|','
name|'download_format'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'action'
op|'=='
string|"'clear'"
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'clear'
op|'('
name|'profile_id'
op|')'
newline|'\n'
name|'clear_callback'
name|'and'
name|'clear_callback'
op|'('
op|')'
newline|'\n'
dedent|''
name|'content'
op|','
name|'headers'
op|'='
name|'self'
op|'.'
name|'index_page'
op|'('
name|'log_files'
op|','
name|'sort'
op|','
name|'limit'
op|','
nl|'\n'
name|'fulldirs'
op|','
name|'nfl_filter'
op|','
nl|'\n'
name|'profile_id'
op|','
name|'url'
op|')'
newline|'\n'
comment|'# GET /__profile__/all'
nl|'\n'
comment|'# GET /__profile__/current'
nl|'\n'
comment|'# GET /__profile__/profile_id'
nl|'\n'
comment|'# GET /__profile__/profile_id/'
nl|'\n'
comment|'# GET /__profile__/profile_id/account.py:50(GETorHEAD)'
nl|'\n'
comment|'# GET /__profile__/profile_id/swift/proxy/controllers'
nl|'\n'
comment|'#      /account.py:50(GETorHEAD)'
nl|'\n'
comment|'# with QUERY_STRING:   ?format=[default|json|csv|ods]'
nl|'\n'
dedent|''
dedent|''
name|'elif'
name|'len'
op|'('
name|'path_entry'
op|')'
op|'>'
number|'2'
name|'and'
name|'method'
op|'=='
string|"'GET'"
op|':'
newline|'\n'
indent|'            '
name|'profile_id'
op|'='
name|'path_entry'
op|'['
number|'2'
op|']'
newline|'\n'
name|'log_files'
op|'='
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'get_logfiles'
op|'('
name|'profile_id'
op|')'
newline|'\n'
name|'pids'
op|'='
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'get_all_pids'
op|'('
op|')'
newline|'\n'
comment|'# return all profiles in a json format by default.'
nl|'\n'
comment|'# GET /__profile__/'
nl|'\n'
name|'if'
name|'profile_id'
op|'=='
string|"''"
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
string|'\'{"profile_ids": ["\''
op|'+'
string|'\'","\''
op|'.'
name|'join'
op|'('
name|'pids'
op|')'
op|'+'
string|'\'"]}\''
newline|'\n'
name|'headers'
op|'='
op|'['
op|'('
string|"'content-type'"
op|','
name|'self'
op|'.'
name|'format_dict'
op|'['
string|"'json'"
op|']'
op|')'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'len'
op|'('
name|'path_entry'
op|')'
op|'>'
number|'3'
name|'and'
name|'path_entry'
op|'['
number|'3'
op|']'
op|'!='
string|"''"
op|':'
newline|'\n'
indent|'                    '
name|'nfl_filter'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
name|'path_entry'
op|'['
number|'3'
op|':'
op|']'
op|')'
newline|'\n'
name|'if'
name|'path_entry'
op|'['
op|'-'
number|'1'
op|']'
op|'.'
name|'find'
op|'('
string|"':0'"
op|')'
op|'=='
op|'-'
number|'1'
op|':'
newline|'\n'
indent|'                        '
name|'nfl_filter'
op|'='
string|"'/'"
op|'+'
name|'nfl_filter'
newline|'\n'
dedent|''
dedent|''
name|'content'
op|','
name|'headers'
op|'='
name|'self'
op|'.'
name|'download'
op|'('
name|'log_files'
op|','
name|'sort'
op|','
op|'-'
number|'1'
op|','
nl|'\n'
name|'nfl_filter'
op|','
name|'download_format'
op|')'
newline|'\n'
dedent|''
name|'headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'Access-Control-Allow-Origin'"
op|','
string|"'*'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'MethodNotAllowed'
op|'('
name|'_'
op|'('
string|"'method %s is not allowed.'"
op|')'
op|'%'
name|'method'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'content'
op|','
name|'headers'
newline|'\n'
nl|'\n'
DECL|member|index_page
dedent|''
name|'def'
name|'index_page'
op|'('
name|'self'
op|','
name|'log_files'
op|'='
name|'None'
op|','
name|'sort'
op|'='
string|"'time'"
op|','
name|'limit'
op|'='
op|'-'
number|'1'
op|','
nl|'\n'
name|'fulldirs'
op|'='
number|'0'
op|','
name|'nfl_filter'
op|'='
string|"''"
op|','
name|'profile_id'
op|'='
string|"'current'"
op|','
name|'url'
op|'='
string|"'#'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'content-type'"
op|','
string|"'text/html'"
op|')'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'log_files'
op|')'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'empty_description'
op|','
name|'headers'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'stats'
op|'='
name|'Stats2'
op|'('
op|'*'
name|'log_files'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'fulldirs'
op|':'
newline|'\n'
indent|'                '
name|'stats'
op|'.'
name|'strip_dirs'
op|'('
op|')'
newline|'\n'
dedent|''
name|'stats'
op|'.'
name|'sort_stats'
op|'('
name|'sort'
op|')'
newline|'\n'
name|'nfl_filter_esc'
op|'='
name|'nfl_filter'
op|'.'
name|'replace'
op|'('
string|"'('"
op|','
string|"'\\('"
op|')'
op|'.'
name|'replace'
op|'('
string|"')'"
op|','
string|"'\\)'"
op|')'
newline|'\n'
name|'amount'
op|'='
op|'['
name|'nfl_filter_esc'
op|','
name|'limit'
op|']'
name|'if'
name|'nfl_filter_esc'
name|'else'
op|'['
name|'limit'
op|']'
newline|'\n'
name|'profile_html'
op|'='
name|'self'
op|'.'
name|'generate_stats_html'
op|'('
name|'stats'
op|','
name|'self'
op|'.'
name|'app_path'
op|','
nl|'\n'
name|'profile_id'
op|','
op|'*'
name|'amount'
op|')'
newline|'\n'
name|'description'
op|'='
string|'"Profiling information is generated by using\\\n                          \'%s\' profiler."'
op|'%'
name|'self'
op|'.'
name|'profile_module'
newline|'\n'
name|'sort_repl'
op|'='
string|'\'<option value="%s">\''
op|'%'
name|'sort'
newline|'\n'
name|'sort_selected'
op|'='
string|'\'<option value="%s" selected>\''
op|'%'
name|'sort'
newline|'\n'
name|'sort'
op|'='
name|'sort_tmpl'
op|'.'
name|'replace'
op|'('
name|'sort_repl'
op|','
name|'sort_selected'
op|')'
newline|'\n'
name|'plist'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
op|'['
string|'\'<option value="%s">%s</option>\''
op|'%'
op|'('
name|'p'
op|','
name|'p'
op|')'
nl|'\n'
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'profile_log'
op|'.'
name|'get_all_pids'
op|'('
op|')'
op|']'
op|')'
newline|'\n'
name|'profile_element'
op|'='
name|'string'
op|'.'
name|'Template'
op|'('
name|'profile_tmpl'
op|')'
op|'.'
name|'substitute'
op|'('
nl|'\n'
op|'{'
string|"'profile_list'"
op|':'
name|'plist'
op|'}'
op|')'
newline|'\n'
name|'profile_repl'
op|'='
string|'\'<option value="%s">\''
op|'%'
name|'profile_id'
newline|'\n'
name|'profile_selected'
op|'='
string|'\'<option value="%s" selected>\''
op|'%'
name|'profile_id'
newline|'\n'
name|'profile_element'
op|'='
name|'profile_element'
op|'.'
name|'replace'
op|'('
name|'profile_repl'
op|','
nl|'\n'
name|'profile_selected'
op|')'
newline|'\n'
name|'limit_repl'
op|'='
string|'\'<option value="%s">\''
op|'%'
name|'limit'
newline|'\n'
name|'limit_selected'
op|'='
string|'\'<option value="%s" selected>\''
op|'%'
name|'limit'
newline|'\n'
name|'limit'
op|'='
name|'limit_tmpl'
op|'.'
name|'replace'
op|'('
name|'limit_repl'
op|','
name|'limit_selected'
op|')'
newline|'\n'
name|'fulldirs_checked'
op|'='
string|"'checked'"
name|'if'
name|'fulldirs'
name|'else'
string|"''"
newline|'\n'
name|'fulldirs_element'
op|'='
name|'string'
op|'.'
name|'Template'
op|'('
name|'fulldirs_tmpl'
op|')'
op|'.'
name|'substitute'
op|'('
nl|'\n'
op|'{'
string|"'fulldir_checked'"
op|':'
name|'fulldirs_checked'
op|'}'
op|')'
newline|'\n'
name|'nfl_filter_element'
op|'='
name|'string'
op|'.'
name|'Template'
op|'('
name|'nfl_filter_tmpl'
op|')'
op|'.'
name|'substitute'
op|'('
op|'{'
string|"'nfl_filter'"
op|':'
name|'nfl_filter'
op|'}'
op|')'
newline|'\n'
name|'form_elements'
op|'='
name|'string'
op|'.'
name|'Template'
op|'('
name|'formelements_tmpl'
op|')'
op|'.'
name|'substitute'
op|'('
nl|'\n'
op|'{'
string|"'description'"
op|':'
name|'description'
op|','
nl|'\n'
string|"'action'"
op|':'
name|'url'
op|','
nl|'\n'
string|"'profile'"
op|':'
name|'profile_element'
op|','
nl|'\n'
string|"'sort'"
op|':'
name|'sort'
op|','
nl|'\n'
string|"'limit'"
op|':'
name|'limit'
op|','
nl|'\n'
string|"'fulldirs'"
op|':'
name|'fulldirs_element'
op|','
nl|'\n'
string|"'nfl_filter'"
op|':'
name|'nfl_filter_element'
op|','
nl|'\n'
op|'}'
nl|'\n'
op|')'
newline|'\n'
name|'content'
op|'='
name|'string'
op|'.'
name|'Template'
op|'('
name|'index_tmpl'
op|')'
op|'.'
name|'substitute'
op|'('
nl|'\n'
op|'{'
string|"'formelements'"
op|':'
name|'form_elements'
op|','
nl|'\n'
string|"'action'"
op|':'
name|'url'
op|','
nl|'\n'
string|"'description'"
op|':'
name|'description'
op|','
nl|'\n'
string|"'profilehtml'"
op|':'
name|'profile_html'
op|','
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'content'
op|','
name|'headers'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DataLoadFailure'
op|'('
name|'_'
op|'('
string|"'Can not load profile data from %s.'"
op|')'
nl|'\n'
op|'%'
name|'log_files'
op|')'
newline|'\n'
nl|'\n'
DECL|member|download
dedent|''
dedent|''
name|'def'
name|'download'
op|'('
name|'self'
op|','
name|'log_files'
op|','
name|'sort'
op|'='
string|"'time'"
op|','
name|'limit'
op|'='
op|'-'
number|'1'
op|','
name|'nfl_filter'
op|'='
string|"''"
op|','
nl|'\n'
name|'output_format'
op|'='
string|"'default'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'len'
op|'('
name|'log_files'
op|')'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'NotFoundException'
op|'('
name|'_'
op|'('
string|"'no log file found'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'nfl_esc'
op|'='
name|'nfl_filter'
op|'.'
name|'replace'
op|'('
string|"'('"
op|','
string|"'\\('"
op|')'
op|'.'
name|'replace'
op|'('
string|"')'"
op|','
string|"'\\)'"
op|')'
newline|'\n'
comment|'# remove the slash that is intentionally added in the URL'
nl|'\n'
comment|'# to avoid failure of filtering stats data.'
nl|'\n'
name|'if'
name|'nfl_esc'
op|'.'
name|'startswith'
op|'('
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'nfl_esc'
op|'='
name|'nfl_esc'
op|'['
number|'1'
op|':'
op|']'
newline|'\n'
dedent|''
name|'stats'
op|'='
name|'Stats2'
op|'('
op|'*'
name|'log_files'
op|')'
newline|'\n'
name|'stats'
op|'.'
name|'sort_stats'
op|'('
name|'sort'
op|')'
newline|'\n'
name|'if'
name|'output_format'
op|'=='
string|"'python'"
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'='
name|'self'
op|'.'
name|'format_source_code'
op|'('
name|'nfl_filter'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'output_format'
op|'=='
string|"'json'"
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'='
name|'stats'
op|'.'
name|'to_json'
op|'('
name|'nfl_esc'
op|','
name|'limit'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'output_format'
op|'=='
string|"'csv'"
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'='
name|'stats'
op|'.'
name|'to_csv'
op|'('
name|'nfl_esc'
op|','
name|'limit'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'output_format'
op|'=='
string|"'ods'"
op|':'
newline|'\n'
indent|'                '
name|'data'
op|'='
name|'stats'
op|'.'
name|'to_ods'
op|'('
name|'nfl_esc'
op|','
name|'limit'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'profile_tmp_all'
op|'='
name|'tempfile'
op|'.'
name|'mktemp'
op|'('
string|"'.profile'"
op|','
string|"'all'"
op|')'
newline|'\n'
name|'stats'
op|'.'
name|'dump_stats'
op|'('
name|'profile_tmp_all'
op|')'
newline|'\n'
name|'data'
op|'='
name|'open'
op|'('
name|'profile_tmp_all'
op|')'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'os'
op|'.'
name|'remove'
op|'('
name|'profile_tmp_all'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'data'
op|','
op|'['
op|'('
string|"'content-type'"
op|','
name|'self'
op|'.'
name|'format_dict'
op|'['
name|'output_format'
op|']'
op|')'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'ODFLIBNotInstalled'
name|'as'
name|'ex'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ex'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'ex'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ProfileException'
op|'('
name|'_'
op|'('
string|"'Data download error: %s'"
op|')'
op|'%'
name|'ex'
op|')'
newline|'\n'
nl|'\n'
DECL|member|plot
dedent|''
dedent|''
name|'def'
name|'plot'
op|'('
name|'self'
op|','
name|'log_files'
op|','
name|'sort'
op|'='
string|"'time'"
op|','
name|'limit'
op|'='
number|'10'
op|','
name|'nfl_filter'
op|'='
string|"''"
op|','
nl|'\n'
name|'metric_selected'
op|'='
string|"'cc'"
op|','
name|'plot_type'
op|'='
string|"'bar'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'PLOTLIB_INSTALLED'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'PLOTLIBNotInstalled'
op|'('
name|'_'
op|'('
string|"'python-matplotlib not installed.'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'log_files'
op|')'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'NotFoundException'
op|'('
name|'_'
op|'('
string|"'no log file found'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'stats'
op|'='
name|'Stats2'
op|'('
op|'*'
name|'log_files'
op|')'
newline|'\n'
name|'stats'
op|'.'
name|'sort_stats'
op|'('
name|'sort'
op|')'
newline|'\n'
name|'stats_dict'
op|'='
name|'stats'
op|'.'
name|'stats'
newline|'\n'
name|'__'
op|','
name|'func_list'
op|'='
name|'stats'
op|'.'
name|'get_print_list'
op|'('
op|'['
name|'nfl_filter'
op|','
name|'limit'
op|']'
op|')'
newline|'\n'
name|'nfls'
op|'='
op|'['
op|']'
newline|'\n'
name|'performance'
op|'='
op|'['
op|']'
newline|'\n'
name|'names'
op|'='
op|'{'
string|"'nc'"
op|':'
string|"'Total Call Count'"
op|','
string|"'cc'"
op|':'
string|"'Primitive Call Count'"
op|','
nl|'\n'
string|"'tt'"
op|':'
string|"'Total Time'"
op|','
string|"'ct'"
op|':'
string|"'Cumulative Time'"
op|'}'
newline|'\n'
name|'for'
name|'func'
name|'in'
name|'func_list'
op|':'
newline|'\n'
indent|'                '
name|'cc'
op|','
name|'nc'
op|','
name|'tt'
op|','
name|'ct'
op|','
name|'__'
op|'='
name|'stats_dict'
op|'['
name|'func'
op|']'
newline|'\n'
name|'metric'
op|'='
op|'{'
string|"'cc'"
op|':'
name|'cc'
op|','
string|"'nc'"
op|':'
name|'nc'
op|','
string|"'tt'"
op|':'
name|'tt'
op|','
string|"'ct'"
op|':'
name|'ct'
op|'}'
newline|'\n'
name|'nfls'
op|'.'
name|'append'
op|'('
name|'func'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
name|'performance'
op|'.'
name|'append'
op|'('
name|'metric'
op|'['
name|'metric_selected'
op|']'
op|')'
newline|'\n'
dedent|''
name|'y_pos'
op|'='
name|'range'
op|'('
name|'len'
op|'('
name|'nfls'
op|')'
op|')'
newline|'\n'
name|'error'
op|'='
op|'['
name|'random'
op|'.'
name|'random'
op|'('
op|')'
name|'for'
name|'__'
name|'in'
name|'y_pos'
op|']'
newline|'\n'
name|'plt'
op|'.'
name|'clf'
op|'('
op|')'
newline|'\n'
name|'if'
name|'plot_type'
op|'=='
string|"'pie'"
op|':'
newline|'\n'
indent|'                '
name|'plt'
op|'.'
name|'pie'
op|'('
name|'x'
op|'='
name|'performance'
op|','
name|'explode'
op|'='
name|'None'
op|','
name|'labels'
op|'='
name|'nfls'
op|','
nl|'\n'
name|'autopct'
op|'='
string|"'%1.1f%%'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'plt'
op|'.'
name|'barh'
op|'('
name|'y_pos'
op|','
name|'performance'
op|','
name|'xerr'
op|'='
name|'error'
op|','
name|'align'
op|'='
string|"'center'"
op|','
nl|'\n'
name|'alpha'
op|'='
number|'0.4'
op|')'
newline|'\n'
name|'plt'
op|'.'
name|'yticks'
op|'('
name|'y_pos'
op|','
name|'nfls'
op|')'
newline|'\n'
name|'plt'
op|'.'
name|'xlabel'
op|'('
name|'names'
op|'['
name|'metric_selected'
op|']'
op|')'
newline|'\n'
dedent|''
name|'plt'
op|'.'
name|'title'
op|'('
string|"'Profile Statistics (by %s)'"
op|'%'
name|'names'
op|'['
name|'metric_selected'
op|']'
op|')'
newline|'\n'
comment|'#plt.gcf().tight_layout(pad=1.2)'
nl|'\n'
name|'profile_img'
op|'='
name|'tempfile'
op|'.'
name|'mktemp'
op|'('
string|"'.png'"
op|','
string|"'plot'"
op|')'
newline|'\n'
name|'plt'
op|'.'
name|'savefig'
op|'('
name|'profile_img'
op|','
name|'dpi'
op|'='
number|'300'
op|')'
newline|'\n'
name|'data'
op|'='
name|'open'
op|'('
name|'profile_img'
op|')'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'os'
op|'.'
name|'remove'
op|'('
name|'profile_img'
op|')'
newline|'\n'
name|'return'
name|'data'
op|','
op|'['
op|'('
string|"'content-type'"
op|','
string|"'image/jpg'"
op|')'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'ex'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ProfileException'
op|'('
name|'_'
op|'('
string|"'plotting results failed due to %s'"
op|')'
op|'%'
name|'ex'
op|')'
newline|'\n'
nl|'\n'
DECL|member|format_source_code
dedent|''
dedent|''
name|'def'
name|'format_source_code'
op|'('
name|'self'
op|','
name|'nfl'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'nfls'
op|'='
name|'re'
op|'.'
name|'split'
op|'('
string|"'[:()]'"
op|','
name|'nfl'
op|')'
newline|'\n'
name|'file_path'
op|'='
name|'nfls'
op|'['
number|'0'
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'lineno'
op|'='
name|'int'
op|'('
name|'nfls'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'lineno'
op|'='
number|'0'
newline|'\n'
comment|'# for security reason, this need to be fixed.'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'file_path'
op|'.'
name|'endswith'
op|'('
string|"'.py'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'_'
op|'('
string|"'The file type are forbidden to access!'"
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'data'
op|'='
op|'['
op|']'
newline|'\n'
name|'i'
op|'='
number|'0'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'file_path'
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'                '
name|'lines'
op|'='
name|'f'
op|'.'
name|'readlines'
op|'('
op|')'
newline|'\n'
name|'max_width'
op|'='
name|'str'
op|'('
name|'len'
op|'('
name|'str'
op|'('
name|'len'
op|'('
name|'lines'
op|')'
op|')'
op|')'
op|')'
newline|'\n'
name|'fmt'
op|'='
string|'\'<span id="L%d" rel="#L%d">%\''
op|'+'
name|'max_width'
op|'+'
string|"'d|<code>%s</code></span>'"
newline|'\n'
name|'for'
name|'line'
name|'in'
name|'lines'
op|':'
newline|'\n'
indent|'                    '
name|'l'
op|'='
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'line'
op|','
name|'quote'
op|'='
name|'None'
op|')'
newline|'\n'
name|'i'
op|'='
name|'i'
op|'+'
number|'1'
newline|'\n'
name|'if'
name|'i'
op|'=='
name|'lineno'
op|':'
newline|'\n'
indent|'                        '
name|'fmt2'
op|'='
string|'\'<span id="L%d" style="background-color: \\\n                            rgb(127,255,127)">%\''
op|'+'
name|'max_width'
op|'+'
string|"'d|<code>%s</code></span>'"
newline|'\n'
name|'data'
op|'.'
name|'append'
op|'('
name|'fmt2'
op|'%'
op|'('
name|'i'
op|','
name|'i'
op|','
name|'l'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'data'
op|'.'
name|'append'
op|'('
name|'fmt'
op|'%'
op|'('
name|'i'
op|','
name|'i'
op|','
name|'i'
op|','
name|'l'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'data'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'data'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'_'
op|'('
string|"'Can not access the file %s.'"
op|')'
op|'%'
name|'file_path'
newline|'\n'
dedent|''
name|'return'
string|"'<pre>%s</pre>'"
op|'%'
name|'data'
newline|'\n'
nl|'\n'
DECL|member|generate_stats_html
dedent|''
name|'def'
name|'generate_stats_html'
op|'('
name|'self'
op|','
name|'stats'
op|','
name|'app_path'
op|','
name|'profile_id'
op|','
op|'*'
name|'selection'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'html'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'filename'
name|'in'
name|'stats'
op|'.'
name|'files'
op|':'
newline|'\n'
indent|'            '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<p>%s</p>'"
op|'%'
name|'filename'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'func'
name|'in'
name|'stats'
op|'.'
name|'top_level'
op|':'
newline|'\n'
indent|'                '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<p>%s</p>'"
op|'%'
name|'func'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
dedent|''
name|'html'
op|'.'
name|'append'
op|'('
string|"'%s function calls'"
op|'%'
name|'stats'
op|'.'
name|'total_calls'
op|')'
newline|'\n'
name|'if'
name|'stats'
op|'.'
name|'total_calls'
op|'!='
name|'stats'
op|'.'
name|'prim_calls'
op|':'
newline|'\n'
indent|'                '
name|'html'
op|'.'
name|'append'
op|'('
string|'"(%d primitive calls)"'
op|'%'
name|'stats'
op|'.'
name|'prim_calls'
op|')'
newline|'\n'
dedent|''
name|'html'
op|'.'
name|'append'
op|'('
string|"'in %.3f seconds'"
op|'%'
name|'stats'
op|'.'
name|'total_tt'
op|')'
newline|'\n'
name|'if'
name|'stats'
op|'.'
name|'fcn_list'
op|':'
newline|'\n'
indent|'                '
name|'stat_list'
op|'='
name|'stats'
op|'.'
name|'fcn_list'
op|'['
op|':'
op|']'
newline|'\n'
name|'msg'
op|'='
string|'"<p>Ordered by: %s</p>"'
op|'%'
name|'stats'
op|'.'
name|'sort_type'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'stat_list'
op|'='
name|'stats'
op|'.'
name|'stats'
op|'.'
name|'keys'
op|'('
op|')'
newline|'\n'
name|'msg'
op|'='
string|"'<p>Random listing order was used</p>'"
newline|'\n'
dedent|''
name|'for'
name|'sel'
name|'in'
name|'selection'
op|':'
newline|'\n'
indent|'                '
name|'stat_list'
op|','
name|'msg'
op|'='
name|'stats'
op|'.'
name|'eval_print_amount'
op|'('
name|'sel'
op|','
name|'stat_list'
op|','
name|'msg'
op|')'
newline|'\n'
dedent|''
name|'html'
op|'.'
name|'append'
op|'('
name|'msg'
op|')'
newline|'\n'
name|'html'
op|'.'
name|'append'
op|'('
string|'\'<table style="border-width: 1px">\''
op|')'
newline|'\n'
name|'if'
name|'stat_list'
op|':'
newline|'\n'
indent|'                '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<tr><th>#</th><th>Call Count</th>\\\n                                    <th>Total Time</th><th>Time/Call</th>\\\n                                    <th>Cumulative Time</th>\\\n                                    <th>Cumulative Time/Call</th>\\\n                                    <th>Filename:Lineno(Function)</th>\\\n                                    <th>JSON</th>\\\n                                </tr>'"
op|')'
newline|'\n'
name|'count'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'func'
name|'in'
name|'stat_list'
op|':'
newline|'\n'
indent|'                    '
name|'count'
op|'='
name|'count'
op|'+'
number|'1'
newline|'\n'
name|'html'
op|'.'
name|'append'
op|'('
string|'\'<tr onMouseOver="this.className=\\\'hover\\\'"\\\n                                     onMouseOut="this.className=\\\'normal\\\'">\\\n                                     <td>%d)</td>\''
op|'%'
name|'count'
op|')'
newline|'\n'
name|'cc'
op|','
name|'nc'
op|','
name|'tt'
op|','
name|'ct'
op|','
name|'__'
op|'='
name|'stats'
op|'.'
name|'stats'
op|'['
name|'func'
op|']'
newline|'\n'
name|'c'
op|'='
name|'str'
op|'('
name|'nc'
op|')'
newline|'\n'
name|'if'
name|'nc'
op|'!='
name|'cc'
op|':'
newline|'\n'
indent|'                        '
name|'c'
op|'='
name|'c'
op|'+'
string|"'/'"
op|'+'
name|'str'
op|'('
name|'cc'
op|')'
newline|'\n'
dedent|''
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>%s</td>'"
op|'%'
name|'c'
op|')'
newline|'\n'
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>%f</td>'"
op|'%'
name|'tt'
op|')'
newline|'\n'
name|'if'
name|'nc'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>-</td>'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>%f</td>'"
op|'%'
op|'('
name|'float'
op|'('
name|'tt'
op|')'
op|'/'
name|'nc'
op|')'
op|')'
newline|'\n'
dedent|''
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>%f</td>'"
op|'%'
name|'ct'
op|')'
newline|'\n'
name|'if'
name|'cc'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>-</td>'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>%f</td>'"
op|'%'
op|'('
name|'float'
op|'('
name|'ct'
op|')'
op|'/'
name|'cc'
op|')'
op|')'
newline|'\n'
dedent|''
name|'nfls'
op|'='
name|'cgi'
op|'.'
name|'escape'
op|'('
name|'stats'
op|'.'
name|'func_std_string'
op|'('
name|'func'
op|')'
op|')'
newline|'\n'
name|'if'
name|'nfls'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'0'
op|']'
name|'not'
name|'in'
op|'['
string|"''"
op|','
string|"'profile'"
op|']'
name|'and'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isfile'
op|'('
name|'nfls'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'0'
op|']'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'html'
op|'.'
name|'append'
op|'('
string|'\'<td><a href="%s/%s%s?format=python#L%d">\\\n                                     %s</a></td>\''
op|'%'
op|'('
name|'app_path'
op|','
name|'profile_id'
op|','
nl|'\n'
name|'nfls'
op|','
name|'func'
op|'['
number|'1'
op|']'
op|','
name|'nfls'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'html'
op|'.'
name|'append'
op|'('
string|"'<td>%s</td>'"
op|'%'
name|'nfls'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'nfls'
op|'.'
name|'startswith'
op|'('
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'nfls'
op|'='
string|"'/'"
op|'+'
name|'nfls'
newline|'\n'
dedent|''
name|'html'
op|'.'
name|'append'
op|'('
string|'\'<td><a href="%s/%s%s?format=json">\\\n                                --></a></td></tr>\''
op|'%'
op|'('
name|'app_path'
op|','
nl|'\n'
name|'profile_id'
op|','
name|'nfls'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'ex'
op|':'
newline|'\n'
indent|'            '
name|'html'
op|'.'
name|'append'
op|'('
string|'"Exception:"'
op|'%'
name|'ex'
op|'.'
name|'message'
op|')'
newline|'\n'
dedent|''
name|'return'
string|"''"
op|'.'
name|'join'
op|'('
name|'html'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit