begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack, LLC.'
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
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
nl|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'closing'
newline|'\n'
name|'from'
name|'gzip'
name|'import'
name|'GzipFile'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'tempfile'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeLogger'
op|','
name|'mock'
name|'as'
name|'unit_mock'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
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
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'base'
name|'as'
name|'object_base'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'server'
name|'import'
name|'DiskFile'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_create_test_ring
name|'def'
name|'_create_test_ring'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'testgz'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'path'
op|','
string|"'object.ring.gz'"
op|')'
newline|'\n'
name|'intended_replica2part2dev_id'
op|'='
op|'['
nl|'\n'
op|'['
number|'0'
op|','
number|'1'
op|','
number|'2'
op|','
number|'3'
op|','
number|'4'
op|','
number|'5'
op|','
number|'6'
op|']'
op|','
nl|'\n'
op|'['
number|'1'
op|','
number|'2'
op|','
number|'3'
op|','
number|'0'
op|','
number|'5'
op|','
number|'6'
op|','
number|'4'
op|']'
op|','
nl|'\n'
op|'['
number|'2'
op|','
number|'3'
op|','
number|'0'
op|','
number|'1'
op|','
number|'6'
op|','
number|'4'
op|','
number|'5'
op|']'
op|']'
newline|'\n'
name|'intended_devs'
op|'='
op|'['
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.0'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'1'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'2'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.2'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'4'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.3'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'4'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'5'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.4'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'5'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'6'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'fe80::202:b3ff:fe1e:8329'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'6'
op|','
string|"'device'"
op|':'
string|"'sda'"
op|','
string|"'zone'"
op|':'
number|'7'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'2001:0db8:85a3:0000:0000:8a2e:0370:7334'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|']'
newline|'\n'
name|'intended_part_shift'
op|'='
number|'30'
newline|'\n'
name|'intended_reload_time'
op|'='
number|'15'
newline|'\n'
name|'with'
name|'closing'
op|'('
name|'GzipFile'
op|'('
name|'testgz'
op|','
string|"'wb'"
op|')'
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'        '
name|'pickle'
op|'.'
name|'dump'
op|'('
nl|'\n'
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'intended_replica2part2dev_id'
op|','
name|'intended_devs'
op|','
nl|'\n'
name|'intended_part_shift'
op|')'
op|','
nl|'\n'
name|'f'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'path'
op|','
name|'ring_name'
op|'='
string|"'object'"
op|','
nl|'\n'
name|'reload_time'
op|'='
name|'intended_reload_time'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectBase
dedent|''
name|'class'
name|'TestObjectBase'
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
indent|'        '
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
op|'='
string|"'endcap'"
newline|'\n'
name|'utils'
op|'.'
name|'HASH_PATH_PREFIX'
op|'='
string|"''"
newline|'\n'
comment|'# Setup a test ring (stolen from common/test_ring.py)'
nl|'\n'
name|'self'
op|'.'
name|'testdir'
op|'='
name|'tempfile'
op|'.'
name|'mkdtemp'
op|'('
op|')'
newline|'\n'
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
dedent|''
name|'self'
op|'.'
name|'ring'
op|'='
name|'_create_test_ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
name|'dict'
op|'('
nl|'\n'
name|'swift_dir'
op|'='
name|'self'
op|'.'
name|'testdir'
op|','
name|'devices'
op|'='
name|'self'
op|'.'
name|'devices'
op|','
name|'mount_check'
op|'='
string|"'false'"
op|','
nl|'\n'
name|'timeout'
op|'='
string|"'300'"
op|','
name|'stats_interval'
op|'='
string|"'1'"
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
DECL|member|test_hash_suffix_hash_dir_is_file_quarantine
dedent|''
name|'def'
name|'test_hash_suffix_hash_dir_is_file_quarantine'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
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
name|'open'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
string|"'wb'"
op|')'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'ohash'
op|'='
name|'hash_path'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data_dir'
op|'='
name|'ohash'
op|'['
op|'-'
number|'3'
op|':'
op|']'
newline|'\n'
name|'whole_path_from'
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
string|"'0'"
op|','
name|'data_dir'
op|')'
newline|'\n'
name|'orig_quarantine_renamer'
op|'='
name|'object_base'
op|'.'
name|'quarantine_renamer'
newline|'\n'
name|'called'
op|'='
op|'['
name|'False'
op|']'
newline|'\n'
nl|'\n'
DECL|function|wrapped
name|'def'
name|'wrapped'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'called'
op|'['
number|'0'
op|']'
op|'='
name|'True'
newline|'\n'
name|'return'
name|'orig_quarantine_renamer'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'object_base'
op|'.'
name|'quarantine_renamer'
op|'='
name|'wrapped'
newline|'\n'
name|'object_base'
op|'.'
name|'hash_suffix'
op|'('
name|'whole_path_from'
op|','
number|'101'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'object_base'
op|'.'
name|'quarantine_renamer'
op|'='
name|'orig_quarantine_renamer'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'called'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_hash_suffix_one_file
dedent|''
name|'def'
name|'test_hash_suffix_one_file'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'f'
op|'='
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
number|'100'
op|')'
op|'+'
string|"'.ts'"
op|')'
op|','
nl|'\n'
string|"'wb'"
op|')'
newline|'\n'
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
name|'f'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'ohash'
op|'='
name|'hash_path'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data_dir'
op|'='
name|'ohash'
op|'['
op|'-'
number|'3'
op|':'
op|']'
newline|'\n'
name|'whole_path_from'
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
string|"'0'"
op|','
name|'data_dir'
op|')'
newline|'\n'
name|'object_base'
op|'.'
name|'hash_suffix'
op|'('
name|'whole_path_from'
op|','
number|'101'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'parts'
op|'['
string|"'0'"
op|']'
op|')'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
name|'object_base'
op|'.'
name|'hash_suffix'
op|'('
name|'whole_path_from'
op|','
number|'99'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'parts'
op|'['
string|"'0'"
op|']'
op|')'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_hash_suffix_multi_file_one
dedent|''
name|'def'
name|'test_hash_suffix_multi_file_one'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'for'
name|'tdiff'
name|'in'
op|'['
number|'1'
op|','
number|'50'
op|','
number|'100'
op|','
number|'500'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'suff'
name|'in'
op|'['
string|"'.meta'"
op|','
string|"'.data'"
op|','
string|"'.ts'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'f'
op|'='
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'df'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'normalize_timestamp'
op|'('
name|'int'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'-'
name|'tdiff'
op|')'
op|'+'
name|'suff'
op|')'
op|','
nl|'\n'
string|"'wb'"
op|')'
newline|'\n'
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
name|'f'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'ohash'
op|'='
name|'hash_path'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data_dir'
op|'='
name|'ohash'
op|'['
op|'-'
number|'3'
op|':'
op|']'
newline|'\n'
name|'whole_path_from'
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
string|"'0'"
op|','
name|'data_dir'
op|')'
newline|'\n'
name|'hsh_path'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'whole_path_from'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'whole_hsh_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'whole_path_from'
op|','
name|'hsh_path'
op|')'
newline|'\n'
nl|'\n'
name|'object_base'
op|'.'
name|'hash_suffix'
op|'('
name|'whole_path_from'
op|','
number|'99'
op|')'
newline|'\n'
comment|'# only the tombstone should be left'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'whole_hsh_path'
op|')'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_hash_suffix_multi_file_two
dedent|''
name|'def'
name|'test_hash_suffix_multi_file_two'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'for'
name|'tdiff'
name|'in'
op|'['
number|'1'
op|','
number|'50'
op|','
number|'100'
op|','
number|'500'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'suffs'
op|'='
op|'['
string|"'.meta'"
op|','
string|"'.data'"
op|']'
newline|'\n'
name|'if'
name|'tdiff'
op|'>'
number|'50'
op|':'
newline|'\n'
indent|'                '
name|'suffs'
op|'.'
name|'append'
op|'('
string|"'.ts'"
op|')'
newline|'\n'
dedent|''
name|'for'
name|'suff'
name|'in'
name|'suffs'
op|':'
newline|'\n'
indent|'                '
name|'f'
op|'='
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'df'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'normalize_timestamp'
op|'('
name|'int'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'-'
name|'tdiff'
op|')'
op|'+'
name|'suff'
op|')'
op|','
nl|'\n'
string|"'wb'"
op|')'
newline|'\n'
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
name|'f'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'ohash'
op|'='
name|'hash_path'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data_dir'
op|'='
name|'ohash'
op|'['
op|'-'
number|'3'
op|':'
op|']'
newline|'\n'
name|'whole_path_from'
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
string|"'0'"
op|','
name|'data_dir'
op|')'
newline|'\n'
name|'hsh_path'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'whole_path_from'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'whole_hsh_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'whole_path_from'
op|','
name|'hsh_path'
op|')'
newline|'\n'
nl|'\n'
name|'object_base'
op|'.'
name|'hash_suffix'
op|'('
name|'whole_path_from'
op|','
number|'99'
op|')'
newline|'\n'
comment|'# only the meta and data should be left'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'whole_hsh_path'
op|')'
op|')'
op|','
number|'2'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_invalidate_hash
dedent|''
name|'def'
name|'test_invalidate_hash'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|assertFileData
indent|'        '
name|'def'
name|'assertFileData'
op|'('
name|'file_path'
op|','
name|'data'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
name|'file_path'
op|','
string|"'r'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
indent|'                '
name|'fdata'
op|'='
name|'fp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'fdata'
op|')'
op|','
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'data'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'ohash'
op|'='
name|'hash_path'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'data_dir'
op|'='
name|'ohash'
op|'['
op|'-'
number|'3'
op|':'
op|']'
newline|'\n'
name|'whole_path_from'
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
string|"'0'"
op|','
name|'data_dir'
op|')'
newline|'\n'
name|'hashes_file'
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
string|"'0'"
op|','
nl|'\n'
name|'object_base'
op|'.'
name|'HASH_FILE'
op|')'
newline|'\n'
comment|'# test that non existent file except caught'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'object_base'
op|'.'
name|'invalidate_hash'
op|'('
name|'whole_path_from'
op|')'
op|','
nl|'\n'
name|'None'
op|')'
newline|'\n'
comment|'# test that hashes get cleared'
nl|'\n'
name|'check_pickle_data'
op|'='
name|'pickle'
op|'.'
name|'dumps'
op|'('
op|'{'
name|'data_dir'
op|':'
name|'None'
op|'}'
op|','
nl|'\n'
name|'object_base'
op|'.'
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
name|'for'
name|'data_hash'
name|'in'
op|'['
op|'{'
name|'data_dir'
op|':'
name|'None'
op|'}'
op|','
op|'{'
name|'data_dir'
op|':'
string|"'abcdefg'"
op|'}'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
name|'hashes_file'
op|','
string|"'wb'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
indent|'                '
name|'pickle'
op|'.'
name|'dump'
op|'('
name|'data_hash'
op|','
name|'fp'
op|','
name|'object_base'
op|'.'
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
dedent|''
name|'object_base'
op|'.'
name|'invalidate_hash'
op|'('
name|'whole_path_from'
op|')'
newline|'\n'
name|'assertFileData'
op|'('
name|'hashes_file'
op|','
name|'check_pickle_data'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_hashes
dedent|''
dedent|''
name|'def'
name|'test_get_hashes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'+'
string|"'.ts'"
op|')'
op|','
nl|'\n'
string|"'wb'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
dedent|''
name|'part'
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
string|"'0'"
op|')'
newline|'\n'
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
name|'part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'hashed'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'a83'"
name|'in'
name|'hashes'
op|')'
newline|'\n'
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
name|'part'
op|','
name|'do_listdir'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'hashed'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'a83'"
name|'in'
name|'hashes'
op|')'
newline|'\n'
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
name|'part'
op|','
name|'recalculate'
op|'='
op|'['
string|"'a83'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'hashed'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'a83'"
name|'in'
name|'hashes'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_hashes_bad_dir
dedent|''
name|'def'
name|'test_get_hashes_bad_dir'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'with'
name|'open'
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
string|"'0'"
op|','
string|"'bad'"
op|')'
op|','
string|"'wb'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
dedent|''
name|'part'
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
string|"'0'"
op|')'
newline|'\n'
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
name|'part'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'hashed'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'a83'"
name|'in'
name|'hashes'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'bad'"
name|'not'
name|'in'
name|'hashes'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_hashes_unmodified
dedent|''
name|'def'
name|'test_get_hashes_unmodified'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'+'
string|"'.ts'"
op|')'
op|','
nl|'\n'
string|"'wb'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
dedent|''
name|'part'
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
string|"'0'"
op|')'
newline|'\n'
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
name|'part'
op|')'
newline|'\n'
name|'i'
op|'='
op|'['
number|'0'
op|']'
newline|'\n'
nl|'\n'
DECL|function|getmtime
name|'def'
name|'getmtime'
op|'('
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'['
number|'0'
op|']'
op|'+='
number|'1'
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'with'
name|'unit_mock'
op|'('
op|'{'
string|"'os.path.getmtime'"
op|':'
name|'getmtime'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
nl|'\n'
name|'part'
op|','
name|'recalculate'
op|'='
op|'['
string|"'a83'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'i'
op|'['
number|'0'
op|']'
op|','
number|'2'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_hashes_unmodified_and_zero_bytes
dedent|''
name|'def'
name|'test_get_hashes_unmodified_and_zero_bytes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'part'
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
string|"'0'"
op|')'
newline|'\n'
name|'open'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'part'
op|','
name|'object_base'
op|'.'
name|'HASH_FILE'
op|')'
op|','
string|"'w'"
op|')'
newline|'\n'
comment|'# Now the hash file is zero bytes.'
nl|'\n'
name|'i'
op|'='
op|'['
number|'0'
op|']'
newline|'\n'
nl|'\n'
DECL|function|getmtime
name|'def'
name|'getmtime'
op|'('
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'['
number|'0'
op|']'
op|'+='
number|'1'
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'with'
name|'unit_mock'
op|'('
op|'{'
string|"'os.path.getmtime'"
op|':'
name|'getmtime'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
nl|'\n'
name|'part'
op|','
name|'recalculate'
op|'='
op|'['
op|']'
op|')'
newline|'\n'
comment|'# getmtime will actually not get called.  Initially, the pickle.load'
nl|'\n'
comment|'# will raise an exception first and later, force_rewrite will'
nl|'\n'
comment|'# short-circuit the if clause to determine whether to write out a fresh'
nl|'\n'
comment|'# hashes_file.'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'i'
op|'['
number|'0'
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'a83'"
name|'in'
name|'hashes'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_hashes_modified
dedent|''
name|'def'
name|'test_get_hashes_modified'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'df'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'+'
string|"'.ts'"
op|')'
op|','
nl|'\n'
string|"'wb'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'write'
op|'('
string|"'1234567890'"
op|')'
newline|'\n'
dedent|''
name|'part'
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
string|"'0'"
op|')'
newline|'\n'
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
name|'part'
op|')'
newline|'\n'
name|'i'
op|'='
op|'['
number|'0'
op|']'
newline|'\n'
nl|'\n'
DECL|function|getmtime
name|'def'
name|'getmtime'
op|'('
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'i'
op|'['
number|'0'
op|']'
op|'<'
number|'3'
op|':'
newline|'\n'
indent|'                '
name|'i'
op|'['
number|'0'
op|']'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'return'
name|'i'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'with'
name|'unit_mock'
op|'('
op|'{'
string|"'os.path.getmtime'"
op|':'
name|'getmtime'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'hashed'
op|','
name|'hashes'
op|'='
name|'object_base'
op|'.'
name|'get_hashes'
op|'('
nl|'\n'
name|'part'
op|','
name|'recalculate'
op|'='
op|'['
string|"'a83'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'i'
op|'['
number|'0'
op|']'
op|','
number|'3'
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
