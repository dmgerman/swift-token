begin_unit
comment|'# Copyright (c) 2012 OpenStack, LLC.'
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
string|'\'\'\'\nCreated on February 27, 2012\n\nA filter that disallows any paths that contain defined forbidden characters\nor that exceed a defined length.\n\nPlace in proxy filter before proxy, e.g.\n\n[pipeline:main]\npipeline = catch_errors healthcheck name_check cache tempauth sos proxy-server\n\n[filter:name_check]\nuse = egg:swift#name_check\nforbidden_chars = \'"`<>\nmaximum_length = 255\n\nThere are default settings for forbidden_chars (FORBIDDEN_CHARS) and\nmaximum_length (MAX_LENGTH)\n\nThe filter returns HTTPBadRequest if path is invalid.\n\n@author: eamonn-otoole\n\'\'\''
newline|'\n'
nl|'\n'
name|'import'
name|'re'
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
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPBadRequest'
newline|'\n'
name|'from'
name|'urllib2'
name|'import'
name|'unquote'
newline|'\n'
nl|'\n'
DECL|variable|FORBIDDEN_CHARS
name|'FORBIDDEN_CHARS'
op|'='
string|'"\\\'\\"`<>"'
newline|'\n'
DECL|variable|MAX_LENGTH
name|'MAX_LENGTH'
op|'='
number|'255'
newline|'\n'
DECL|variable|FORBIDDEN_REGEXP
name|'FORBIDDEN_REGEXP'
op|'='
string|'"/\\./|/\\.\\./|/\\.$|/\\.\\.$"'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|NameCheckMiddleware
name|'class'
name|'NameCheckMiddleware'
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
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'forbidden_chars'
op|'='
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'forbidden_chars'"
op|','
nl|'\n'
name|'FORBIDDEN_CHARS'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'maximum_length'
op|'='
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'maximum_length'"
op|','
name|'MAX_LENGTH'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'forbidden_regexp'
op|'='
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'forbidden_regexp'"
op|','
nl|'\n'
name|'FORBIDDEN_REGEXP'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'forbidden_regexp'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'forbidden_regexp_compiled'
op|'='
name|'re'
op|'.'
name|'compile'
op|'('
name|'self'
op|'.'
name|'forbidden_regexp'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'forbidden_regexp_compiled'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'log_route'
op|'='
string|"'name_check'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|check_character
dedent|''
name|'def'
name|'check_character'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Checks req.path for any forbidden characters\n        Returns True if there are any forbidden characters\n        Returns False if there aren't any forbidden characters\n        '''"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|'"name_check: path %s"'
op|'%'
name|'req'
op|'.'
name|'path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|'"name_check: self.forbidden_chars %s"'
op|'%'
nl|'\n'
name|'self'
op|'.'
name|'forbidden_chars'
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'c'
name|'in'
name|'unquote'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'c'
name|'in'
name|'self'
op|'.'
name|'forbidden_chars'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'False'
newline|'\n'
nl|'\n'
DECL|member|check_length
dedent|''
name|'def'
name|'check_length'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Checks that req.path doesn't exceed the defined maximum length\n        Returns True if the length exceeds the maximum\n        Returns False if the length is <= the maximum\n        '''"
newline|'\n'
name|'length'
op|'='
name|'len'
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
name|'length'
op|'>'
name|'self'
op|'.'
name|'maximum_length'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
DECL|member|check_regexp
dedent|''
dedent|''
name|'def'
name|'check_regexp'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Checks that req.path doesn't contain a substring matching regexps.\n        Returns True if there are any forbidden substring\n        Returns False if there aren't any forbidden substring\n        '''"
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'forbidden_regexp_compiled'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|'"name_check: path %s"'
op|'%'
name|'req'
op|'.'
name|'path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|'"name_check: self.forbidden_regexp %s"'
op|'%'
nl|'\n'
name|'self'
op|'.'
name|'forbidden_regexp'
op|')'
newline|'\n'
nl|'\n'
name|'unquoted_path'
op|'='
name|'unquote'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
newline|'\n'
name|'match'
op|'='
name|'self'
op|'.'
name|'forbidden_regexp_compiled'
op|'.'
name|'search'
op|'('
name|'unquoted_path'
op|')'
newline|'\n'
name|'return'
op|'('
name|'match'
name|'is'
name|'not'
name|'None'
op|')'
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
nl|'\n'
name|'if'
name|'self'
op|'.'
name|'check_character'
op|'('
name|'req'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
op|'('
string|'"Object/Container name contains forbidden chars from %s"'
nl|'\n'
op|'%'
name|'self'
op|'.'
name|'forbidden_chars'
op|')'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'check_length'
op|'('
name|'req'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
op|'('
string|'"Object/Container name longer than the allowed maximum %s"'
nl|'\n'
op|'%'
name|'self'
op|'.'
name|'maximum_length'
op|')'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'check_regexp'
op|'('
name|'req'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
op|'('
string|'"Object/Container name contains a forbidden substring "'
nl|'\n'
string|'"from regular expression %s"'
nl|'\n'
op|'%'
name|'self'
op|'.'
name|'forbidden_regexp'
op|')'
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
comment|'# Pass on to downstream WSGI component'
nl|'\n'
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
DECL|function|name_check_filter
name|'def'
name|'name_check_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'NameCheckMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'name_check_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
