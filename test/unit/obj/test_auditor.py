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
comment|'# TODO: Tests'
nl|'\n'
nl|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'tempfile'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'auditor'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'server'
name|'import'
name|'DiskFile'
op|','
name|'write_metadata'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'hash_path'
op|','
name|'mkdirs'
op|','
name|'normalize_timestamp'
op|','
name|'renamer'
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
name|'exceptions'
name|'import'
name|'AuditException'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAuditor
name|'class'
name|'TestAuditor'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|setUp
indent|'    '
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Setup a test ring (stolen from common/test_ring.py)'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'path_to_test_xfs'
op|'='
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'PATH_TO_TEST_XFS'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'path_to_test_xfs'
name|'or'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'self'
op|'.'
name|'path_to_test_xfs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'print'
op|'>>'
name|'sys'
op|'.'
name|'stderr'
op|','
string|"'WARNING: PATH_TO_TEST_XFS not set or not '"
string|"'pointing to a valid directory.\\n'"
string|"'Please set PATH_TO_TEST_XFS to a directory on an XFS file '"
string|"'system for testing.'"
newline|'\n'
name|'self'
op|'.'
name|'testdir'
op|'='
string|"'/tmp/SWIFTUNITTEST'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'testdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'path_to_test_xfs'
op|','
nl|'\n'
string|"'tmp_test_object_auditor'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'devices'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'node'"
op|')'
newline|'\n'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
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
string|"'sda'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'objects'
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
string|"'sda'"
op|','
string|"'objects'"
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'mkdir'
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
string|"'sdb'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'objects_2'
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
string|"'sdb'"
op|','
string|"'objects'"
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'objects'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'parts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part'
name|'in'
op|'['
string|"'0'"
op|','
string|"'1'"
op|','
string|"'2'"
op|','
string|"'3'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'parts'
op|'['
name|'part'
op|']'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'objects'
op|','
name|'part'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'objects'
op|','
name|'part'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'conf'
op|'='
name|'dict'
op|'('
nl|'\n'
name|'devices'
op|'='
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'mount_check'
op|'='
string|"'false'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_extra_data
dedent|''
name|'def'
name|'test_object_audit_extra_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'cur_part'
op|'='
string|"'0'"
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'disk_file'
op|'.'
name|'put'
op|'('
name|'fd'
op|','
name|'tmppath'
op|','
name|'metadata'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
name|'cur_part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
string|"'extra_data'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
name|'cur_part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_diff_data
dedent|''
dedent|''
name|'def'
name|'test_object_audit_diff_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'cur_part'
op|'='
string|"'0'"
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'disk_file'
op|'.'
name|'put'
op|'('
name|'fd'
op|','
name|'tmppath'
op|','
name|'metadata'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
name|'cur_part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
string|"'1'"
op|'+'
string|"'0'"
op|'*'
number|'1023'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|'='
name|'etag'
newline|'\n'
name|'write_metadata'
op|'('
name|'fd'
op|','
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
name|'cur_part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_no_meta
dedent|''
dedent|''
name|'def'
name|'test_object_audit_no_meta'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'cur_part'
op|'='
string|"'0'"
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'fsync'
op|'('
name|'fd'
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
name|'disk_file'
op|'.'
name|'datadir'
op|')'
op|')'
newline|'\n'
name|'renamer'
op|'('
name|'tmppath'
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'disk_file'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
name|'cur_part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_bad_args
dedent|''
dedent|''
name|'def'
name|'test_object_audit_bad_args'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'pre_errors'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'errors'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
number|'5'
op|','
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'errors'
op|','
name|'pre_errors'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'pre_errors'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'errors'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
string|"'badpath'"
op|','
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'errors'
op|','
name|'pre_errors'
op|')'
comment|'# just returns'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_once_pass
dedent|''
name|'def'
name|'test_object_run_once_pass'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'log_time'
op|'='
number|'0'
newline|'\n'
name|'cur_part'
op|'='
string|"'0'"
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'disk_file'
op|'.'
name|'put'
op|'('
name|'fd'
op|','
name|'tmppath'
op|','
name|'metadata'
op|')'
newline|'\n'
name|'disk_file'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_once_no_sda
dedent|''
name|'def'
name|'test_object_run_once_no_sda'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'cur_part'
op|'='
string|"'0'"
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sdb'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'disk_file'
op|'.'
name|'put'
op|'('
name|'fd'
op|','
name|'tmppath'
op|','
name|'metadata'
op|')'
newline|'\n'
name|'disk_file'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
string|"'extra_data'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_once_multi_devices
dedent|''
name|'def'
name|'test_object_run_once_multi_devices'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'cur_part'
op|'='
string|"'0'"
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'10'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'disk_file'
op|'.'
name|'put'
op|'('
name|'fd'
op|','
name|'tmppath'
op|','
name|'metadata'
op|')'
newline|'\n'
name|'disk_file'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sdb'"
op|','
name|'cur_part'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'ob'"
op|')'
newline|'\n'
name|'data'
op|'='
string|"'1'"
op|'*'
number|'10'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'disk_file'
op|'.'
name|'mkstemp'
op|'('
op|')'
name|'as'
op|'('
name|'fd'
op|','
name|'tmppath'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'disk_file'
op|'.'
name|'put'
op|'('
name|'fd'
op|','
name|'tmppath'
op|','
name|'metadata'
op|')'
newline|'\n'
name|'disk_file'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'os'
op|'.'
name|'write'
op|'('
name|'fd'
op|','
string|"'extra_data'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
