begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack Foundation'
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
name|'urllib'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'random'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'join'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'sleep'
op|','
name|'Timeout'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'greenpool'
name|'import'
name|'GreenPool'
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
name|'internal_client'
name|'import'
name|'InternalClient'
op|','
name|'UnexpectedResponse'
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
name|'dump_recon_cache'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_NOT_FOUND'
op|','
name|'HTTP_CONFLICT'
op|','
name|'HTTP_PRECONDITION_FAILED'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'reconciler'
name|'import'
name|'direct_delete_container_entry'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ObjectExpirer
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
op|','
name|'logger'
op|'='
name|'None'
op|','
name|'swift'
op|'='
name|'None'
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
name|'logger'
name|'or'
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
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'expiring_objects_account_name'"
op|')'
name|'or'
string|"'expiring_objects'"
op|')'
newline|'\n'
name|'conf_path'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'__file__'"
op|')'
name|'or'
string|"'/etc/swift/object-expirer.conf'"
newline|'\n'
name|'request_tries'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'request_tries'"
op|')'
name|'or'
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'swift'
op|'='
name|'swift'
name|'or'
name|'InternalClient'
op|'('
nl|'\n'
name|'conf_path'
op|','
string|"'Swift Object Expirer'"
op|','
name|'request_tries'
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
name|'self'
op|'.'
name|'recon_cache_path'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'recon_cache_path'"
op|','
nl|'\n'
string|"'/var/cache/swift'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'rcache'
op|'='
name|'join'
op|'('
name|'self'
op|'.'
name|'recon_cache_path'
op|','
string|"'object.recon'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'concurrency'"
op|','
number|'1'
op|')'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'concurrency'
op|'<'
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|'"concurrency must be set to at least 1"'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'processes'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'processes'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'process'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'process'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reclaim_age'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'reclaim_age'"
op|','
number|'86400'
op|'*'
number|'7'
op|')'
op|')'
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
name|'dump_recon_cache'
op|'('
op|'{'
string|"'object_expiration_pass'"
op|':'
name|'elapsed'
op|','
nl|'\n'
string|"'expired_last_pass'"
op|':'
name|'self'
op|'.'
name|'report_objects'
op|'}'
op|','
nl|'\n'
name|'self'
op|'.'
name|'rcache'
op|','
name|'self'
op|'.'
name|'logger'
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
string|'"""\n        Executes a single pass, looking for objects to expire.\n\n        :param args: Extra args to fulfill the Daemon interface; this daemon\n                     has no additional args.\n        :param kwargs: Extra keyword args to fulfill the Daemon interface; this\n                       daemon accepts processes and process keyword args.\n                       These will override the values from the config file if\n                       provided.\n        """'
newline|'\n'
name|'processes'
op|','
name|'process'
op|'='
name|'self'
op|'.'
name|'get_process_values'
op|'('
name|'kwargs'
op|')'
newline|'\n'
name|'pool'
op|'='
name|'GreenPool'
op|'('
name|'self'
op|'.'
name|'concurrency'
op|')'
newline|'\n'
name|'containers_to_delete'
op|'='
op|'['
op|']'
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
string|"'Run begin'"
op|')'
newline|'\n'
name|'containers'
op|','
name|'objects'
op|'='
name|'self'
op|'.'
name|'swift'
op|'.'
name|'get_account_info'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
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
op|'('
name|'containers'
op|','
name|'objects'
op|')'
op|')'
newline|'\n'
name|'for'
name|'c'
name|'in'
name|'self'
op|'.'
name|'swift'
op|'.'
name|'iter_containers'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'container'
op|'='
name|'c'
op|'['
string|"'name'"
op|']'
newline|'\n'
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
name|'containers_to_delete'
op|'.'
name|'append'
op|'('
name|'container'
op|')'
newline|'\n'
name|'for'
name|'o'
name|'in'
name|'self'
op|'.'
name|'swift'
op|'.'
name|'iter_objects'
op|'('
name|'self'
op|'.'
name|'expiring_objects_account'
op|','
nl|'\n'
name|'container'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'obj'
op|'='
name|'o'
op|'['
string|"'name'"
op|']'
op|'.'
name|'encode'
op|'('
string|"'utf8'"
op|')'
newline|'\n'
name|'if'
name|'processes'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'obj_process'
op|'='
name|'int'
op|'('
nl|'\n'
name|'hashlib'
op|'.'
name|'md5'
op|'('
string|"'%s/%s'"
op|'%'
op|'('
name|'container'
op|','
name|'obj'
op|')'
op|')'
op|'.'
nl|'\n'
name|'hexdigest'
op|'('
op|')'
op|','
number|'16'
op|')'
newline|'\n'
name|'if'
name|'obj_process'
op|'%'
name|'processes'
op|'!='
name|'process'
op|':'
newline|'\n'
indent|'                            '
name|'continue'
newline|'\n'
dedent|''
dedent|''
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
name|'pool'
op|'.'
name|'spawn_n'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'delete_object'
op|','
name|'actual_obj'
op|','
name|'timestamp'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
name|'for'
name|'container'
name|'in'
name|'containers_to_delete'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'swift'
op|'.'
name|'delete_container'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'expiring_objects_account'
op|','
nl|'\n'
name|'container'
op|','
nl|'\n'
name|'acceptable_statuses'
op|'='
op|'('
number|'2'
op|','
name|'HTTP_NOT_FOUND'
op|','
name|'HTTP_CONFLICT'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
name|'as'
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
string|"'Run end'"
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
name|'Timeout'
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
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
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
DECL|member|get_process_values
dedent|''
dedent|''
dedent|''
name|'def'
name|'get_process_values'
op|'('
name|'self'
op|','
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Gets the processes, process from the kwargs if those values exist.\n\n        Otherwise, return processes, process set in the config file.\n\n        :param kwargs: Keyword args passed into the run_forever(), run_once()\n                       methods.  They have values specified on the command\n                       line when the daemon is run.\n        """'
newline|'\n'
name|'if'
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'processes'"
op|')'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'processes'
op|'='
name|'int'
op|'('
name|'kwargs'
op|'['
string|"'processes'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'processes'
op|'='
name|'self'
op|'.'
name|'processes'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'process'"
op|')'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'process'
op|'='
name|'int'
op|'('
name|'kwargs'
op|'['
string|"'process'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'process'
op|'='
name|'self'
op|'.'
name|'process'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'process'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'process must be an integer greater than or equal to 0'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'processes'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'processes must be an integer greater than or equal to 0'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'processes'
name|'and'
name|'process'
op|'>='
name|'processes'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'process must be less than or equal to processes'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'processes'
op|','
name|'process'
newline|'\n'
nl|'\n'
DECL|member|delete_object
dedent|''
name|'def'
name|'delete_object'
op|'('
name|'self'
op|','
name|'actual_obj'
op|','
name|'timestamp'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'start_time'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'delete_actual_object'
op|'('
name|'actual_obj'
op|','
name|'timestamp'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'UnexpectedResponse'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'err'
op|'.'
name|'resp'
op|'.'
name|'status_int'
op|'!='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
newline|'\n'
dedent|''
name|'if'
name|'float'
op|'('
name|'timestamp'
op|')'
op|'>'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'reclaim_age'
op|':'
newline|'\n'
comment|"# we'll have to retry the DELETE later"
nl|'\n'
indent|'                    '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'pop_queue'
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
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'objects'"
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
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
name|'logger'
op|'.'
name|'timing_since'
op|'('
string|"'timing'"
op|','
name|'start_time'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|pop_queue
dedent|''
name|'def'
name|'pop_queue'
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
string|'"""\n        Issue a delete object request to the container for the expiring object\n        queue entry.\n        """'
newline|'\n'
name|'direct_delete_container_entry'
op|'('
name|'self'
op|'.'
name|'swift'
op|'.'
name|'container_ring'
op|','
nl|'\n'
name|'self'
op|'.'
name|'expiring_objects_account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete_actual_object
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
name|'path'
op|'='
string|"'/v1/'"
op|'+'
name|'urllib'
op|'.'
name|'quote'
op|'('
name|'actual_obj'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'swift'
op|'.'
name|'make_request'
op|'('
string|"'DELETE'"
op|','
name|'path'
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
nl|'\n'
op|'('
number|'2'
op|','
name|'HTTP_PRECONDITION_FAILED'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
