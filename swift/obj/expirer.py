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
name|'from'
name|'random'
name|'import'
name|'random'
newline|'\n'
name|'from'
name|'sys'
name|'import'
name|'exc_info'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'sleep'
op|','
name|'TimeoutError'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'loadapp'
newline|'\n'
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
name|'daemon'
name|'import'
name|'Daemon'
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
name|'try'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'simplejson'
name|'as'
name|'json'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'json'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ObjectExpirer
dedent|''
name|'class'
name|'ObjectExpirer'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Daemon that queries the internal hidden expiring_objects_account to\n    discover objects that need to be deleted.\n\n    :param conf: The daemon configuration.\n    """'
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
name|'conf'
op|'='
name|'conf'
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
string|"'object-expirer'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'interval'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'interval'"
op|')'
name|'or'
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'expiring_objects_account'
op|'='
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'auto_create_account_prefix'"
op|')'
name|'or'
string|"'.'"
op|')'
op|'+'
string|"'expiring_objects'"
newline|'\n'
name|'self'
op|'.'
name|'retries'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'retries'"
op|')'
name|'or'
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'loadapp'
op|'('
string|"'config:'"
op|'+'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'__file__'"
op|')'
name|'or'
nl|'\n'
string|"'/etc/swift/object-expirer.conf'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report_interval'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'report_interval'"
op|')'
name|'or'
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report_first_time'
op|'='
name|'self'
op|'.'
name|'report_last_time'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report_objects'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|report
dedent|''
name|'def'
name|'report'
op|'('
name|'self'
op|','
name|'final'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Emits a log line report of the progress so far, or the final progress\n        is final=True.\n\n        :param final: Set to True for the last report once the expiration pass\n                      has completed.\n        """'
newline|'\n'
name|'if'
name|'final'
op|':'
newline|'\n'
indent|'            '
name|'elapsed'
op|'='
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'report_first_time'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Pass completed in %ds; %d objects expired'"
op|')'
op|'%'
nl|'\n'
op|'('
name|'elapsed'
op|','
name|'self'
op|'.'
name|'report_objects'
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'report_last_time'
op|'>='
name|'self'
op|'.'
name|'report_interval'
op|':'
newline|'\n'
indent|'            '
name|'elapsed'
op|'='
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'report_first_time'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Pass so far %ds; %d objects expired'"
op|')'
op|'%'
nl|'\n'
op|'('
name|'elapsed'
op|','
name|'self'
op|'.'
name|'report_objects'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report_last_time'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
dedent|''
name|'def'
name|'run_once'
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
string|'"""\n        Executes a single pass, looking for objects to expire.\n\n        :param args: Extra args to fulfill the Daemon interface; this daemon\n                     has no additional args.\n        :param kwargs: Extra keyword args to fulfill the Daemon interface; this\n                       daemon has no additional keyword args.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'report_first_time'
op|'='
name|'self'
op|'.'
name|'report_last_time'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report_objects'
op|'='
number|'0'
newline|'\n'
name|'try'
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
string|"'Run begin'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Pass beginning; %s possible containers; %s '"
nl|'\n'
string|"'possible objects'"
op|')'
op|'%'
name|'self'
op|'.'
name|'get_account_info'
op|'('
op|')'
op|')'
newline|'\n'
name|'for'
name|'container'
name|'in'
name|'self'
op|'.'
name|'iter_containers'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'timestamp'
op|'='
name|'int'
op|'('
name|'container'
op|')'
newline|'\n'
name|'if'
name|'timestamp'
op|'>'
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'for'
name|'obj'
name|'in'
name|'self'
op|'.'
name|'iter_objects'
op|'('
name|'container'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'timestamp'
op|','
name|'actual_obj'
op|'='
name|'obj'
op|'.'
name|'split'
op|'('
string|"'-'"
op|','
number|'1'
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'int'
op|'('
name|'timestamp'
op|')'
newline|'\n'
name|'if'
name|'timestamp'
op|'>'
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'break'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'delete_actual_object'
op|'('
name|'actual_obj'
op|','
name|'timestamp'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'delete_object'
op|'('
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report_objects'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'TimeoutError'
op|')'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception while deleting object %s %s %s'"
op|')'
op|'%'
nl|'\n'
op|'('
name|'container'
op|','
name|'obj'
op|','
name|'str'
op|'('
name|'err'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'delete_container'
op|'('
name|'container'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'TimeoutError'
op|')'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception while deleting container %s %s'"
op|')'
op|'%'
nl|'\n'
op|'('
name|'container'
op|','
name|'str'
op|'('
name|'err'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Run end'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report'
op|'('
name|'final'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'TimeoutError'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'Unhandled exception'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
dedent|''
name|'def'
name|'run_forever'
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
string|'"""\n        Executes passes forever, looking for objects to expire.\n\n        :param args: Extra args to fulfill the Daemon interface; this daemon\n                     has no additional args.\n        :param kwargs: Extra keyword args to fulfill the Daemon interface; this\n                       daemon has no additional keyword args.\n        """'
newline|'\n'
name|'sleep'
op|'('
name|'random'
op|'('
op|')'
op|'*'
name|'self'
op|'.'
name|'interval'
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'begin'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'TimeoutError'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'Unhandled exception'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'elapsed'
op|'='
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
newline|'\n'
name|'if'
name|'elapsed'
op|'<'
name|'self'
op|'.'
name|'interval'
op|':'
newline|'\n'
indent|'                '
name|'sleep'
op|'('
name|'random'
op|'('
op|')'
op|'*'
op|'('
name|'self'
op|'.'
name|'interval'
op|'-'
name|'elapsed'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_response
dedent|''
dedent|''
dedent|''
name|'def'
name|'get_response'
op|'('
name|'self'
op|','
name|'method'
op|','
name|'path'
op|','
name|'headers'
op|','
name|'acceptable_statuses'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'['
string|"'user-agent'"
op|']'
op|'='
string|"'Swift Object Expirer'"
newline|'\n'
name|'resp'
op|'='
name|'exc_type'
op|'='
name|'exc_value'
op|'='
name|'exc_traceback'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'attempt'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'retries'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
name|'method'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'req'
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
name|'in'
name|'acceptable_statuses'
name|'or'
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
name|'in'
name|'acceptable_statuses'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'resp'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'TimeoutError'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'exc_type'
op|','
name|'exc_value'
op|','
name|'exc_traceback'
op|'='
name|'exc_info'
op|'('
op|')'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'2'
op|'**'
op|'('
name|'attempt'
op|'+'
number|'1'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'resp'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
name|'_'
op|'('
string|"'Unexpected response %s'"
op|')'
op|'%'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'exc_type'
op|':'
newline|'\n'
comment|'# To make pep8 tool happy, in place of raise t, v, tb:'
nl|'\n'
indent|'            '
name|'raise'
name|'exc_type'
op|'('
op|'*'
name|'exc_value'
op|'.'
name|'args'
op|')'
op|','
name|'None'
op|','
name|'exc_traceback'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
dedent|''
name|'def'
name|'get_account_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns (container_count, object_count) tuple indicating the values for\n        the hidden expiration account.\n        """'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'get_response'
op|'('
string|"'HEAD'"
op|','
nl|'\n'
string|"'/v1/'"
op|'+'
name|'quote'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|')'
op|','
op|'{'
op|'}'
op|','
op|'('
number|'2'
op|','
number|'404'
op|')'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'('
number|'0'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'return'
op|'('
name|'int'
op|'('
name|'resp'
op|'.'
name|'headers'
op|'['
string|"'x-account-container-count'"
op|']'
op|')'
op|','
nl|'\n'
name|'int'
op|'('
name|'resp'
op|'.'
name|'headers'
op|'['
string|"'x-account-object-count'"
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|iter_containers
dedent|''
name|'def'
name|'iter_containers'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns an iterator of container names of the hidden expiration account\n        listing.\n        """'
newline|'\n'
name|'path'
op|'='
string|"'/v1/%s?format=json'"
op|'%'
op|'('
name|'quote'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|')'
op|','
op|')'
newline|'\n'
name|'marker'
op|'='
string|"''"
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'self'
op|'.'
name|'get_response'
op|'('
string|"'GET'"
op|','
name|'path'
op|'+'
string|"'&marker='"
op|'+'
name|'quote'
op|'('
name|'marker'
op|')'
op|','
nl|'\n'
op|'{'
op|'}'
op|','
op|'('
number|'2'
op|','
number|'404'
op|')'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
name|'in'
op|'('
number|'204'
op|','
number|'404'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'data'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'for'
name|'item'
name|'in'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'item'
op|'['
string|"'name'"
op|']'
newline|'\n'
dedent|''
name|'marker'
op|'='
name|'data'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'name'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|iter_objects
dedent|''
dedent|''
name|'def'
name|'iter_objects'
op|'('
name|'self'
op|','
name|'container'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns an iterator of object names of the hidden expiration account\'s\n        container listing for the container name given.\n\n        :param container: The name of the container to list.\n        """'
newline|'\n'
name|'path'
op|'='
string|"'/v1/%s/%s?format=json'"
op|'%'
op|'('
name|'quote'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|')'
op|','
name|'quote'
op|'('
name|'container'
op|')'
op|')'
newline|'\n'
name|'marker'
op|'='
string|"''"
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'self'
op|'.'
name|'get_response'
op|'('
string|"'GET'"
op|','
name|'path'
op|'+'
string|"'&'"
op|'+'
name|'quote'
op|'('
name|'marker'
op|')'
op|','
nl|'\n'
op|'{'
op|'}'
op|','
op|'('
number|'2'
op|','
number|'404'
op|')'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
name|'in'
op|'('
number|'204'
op|','
number|'404'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'data'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'for'
name|'item'
name|'in'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'item'
op|'['
string|"'name'"
op|']'
newline|'\n'
dedent|''
name|'marker'
op|'='
name|'data'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'name'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|delete_actual_object
dedent|''
dedent|''
name|'def'
name|'delete_actual_object'
op|'('
name|'self'
op|','
name|'actual_obj'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Deletes the end-user object indicated by the actual object name given\n        \'<account>/<container>/<object>\' if and only if the X-Delete-At value\n        of the object is exactly the timestamp given.\n\n        :param actual_obj: The name of the end-user object to delete:\n                           \'<account>/<container>/<object>\'\n        :param timestamp: The timestamp the X-Delete-At value must match to\n                          perform the actual delete.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'get_response'
op|'('
string|"'DELETE'"
op|','
string|"'/v1/%s'"
op|'%'
op|'('
name|'quote'
op|'('
name|'actual_obj'
op|')'
op|','
op|')'
op|','
nl|'\n'
op|'{'
string|"'X-If-Delete-At'"
op|':'
name|'str'
op|'('
name|'timestamp'
op|')'
op|'}'
op|','
op|'('
number|'2'
op|','
number|'404'
op|','
number|'412'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete_object
dedent|''
name|'def'
name|'delete_object'
op|'('
name|'self'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Deletes an object from the hidden expiring object account.\n\n        :param container: The name of the container for the object.\n        :param obj: The name of the object to delete.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'get_response'
op|'('
string|"'DELETE'"
op|','
nl|'\n'
string|"'/v1/%s/%s/%s'"
op|'%'
op|'('
name|'quote'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|')'
op|','
nl|'\n'
name|'quote'
op|'('
name|'container'
op|')'
op|','
name|'quote'
op|'('
name|'obj'
op|')'
op|')'
op|','
nl|'\n'
op|'{'
op|'}'
op|','
op|'('
number|'2'
op|','
number|'404'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete_container
dedent|''
name|'def'
name|'delete_container'
op|'('
name|'self'
op|','
name|'container'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Deletes a container from the hidden expiring object account.\n\n        :param container: The name of the container to delete.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'get_response'
op|'('
string|"'DELETE'"
op|','
nl|'\n'
string|"'/v1/%s/%s'"
op|'%'
op|'('
name|'quote'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|')'
op|','
nl|'\n'
name|'quote'
op|'('
name|'container'
op|')'
op|')'
op|','
nl|'\n'
op|'{'
op|'}'
op|','
op|'('
number|'2'
op|','
number|'404'
op|','
number|'409'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
