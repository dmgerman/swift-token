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
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'random'
newline|'\n'
nl|'\n'
name|'import'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
name|'import'
name|'server'
name|'as'
name|'account_server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
op|'.'
name|'backend'
name|'import'
name|'AccountBroker'
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
op|','
name|'dump_recon_cache'
op|','
name|'ratelimit_sleep'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ondisk'
name|'import'
name|'audit_location_generator'
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
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccountAuditor
name|'class'
name|'AccountAuditor'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Audit accounts."""'
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
string|"'account-auditor'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'conf'
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
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
string|"'true'"
op|')'
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
op|','
number|'1800'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'account_failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'accounts_running_time'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'max_accounts_per_second'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'accounts_per_second'"
op|','
number|'200'
op|')'
op|')'
newline|'\n'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
op|'.'
name|'DB_PREALLOCATION'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'db_preallocation'"
op|','
string|"'f'"
op|')'
op|')'
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
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'recon_cache_path'
op|','
string|'"account.recon"'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_one_audit_pass
dedent|''
name|'def'
name|'_one_audit_pass'
op|'('
name|'self'
op|','
name|'reported'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'all_locs'
op|'='
name|'audit_location_generator'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'account_server'
op|'.'
name|'DATADIR'
op|','
string|"'.db'"
op|','
nl|'\n'
name|'mount_check'
op|'='
name|'self'
op|'.'
name|'mount_check'
op|','
nl|'\n'
name|'logger'
op|'='
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'for'
name|'path'
op|','
name|'device'
op|','
name|'partition'
name|'in'
name|'all_locs'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'account_audit'
op|'('
name|'path'
op|')'
newline|'\n'
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'reported'
op|'>='
number|'3600'
op|':'
comment|'# once an hour'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Since %(time)s: Account audits: '"
nl|'\n'
string|"'%(passed)s passed audit,'"
nl|'\n'
string|"'%(failed)s failed audit'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'time'"
op|':'
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
nl|'\n'
string|"'passed'"
op|':'
name|'self'
op|'.'
name|'account_passes'
op|','
nl|'\n'
string|"'failed'"
op|':'
name|'self'
op|'.'
name|'account_failures'
op|'}'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'account_audits_since'"
op|':'
name|'reported'
op|','
nl|'\n'
string|"'account_audits_passed'"
op|':'
name|'self'
op|'.'
name|'account_passes'
op|','
nl|'\n'
string|"'account_audits_failed'"
op|':'
nl|'\n'
name|'self'
op|'.'
name|'account_failures'
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
name|'reported'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'account_failures'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'accounts_running_time'
op|'='
name|'ratelimit_sleep'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'accounts_running_time'
op|','
name|'self'
op|'.'
name|'max_accounts_per_second'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'reported'
newline|'\n'
nl|'\n'
DECL|member|run_forever
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
string|'"""Run the account audit until stopped."""'
newline|'\n'
name|'reported'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'time'
op|'.'
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
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Begin account audit pass.'"
op|')'
op|')'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'reported'
op|'='
name|'self'
op|'.'
name|'_one_audit_pass'
op|'('
name|'reported'
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
name|'_'
op|'('
string|"'ERROR auditing'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'elapsed'
op|'='
name|'time'
op|'.'
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
name|'time'
op|'.'
name|'sleep'
op|'('
name|'self'
op|'.'
name|'interval'
op|'-'
name|'elapsed'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Account audit pass completed: %.02fs'"
op|')'
op|','
name|'elapsed'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'account_auditor_pass_completed'"
op|':'
name|'elapsed'
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
string|'"""Run the account audit once."""'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'\'Begin account audit "once" mode\''
op|')'
op|')'
newline|'\n'
name|'begin'
op|'='
name|'reported'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_one_audit_pass'
op|'('
name|'reported'
op|')'
newline|'\n'
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|'\'Account audit "once" mode completed: %.02fs\''
op|')'
op|','
name|'elapsed'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'account_auditor_pass_completed'"
op|':'
name|'elapsed'
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
nl|'\n'
DECL|member|account_audit
dedent|''
name|'def'
name|'account_audit'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Audits the given account path\n\n        :param path: the path to an account db\n        """'
newline|'\n'
name|'start_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'broker'
op|'='
name|'AccountBroker'
op|'('
name|'path'
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
indent|'                '
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'passes'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_passes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Audit passed for %s'"
op|')'
op|'%'
name|'broker'
op|'.'
name|'db_file'
op|')'
newline|'\n'
dedent|''
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
name|'increment'
op|'('
string|"'failures'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_failures'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR Could not get account info %s'"
op|')'
op|','
nl|'\n'
op|'('
name|'broker'
op|'.'
name|'db_file'
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
dedent|''
dedent|''
endmarker|''
end_unit
