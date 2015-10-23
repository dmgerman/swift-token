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
name|'six'
op|'.'
name|'moves'
op|'.'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'mock'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'unittest'
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
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeLogger'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'spawn'
op|','
name|'Timeout'
op|','
name|'listen'
newline|'\n'
nl|'\n'
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
name|'container'
name|'import'
name|'updater'
name|'as'
name|'container_updater'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'backend'
name|'import'
name|'ContainerBroker'
op|','
name|'DATADIR'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'RingData'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'normalize_timestamp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestContainerUpdater
name|'class'
name|'TestContainerUpdater'
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
string|"'startcap'"
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
name|'mkdtemp'
op|'('
op|')'
op|','
string|"'tmp_test_container_updater'"
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
name|'ring_file'
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
string|"'account.ring.gz'"
op|')'
newline|'\n'
name|'with'
name|'closing'
op|'('
name|'GzipFile'
op|'('
name|'ring_file'
op|','
string|"'wb'"
op|')'
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'pickle'
op|'.'
name|'dump'
op|'('
nl|'\n'
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
number|'1'
op|','
number|'0'
op|','
number|'1'
op|','
number|'0'
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
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'12345'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sda1'"
op|','
string|"'zone'"
op|':'
number|'0'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'12345'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sda1'"
op|','
string|"'zone'"
op|':'
number|'2'
op|'}'
op|']'
op|','
number|'30'
op|')'
op|','
nl|'\n'
name|'f'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'devices_dir'
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
string|"'devices'"
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'devices_dir'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'sda1'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices_dir'
op|','
string|"'sda1'"
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'sda1'
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
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
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
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'false'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'2'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'5.'"
op|','
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'hasattr'
op|'('
name|'cu'
op|','
string|"'logger'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'cu'
op|'.'
name|'logger'
name|'is'
name|'not'
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'cu'
op|'.'
name|'devices'
op|','
name|'self'
op|'.'
name|'devices_dir'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'cu'
op|'.'
name|'interval'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'cu'
op|'.'
name|'concurrency'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'cu'
op|'.'
name|'node_timeout'
op|','
number|'5.'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'cu'
op|'.'
name|'get_account_ring'
op|'('
op|')'
name|'is'
name|'not'
name|'None'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'.'
name|'object'
op|'('
name|'container_updater'
op|','
string|"'ismount'"
op|')'
newline|'\n'
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'.'
name|'object'
op|'('
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|','
string|"'container_sweep'"
op|')'
newline|'\n'
DECL|member|test_run_once_with_device_unmounted
name|'def'
name|'test_run_once_with_device_unmounted'
op|'('
name|'self'
op|','
name|'mock_sweep'
op|','
name|'mock_ismount'
op|')'
op|':'
newline|'\n'
nl|'\n'
indent|'        '
name|'mock_ismount'
op|'.'
name|'return_value'
op|'='
name|'False'
newline|'\n'
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'false'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'15'"
op|','
nl|'\n'
string|"'account_suppression_time'"
op|':'
number|'0'
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'containers_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'sda1'
op|','
name|'DATADIR'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'containers_dir'
op|')'
newline|'\n'
name|'partition_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'containers_dir'
op|','
string|'"a"'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'partition_dir'
op|')'
newline|'\n'
nl|'\n'
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'containers_dir'
op|')'
op|')'
comment|'# sanity check'
newline|'\n'
nl|'\n'
comment|'# only called if a partition dir exists'
nl|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'mock_sweep'
op|'.'
name|'called'
op|')'
newline|'\n'
nl|'\n'
name|'mock_sweep'
op|'.'
name|'reset_mock'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'true'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'15'"
op|','
nl|'\n'
string|"'account_suppression_time'"
op|':'
number|'0'
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'log_lines'
op|'='
name|'cu'
op|'.'
name|'logger'
op|'.'
name|'get_lines_for_level'
op|'('
string|"'warning'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'len'
op|'('
name|'log_lines'
op|')'
op|'>'
number|'0'
op|')'
newline|'\n'
name|'msg'
op|'='
string|"'sda1 is not mounted'"
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'log_lines'
op|'['
number|'0'
op|']'
op|','
name|'msg'
op|')'
newline|'\n'
comment|'# Ensure that the container_sweep did not run'
nl|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'mock_sweep'
op|'.'
name|'called'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run_once
dedent|''
name|'def'
name|'test_run_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'false'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'15'"
op|','
nl|'\n'
string|"'account_suppression_time'"
op|':'
number|'0'
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'containers_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'sda1'
op|','
name|'DATADIR'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'containers_dir'
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'containers_dir'
op|')'
op|')'
newline|'\n'
name|'subdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'containers_dir'
op|','
string|"'subdir'"
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'subdir'
op|')'
newline|'\n'
name|'cb'
op|'='
name|'ContainerBroker'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'subdir'
op|','
string|"'hash.db'"
op|')'
op|','
name|'account'
op|'='
string|"'a'"
op|','
nl|'\n'
name|'container'
op|'='
string|"'c'"
op|')'
newline|'\n'
name|'cb'
op|'.'
name|'initialize'
op|'('
name|'normalize_timestamp'
op|'('
number|'1'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'info'
op|'='
name|'cb'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_object_count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_bytes_used'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'cb'
op|'.'
name|'put_object'
op|'('
string|"'o'"
op|','
name|'normalize_timestamp'
op|'('
number|'2'
op|')'
op|','
number|'3'
op|','
string|"'text/plain'"
op|','
nl|'\n'
string|"'68b329da9893e34099c7d8ad5cb9c940'"
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'info'
op|'='
name|'cb'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|','
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_object_count'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_bytes_used'"
op|']'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|function|accept
name|'def'
name|'accept'
op|'('
name|'sock'
op|','
name|'addr'
op|','
name|'return_code'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'Timeout'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'inc'
op|'='
name|'sock'
op|'.'
name|'makefile'
op|'('
string|"'rb'"
op|')'
newline|'\n'
name|'out'
op|'='
name|'sock'
op|'.'
name|'makefile'
op|'('
string|"'wb'"
op|')'
newline|'\n'
name|'out'
op|'.'
name|'write'
op|'('
string|"'HTTP/1.1 %d OK\\r\\nContent-Length: 0\\r\\n\\r\\n'"
op|'%'
nl|'\n'
name|'return_code'
op|')'
newline|'\n'
name|'out'
op|'.'
name|'flush'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'inc'
op|'.'
name|'readline'
op|'('
op|')'
op|','
nl|'\n'
string|"'PUT /sda1/0/a/c HTTP/1.1\\r\\n'"
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'line'
op|'='
name|'inc'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
name|'while'
name|'line'
name|'and'
name|'line'
op|'!='
string|"'\\r\\n'"
op|':'
newline|'\n'
indent|'                        '
name|'headers'
op|'['
name|'line'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'line'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'1'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'line'
op|'='
name|'inc'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'x-put-timestamp'"
name|'in'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'x-delete-timestamp'"
name|'in'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'x-object-count'"
name|'in'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'x-bytes-used'"
name|'in'
name|'headers'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'BaseException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'import'
name|'traceback'
newline|'\n'
name|'traceback'
op|'.'
name|'print_exc'
op|'('
op|')'
newline|'\n'
name|'return'
name|'err'
newline|'\n'
dedent|''
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'bindsock'
op|'='
name|'listen'
op|'('
op|'('
string|"'127.0.0.1'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|spawn_accepts
name|'def'
name|'spawn_accepts'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'events'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'_junk'
name|'in'
name|'range'
op|'('
number|'2'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|','
name|'addr'
op|'='
name|'bindsock'
op|'.'
name|'accept'
op|'('
op|')'
newline|'\n'
name|'events'
op|'.'
name|'append'
op|'('
name|'spawn'
op|'('
name|'accept'
op|','
name|'sock'
op|','
name|'addr'
op|','
number|'201'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'events'
newline|'\n'
nl|'\n'
dedent|''
name|'spawned'
op|'='
name|'spawn'
op|'('
name|'spawn_accepts'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'cu'
op|'.'
name|'get_account_ring'
op|'('
op|')'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'dev'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'dev'
op|'['
string|"'port'"
op|']'
op|'='
name|'bindsock'
op|'.'
name|'getsockname'
op|'('
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'for'
name|'event'
name|'in'
name|'spawned'
op|'.'
name|'wait'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'err'
op|'='
name|'event'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'err'
newline|'\n'
dedent|''
dedent|''
name|'info'
op|'='
name|'cb'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|','
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_object_count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_bytes_used'"
op|']'
op|','
number|'3'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'os.listdir'"
op|')'
newline|'\n'
DECL|member|test_listdir_with_exception
name|'def'
name|'test_listdir_with_exception'
op|'('
name|'self'
op|','
name|'mock_listdir'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'e'
op|'='
name|'OSError'
op|'('
string|"'permission_denied'"
op|')'
newline|'\n'
name|'mock_listdir'
op|'.'
name|'side_effect'
op|'='
name|'e'
newline|'\n'
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'false'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'15'"
op|','
nl|'\n'
string|"'account_suppression_time'"
op|':'
number|'0'
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'paths'
op|'='
name|'cu'
op|'.'
name|'get_paths'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'paths'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'log_lines'
op|'='
name|'cu'
op|'.'
name|'logger'
op|'.'
name|'get_lines_for_level'
op|'('
string|"'error'"
op|')'
newline|'\n'
name|'msg'
op|'='
op|'('
string|"'ERROR:  Failed to get paths to drive partitions: '"
nl|'\n'
string|"'permission_denied'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'log_lines'
op|'['
number|'0'
op|']'
op|','
name|'msg'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'os.listdir'"
op|','
name|'return_value'
op|'='
op|'['
string|"'foo'"
op|','
string|"'bar'"
op|']'
op|')'
newline|'\n'
DECL|member|test_listdir_without_exception
name|'def'
name|'test_listdir_without_exception'
op|'('
name|'self'
op|','
name|'mock_listdir'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'false'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'15'"
op|','
nl|'\n'
string|"'account_suppression_time'"
op|':'
number|'0'
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'cu'
op|'.'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'path'
op|'='
name|'cu'
op|'.'
name|'_listdir'
op|'('
string|"'foo/bar/'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'path'
op|','
op|'['
string|"'foo'"
op|','
string|"'bar'"
op|']'
op|')'
newline|'\n'
name|'log_lines'
op|'='
name|'cu'
op|'.'
name|'logger'
op|'.'
name|'get_lines_for_level'
op|'('
string|"'error'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'len'
op|'('
name|'log_lines'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_unicode
dedent|''
name|'def'
name|'test_unicode'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cu'
op|'='
name|'container_updater'
op|'.'
name|'ContainerUpdater'
op|'('
op|'{'
nl|'\n'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'devices_dir'
op|','
nl|'\n'
string|"'mount_check'"
op|':'
string|"'false'"
op|','
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'interval'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'concurrency'"
op|':'
string|"'1'"
op|','
nl|'\n'
string|"'node_timeout'"
op|':'
string|"'15'"
op|','
nl|'\n'
op|'}'
op|')'
newline|'\n'
name|'containers_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'sda1'
op|','
name|'DATADIR'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'containers_dir'
op|')'
newline|'\n'
name|'subdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'containers_dir'
op|','
string|"'subdir'"
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'subdir'
op|')'
newline|'\n'
name|'cb'
op|'='
name|'ContainerBroker'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'subdir'
op|','
string|"'hash.db'"
op|')'
op|','
name|'account'
op|'='
string|"'a'"
op|','
nl|'\n'
name|'container'
op|'='
string|"'\\xce\\xa9'"
op|')'
newline|'\n'
name|'cb'
op|'.'
name|'initialize'
op|'('
name|'normalize_timestamp'
op|'('
number|'1'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
name|'cb'
op|'.'
name|'put_object'
op|'('
string|"'\\xce\\xa9'"
op|','
name|'normalize_timestamp'
op|'('
number|'2'
op|')'
op|','
number|'3'
op|','
string|"'text/plain'"
op|','
nl|'\n'
string|"'68b329da9893e34099c7d8ad5cb9c940'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|accept
name|'def'
name|'accept'
op|'('
name|'sock'
op|','
name|'addr'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'Timeout'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'inc'
op|'='
name|'sock'
op|'.'
name|'makefile'
op|'('
string|"'rb'"
op|')'
newline|'\n'
name|'out'
op|'='
name|'sock'
op|'.'
name|'makefile'
op|'('
string|"'wb'"
op|')'
newline|'\n'
name|'out'
op|'.'
name|'write'
op|'('
string|"'HTTP/1.1 201 OK\\r\\nContent-Length: 0\\r\\n\\r\\n'"
op|')'
newline|'\n'
name|'out'
op|'.'
name|'flush'
op|'('
op|')'
newline|'\n'
name|'inc'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'BaseException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'import'
name|'traceback'
newline|'\n'
name|'traceback'
op|'.'
name|'print_exc'
op|'('
op|')'
newline|'\n'
name|'return'
name|'err'
newline|'\n'
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
dedent|''
name|'bindsock'
op|'='
name|'listen'
op|'('
op|'('
string|"'127.0.0.1'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|spawn_accepts
name|'def'
name|'spawn_accepts'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'events'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'_junk'
name|'in'
name|'range'
op|'('
number|'2'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'Timeout'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'sock'
op|','
name|'addr'
op|'='
name|'bindsock'
op|'.'
name|'accept'
op|'('
op|')'
newline|'\n'
name|'events'
op|'.'
name|'append'
op|'('
name|'spawn'
op|'('
name|'accept'
op|','
name|'sock'
op|','
name|'addr'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'events'
newline|'\n'
nl|'\n'
dedent|''
name|'spawned'
op|'='
name|'spawn'
op|'('
name|'spawn_accepts'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'cu'
op|'.'
name|'get_account_ring'
op|'('
op|')'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'dev'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'dev'
op|'['
string|"'port'"
op|']'
op|'='
name|'bindsock'
op|'.'
name|'getsockname'
op|'('
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'cu'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'for'
name|'event'
name|'in'
name|'spawned'
op|'.'
name|'wait'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'err'
op|'='
name|'event'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'err'
newline|'\n'
dedent|''
dedent|''
name|'info'
op|'='
name|'cb'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|','
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_object_count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'info'
op|'['
string|"'reported_bytes_used'"
op|']'
op|','
number|'3'
op|')'
newline|'\n'
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
