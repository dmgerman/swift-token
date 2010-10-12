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
name|'socket'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'choice'
op|','
name|'random'
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
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'server'
name|'as'
name|'object_server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'replicator'
name|'import'
name|'invalidate_hash'
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
name|'renamer'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'AuditException'
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
DECL|class|ObjectAuditor
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
name|'mount_check'
op|'='
name|'conf'
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
nl|'\n'
DECL|member|DiskFile_generator
dedent|''
name|'def'
name|'DiskFile_generator'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
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
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
string|"'Skipping %s as it is not mounted'"
op|'%'
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'datadir'
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
nl|'\n'
name|'object_server'
op|'.'
name|'DATADIR'
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
name|'datadir'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'partitions'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'datadir'
op|')'
newline|'\n'
name|'for'
name|'partition'
name|'in'
name|'partitions'
op|':'
newline|'\n'
indent|'                '
name|'part_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'datadir'
op|','
name|'partition'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'part_path'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'suffixes'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'part_path'
op|')'
newline|'\n'
name|'for'
name|'suffix'
name|'in'
name|'suffixes'
op|':'
newline|'\n'
indent|'                    '
name|'suff_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'part_path'
op|','
name|'suffix'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'suff_path'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'continue'
newline|'\n'
dedent|''
name|'hashes'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'suff_path'
op|')'
newline|'\n'
name|'for'
name|'hsh'
name|'in'
name|'hashes'
op|':'
newline|'\n'
indent|'                        '
name|'hash_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'suff_path'
op|','
name|'hsh'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'hash_path'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'continue'
newline|'\n'
dedent|''
name|'name'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'fname'
name|'in'
name|'sorted'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'hash_path'
op|')'
op|','
nl|'\n'
name|'reverse'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'if'
name|'fname'
op|'.'
name|'endswith'
op|'('
string|"'.ts'"
op|')'
op|':'
newline|'\n'
indent|'                                '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'fname'
op|'.'
name|'endswith'
op|'('
string|"'.data'"
op|')'
op|':'
newline|'\n'
indent|'                                '
name|'name'
op|'='
name|'object_server'
op|'.'
name|'read_metadata'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'hash_path'
op|','
name|'fname'
op|')'
op|')'
op|'['
string|"'name'"
op|']'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'name'
op|':'
newline|'\n'
indent|'                            '
name|'_'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'name'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'3'
op|')'
newline|'\n'
name|'df'
op|'='
name|'object_server'
op|'.'
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'device'
op|','
nl|'\n'
name|'partition'
op|','
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
name|'keep_data_fp'
op|'='
name|'True'
op|')'
newline|'\n'
name|'yield'
name|'df'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'run_forever'
op|'('
name|'self'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'        '
string|'"""Run the object audit until stopped."""'
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
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'all_dfs'
op|'='
name|'self'
op|'.'
name|'DiskFile_generator'
op|'('
op|')'
newline|'\n'
name|'for'
name|'df'
name|'in'
name|'all_dfs'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'object_audit'
op|'('
name|'df'
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
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|"'Since %s: Locally: %d passed audit, %d quarantined, %d '"
nl|'\n'
string|"'errors'"
op|'%'
op|'('
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
name|'self'
op|'.'
name|'passes'
op|','
nl|'\n'
name|'self'
op|'.'
name|'quarantines'
op|','
name|'self'
op|'.'
name|'errors'
op|')'
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
indent|'                    '
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
nl|'\n'
DECL|member|run_once
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Run the object audit once."""'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|'\'Begin object audit "once" mode\''
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
name|'self'
op|'.'
name|'object_audit'
op|'('
name|'self'
op|'.'
name|'DiskFile_generator'
op|'('
op|')'
op|'.'
name|'next'
op|'('
op|')'
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
string|'\'Object audit "once" mode completed: %.02fs\''
op|'%'
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|object_audit
dedent|''
name|'def'
name|'object_audit'
op|'('
name|'self'
op|','
name|'df'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Walk the device, and audit any objects found."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'df'
op|'.'
name|'data_file'
op|')'
op|'!='
name|'int'
op|'('
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'AuditException'
op|'('
string|"'Content-Length of %s does not match '"
nl|'\n'
string|"'file size of %s'"
op|'%'
op|'('
name|'int'
op|'('
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
op|','
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'df'
op|'.'
name|'data_file'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'chunk'
name|'in'
name|'df'
op|':'
newline|'\n'
indent|'                '
name|'etag'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'if'
name|'etag'
op|'!='
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'AuditException'
op|'('
string|'"ETag of %s does not match file\'s md5 of "'
nl|'\n'
string|'"%s"'
op|'%'
op|'('
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|','
name|'etag'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'AuditException'
op|','
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
string|"'ERROR Object %s failed audit and will be '"
nl|'\n'
string|"'quarantined: %s'"
op|'%'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
name|'invalidate_hash'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
op|')'
newline|'\n'
name|'renamer'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
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
nl|'\n'
string|"'quarantined'"
op|','
string|"'objects'"
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
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
string|"'ERROR Trying to audit %s'"
op|'%'
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'passes'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
