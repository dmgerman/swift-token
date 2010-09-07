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
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
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
name|'common'
op|'.'
name|'db'
name|'import'
name|'AccountBroker'
newline|'\n'
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
name|'utils'
name|'import'
name|'renamer'
op|','
name|'get_logger'
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
DECL|class|AccountStat
name|'class'
name|'AccountStat'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
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
name|'self'
op|','
name|'AccountStat'
op|')'
op|'.'
name|'__init__'
op|'('
name|'stats_conf'
op|')'
newline|'\n'
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
name|'account_server_conf_loc'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'account_server_conf'"
op|','
nl|'\n'
string|"'/etc/swift/account-server.conf'"
op|')'
newline|'\n'
name|'server_conf'
op|'='
name|'utils'
op|'.'
name|'readconf'
op|'('
name|'account_server_conf_loc'
op|','
string|"'account-server'"
op|')'
newline|'\n'
name|'filename_format'
op|'='
name|'stats_conf'
op|'['
string|"'source_filename_format'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'filename_format'
op|'='
name|'filename_format'
newline|'\n'
name|'self'
op|'.'
name|'target_dir'
op|'='
name|'target_dir'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'server_conf'
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
name|'server_conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
string|"'true'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'true'"
op|','
string|"'t'"
op|','
string|"'1'"
op|','
string|"'on'"
op|','
string|"'yes'"
op|','
string|"'y'"
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
string|"'swift-account-stats-logger'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
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
string|'"Gathering account stats"'
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
string|'"Gathering account stats complete (%0.2f minutes)"'
op|'%'
nl|'\n'
op|'('
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
name|'tmp_filename'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
string|"'/tmp'"
op|','
name|'src_filename'
op|')'
newline|'\n'
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
comment|"#statfile.write('Account Name, Container Count, Object Count, Bytes Used, Created At\\n')"
nl|'\n'
indent|'            '
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
indent|'                '
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'ismount'
op|'('
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
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|'"Device %s is not mounted, skipping."'
op|'%'
nl|'\n'
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'accounts'
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
nl|'\n'
name|'device'
op|','
nl|'\n'
name|'account_server_data_dir'
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
name|'accounts'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|'"Path %s does not exist, skipping."'
op|'%'
nl|'\n'
name|'accounts'
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
name|'accounts'
op|','
name|'topdown'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'filename'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.db'"
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'broker'
op|'='
name|'AccountBroker'
op|'('
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
indent|'                                '
name|'account_name'
op|','
newline|'\n'
name|'created_at'
op|','
newline|'\n'
name|'_'
op|','
name|'_'
op|','
newline|'\n'
name|'container_count'
op|','
newline|'\n'
name|'object_count'
op|','
newline|'\n'
name|'bytes_used'
op|','
newline|'\n'
name|'_'
op|','
name|'_'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'line_data'
op|'='
string|'\'"%s",%d,%d,%d,%s\\n\''
op|'%'
op|'('
name|'account_name'
op|','
nl|'\n'
name|'container_count'
op|','
nl|'\n'
name|'object_count'
op|','
nl|'\n'
name|'bytes_used'
op|','
nl|'\n'
name|'created_at'
op|')'
newline|'\n'
name|'statfile'
op|'.'
name|'write'
op|'('
name|'line_data'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
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
dedent|''
endmarker|''
end_unit
