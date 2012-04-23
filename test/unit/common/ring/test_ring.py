begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack, LLC.'
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
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'unittest'
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
name|'from'
name|'time'
name|'import'
name|'sleep'
op|','
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'ring'
op|','
name|'utils'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestRingData
name|'class'
name|'TestRingData'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_attrs
indent|'    '
name|'def'
name|'test_attrs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'r2p2d'
op|'='
op|'['
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|','
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|']'
newline|'\n'
name|'d'
op|'='
op|'['
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'zone'"
op|':'
number|'0'
op|'}'
op|','
op|'{'
string|"'id'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|'}'
op|']'
newline|'\n'
name|'s'
op|'='
number|'30'
newline|'\n'
name|'rd'
op|'='
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'r2p2d'
op|','
name|'d'
op|','
name|'s'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rd'
op|'.'
name|'_replica2part2dev_id'
op|','
name|'r2p2d'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rd'
op|'.'
name|'devs'
op|','
name|'d'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rd'
op|'.'
name|'_part_shift'
op|','
name|'s'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pickleable
dedent|''
name|'def'
name|'test_pickleable'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rd'
op|'='
name|'ring'
op|'.'
name|'RingData'
op|'('
op|'['
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|','
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|']'
op|','
nl|'\n'
op|'['
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'zone'"
op|':'
number|'0'
op|'}'
op|','
op|'{'
string|"'id'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|'}'
op|']'
op|','
number|'30'
op|')'
newline|'\n'
name|'for'
name|'p'
name|'in'
name|'xrange'
op|'('
name|'pickle'
op|'.'
name|'HIGHEST_PROTOCOL'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'pickle'
op|'.'
name|'dumps'
op|'('
name|'rd'
op|','
name|'protocol'
op|'='
name|'p'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestRing
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestRing'
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
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'__file__'
op|')'
op|','
string|"'ring'"
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
name|'self'
op|'.'
name|'testgz'
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
string|"'whatever.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'intended_replica2part2dev_id'
op|'='
op|'['
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|','
nl|'\n'
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|','
nl|'\n'
op|'['
number|'3'
op|','
number|'4'
op|','
number|'3'
op|','
number|'4'
op|']'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'='
op|'['
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.1.1'"
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.1.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|','
nl|'\n'
name|'None'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.2.1'"
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.2.2'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'intended_part_shift'
op|'='
number|'30'
newline|'\n'
name|'self'
op|'.'
name|'intended_reload_time'
op|'='
number|'15'
newline|'\n'
name|'pickle'
op|'.'
name|'dump'
op|'('
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'self'
op|'.'
name|'intended_replica2part2dev_id'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|','
name|'self'
op|'.'
name|'intended_part_shift'
op|')'
op|','
nl|'\n'
name|'GzipFile'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
string|"'wb'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
name|'reload_time'
op|'='
name|'self'
op|'.'
name|'intended_reload_time'
op|','
name|'ring_name'
op|'='
string|"'whatever'"
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
DECL|member|test_creation
dedent|''
name|'def'
name|'test_creation'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_replica2part2dev_id'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_replica2part2dev_id'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_part_shift'
op|','
name|'self'
op|'.'
name|'intended_part_shift'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|','
name|'self'
op|'.'
name|'intended_devs'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'reload_time'
op|','
name|'self'
op|'.'
name|'intended_reload_time'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'pickle_gz_path'
op|','
name|'self'
op|'.'
name|'testgz'
op|')'
newline|'\n'
comment|'# test invalid endcap'
nl|'\n'
name|'_orig_hash_path_suffix'
op|'='
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'SystemExit'
op|','
name|'ring'
op|'.'
name|'Ring'
op|','
name|'self'
op|'.'
name|'testdir'
op|','
string|"'whatever'"
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
op|'='
name|'_orig_hash_path_suffix'
newline|'\n'
nl|'\n'
DECL|member|test_has_changed
dedent|''
dedent|''
name|'def'
name|'test_has_changed'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'has_changed'
op|'('
op|')'
op|','
name|'False'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'utime'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
op|'('
name|'time'
op|'('
op|')'
op|'+'
number|'60'
op|','
name|'time'
op|'('
op|')'
op|'+'
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'has_changed'
op|'('
op|')'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_reload
dedent|''
name|'def'
name|'test_reload'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'os'
op|'.'
name|'utime'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'300'
op|','
name|'time'
op|'('
op|')'
op|'-'
number|'300'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'reload_time'
op|'='
number|'0.001'
op|','
nl|'\n'
name|'ring_name'
op|'='
string|"'whatever'"
op|')'
newline|'\n'
name|'orig_mtime'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_mtime'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
number|'5'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'.'
name|'append'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'3'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|'}'
op|')'
newline|'\n'
name|'pickle'
op|'.'
name|'dump'
op|'('
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'self'
op|'.'
name|'intended_replica2part2dev_id'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|','
name|'self'
op|'.'
name|'intended_part_shift'
op|')'
op|','
nl|'\n'
name|'GzipFile'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
string|"'wb'"
op|')'
op|')'
newline|'\n'
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
number|'6'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_mtime'
op|','
name|'orig_mtime'
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'utime'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'300'
op|','
name|'time'
op|'('
op|')'
op|'-'
number|'300'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'reload_time'
op|'='
number|'0.001'
op|','
nl|'\n'
name|'ring_name'
op|'='
string|"'whatever'"
op|')'
newline|'\n'
name|'orig_mtime'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_mtime'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
number|'6'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'.'
name|'append'
op|'('
op|'{'
string|"'id'"
op|':'
number|'5'
op|','
string|"'zone'"
op|':'
number|'4'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|'}'
op|')'
newline|'\n'
name|'pickle'
op|'.'
name|'dump'
op|'('
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'self'
op|'.'
name|'intended_replica2part2dev_id'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|','
name|'self'
op|'.'
name|'intended_part_shift'
op|')'
op|','
nl|'\n'
name|'GzipFile'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
string|"'wb'"
op|')'
op|')'
newline|'\n'
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_part_nodes'
op|'('
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
number|'7'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_mtime'
op|','
name|'orig_mtime'
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'utime'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
op|'('
name|'time'
op|'('
op|')'
op|'-'
number|'300'
op|','
name|'time'
op|'('
op|')'
op|'-'
number|'300'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'reload_time'
op|'='
number|'0.001'
op|','
nl|'\n'
name|'ring_name'
op|'='
string|"'whatever'"
op|')'
newline|'\n'
name|'orig_mtime'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_mtime'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
number|'7'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'.'
name|'append'
op|'('
op|'{'
string|"'id'"
op|':'
number|'6'
op|','
string|"'zone'"
op|':'
number|'5'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|'}'
op|')'
newline|'\n'
name|'pickle'
op|'.'
name|'dump'
op|'('
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'self'
op|'.'
name|'intended_replica2part2dev_id'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|','
name|'self'
op|'.'
name|'intended_part_shift'
op|')'
op|','
nl|'\n'
name|'GzipFile'
op|'('
name|'self'
op|'.'
name|'testgz'
op|','
string|"'wb'"
op|')'
op|')'
newline|'\n'
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
number|'8'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEquals'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_mtime'
op|','
name|'orig_mtime'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_part_nodes
dedent|''
name|'def'
name|'test_get_part_nodes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_part_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_nodes
dedent|''
name|'def'
name|'test_get_nodes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Yes, these tests are deliberately very fragile. We want to make sure'
nl|'\n'
comment|'# that if someones changes the results the ring produces, they know it.'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'TypeError'
op|','
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|')'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'aa'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c3'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o5'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|add_dev_to_ring
dedent|''
name|'def'
name|'add_dev_to_ring'
op|'('
name|'self'
op|','
name|'new_dev'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|'.'
name|'append'
op|'('
name|'new_dev'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_rebuild_tier_data'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_more_nodes
dedent|''
name|'def'
name|'test_get_more_nodes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Yes, these tests are deliberately very fragile. We want to make sure'
nl|'\n'
comment|'# that if someone changes the results the ring produces, they know it.'
nl|'\n'
indent|'        '
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'new_dev'
op|'='
op|'{'
string|"'id'"
op|':'
number|'5'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.1.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'add_dev_to_ring'
op|'('
name|'new_dev'
op|')'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'new_dev'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|'['
number|'5'
op|']'
op|'['
string|"'zone'"
op|']'
op|'='
number|'3'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'_rebuild_tier_data'
op|'('
op|')'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'new_dev'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|'.'
name|'append'
op|'('
name|'None'
op|')'
newline|'\n'
name|'new_dev2'
op|'='
op|'{'
string|"'id'"
op|':'
number|'6'
op|','
string|"'zone'"
op|':'
number|'6'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.6.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'add_dev_to_ring'
op|'('
name|'new_dev2'
op|')'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'part'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'3'
op|']'
op|']'
op|')'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'new_dev'
op|','
nl|'\n'
name|'new_dev2'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'new_dev3'
op|'='
op|'{'
string|"'id'"
op|':'
number|'7'
op|','
string|"'zone'"
op|':'
number|'7'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.7.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'add_dev_to_ring'
op|'('
name|'new_dev3'
op|')'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'new_dev'
op|','
name|'new_dev2'
op|','
name|'new_dev3'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
name|'new_dev3'
op|'['
string|"'weight'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'new_dev'
op|','
name|'new_dev2'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ring'
op|'.'
name|'devs'
op|'['
number|'7'
op|']'
op|'['
string|"'weight'"
op|']'
op|'='
number|'1.0'
newline|'\n'
nl|'\n'
name|'new_dev4'
op|'='
op|'{'
string|"'id'"
op|':'
number|'8'
op|','
string|"'zone'"
op|':'
number|'8'
op|','
string|"'weight'"
op|':'
number|'0.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.8.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'add_dev_to_ring'
op|'('
name|'new_dev4'
op|')'
newline|'\n'
name|'nodes'
op|'='
name|'list'
op|'('
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'nodes'
op|','
op|'['
name|'new_dev'
op|','
name|'new_dev2'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'4'
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'intended_devs'
op|'['
number|'1'
op|']'
op|']'
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
