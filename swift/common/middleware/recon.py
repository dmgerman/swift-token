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
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
name|'import'
name|'__version__'
name|'as'
name|'swiftver'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
op|','
name|'Response'
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
name|'json'
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
name|'resource'
name|'import'
name|'getpagesize'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ReconMiddleware
name|'class'
name|'ReconMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Recon middleware used for monitoring.\n\n    /recon/load|mem|async... will return various system metrics.\n\n    Needs to be added to the pipeline and a requires a filter\n    declaration in the object-server.conf:\n\n    [filter:recon]\n    use = egg:swift#recon\n    recon_cache_path = /var/cache/swift\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'conf'
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
name|'app'
op|'='
name|'app'
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
string|"'/srv/node/'"
op|')'
newline|'\n'
name|'swift_dir'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'swift_dir'"
op|','
string|"'/etc/swift'"
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
string|"'recon'"
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
name|'object_recon_cache'
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
nl|'\n'
string|"'object.recon'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_recon_cache'
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
nl|'\n'
string|"'container.recon'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_recon_cache'
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
nl|'\n'
string|"'account.recon'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'account.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'container.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'object.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'rings'
op|'='
op|'['
name|'self'
op|'.'
name|'account_ring_path'
op|','
name|'self'
op|'.'
name|'container_ring_path'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_ring_path'
op|']'
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
nl|'\n'
DECL|member|_from_recon_cache
dedent|''
name|'def'
name|'_from_recon_cache'
op|'('
name|'self'
op|','
name|'cache_keys'
op|','
name|'cache_file'
op|','
name|'openr'
op|'='
name|'open'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""retrieve values from a recon cache file\n\n        :params cache_keys: list of cache items to retrieve\n        :params cache_file: cache file to retrieve items from.\n        :params openr: open to use [for unittests]\n        :return: dict of cache items and their value or none if not found\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'openr'
op|'('
name|'cache_file'
op|','
string|"'r'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'                '
name|'recondata'
op|'='
name|'json'
op|'.'
name|'load'
op|'('
name|'f'
op|')'
newline|'\n'
name|'return'
name|'dict'
op|'('
op|'('
name|'key'
op|','
name|'recondata'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
op|')'
name|'for'
name|'key'
name|'in'
name|'cache_keys'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'IOError'
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
string|"'Error reading recon cache file'"
op|')'
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
name|'exception'
op|'('
name|'_'
op|'('
string|"'Error parsing recon cache file'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
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
string|"'Error retrieving recon data'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'dict'
op|'('
op|'('
name|'key'
op|','
name|'None'
op|')'
name|'for'
name|'key'
name|'in'
name|'cache_keys'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_version
dedent|''
name|'def'
name|'get_version'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get swift version"""'
newline|'\n'
name|'verinfo'
op|'='
op|'{'
string|"'version'"
op|':'
name|'swiftver'
op|'}'
newline|'\n'
name|'return'
name|'verinfo'
newline|'\n'
nl|'\n'
DECL|member|get_mounted
dedent|''
name|'def'
name|'get_mounted'
op|'('
name|'self'
op|','
name|'openr'
op|'='
name|'open'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get ALL mounted fs from /proc/mounts"""'
newline|'\n'
name|'mounts'
op|'='
op|'['
op|']'
newline|'\n'
name|'with'
name|'openr'
op|'('
string|"'/proc/mounts'"
op|','
string|"'r'"
op|')'
name|'as'
name|'procmounts'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'line'
name|'in'
name|'procmounts'
op|':'
newline|'\n'
indent|'                '
name|'mount'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'mount'
op|'['
string|"'device'"
op|']'
op|','
name|'mount'
op|'['
string|"'path'"
op|']'
op|','
name|'opt1'
op|','
name|'opt2'
op|','
name|'opt3'
op|','
name|'opt4'
op|'='
name|'line'
op|'.'
name|'rstrip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'mounts'
op|'.'
name|'append'
op|'('
name|'mount'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'mounts'
newline|'\n'
nl|'\n'
DECL|member|get_load
dedent|''
name|'def'
name|'get_load'
op|'('
name|'self'
op|','
name|'openr'
op|'='
name|'open'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get info from /proc/loadavg"""'
newline|'\n'
name|'loadavg'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'openr'
op|'('
string|"'/proc/loadavg'"
op|','
string|"'r'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'onemin'
op|','
name|'fivemin'
op|','
name|'ftmin'
op|','
name|'tasks'
op|','
name|'procs'
op|'='
name|'f'
op|'.'
name|'read'
op|'('
op|')'
op|'.'
name|'rstrip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
dedent|''
name|'loadavg'
op|'['
string|"'1m'"
op|']'
op|'='
name|'float'
op|'('
name|'onemin'
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'5m'"
op|']'
op|'='
name|'float'
op|'('
name|'fivemin'
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'15m'"
op|']'
op|'='
name|'float'
op|'('
name|'ftmin'
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'tasks'"
op|']'
op|'='
name|'tasks'
newline|'\n'
name|'loadavg'
op|'['
string|"'processes'"
op|']'
op|'='
name|'int'
op|'('
name|'procs'
op|')'
newline|'\n'
name|'return'
name|'loadavg'
newline|'\n'
nl|'\n'
DECL|member|get_mem
dedent|''
name|'def'
name|'get_mem'
op|'('
name|'self'
op|','
name|'openr'
op|'='
name|'open'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get info from /proc/meminfo"""'
newline|'\n'
name|'meminfo'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'openr'
op|'('
string|"'/proc/meminfo'"
op|','
string|"'r'"
op|')'
name|'as'
name|'memlines'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'i'
name|'in'
name|'memlines'
op|':'
newline|'\n'
indent|'                '
name|'entry'
op|'='
name|'i'
op|'.'
name|'rstrip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
string|'":"'
op|')'
newline|'\n'
name|'meminfo'
op|'['
name|'entry'
op|'['
number|'0'
op|']'
op|']'
op|'='
name|'entry'
op|'['
number|'1'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'meminfo'
newline|'\n'
nl|'\n'
DECL|member|get_async_info
dedent|''
name|'def'
name|'get_async_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get # of async pendings"""'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'async_pending'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_recon_cache'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_replication_info
dedent|''
name|'def'
name|'get_replication_info'
op|'('
name|'self'
op|','
name|'recon_type'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get replication info"""'
newline|'\n'
name|'if'
name|'recon_type'
op|'=='
string|"'account'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'replication_time'"
op|','
nl|'\n'
string|"'replication_stats'"
op|','
nl|'\n'
string|"'replication_last'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'recon_type'
op|'=='
string|"'container'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'replication_time'"
op|','
nl|'\n'
string|"'replication_stats'"
op|','
nl|'\n'
string|"'replication_last'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'recon_type'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'object_replication_time'"
op|','
nl|'\n'
string|"'object_replication_last'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_device_info
dedent|''
dedent|''
name|'def'
name|'get_device_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get devices"""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'{'
name|'self'
op|'.'
name|'devices'
op|':'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
op|'}'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
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
string|"'Error listing devices'"
op|')'
op|')'
newline|'\n'
name|'return'
op|'{'
name|'self'
op|'.'
name|'devices'
op|':'
name|'None'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get_updater_info
dedent|''
dedent|''
name|'def'
name|'get_updater_info'
op|'('
name|'self'
op|','
name|'recon_type'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get updater info"""'
newline|'\n'
name|'if'
name|'recon_type'
op|'=='
string|"'container'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'container_updater_sweep'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'recon_type'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'object_updater_sweep'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_expirer_info
dedent|''
dedent|''
name|'def'
name|'get_expirer_info'
op|'('
name|'self'
op|','
name|'recon_type'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get expirer info"""'
newline|'\n'
name|'if'
name|'recon_type'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'object_expiration_pass'"
op|','
nl|'\n'
string|"'expired_last_pass'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_recon_cache'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_auditor_info
dedent|''
dedent|''
name|'def'
name|'get_auditor_info'
op|'('
name|'self'
op|','
name|'recon_type'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get auditor info"""'
newline|'\n'
name|'if'
name|'recon_type'
op|'=='
string|"'account'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'account_audits_passed'"
op|','
nl|'\n'
string|"'account_auditor_pass_completed'"
op|','
nl|'\n'
string|"'account_audits_since'"
op|','
nl|'\n'
string|"'account_audits_failed'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'recon_type'
op|'=='
string|"'container'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'container_audits_passed'"
op|','
nl|'\n'
string|"'container_auditor_pass_completed'"
op|','
nl|'\n'
string|"'container_audits_since'"
op|','
nl|'\n'
string|"'container_audits_failed'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'recon_type'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_from_recon_cache'
op|'('
op|'['
string|"'object_auditor_stats_ALL'"
op|','
nl|'\n'
string|"'object_auditor_stats_ZBF'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_recon_cache'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_unmounted
dedent|''
dedent|''
name|'def'
name|'get_unmounted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""list unmounted (failed?) devices"""'
newline|'\n'
name|'mountlist'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'entry'
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
indent|'            '
name|'mpoint'
op|'='
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
nl|'\n'
string|"'mounted'"
op|':'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'entry'
op|')'
op|'}'
newline|'\n'
name|'if'
name|'not'
name|'mpoint'
op|'['
string|"'mounted'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'mountlist'
op|'.'
name|'append'
op|'('
name|'mpoint'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'mountlist'
newline|'\n'
nl|'\n'
DECL|member|get_diskusage
dedent|''
name|'def'
name|'get_diskusage'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get disk utilization statistics"""'
newline|'\n'
name|'devices'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'entry'
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
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'mounted'
op|'='
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'entry'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'devices'
op|'.'
name|'append'
op|'('
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
string|"'mounted'"
op|':'
name|'str'
op|'('
name|'err'
op|')'
op|','
nl|'\n'
string|"'size'"
op|':'
string|"''"
op|','
string|"'used'"
op|':'
string|"''"
op|','
string|"'avail'"
op|':'
string|"''"
op|'}'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'mounted'
op|':'
newline|'\n'
indent|'                '
name|'path'
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
name|'entry'
op|')'
newline|'\n'
name|'disk'
op|'='
name|'os'
op|'.'
name|'statvfs'
op|'('
name|'path'
op|')'
newline|'\n'
name|'capacity'
op|'='
name|'disk'
op|'.'
name|'f_bsize'
op|'*'
name|'disk'
op|'.'
name|'f_blocks'
newline|'\n'
name|'available'
op|'='
name|'disk'
op|'.'
name|'f_bsize'
op|'*'
name|'disk'
op|'.'
name|'f_bavail'
newline|'\n'
name|'used'
op|'='
name|'disk'
op|'.'
name|'f_bsize'
op|'*'
op|'('
name|'disk'
op|'.'
name|'f_blocks'
op|'-'
name|'disk'
op|'.'
name|'f_bavail'
op|')'
newline|'\n'
name|'devices'
op|'.'
name|'append'
op|'('
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
string|"'mounted'"
op|':'
name|'True'
op|','
nl|'\n'
string|"'size'"
op|':'
name|'capacity'
op|','
string|"'used'"
op|':'
name|'used'
op|','
nl|'\n'
string|"'avail'"
op|':'
name|'available'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'devices'
op|'.'
name|'append'
op|'('
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
string|"'mounted'"
op|':'
name|'False'
op|','
nl|'\n'
string|"'size'"
op|':'
string|"''"
op|','
string|"'used'"
op|':'
string|"''"
op|','
string|"'avail'"
op|':'
string|"''"
op|'}'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'devices'
newline|'\n'
nl|'\n'
DECL|member|get_ring_md5
dedent|''
name|'def'
name|'get_ring_md5'
op|'('
name|'self'
op|','
name|'openr'
op|'='
name|'open'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get all ring md5sum\'s"""'
newline|'\n'
name|'sums'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'ringfile'
name|'in'
name|'self'
op|'.'
name|'rings'
op|':'
newline|'\n'
indent|'            '
name|'md5sum'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'ringfile'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'with'
name|'openr'
op|'('
name|'ringfile'
op|','
string|"'rb'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'                        '
name|'block'
op|'='
name|'f'
op|'.'
name|'read'
op|'('
number|'4096'
op|')'
newline|'\n'
name|'while'
name|'block'
op|':'
newline|'\n'
indent|'                            '
name|'md5sum'
op|'.'
name|'update'
op|'('
name|'block'
op|')'
newline|'\n'
name|'block'
op|'='
name|'f'
op|'.'
name|'read'
op|'('
number|'4096'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'sums'
op|'['
name|'ringfile'
op|']'
op|'='
name|'md5sum'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'sums'
op|'['
name|'ringfile'
op|']'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'err'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'Error reading ringfile'"
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'return'
name|'sums'
newline|'\n'
nl|'\n'
DECL|member|get_quarantine_count
dedent|''
name|'def'
name|'get_quarantine_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get obj/container/account quarantine counts"""'
newline|'\n'
name|'qcounts'
op|'='
op|'{'
string|'"objects"'
op|':'
number|'0'
op|','
string|'"containers"'
op|':'
number|'0'
op|','
string|'"accounts"'
op|':'
number|'0'
op|'}'
newline|'\n'
name|'qdir'
op|'='
string|'"quarantined"'
newline|'\n'
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
indent|'            '
name|'for'
name|'qtype'
name|'in'
name|'qcounts'
op|':'
newline|'\n'
indent|'                '
name|'qtgt'
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
name|'qdir'
op|','
name|'qtype'
op|')'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'qtgt'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'linkcount'
op|'='
name|'os'
op|'.'
name|'lstat'
op|'('
name|'qtgt'
op|')'
op|'.'
name|'st_nlink'
newline|'\n'
name|'if'
name|'linkcount'
op|'>'
number|'2'
op|':'
newline|'\n'
indent|'                        '
name|'qcounts'
op|'['
name|'qtype'
op|']'
op|'+='
name|'linkcount'
op|'-'
number|'2'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'return'
name|'qcounts'
newline|'\n'
nl|'\n'
DECL|member|get_socket_info
dedent|''
name|'def'
name|'get_socket_info'
op|'('
name|'self'
op|','
name|'openr'
op|'='
name|'open'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        get info from /proc/net/sockstat and sockstat6\n\n        Note: The mem value is actually kernel pages, but we return bytes\n        allocated based on the systems page size.\n        """'
newline|'\n'
name|'sockstat'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'openr'
op|'('
string|"'/proc/net/sockstat'"
op|','
string|"'r'"
op|')'
name|'as'
name|'proc_sockstat'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'entry'
name|'in'
name|'proc_sockstat'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'entry'
op|'.'
name|'startswith'
op|'('
string|'"TCP: inuse"'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'tcpstats'
op|'='
name|'entry'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'tcp_in_use'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'orphan'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'4'
op|']'
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'time_wait'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'6'
op|']'
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'tcp_mem_allocated_bytes'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'10'
op|']'
op|')'
op|'*'
name|'getpagesize'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'e'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'openr'
op|'('
string|"'/proc/net/sockstat6'"
op|','
string|"'r'"
op|')'
name|'as'
name|'proc_sockstat6'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'entry'
name|'in'
name|'proc_sockstat6'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'entry'
op|'.'
name|'startswith'
op|'('
string|'"TCP6: inuse"'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'sockstat'
op|'['
string|"'tcp6_in_use'"
op|']'
op|'='
name|'int'
op|'('
name|'entry'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'e'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'sockstat'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'root'
op|','
name|'rcheck'
op|','
name|'rtype'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'1'
op|','
number|'3'
op|','
name|'True'
op|')'
newline|'\n'
name|'all_rtypes'
op|'='
op|'['
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|']'
newline|'\n'
name|'if'
name|'rcheck'
op|'=='
string|'"mem"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_mem'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"load"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_load'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"async"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_async_info'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|"'replication'"
name|'and'
name|'rtype'
name|'in'
name|'all_rtypes'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_replication_info'
op|'('
name|'rtype'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|"'replication'"
name|'and'
name|'rtype'
name|'is'
name|'None'
op|':'
newline|'\n'
comment|'#handle old style object replication requests'
nl|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_replication_info'
op|'('
string|"'object'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"devices"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_device_info'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"updater"'
name|'and'
name|'rtype'
name|'in'
op|'['
string|"'container'"
op|','
string|"'object'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_updater_info'
op|'('
name|'rtype'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"auditor"'
name|'and'
name|'rtype'
name|'in'
name|'all_rtypes'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_auditor_info'
op|'('
name|'rtype'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"expirer"'
name|'and'
name|'rtype'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_expirer_info'
op|'('
name|'rtype'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"mounted"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_mounted'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"unmounted"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_unmounted'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"diskusage"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_diskusage'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"ringmd5"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_ring_md5'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"quarantined"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_quarantine_count'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"sockstat"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_socket_info'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'rcheck'
op|'=='
string|'"version"'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
name|'self'
op|'.'
name|'get_version'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'content'
op|'='
string|'"Invalid path: %s"'
op|'%'
name|'req'
op|'.'
name|'path'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'status'
op|'='
string|'"404 Not Found"'
op|','
nl|'\n'
name|'body'
op|'='
name|'content'
op|','
name|'content_type'
op|'='
string|'"text/plain"'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'content'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'content'
op|')'
op|','
nl|'\n'
name|'content_type'
op|'='
string|'"application/json"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'status'
op|'='
string|'"500 Server Error"'
op|','
nl|'\n'
name|'body'
op|'='
string|'"Internal server error."'
op|','
nl|'\n'
name|'content_type'
op|'='
string|'"text/plain"'
op|')'
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
name|'if'
name|'req'
op|'.'
name|'path'
op|'.'
name|'startswith'
op|'('
string|"'/recon/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'GET'
op|'('
name|'req'
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
DECL|function|recon_filter
name|'def'
name|'recon_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ReconMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'recon_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
