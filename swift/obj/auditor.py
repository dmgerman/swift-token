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
name|'json'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'re'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'shuffle'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'closing'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'diskfile'
op|','
name|'replicator'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
op|'('
nl|'\n'
name|'get_logger'
op|','
name|'ratelimit_sleep'
op|','
name|'dump_recon_cache'
op|','
name|'list_from_csv'
op|','
name|'listdir'
op|','
nl|'\n'
name|'unlink_paths_older_than'
op|','
name|'readconf'
op|','
name|'config_auto_int_value'
op|')'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'DiskFileQuarantined'
op|','
name|'DiskFileNotExist'
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
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
newline|'\n'
nl|'\n'
comment|'# This matches rsync tempfiles, like ".<timestamp>.data.Xy095a"'
nl|'\n'
DECL|variable|RE_RSYNC_TEMPFILE
name|'RE_RSYNC_TEMPFILE'
op|'='
name|'re'
op|'.'
name|'compile'
op|'('
string|"r'^\\..*\\.([a-zA-Z0-9_]){6}$'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AuditorWorker
name|'class'
name|'AuditorWorker'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Walk through file system to audit objects"""'
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
op|','
name|'rcache'
op|','
name|'devices'
op|','
name|'zero_byte_only_at_fps'
op|'='
number|'0'
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
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'devices'
newline|'\n'
name|'self'
op|'.'
name|'diskfile_router'
op|'='
name|'diskfile'
op|'.'
name|'DiskFileRouter'
op|'('
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_files_per_second'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'files_per_second'"
op|','
number|'20'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_bytes_per_second'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bytes_per_second'"
op|','
nl|'\n'
number|'10000000'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
comment|'# ideally unless ops overrides the rsync_tempfile_timeout in the'
nl|'\n'
comment|'# auditor section we can base our behavior on whatever they'
nl|'\n'
comment|'# configure for their replicator'
nl|'\n'
indent|'            '
name|'replicator_config'
op|'='
name|'readconf'
op|'('
name|'self'
op|'.'
name|'conf'
op|'['
string|"'__file__'"
op|']'
op|','
nl|'\n'
string|"'object-replicator'"
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'KeyError'
op|','
name|'SystemExit'
op|')'
op|':'
newline|'\n'
comment|"# if we can't parse the real config (generally a KeyError on"
nl|'\n'
comment|'# __file__, or SystemExit on no object-replicator section) we use'
nl|'\n'
comment|'# a very conservative default'
nl|'\n'
indent|'            '
name|'default'
op|'='
number|'86400'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'replicator_rsync_timeout'
op|'='
name|'int'
op|'('
name|'replicator_config'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'rsync_timeout'"
op|','
name|'replicator'
op|'.'
name|'DEFAULT_RSYNC_TIMEOUT'
op|')'
op|')'
newline|'\n'
comment|"# Here we can do some light math for ops and use the *replicator's*"
nl|'\n'
comment|'# rsync_timeout (plus 15 mins to avoid deleting local tempfiles'
nl|'\n'
comment|"# before the remote replicator kills it's rsync)"
nl|'\n'
name|'default'
op|'='
name|'replicator_rsync_timeout'
op|'+'
number|'900'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'rsync_tempfile_timeout'
op|'='
name|'config_auto_int_value'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'rsync_tempfile_timeout'"
op|')'
op|','
name|'default'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'auditor_type'
op|'='
string|"'ALL'"
newline|'\n'
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|'='
name|'zero_byte_only_at_fps'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'max_files_per_second'
op|'='
name|'float'
op|'('
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor_type'
op|'='
string|"'ZBF'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'log_time'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_time'"
op|','
number|'3600'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'last_logged'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'files_running_time'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'bytes_running_time'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'total_bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'total_files_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'quarantines'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'errors'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'rcache'
op|'='
name|'rcache'
newline|'\n'
name|'self'
op|'.'
name|'stats_sizes'
op|'='
name|'sorted'
op|'('
nl|'\n'
op|'['
name|'int'
op|'('
name|'s'
op|')'
name|'for'
name|'s'
name|'in'
name|'list_from_csv'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'object_size_stats'"
op|')'
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'stats_buckets'
op|'='
name|'dict'
op|'('
nl|'\n'
op|'['
op|'('
name|'s'
op|','
number|'0'
op|')'
name|'for'
name|'s'
name|'in'
name|'self'
op|'.'
name|'stats_sizes'
op|'+'
op|'['
string|"'OVER'"
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_recon_nested_dict
dedent|''
name|'def'
name|'create_recon_nested_dict'
op|'('
name|'self'
op|','
name|'top_level_key'
op|','
name|'device_list'
op|','
name|'item'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'device_list'
op|':'
newline|'\n'
indent|'            '
name|'device_key'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'sorted'
op|'('
name|'device_list'
op|')'
op|')'
newline|'\n'
name|'return'
op|'{'
name|'top_level_key'
op|':'
op|'{'
name|'device_key'
op|':'
name|'item'
op|'}'
op|'}'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'{'
name|'top_level_key'
op|':'
name|'item'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|audit_all_objects
dedent|''
dedent|''
name|'def'
name|'audit_all_objects'
op|'('
name|'self'
op|','
name|'mode'
op|'='
string|"'once'"
op|','
name|'device_dirs'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'description'
op|'='
string|"''"
newline|'\n'
name|'if'
name|'device_dirs'
op|':'
newline|'\n'
indent|'            '
name|'device_dir_str'
op|'='
string|"','"
op|'.'
name|'join'
op|'('
name|'sorted'
op|'('
name|'device_dirs'
op|')'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'auditor_type'
op|'=='
string|"'ALL'"
op|':'
newline|'\n'
indent|'                '
name|'description'
op|'='
name|'_'
op|'('
string|"' - parallel, %s'"
op|')'
op|'%'
name|'device_dir_str'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'description'
op|'='
name|'_'
op|'('
string|"' - %s'"
op|')'
op|'%'
name|'device_dir_str'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'\'Begin object audit "%(mode)s" mode (%(audi_type)s\''
nl|'\n'
string|"'%(description)s)'"
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'mode'"
op|':'
name|'mode'
op|','
string|"'audi_type'"
op|':'
name|'self'
op|'.'
name|'auditor_type'
op|','
nl|'\n'
string|"'description'"
op|':'
name|'description'
op|'}'
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
name|'total_bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'total_files_processed'
op|'='
number|'0'
newline|'\n'
name|'total_quarantines'
op|'='
number|'0'
newline|'\n'
name|'total_errors'
op|'='
number|'0'
newline|'\n'
name|'time_auditing'
op|'='
number|'0'
newline|'\n'
comment|'# TODO: we should move audit-location generation to the storage policy,'
nl|'\n'
comment|'# as we may (conceivably) have a different filesystem layout for each.'
nl|'\n'
comment|"# We'd still need to generate the policies to audit from the actual"
nl|'\n'
comment|'# directories found on-disk, and have appropriate error reporting if we'
nl|'\n'
comment|"# find a directory that doesn't correspond to any known policy. This"
nl|'\n'
comment|'# will require a sizable refactor, but currently all diskfile managers'
nl|'\n'
comment|'# can find all diskfile locations regardless of policy -- so for now'
nl|'\n'
comment|"# just use Policy-0's manager."
nl|'\n'
name|'all_locs'
op|'='
op|'('
name|'self'
op|'.'
name|'diskfile_router'
op|'['
name|'POLICIES'
op|'['
number|'0'
op|']'
op|']'
nl|'\n'
op|'.'
name|'object_audit_location_generator'
op|'('
nl|'\n'
name|'device_dirs'
op|'='
name|'device_dirs'
op|','
nl|'\n'
name|'auditor_type'
op|'='
name|'self'
op|'.'
name|'auditor_type'
op|')'
op|')'
newline|'\n'
name|'for'
name|'location'
name|'in'
name|'all_locs'
op|':'
newline|'\n'
indent|'            '
name|'loop_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failsafe_object_audit'
op|'('
name|'location'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'timing_since'
op|'('
string|"'timing'"
op|','
name|'loop_time'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'files_running_time'
op|'='
name|'ratelimit_sleep'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'files_running_time'
op|','
name|'self'
op|'.'
name|'max_files_per_second'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_files_processed'
op|'+='
number|'1'
newline|'\n'
name|'now'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'if'
name|'now'
op|'-'
name|'self'
op|'.'
name|'last_logged'
op|'>='
name|'self'
op|'.'
name|'log_time'
op|':'
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
nl|'\n'
string|"'Object audit (%(type)s). '"
nl|'\n'
string|"'Since %(start_time)s: Locally: %(passes)d passed, '"
nl|'\n'
string|"'%(quars)d quarantined, %(errors)d errors, '"
nl|'\n'
string|"'files/sec: %(frate).2f, bytes/sec: %(brate).2f, '"
nl|'\n'
string|"'Total time: %(total).2f, Auditing time: %(audit).2f, '"
nl|'\n'
string|"'Rate: %(audit_rate).2f'"
op|')'
op|'%'
op|'{'
nl|'\n'
string|"'type'"
op|':'
string|"'%s%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'auditor_type'
op|','
name|'description'
op|')'
op|','
nl|'\n'
string|"'start_time'"
op|':'
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
nl|'\n'
string|"'passes'"
op|':'
name|'self'
op|'.'
name|'passes'
op|','
string|"'quars'"
op|':'
name|'self'
op|'.'
name|'quarantines'
op|','
nl|'\n'
string|"'errors'"
op|':'
name|'self'
op|'.'
name|'errors'
op|','
nl|'\n'
string|"'frate'"
op|':'
name|'self'
op|'.'
name|'passes'
op|'/'
op|'('
name|'now'
op|'-'
name|'reported'
op|')'
op|','
nl|'\n'
string|"'brate'"
op|':'
name|'self'
op|'.'
name|'bytes_processed'
op|'/'
op|'('
name|'now'
op|'-'
name|'reported'
op|')'
op|','
nl|'\n'
string|"'total'"
op|':'
op|'('
name|'now'
op|'-'
name|'begin'
op|')'
op|','
string|"'audit'"
op|':'
name|'time_auditing'
op|','
nl|'\n'
string|"'audit_rate'"
op|':'
name|'time_auditing'
op|'/'
op|'('
name|'now'
op|'-'
name|'begin'
op|')'
op|'}'
op|')'
newline|'\n'
name|'cache_entry'
op|'='
name|'self'
op|'.'
name|'create_recon_nested_dict'
op|'('
nl|'\n'
string|"'object_auditor_stats_%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'auditor_type'
op|')'
op|','
nl|'\n'
name|'device_dirs'
op|','
nl|'\n'
op|'{'
string|"'errors'"
op|':'
name|'self'
op|'.'
name|'errors'
op|','
string|"'passes'"
op|':'
name|'self'
op|'.'
name|'passes'
op|','
nl|'\n'
string|"'quarantined'"
op|':'
name|'self'
op|'.'
name|'quarantines'
op|','
nl|'\n'
string|"'bytes_processed'"
op|':'
name|'self'
op|'.'
name|'bytes_processed'
op|','
nl|'\n'
string|"'start_time'"
op|':'
name|'reported'
op|','
string|"'audit_time'"
op|':'
name|'time_auditing'
op|'}'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
name|'cache_entry'
op|','
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
name|'now'
newline|'\n'
name|'total_quarantines'
op|'+='
name|'self'
op|'.'
name|'quarantines'
newline|'\n'
name|'total_errors'
op|'+='
name|'self'
op|'.'
name|'errors'
newline|'\n'
name|'self'
op|'.'
name|'passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'quarantines'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'errors'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'last_logged'
op|'='
name|'now'
newline|'\n'
dedent|''
name|'time_auditing'
op|'+='
op|'('
name|'now'
op|'-'
name|'loop_time'
op|')'
newline|'\n'
comment|'# Avoid divide by zero during very short runs'
nl|'\n'
dedent|''
name|'elapsed'
op|'='
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
name|'or'
number|'0.000001'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
nl|'\n'
string|'\'Object audit (%(type)s) "%(mode)s" mode \''
nl|'\n'
string|"'completed: %(elapsed).02fs. Total quarantined: %(quars)d, '"
nl|'\n'
string|"'Total errors: %(errors)d, Total files/sec: %(frate).2f, '"
nl|'\n'
string|"'Total bytes/sec: %(brate).2f, Auditing time: %(audit).2f, '"
nl|'\n'
string|"'Rate: %(audit_rate).2f'"
op|')'
op|'%'
op|'{'
nl|'\n'
string|"'type'"
op|':'
string|"'%s%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'auditor_type'
op|','
name|'description'
op|')'
op|','
nl|'\n'
string|"'mode'"
op|':'
name|'mode'
op|','
string|"'elapsed'"
op|':'
name|'elapsed'
op|','
nl|'\n'
string|"'quars'"
op|':'
name|'total_quarantines'
op|'+'
name|'self'
op|'.'
name|'quarantines'
op|','
nl|'\n'
string|"'errors'"
op|':'
name|'total_errors'
op|'+'
name|'self'
op|'.'
name|'errors'
op|','
nl|'\n'
string|"'frate'"
op|':'
name|'self'
op|'.'
name|'total_files_processed'
op|'/'
name|'elapsed'
op|','
nl|'\n'
string|"'brate'"
op|':'
name|'self'
op|'.'
name|'total_bytes_processed'
op|'/'
name|'elapsed'
op|','
nl|'\n'
string|"'audit'"
op|':'
name|'time_auditing'
op|','
string|"'audit_rate'"
op|':'
name|'time_auditing'
op|'/'
name|'elapsed'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'stats_sizes'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Object audit stats: %s'"
op|')'
op|'%'
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'stats_buckets'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# Unset remaining partitions to not skip them in the next run'
nl|'\n'
dedent|''
name|'diskfile'
op|'.'
name|'clear_auditor_status'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'self'
op|'.'
name|'auditor_type'
op|')'
newline|'\n'
nl|'\n'
DECL|member|record_stats
dedent|''
name|'def'
name|'record_stats'
op|'('
name|'self'
op|','
name|'obj_size'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Based on config\'s object_size_stats will keep track of how many objects\n        fall into the specified ranges. For example with the following:\n\n        object_size_stats = 10, 100, 1024\n\n        and your system has 3 objects of sizes: 5, 20, and 10000 bytes the log\n        will look like: {"10": 1, "100": 1, "1024": 0, "OVER": 1}\n        """'
newline|'\n'
name|'for'
name|'size'
name|'in'
name|'self'
op|'.'
name|'stats_sizes'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj_size'
op|'<='
name|'size'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'stats_buckets'
op|'['
name|'size'
op|']'
op|'+='
number|'1'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'stats_buckets'
op|'['
string|'"OVER"'
op|']'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|failsafe_object_audit
dedent|''
dedent|''
name|'def'
name|'failsafe_object_audit'
op|'('
name|'self'
op|','
name|'location'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Entrypoint to object_audit, with a failsafe generic exception handler.\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'object_audit'
op|'('
name|'location'
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
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'errors'
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
string|"'ERROR Trying to audit %s'"
op|')'
op|','
name|'location'
op|')'
newline|'\n'
nl|'\n'
DECL|member|object_audit
dedent|''
dedent|''
name|'def'
name|'object_audit'
op|'('
name|'self'
op|','
name|'location'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Audits the given object location.\n\n        :param location: an audit location\n                         (from diskfile.object_audit_location_generator)\n        """'
newline|'\n'
DECL|function|raise_dfq
name|'def'
name|'raise_dfq'
op|'('
name|'msg'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DiskFileQuarantined'
op|'('
name|'msg'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'diskfile_mgr'
op|'='
name|'self'
op|'.'
name|'diskfile_router'
op|'['
name|'location'
op|'.'
name|'policy'
op|']'
newline|'\n'
comment|"# this method doesn't normally raise errors, even if the audit"
nl|'\n'
comment|'# location does not exist; if this raises an unexpected error it'
nl|'\n'
comment|'# will get logged in failsafe'
nl|'\n'
name|'df'
op|'='
name|'diskfile_mgr'
op|'.'
name|'get_diskfile_from_audit_location'
op|'('
name|'location'
op|')'
newline|'\n'
name|'reader'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'df'
op|'.'
name|'open'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'metadata'
op|'='
name|'df'
op|'.'
name|'get_metadata'
op|'('
op|')'
newline|'\n'
name|'obj_size'
op|'='
name|'int'
op|'('
name|'metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'stats_sizes'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'record_stats'
op|'('
name|'obj_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'obj_size'
name|'and'
name|'not'
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|':'
newline|'\n'
indent|'                    '
name|'reader'
op|'='
name|'df'
op|'.'
name|'reader'
op|'('
name|'_quarantine_hook'
op|'='
name|'raise_dfq'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'reader'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'closing'
op|'('
name|'reader'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'chunk'
name|'in'
name|'reader'
op|':'
newline|'\n'
indent|'                        '
name|'chunk_len'
op|'='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'bytes_running_time'
op|'='
name|'ratelimit_sleep'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'bytes_running_time'
op|','
nl|'\n'
name|'self'
op|'.'
name|'max_bytes_per_second'
op|','
nl|'\n'
name|'incr_by'
op|'='
name|'chunk_len'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'bytes_processed'
op|'+='
name|'chunk_len'
newline|'\n'
name|'self'
op|'.'
name|'total_bytes_processed'
op|'+='
name|'chunk_len'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'DiskFileNotExist'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'except'
name|'DiskFileQuarantined'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'quarantines'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|"'ERROR Object %(obj)s failed audit and was'"
nl|'\n'
string|"' quarantined: %(err)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'obj'"
op|':'
name|'location'
op|','
string|"'err'"
op|':'
name|'err'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'passes'
op|'+='
number|'1'
newline|'\n'
comment|'# _ondisk_info attr is initialized to None and filled in by open'
nl|'\n'
name|'ondisk_info_dict'
op|'='
name|'df'
op|'.'
name|'_ondisk_info'
name|'or'
op|'{'
op|'}'
newline|'\n'
name|'if'
string|"'unexpected'"
name|'in'
name|'ondisk_info_dict'
op|':'
newline|'\n'
indent|'            '
name|'is_rsync_tempfile'
op|'='
name|'lambda'
name|'fpath'
op|':'
name|'RE_RSYNC_TEMPFILE'
op|'.'
name|'match'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'fpath'
op|')'
op|')'
newline|'\n'
name|'rsync_tempfile_paths'
op|'='
name|'filter'
op|'('
name|'is_rsync_tempfile'
op|','
nl|'\n'
name|'ondisk_info_dict'
op|'['
string|"'unexpected'"
op|']'
op|')'
newline|'\n'
name|'mtime'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'rsync_tempfile_timeout'
newline|'\n'
name|'unlink_paths_older_than'
op|'('
name|'rsync_tempfile_paths'
op|','
name|'mtime'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ObjectAuditor
dedent|''
dedent|''
dedent|''
name|'class'
name|'ObjectAuditor'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Audit objects."""'
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
op|'**'
name|'options'
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
string|"'object-auditor'"
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
name|'self'
op|'.'
name|'conf_zero_byte_fps'
op|'='
name|'int'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'zero_byte_files_per_second'"
op|','
number|'50'
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
string|'"object.recon"'
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
number|'30'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_sleep
dedent|''
name|'def'
name|'_sleep'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'time'
op|'.'
name|'sleep'
op|'('
name|'self'
op|'.'
name|'interval'
op|')'
newline|'\n'
nl|'\n'
DECL|member|clear_recon_cache
dedent|''
name|'def'
name|'clear_recon_cache'
op|'('
name|'self'
op|','
name|'auditor_type'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Clear recon cache entries"""'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'object_auditor_stats_%s'"
op|'%'
name|'auditor_type'
op|':'
op|'{'
op|'}'
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
DECL|member|run_audit
dedent|''
name|'def'
name|'run_audit'
op|'('
name|'self'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Run the object audit"""'
newline|'\n'
name|'mode'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'mode'"
op|')'
newline|'\n'
name|'zero_byte_only_at_fps'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'zero_byte_fps'"
op|','
number|'0'
op|')'
newline|'\n'
name|'device_dirs'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'device_dirs'"
op|')'
newline|'\n'
name|'worker'
op|'='
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'rcache'
op|','
nl|'\n'
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'zero_byte_only_at_fps'
op|'='
name|'zero_byte_only_at_fps'
op|')'
newline|'\n'
name|'worker'
op|'.'
name|'audit_all_objects'
op|'('
name|'mode'
op|'='
name|'mode'
op|','
name|'device_dirs'
op|'='
name|'device_dirs'
op|')'
newline|'\n'
nl|'\n'
DECL|member|fork_child
dedent|''
name|'def'
name|'fork_child'
op|'('
name|'self'
op|','
name|'zero_byte_fps'
op|'='
name|'False'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Child execution"""'
newline|'\n'
name|'pid'
op|'='
name|'os'
op|'.'
name|'fork'
op|'('
op|')'
newline|'\n'
name|'if'
name|'pid'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'pid'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'if'
name|'zero_byte_fps'
op|':'
newline|'\n'
indent|'                '
name|'kwargs'
op|'['
string|"'zero_byte_fps'"
op|']'
op|'='
name|'self'
op|'.'
name|'conf_zero_byte_fps'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'run_audit'
op|'('
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|'"ERROR: Unable to run auditing: %s"'
op|')'
op|'%'
name|'e'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'sys'
op|'.'
name|'exit'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|audit_loop
dedent|''
dedent|''
dedent|''
name|'def'
name|'audit_loop'
op|'('
name|'self'
op|','
name|'parent'
op|','
name|'zbo_fps'
op|','
name|'override_devices'
op|'='
name|'None'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Parallel audit loop"""'
newline|'\n'
name|'self'
op|'.'
name|'clear_recon_cache'
op|'('
string|"'ALL'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'clear_recon_cache'
op|'('
string|"'ZBF'"
op|')'
newline|'\n'
name|'once'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'mode'"
op|')'
op|'=='
string|"'once'"
newline|'\n'
name|'kwargs'
op|'['
string|"'device_dirs'"
op|']'
op|'='
name|'override_devices'
newline|'\n'
name|'if'
name|'parent'
op|':'
newline|'\n'
indent|'            '
name|'kwargs'
op|'['
string|"'zero_byte_fps'"
op|']'
op|'='
name|'zbo_fps'
newline|'\n'
name|'self'
op|'.'
name|'run_audit'
op|'('
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'pids'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
op|':'
newline|'\n'
indent|'                '
name|'zbf_pid'
op|'='
name|'self'
op|'.'
name|'fork_child'
op|'('
name|'zero_byte_fps'
op|'='
name|'True'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'pids'
op|'.'
name|'add'
op|'('
name|'zbf_pid'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'concurrency'
op|'=='
number|'1'
op|':'
newline|'\n'
comment|'# Audit all devices in 1 process'
nl|'\n'
indent|'                '
name|'pids'
op|'.'
name|'add'
op|'('
name|'self'
op|'.'
name|'fork_child'
op|'('
op|'**'
name|'kwargs'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# Divide devices amongst parallel processes set by'
nl|'\n'
comment|'# self.concurrency.  Total number of parallel processes'
nl|'\n'
comment|'# is self.concurrency + 1 if zero_byte_fps.'
nl|'\n'
indent|'                '
name|'parallel_proc'
op|'='
name|'self'
op|'.'
name|'concurrency'
op|'+'
number|'1'
name|'if'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
name|'else'
name|'self'
op|'.'
name|'concurrency'
newline|'\n'
name|'device_list'
op|'='
name|'list'
op|'('
name|'override_devices'
op|')'
name|'if'
name|'override_devices'
name|'else'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
newline|'\n'
name|'shuffle'
op|'('
name|'device_list'
op|')'
newline|'\n'
name|'while'
name|'device_list'
op|':'
newline|'\n'
indent|'                    '
name|'pid'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'pids'
op|')'
op|'=='
name|'parallel_proc'
op|':'
newline|'\n'
indent|'                        '
name|'pid'
op|'='
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'pids'
op|'.'
name|'discard'
op|'('
name|'pid'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
name|'and'
name|'pid'
op|'=='
name|'zbf_pid'
name|'and'
name|'once'
op|':'
newline|'\n'
comment|"# If we're only running one pass and the ZBF scanner"
nl|'\n'
comment|"# finished, don't bother restarting it."
nl|'\n'
indent|'                        '
name|'zbf_pid'
op|'='
op|'-'
number|'100'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
name|'and'
name|'pid'
op|'=='
name|'zbf_pid'
op|':'
newline|'\n'
comment|"# When we're running forever, the ZBF scanner must"
nl|'\n'
comment|'# be restarted as soon as it finishes.'
nl|'\n'
indent|'                        '
name|'kwargs'
op|'['
string|"'device_dirs'"
op|']'
op|'='
name|'override_devices'
newline|'\n'
comment|'# sleep between ZBF scanner forks'
nl|'\n'
name|'self'
op|'.'
name|'_sleep'
op|'('
op|')'
newline|'\n'
name|'zbf_pid'
op|'='
name|'self'
op|'.'
name|'fork_child'
op|'('
name|'zero_byte_fps'
op|'='
name|'True'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'pids'
op|'.'
name|'add'
op|'('
name|'zbf_pid'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'kwargs'
op|'['
string|"'device_dirs'"
op|']'
op|'='
op|'['
name|'device_list'
op|'.'
name|'pop'
op|'('
op|')'
op|']'
newline|'\n'
name|'pids'
op|'.'
name|'add'
op|'('
name|'self'
op|'.'
name|'fork_child'
op|'('
op|'**'
name|'kwargs'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'while'
name|'pids'
op|':'
newline|'\n'
indent|'                '
name|'pid'
op|'='
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
comment|'# ZBF scanner must be restarted as soon as it finishes'
nl|'\n'
comment|"# unless we're in run-once mode"
nl|'\n'
name|'if'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
name|'and'
name|'pid'
op|'=='
name|'zbf_pid'
name|'and'
name|'len'
op|'('
name|'pids'
op|')'
op|'>'
number|'1'
name|'and'
name|'not'
name|'once'
op|':'
newline|'\n'
indent|'                    '
name|'kwargs'
op|'['
string|"'device_dirs'"
op|']'
op|'='
name|'override_devices'
newline|'\n'
comment|'# sleep between ZBF scanner forks'
nl|'\n'
name|'self'
op|'.'
name|'_sleep'
op|'('
op|')'
newline|'\n'
name|'zbf_pid'
op|'='
name|'self'
op|'.'
name|'fork_child'
op|'('
name|'zero_byte_fps'
op|'='
name|'True'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'pids'
op|'.'
name|'add'
op|'('
name|'zbf_pid'
op|')'
newline|'\n'
dedent|''
name|'pids'
op|'.'
name|'discard'
op|'('
name|'pid'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
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
string|'"""Run the object audit until stopped."""'
newline|'\n'
comment|'# zero byte only command line option'
nl|'\n'
name|'zbo_fps'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'zero_byte_fps'"
op|','
number|'0'
op|')'
newline|'\n'
name|'parent'
op|'='
name|'False'
newline|'\n'
name|'if'
name|'zbo_fps'
op|':'
newline|'\n'
comment|'# only start parent'
nl|'\n'
indent|'            '
name|'parent'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'kwargs'
op|'='
op|'{'
string|"'mode'"
op|':'
string|"'forever'"
op|'}'
newline|'\n'
nl|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'audit_loop'
op|'('
name|'parent'
op|','
name|'zbo_fps'
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
name|'as'
name|'err'
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
string|"'ERROR auditing: %s'"
op|')'
op|','
name|'err'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_sleep'
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
string|'"""Run the object audit once"""'
newline|'\n'
comment|'# zero byte only command line option'
nl|'\n'
name|'zbo_fps'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'zero_byte_fps'"
op|','
number|'0'
op|')'
newline|'\n'
name|'override_devices'
op|'='
name|'list_from_csv'
op|'('
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'devices'"
op|')'
op|')'
newline|'\n'
comment|'# Remove bogus entries and duplicates from override_devices'
nl|'\n'
name|'override_devices'
op|'='
name|'list'
op|'('
nl|'\n'
name|'set'
op|'('
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
op|')'
op|'.'
name|'intersection'
op|'('
name|'set'
op|'('
name|'override_devices'
op|')'
op|')'
op|')'
newline|'\n'
name|'parent'
op|'='
name|'False'
newline|'\n'
name|'if'
name|'zbo_fps'
op|':'
newline|'\n'
comment|'# only start parent'
nl|'\n'
indent|'            '
name|'parent'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'kwargs'
op|'='
op|'{'
string|"'mode'"
op|':'
string|"'once'"
op|'}'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'audit_loop'
op|'('
name|'parent'
op|','
name|'zbo_fps'
op|','
name|'override_devices'
op|'='
name|'override_devices'
op|','
nl|'\n'
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
name|'as'
name|'err'
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
string|"'ERROR auditing: %s'"
op|')'
op|','
name|'err'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
