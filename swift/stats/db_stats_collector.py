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
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'appconfig'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
name|'import'
name|'urllib'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
op|'.'
name|'server'
name|'import'
name|'DATADIR'
name|'as'
name|'account_server_data_dir'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'server'
name|'import'
name|'DATADIR'
name|'as'
name|'container_server_data_dir'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'AccountBroker'
op|','
name|'ContainerBroker'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'renamer'
op|','
name|'get_logger'
op|','
name|'readconf'
op|','
name|'mkdirs'
op|','
name|'TRUE_VALUES'
op|','
name|'remove_file'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_mount'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'daemon'
name|'import'
name|'Daemon'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DatabaseStatsCollector
name|'class'
name|'DatabaseStatsCollector'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Extract storage stats from account databases on the account\n    storage nodes\n\n    Any subclasses must define the function get_data.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'stats_conf'
op|','
name|'stats_type'
op|','
name|'data_dir'
op|','
name|'filename_format'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'DatabaseStatsCollector'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'stats_conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'stats_type'
op|'='
name|'stats_type'
newline|'\n'
name|'self'
op|'.'
name|'data_dir'
op|'='
name|'data_dir'
newline|'\n'
name|'self'
op|'.'
name|'filename_format'
op|'='
name|'filename_format'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'devices'"
op|','
string|"'/srv/node'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'mount_check'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
nl|'\n'
string|"'true'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
name|'TRUE_VALUES'
newline|'\n'
name|'self'
op|'.'
name|'target_dir'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'log_dir'"
op|','
string|"'/var/log/swift'"
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'self'
op|'.'
name|'target_dir'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'stats_conf'
op|','
nl|'\n'
name|'log_route'
op|'='
string|"'%s-stats'"
op|'%'
name|'stats_type'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
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
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Gathering %s stats"'
op|'%'
name|'self'
op|'.'
name|'stats_type'
op|')'
op|')'
newline|'\n'
name|'start'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'find_and_process'
op|'('
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
string|'"Gathering %s stats complete (%0.2f minutes)"'
op|')'
op|'%'
nl|'\n'
op|'('
name|'self'
op|'.'
name|'stats_type'
op|','
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
op|')'
op|'/'
number|'60'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_data
dedent|''
name|'def'
name|'get_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'Not Implemented'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|find_and_process
dedent|''
name|'def'
name|'find_and_process'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'src_filename'
op|'='
name|'time'
op|'.'
name|'strftime'
op|'('
name|'self'
op|'.'
name|'filename_format'
op|')'
newline|'\n'
name|'working_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'target_dir'
op|','
nl|'\n'
string|"'.%-stats_tmp'"
op|'%'
name|'self'
op|'.'
name|'stats_type'
op|')'
newline|'\n'
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'working_dir'
op|','
name|'ignore_errors'
op|'='
name|'True'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'working_dir'
op|')'
newline|'\n'
name|'tmp_filename'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'working_dir'
op|','
name|'src_filename'
op|')'
newline|'\n'
name|'hasher'
op|'='
name|'hashlib'
op|'.'
name|'md5'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
name|'tmp_filename'
op|','
string|"'wb'"
op|')'
name|'as'
name|'statfile'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'device'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'device'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
nl|'\n'
name|'_'
op|'('
string|'"Device %s is not mounted, skipping."'
op|')'
op|'%'
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'db_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'device'
op|','
name|'self'
op|'.'
name|'data_dir'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'db_dir'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
name|'_'
op|'('
string|'"Path %s does not exist, skipping."'
op|')'
op|'%'
name|'db_dir'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'root'
op|','
name|'dirs'
op|','
name|'files'
name|'in'
name|'os'
op|'.'
name|'walk'
op|'('
name|'db_dir'
op|','
name|'topdown'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'for'
name|'filename'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'                            '
name|'if'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.db'"
op|')'
op|':'
newline|'\n'
indent|'                                '
name|'db_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'root'
op|','
name|'filename'
op|')'
newline|'\n'
name|'line_data'
op|'='
name|'self'
op|'.'
name|'get_data'
op|'('
name|'db_path'
op|')'
newline|'\n'
name|'if'
name|'line_data'
op|':'
newline|'\n'
indent|'                                    '
name|'statfile'
op|'.'
name|'write'
op|'('
name|'line_data'
op|')'
newline|'\n'
name|'hasher'
op|'.'
name|'update'
op|'('
name|'line_data'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'src_filename'
op|'+='
name|'hasher'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'renamer'
op|'('
name|'tmp_filename'
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'target_dir'
op|','
name|'src_filename'
op|')'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'working_dir'
op|','
name|'ignore_errors'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccountStatsCollector
dedent|''
dedent|''
dedent|''
name|'class'
name|'AccountStatsCollector'
op|'('
name|'DatabaseStatsCollector'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Extract storage stats from account databases on the account\n    storage nodes\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'stats_conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'AccountStatsCollector'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'stats_conf'
op|','
string|"'account'"
op|','
nl|'\n'
name|'account_server_data_dir'
op|','
nl|'\n'
string|"'stats-%Y%m%d%H_'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_data
dedent|''
name|'def'
name|'get_data'
op|'('
name|'self'
op|','
name|'db_path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Data for generated csv has the following columns:\n        Account Hash, Container Count, Object Count, Bytes Used\n        """'
newline|'\n'
name|'line_data'
op|'='
name|'None'
newline|'\n'
name|'broker'
op|'='
name|'AccountBroker'
op|'('
name|'db_path'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'line_data'
op|'='
string|'\'"%s",%d,%d,%d\\n\''
op|'%'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'container_count'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'line_data'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerStatsCollector
dedent|''
dedent|''
name|'class'
name|'ContainerStatsCollector'
op|'('
name|'DatabaseStatsCollector'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Extract storage stats from container databases on the container\n    storage nodes\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'stats_conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'ContainerStatsCollector'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'stats_conf'
op|','
string|"'container'"
op|','
nl|'\n'
name|'container_server_data_dir'
op|','
nl|'\n'
string|"'container-stats-%Y%m%d%H_'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_data
dedent|''
name|'def'
name|'get_data'
op|'('
name|'self'
op|','
name|'db_path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Data for generated csv has the following columns:\n        Account Hash, Container Name, Object Count, Bytes Used\n        """'
newline|'\n'
name|'line_data'
op|'='
name|'None'
newline|'\n'
name|'broker'
op|'='
name|'ContainerBroker'
op|'('
name|'db_path'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'encoded_container_name'
op|'='
name|'urllib'
op|'.'
name|'quote'
op|'('
name|'info'
op|'['
string|"'container'"
op|']'
op|')'
newline|'\n'
name|'line_data'
op|'='
string|'\'"%s","%s",%d,%d\\n\''
op|'%'
op|'('
nl|'\n'
name|'info'
op|'['
string|"'account'"
op|']'
op|','
nl|'\n'
name|'encoded_container_name'
op|','
nl|'\n'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'line_data'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
