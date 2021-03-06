begin_unit
comment|'# Copyright (c) 2014 OpenStack Foundation'
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
string|"'''Tests for `swift.common.splice`'''"
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'ctypes'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'tempfile'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'contextlib'
newline|'\n'
name|'import'
name|'re'
newline|'\n'
nl|'\n'
name|'import'
name|'mock'
newline|'\n'
name|'import'
name|'nose'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'splice'
name|'import'
name|'splice'
op|','
name|'tee'
newline|'\n'
nl|'\n'
DECL|variable|LOGGER
name|'LOGGER'
op|'='
name|'logging'
op|'.'
name|'getLogger'
op|'('
name|'__name__'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|safe_close
name|'def'
name|'safe_close'
op|'('
name|'fd'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Close a file descriptor, ignoring any exceptions'''"
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'os'
op|'.'
name|'close'
op|'('
name|'fd'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'        '
name|'LOGGER'
op|'.'
name|'exception'
op|'('
string|"'Error while closing FD'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'contextlib'
op|'.'
name|'contextmanager'
newline|'\n'
DECL|function|pipe
name|'def'
name|'pipe'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Context-manager providing 2 ends of a pipe, closing them at exit'''"
newline|'\n'
nl|'\n'
name|'fds'
op|'='
name|'os'
op|'.'
name|'pipe'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'fds'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'safe_close'
op|'('
name|'fds'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'safe_close'
op|'('
name|'fds'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestSplice
dedent|''
dedent|''
name|'class'
name|'TestSplice'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Tests for `splice`'''"
newline|'\n'
nl|'\n'
DECL|member|setUp
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'splice'
op|'.'
name|'available'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'nose'
op|'.'
name|'SkipTest'
op|'('
string|"'splice not available'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_flags
dedent|''
dedent|''
name|'def'
name|'test_flags'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test flag attribute availability'''"
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'hasattr'
op|'('
name|'splice'
op|','
string|"'SPLICE_F_MOVE'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'hasattr'
op|'('
name|'splice'
op|','
string|"'SPLICE_F_NONBLOCK'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'hasattr'
op|'('
name|'splice'
op|','
string|"'SPLICE_F_MORE'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'hasattr'
op|'('
name|'splice'
op|','
string|"'SPLICE_F_GIFT'"
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.common.splice.splice._c_splice'"
op|','
name|'None'
op|')'
newline|'\n'
DECL|member|test_available
name|'def'
name|'test_available'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `available` attribute correctness'''"
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'splice'
op|'.'
name|'available'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_splice_pipe_to_pipe
dedent|''
name|'def'
name|'test_splice_pipe_to_pipe'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `splice` from a pipe to a pipe'''"
newline|'\n'
nl|'\n'
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'p1a'
op|','
name|'p1b'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'p2a'
op|','
name|'p2b'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'write'
op|'('
name|'p1b'
op|','
string|"'abcdef'"
op|')'
newline|'\n'
name|'res'
op|'='
name|'splice'
op|'('
name|'p1a'
op|','
name|'None'
op|','
name|'p2b'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'('
number|'3'
op|','
name|'None'
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'read'
op|'('
name|'p2a'
op|','
number|'3'
op|')'
op|','
string|"'abc'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'read'
op|'('
name|'p1a'
op|','
number|'3'
op|')'
op|','
string|"'def'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_splice_file_to_pipe
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_splice_file_to_pipe'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `splice` from a file to a pipe'''"
newline|'\n'
nl|'\n'
name|'with'
name|'tempfile'
op|'.'
name|'NamedTemporaryFile'
op|'('
name|'bufsize'
op|'='
number|'0'
op|')'
name|'as'
name|'fd'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'pa'
op|','
name|'pb'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'fd'
op|'.'
name|'write'
op|'('
string|"'abcdef'"
op|')'
newline|'\n'
name|'fd'
op|'.'
name|'seek'
op|'('
number|'0'
op|','
name|'os'
op|'.'
name|'SEEK_SET'
op|')'
newline|'\n'
nl|'\n'
name|'res'
op|'='
name|'splice'
op|'('
name|'fd'
op|','
name|'None'
op|','
name|'pb'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'('
number|'3'
op|','
name|'None'
op|','
name|'None'
op|')'
op|')'
newline|'\n'
comment|"# `fd.tell()` isn't updated..."
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'lseek'
op|'('
name|'fd'
op|'.'
name|'fileno'
op|'('
op|')'
op|','
number|'0'
op|','
name|'os'
op|'.'
name|'SEEK_CUR'
op|')'
op|','
number|'3'
op|')'
newline|'\n'
nl|'\n'
name|'fd'
op|'.'
name|'seek'
op|'('
number|'0'
op|','
name|'os'
op|'.'
name|'SEEK_SET'
op|')'
newline|'\n'
name|'res'
op|'='
name|'splice'
op|'('
name|'fd'
op|','
number|'3'
op|','
name|'pb'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'('
number|'3'
op|','
number|'6'
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'lseek'
op|'('
name|'fd'
op|'.'
name|'fileno'
op|'('
op|')'
op|','
number|'0'
op|','
name|'os'
op|'.'
name|'SEEK_CUR'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'read'
op|'('
name|'pa'
op|','
number|'6'
op|')'
op|','
string|"'abcdef'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_splice_pipe_to_file
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_splice_pipe_to_file'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `splice` from a pipe to a file'''"
newline|'\n'
nl|'\n'
name|'with'
name|'tempfile'
op|'.'
name|'NamedTemporaryFile'
op|'('
name|'bufsize'
op|'='
number|'0'
op|')'
name|'as'
name|'fd'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'pa'
op|','
name|'pb'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'write'
op|'('
name|'pb'
op|','
string|"'abcdef'"
op|')'
newline|'\n'
nl|'\n'
name|'res'
op|'='
name|'splice'
op|'('
name|'pa'
op|','
name|'None'
op|','
name|'fd'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'('
number|'3'
op|','
name|'None'
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'fd'
op|'.'
name|'tell'
op|'('
op|')'
op|','
number|'3'
op|')'
newline|'\n'
nl|'\n'
name|'fd'
op|'.'
name|'seek'
op|'('
number|'0'
op|','
name|'os'
op|'.'
name|'SEEK_SET'
op|')'
newline|'\n'
nl|'\n'
name|'res'
op|'='
name|'splice'
op|'('
name|'pa'
op|','
name|'None'
op|','
name|'fd'
op|','
number|'3'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'('
number|'3'
op|','
name|'None'
op|','
number|'6'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'fd'
op|'.'
name|'tell'
op|'('
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'fd'
op|'.'
name|'read'
op|'('
number|'6'
op|')'
op|','
string|"'abcdef'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'.'
name|'object'
op|'('
name|'splice'
op|','
string|"'_c_splice'"
op|')'
newline|'\n'
DECL|member|test_fileno
name|'def'
name|'test_fileno'
op|'('
name|'self'
op|','
name|'mock_splice'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test handling of file-descriptors'''"
newline|'\n'
nl|'\n'
name|'splice'
op|'('
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_splice'
op|'.'
name|'call_args'
op|','
nl|'\n'
op|'('
op|'('
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'mock_splice'
op|'.'
name|'reset_mock'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'open'
op|'('
string|"'/dev/zero'"
op|','
string|"'r'"
op|')'
name|'as'
name|'fd'
op|':'
newline|'\n'
indent|'            '
name|'splice'
op|'('
name|'fd'
op|','
name|'None'
op|','
name|'fd'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_splice'
op|'.'
name|'call_args'
op|','
nl|'\n'
op|'('
op|'('
name|'fd'
op|'.'
name|'fileno'
op|'('
op|')'
op|','
name|'None'
op|','
name|'fd'
op|'.'
name|'fileno'
op|'('
op|')'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
op|','
nl|'\n'
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'.'
name|'object'
op|'('
name|'splice'
op|','
string|"'_c_splice'"
op|')'
newline|'\n'
DECL|member|test_flags_list
name|'def'
name|'test_flags_list'
op|'('
name|'self'
op|','
name|'mock_splice'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test handling of flag lists'''"
newline|'\n'
nl|'\n'
name|'splice'
op|'('
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'3'
op|','
nl|'\n'
op|'['
name|'splice'
op|'.'
name|'SPLICE_F_MOVE'
op|','
name|'splice'
op|'.'
name|'SPLICE_F_NONBLOCK'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'flags'
op|'='
name|'splice'
op|'.'
name|'SPLICE_F_MOVE'
op|'|'
name|'splice'
op|'.'
name|'SPLICE_F_NONBLOCK'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_splice'
op|'.'
name|'call_args'
op|','
nl|'\n'
op|'('
op|'('
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'3'
op|','
name|'flags'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'mock_splice'
op|'.'
name|'reset_mock'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'splice'
op|'('
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'3'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_splice'
op|'.'
name|'call_args'
op|','
nl|'\n'
op|'('
op|'('
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_errno
dedent|''
name|'def'
name|'test_errno'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test handling of failures'''"
newline|'\n'
nl|'\n'
comment|'# Invoke EBADF by using a read-only FD as fd_out'
nl|'\n'
name|'with'
name|'open'
op|'('
string|"'/dev/null'"
op|','
string|"'r'"
op|')'
name|'as'
name|'fd'
op|':'
newline|'\n'
indent|'            '
name|'err'
op|'='
name|'errno'
op|'.'
name|'EBADF'
newline|'\n'
name|'msg'
op|'='
string|"r'\\[Errno %d\\] splice: %s'"
op|'%'
op|'('
name|'err'
op|','
name|'os'
op|'.'
name|'strerror'
op|'('
name|'err'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'splice'
op|'('
name|'fd'
op|','
name|'None'
op|','
name|'fd'
op|','
name|'None'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'re'
op|'.'
name|'match'
op|'('
name|'msg'
op|','
name|'str'
op|'('
name|'e'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Expected IOError was not raised'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ctypes'
op|'.'
name|'get_errno'
op|'('
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.common.splice.splice._c_splice'"
op|','
name|'None'
op|')'
newline|'\n'
DECL|member|test_unavailable
name|'def'
name|'test_unavailable'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test exception when unavailable'''"
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'EnvironmentError'
op|','
name|'splice'
op|','
number|'1'
op|','
name|'None'
op|','
number|'2'
op|','
name|'None'
op|','
number|'2'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_unavailable_in_libc
dedent|''
name|'def'
name|'test_unavailable_in_libc'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `available` attribute when `libc` has no `splice` support'''"
newline|'\n'
nl|'\n'
DECL|class|LibC
name|'class'
name|'LibC'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'            '
string|"'''A fake `libc` object tracking `splice` attribute access'''"
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'splice_retrieved'
op|'='
name|'False'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|splice
name|'def'
name|'splice'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'splice_retrieved'
op|'='
name|'True'
newline|'\n'
name|'raise'
name|'AttributeError'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'libc'
op|'='
name|'LibC'
op|'('
op|')'
newline|'\n'
name|'mock_cdll'
op|'='
name|'mock'
op|'.'
name|'Mock'
op|'('
name|'return_value'
op|'='
name|'libc'
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'ctypes.CDLL'"
op|','
name|'new'
op|'='
name|'mock_cdll'
op|')'
op|':'
newline|'\n'
comment|'# Force re-construction of a `Splice` instance'
nl|'\n'
comment|"# Something you're not supposed to do in actual code"
nl|'\n'
DECL|variable|new_splice
indent|'            '
name|'new_splice'
op|'='
name|'type'
op|'('
name|'splice'
op|')'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'new_splice'
op|'.'
name|'available'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'libc_name'
op|'='
name|'ctypes'
op|'.'
name|'util'
op|'.'
name|'find_library'
op|'('
string|"'c'"
op|')'
newline|'\n'
nl|'\n'
name|'mock_cdll'
op|'.'
name|'assert_called_once_with'
op|'('
name|'libc_name'
op|','
name|'use_errno'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'libc'
op|'.'
name|'splice_retrieved'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestTee
dedent|''
dedent|''
name|'class'
name|'TestTee'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Tests for `tee`'''"
newline|'\n'
nl|'\n'
DECL|member|setUp
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'tee'
op|'.'
name|'available'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'nose'
op|'.'
name|'SkipTest'
op|'('
string|"'tee not available'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.common.splice.tee._c_tee'"
op|','
name|'None'
op|')'
newline|'\n'
DECL|member|test_available
name|'def'
name|'test_available'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `available` attribute correctness'''"
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'tee'
op|'.'
name|'available'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_tee_pipe_to_pipe
dedent|''
name|'def'
name|'test_tee_pipe_to_pipe'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `tee` from a pipe to a pipe'''"
newline|'\n'
nl|'\n'
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'p1a'
op|','
name|'p1b'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'p2a'
op|','
name|'p2b'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'write'
op|'('
name|'p1b'
op|','
string|"'abcdef'"
op|')'
newline|'\n'
name|'res'
op|'='
name|'tee'
op|'('
name|'p1a'
op|','
name|'p2b'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'read'
op|'('
name|'p2a'
op|','
number|'3'
op|')'
op|','
string|"'abc'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'os'
op|'.'
name|'read'
op|'('
name|'p1a'
op|','
number|'6'
op|')'
op|','
string|"'abcdef'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'.'
name|'object'
op|'('
name|'tee'
op|','
string|"'_c_tee'"
op|')'
newline|'\n'
DECL|member|test_fileno
name|'def'
name|'test_fileno'
op|'('
name|'self'
op|','
name|'mock_tee'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test handling of file-descriptors'''"
newline|'\n'
nl|'\n'
name|'with'
name|'pipe'
op|'('
op|')'
name|'as'
op|'('
name|'pa'
op|','
name|'pb'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'tee'
op|'('
name|'pa'
op|','
name|'pb'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_tee'
op|'.'
name|'call_args'
op|','
op|'('
op|'('
name|'pa'
op|','
name|'pb'
op|','
number|'3'
op|','
number|'0'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'mock_tee'
op|'.'
name|'reset_mock'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'tee'
op|'('
name|'os'
op|'.'
name|'fdopen'
op|'('
name|'pa'
op|','
string|"'r'"
op|')'
op|','
name|'os'
op|'.'
name|'fdopen'
op|'('
name|'pb'
op|','
string|"'w'"
op|')'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_tee'
op|'.'
name|'call_args'
op|','
op|'('
op|'('
name|'pa'
op|','
name|'pb'
op|','
number|'3'
op|','
number|'0'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'.'
name|'object'
op|'('
name|'tee'
op|','
string|"'_c_tee'"
op|')'
newline|'\n'
DECL|member|test_flags_list
name|'def'
name|'test_flags_list'
op|'('
name|'self'
op|','
name|'mock_tee'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test handling of flag lists'''"
newline|'\n'
nl|'\n'
name|'tee'
op|'('
number|'1'
op|','
number|'2'
op|','
number|'3'
op|','
op|'['
name|'splice'
op|'.'
name|'SPLICE_F_MOVE'
op|'|'
name|'splice'
op|'.'
name|'SPLICE_F_NONBLOCK'
op|']'
op|')'
newline|'\n'
name|'flags'
op|'='
name|'splice'
op|'.'
name|'SPLICE_F_MOVE'
op|'|'
name|'splice'
op|'.'
name|'SPLICE_F_NONBLOCK'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_tee'
op|'.'
name|'call_args'
op|','
op|'('
op|'('
number|'1'
op|','
number|'2'
op|','
number|'3'
op|','
name|'flags'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'mock_tee'
op|'.'
name|'reset_mock'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'tee'
op|'('
number|'1'
op|','
number|'2'
op|','
number|'3'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'mock_tee'
op|'.'
name|'call_args'
op|','
op|'('
op|'('
number|'1'
op|','
number|'2'
op|','
number|'3'
op|','
number|'0'
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_errno
dedent|''
name|'def'
name|'test_errno'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test handling of failures'''"
newline|'\n'
nl|'\n'
comment|'# Invoke EBADF by using a read-only FD as fd_out'
nl|'\n'
name|'with'
name|'open'
op|'('
string|"'/dev/null'"
op|','
string|"'r'"
op|')'
name|'as'
name|'fd'
op|':'
newline|'\n'
indent|'            '
name|'err'
op|'='
name|'errno'
op|'.'
name|'EBADF'
newline|'\n'
name|'msg'
op|'='
string|"r'\\[Errno %d\\] tee: %s'"
op|'%'
op|'('
name|'err'
op|','
name|'os'
op|'.'
name|'strerror'
op|'('
name|'err'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'tee'
op|'('
name|'fd'
op|','
name|'fd'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'re'
op|'.'
name|'match'
op|'('
name|'msg'
op|','
name|'str'
op|'('
name|'e'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Expected IOError was not raised'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ctypes'
op|'.'
name|'get_errno'
op|'('
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.common.splice.tee._c_tee'"
op|','
name|'None'
op|')'
newline|'\n'
DECL|member|test_unavailable
name|'def'
name|'test_unavailable'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test exception when unavailable'''"
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'EnvironmentError'
op|','
name|'tee'
op|','
number|'1'
op|','
number|'2'
op|','
number|'2'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_unavailable_in_libc
dedent|''
name|'def'
name|'test_unavailable_in_libc'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Test `available` attribute when `libc` has no `tee` support'''"
newline|'\n'
nl|'\n'
DECL|class|LibC
name|'class'
name|'LibC'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'            '
string|"'''A fake `libc` object tracking `tee` attribute access'''"
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'tee_retrieved'
op|'='
name|'False'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|tee
name|'def'
name|'tee'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'tee_retrieved'
op|'='
name|'True'
newline|'\n'
name|'raise'
name|'AttributeError'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'libc'
op|'='
name|'LibC'
op|'('
op|')'
newline|'\n'
name|'mock_cdll'
op|'='
name|'mock'
op|'.'
name|'Mock'
op|'('
name|'return_value'
op|'='
name|'libc'
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'ctypes.CDLL'"
op|','
name|'new'
op|'='
name|'mock_cdll'
op|')'
op|':'
newline|'\n'
comment|'# Force re-construction of a `Tee` instance'
nl|'\n'
comment|"# Something you're not supposed to do in actual code"
nl|'\n'
DECL|variable|new_tee
indent|'            '
name|'new_tee'
op|'='
name|'type'
op|'('
name|'tee'
op|')'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'new_tee'
op|'.'
name|'available'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'libc_name'
op|'='
name|'ctypes'
op|'.'
name|'util'
op|'.'
name|'find_library'
op|'('
string|"'c'"
op|')'
newline|'\n'
nl|'\n'
name|'mock_cdll'
op|'.'
name|'assert_called_once_with'
op|'('
name|'libc_name'
op|','
name|'use_errno'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'libc'
op|'.'
name|'tee_retrieved'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
