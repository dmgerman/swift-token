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
string|'"""Miscellaneous utility functions for use with Swift."""'
newline|'\n'
nl|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'fcntl'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'pwd'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'mimetools'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'shuffle'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'import'
name|'ctypes'
newline|'\n'
name|'import'
name|'ctypes'
op|'.'
name|'util'
newline|'\n'
name|'import'
name|'fcntl'
newline|'\n'
name|'import'
name|'struct'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'greenio'
op|','
name|'GreenPool'
op|','
name|'sleep'
op|','
name|'Timeout'
op|','
name|'listen'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
name|'import'
name|'socket'
op|','
name|'subprocess'
op|','
name|'ssl'
op|','
name|'thread'
op|','
name|'threading'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'LockTimeout'
op|','
name|'MessageTimeout'
newline|'\n'
nl|'\n'
comment|"# logging doesn't import patched as cleanly as one would like"
nl|'\n'
name|'from'
name|'logging'
op|'.'
name|'handlers'
name|'import'
name|'SysLogHandler'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'logging'
op|'.'
name|'thread'
op|'='
name|'eventlet'
op|'.'
name|'green'
op|'.'
name|'thread'
newline|'\n'
name|'logging'
op|'.'
name|'threading'
op|'='
name|'eventlet'
op|'.'
name|'green'
op|'.'
name|'threading'
newline|'\n'
name|'logging'
op|'.'
name|'_lock'
op|'='
name|'logging'
op|'.'
name|'threading'
op|'.'
name|'RLock'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# These are lazily pulled from libc elsewhere'
nl|'\n'
DECL|variable|_sys_fallocate
name|'_sys_fallocate'
op|'='
name|'None'
newline|'\n'
DECL|variable|_posix_fadvise
name|'_posix_fadvise'
op|'='
name|'None'
newline|'\n'
nl|'\n'
comment|'# Used by hash_path to offer a bit more security when generating hashes for'
nl|'\n'
comment|'# paths. It simply appends this value to all paths; guessing the hash a path'
nl|'\n'
comment|'# will end up with would also require knowing this suffix.'
nl|'\n'
DECL|variable|HASH_PATH_SUFFIX
name|'HASH_PATH_SUFFIX'
op|'='
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_HASH_PATH_SUFFIX'"
op|','
string|"'endcap'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|load_libc_function
name|'def'
name|'load_libc_function'
op|'('
name|'func_name'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Attempt to find the function in libc, otherwise return a no-op func.\n\n    :param func_name: name of the function to pull from libc.\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'libc'
op|'='
name|'ctypes'
op|'.'
name|'CDLL'
op|'('
name|'ctypes'
op|'.'
name|'util'
op|'.'
name|'find_library'
op|'('
string|"'c'"
op|')'
op|')'
newline|'\n'
name|'return'
name|'getattr'
op|'('
name|'libc'
op|','
name|'func_name'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'        '
name|'logging'
op|'.'
name|'warn'
op|'('
string|'"Unable to locate %s in libc.  Leaving as a no-op."'
nl|'\n'
op|'%'
name|'func_name'
op|')'
newline|'\n'
nl|'\n'
DECL|function|noop_libc_function
name|'def'
name|'noop_libc_function'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
newline|'\n'
dedent|''
name|'return'
name|'noop_libc_function'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_param
dedent|''
dedent|''
name|'def'
name|'get_param'
op|'('
name|'req'
op|','
name|'name'
op|','
name|'default'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get parameters from an HTTP request ensuring proper handling UTF-8\n    encoding.\n\n    :param req: Webob request object\n    :param name: parameter name\n    :param default: result to return if the parameter is not found\n    :returns: HTTP request parameter value\n    """'
newline|'\n'
name|'value'
op|'='
name|'req'
op|'.'
name|'str_params'
op|'.'
name|'get'
op|'('
name|'name'
op|','
name|'default'
op|')'
newline|'\n'
name|'if'
name|'value'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'.'
name|'decode'
op|'('
string|"'utf8'"
op|')'
comment|'# Ensure UTF8ness'
newline|'\n'
dedent|''
name|'return'
name|'value'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|fallocate
dedent|''
name|'def'
name|'fallocate'
op|'('
name|'fd'
op|','
name|'size'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Pre-allocate disk space for a file file.\n\n    :param fd: file descriptor\n    :param size: size to allocate (in bytes)\n    """'
newline|'\n'
name|'global'
name|'_sys_fallocate'
newline|'\n'
name|'if'
name|'_sys_fallocate'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'_sys_fallocate'
op|'='
name|'load_libc_function'
op|'('
string|"'fallocate'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'size'
op|'>'
number|'0'
op|':'
newline|'\n'
comment|'# 1 means "FALLOC_FL_KEEP_SIZE", which means it pre-allocates invisibly'
nl|'\n'
indent|'        '
name|'ret'
op|'='
name|'_sys_fallocate'
op|'('
name|'fd'
op|','
number|'1'
op|','
number|'0'
op|','
name|'ctypes'
op|'.'
name|'c_uint64'
op|'('
name|'size'
op|')'
op|')'
newline|'\n'
comment|'# XXX: in (not very thorough) testing, errno always seems to be 0?'
nl|'\n'
name|'err'
op|'='
name|'ctypes'
op|'.'
name|'get_errno'
op|'('
op|')'
newline|'\n'
name|'if'
name|'ret'
name|'and'
name|'err'
name|'not'
name|'in'
op|'('
number|'0'
op|','
name|'errno'
op|'.'
name|'ENOSYS'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'OSError'
op|'('
name|'err'
op|','
string|"'Unable to fallocate(%s)'"
op|'%'
name|'size'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|drop_buffer_cache
dedent|''
dedent|''
dedent|''
name|'def'
name|'drop_buffer_cache'
op|'('
name|'fd'
op|','
name|'offset'
op|','
name|'length'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Drop \'buffer\' cache for the given range of the given file.\n\n    :param fd: file descriptor\n    :param offset: start offset\n    :param length: length\n    """'
newline|'\n'
name|'global'
name|'_posix_fadvise'
newline|'\n'
name|'if'
name|'_posix_fadvise'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'_posix_fadvise'
op|'='
name|'load_libc_function'
op|'('
string|"'posix_fadvise'"
op|')'
newline|'\n'
comment|'# 4 means "POSIX_FADV_DONTNEED"'
nl|'\n'
dedent|''
name|'ret'
op|'='
name|'_posix_fadvise'
op|'('
name|'fd'
op|','
name|'ctypes'
op|'.'
name|'c_uint64'
op|'('
name|'offset'
op|')'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_uint64'
op|'('
name|'length'
op|')'
op|','
number|'4'
op|')'
newline|'\n'
name|'if'
name|'ret'
op|'!='
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'logging'
op|'.'
name|'warn'
op|'('
string|'"posix_fadvise(%s, %s, %s, 4) -> %s"'
nl|'\n'
op|'%'
op|'('
name|'fd'
op|','
name|'offset'
op|','
name|'length'
op|','
name|'ret'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|normalize_timestamp
dedent|''
dedent|''
name|'def'
name|'normalize_timestamp'
op|'('
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Format a timestamp (string or numeric) into a standardized\n    xxxxxxxxxx.xxxxx format.\n\n    :param timestamp: unix timestamp\n    :returns: normalized timestamp as a string\n    """'
newline|'\n'
name|'return'
string|'"%016.05f"'
op|'%'
op|'('
name|'float'
op|'('
name|'timestamp'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|mkdirs
dedent|''
name|'def'
name|'mkdirs'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Ensures the path is a directory or makes it if not. Errors if the path\n    exists but is a file or on permissions failure.\n\n    :param path: path to create\n    """'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'makedirs'
op|'('
name|'path'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'EEXIST'
name|'or'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|renamer
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'renamer'
op|'('
name|'old'
op|','
name|'new'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'    '
string|'"""\n    Attempt to fix^H^H^Hhide race conditions like empty object directories\n    being removed by backend processes during uploads, by retrying.\n\n    :param old: old path to be renamed\n    :param new: new path to be renamed to\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'new'
op|')'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'rename'
op|'('
name|'old'
op|','
name|'new'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'        '
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'new'
op|')'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'rename'
op|'('
name|'old'
op|','
name|'new'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|split_path
dedent|''
dedent|''
name|'def'
name|'split_path'
op|'('
name|'path'
op|','
name|'minsegs'
op|'='
number|'1'
op|','
name|'maxsegs'
op|'='
name|'None'
op|','
name|'rest_with_last'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Validate and split the given HTTP request path.\n\n    **Examples**::\n\n        [\'a\'] = split_path(\'/a\')\n        [\'a\', None] = split_path(\'/a\', 1, 2)\n        [\'a\', \'c\'] = split_path(\'/a/c\', 1, 2)\n        [\'a\', \'c\', \'o/r\'] = split_path(\'/a/c/o/r\', 1, 3, True)\n\n    :param path: HTTP Request path to be split\n    :param minsegs: Minimum number of segments to be extracted\n    :param maxsegs: Maximum number of segments to be extracted\n    :param rest_with_last: If True, trailing data will be returned as part\n                           of last segment.  If False, and there is\n                           trailing data, raises ValueError.\n    :returns: list of segments with a length of maxsegs (non-existant\n              segments will return as None)\n    """'
newline|'\n'
name|'if'
name|'not'
name|'maxsegs'
op|':'
newline|'\n'
indent|'        '
name|'maxsegs'
op|'='
name|'minsegs'
newline|'\n'
dedent|''
name|'if'
name|'minsegs'
op|'>'
name|'maxsegs'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|"'minsegs > maxsegs: %d > %d'"
op|'%'
op|'('
name|'minsegs'
op|','
name|'maxsegs'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'rest_with_last'
op|':'
newline|'\n'
indent|'        '
name|'segs'
op|'='
name|'path'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
name|'maxsegs'
op|')'
newline|'\n'
name|'minsegs'
op|'+='
number|'1'
newline|'\n'
name|'maxsegs'
op|'+='
number|'1'
newline|'\n'
name|'count'
op|'='
name|'len'
op|'('
name|'segs'
op|')'
newline|'\n'
name|'if'
name|'segs'
op|'['
number|'0'
op|']'
name|'or'
name|'count'
op|'<'
name|'minsegs'
name|'or'
name|'count'
op|'>'
name|'maxsegs'
name|'or'
string|"''"
name|'in'
name|'segs'
op|'['
number|'1'
op|':'
name|'minsegs'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|"'Invalid path: %s'"
op|'%'
name|'quote'
op|'('
name|'path'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'minsegs'
op|'+='
number|'1'
newline|'\n'
name|'maxsegs'
op|'+='
number|'1'
newline|'\n'
name|'segs'
op|'='
name|'path'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
name|'maxsegs'
op|')'
newline|'\n'
name|'count'
op|'='
name|'len'
op|'('
name|'segs'
op|')'
newline|'\n'
name|'if'
name|'segs'
op|'['
number|'0'
op|']'
name|'or'
name|'count'
op|'<'
name|'minsegs'
name|'or'
name|'count'
op|'>'
name|'maxsegs'
op|'+'
number|'1'
name|'or'
string|"''"
name|'in'
name|'segs'
op|'['
number|'1'
op|':'
name|'minsegs'
op|']'
name|'or'
op|'('
name|'count'
op|'=='
name|'maxsegs'
op|'+'
number|'1'
name|'and'
name|'segs'
op|'['
name|'maxsegs'
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|"'Invalid path: %s'"
op|'%'
name|'quote'
op|'('
name|'path'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'segs'
op|'='
name|'segs'
op|'['
number|'1'
op|':'
name|'maxsegs'
op|']'
newline|'\n'
name|'segs'
op|'.'
name|'extend'
op|'('
op|'['
name|'None'
op|']'
op|'*'
op|'('
name|'maxsegs'
op|'-'
number|'1'
op|'-'
name|'len'
op|'('
name|'segs'
op|')'
op|')'
op|')'
newline|'\n'
name|'return'
name|'segs'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|NullLogger
dedent|''
name|'class'
name|'NullLogger'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""A no-op logger for eventlet wsgi."""'
newline|'\n'
nl|'\n'
DECL|member|write
name|'def'
name|'write'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
comment|'#"Logs" the args to nowhere'
nl|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|LoggerFileObject
dedent|''
dedent|''
name|'class'
name|'LoggerFileObject'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
nl|'\n'
DECL|member|write
dedent|''
name|'def'
name|'write'
op|'('
name|'self'
op|','
name|'value'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'value'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'value'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'Connection reset by peer'"
name|'in'
name|'value'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'STDOUT: Connection reset by peer'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'STDOUT: %s'"
op|'%'
name|'value'
op|')'
newline|'\n'
nl|'\n'
DECL|member|writelines
dedent|''
dedent|''
dedent|''
name|'def'
name|'writelines'
op|'('
name|'self'
op|','
name|'values'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'STDOUT: %s'"
op|'%'
string|"'#012'"
op|'.'
name|'join'
op|'('
name|'values'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|flush
dedent|''
name|'def'
name|'flush'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|__iter__
dedent|''
name|'def'
name|'__iter__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|next
dedent|''
name|'def'
name|'next'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
op|'('
name|'errno'
op|'.'
name|'EBADF'
op|','
string|"'Bad file descriptor'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'size'
op|'='
op|'-'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
op|'('
name|'errno'
op|'.'
name|'EBADF'
op|','
string|"'Bad file descriptor'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|','
name|'size'
op|'='
op|'-'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
op|'('
name|'errno'
op|'.'
name|'EBADF'
op|','
string|"'Bad file descriptor'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|tell
dedent|''
name|'def'
name|'tell'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
number|'0'
newline|'\n'
nl|'\n'
DECL|member|xreadlines
dedent|''
name|'def'
name|'xreadlines'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|drop_privileges
dedent|''
dedent|''
name|'def'
name|'drop_privileges'
op|'('
name|'user'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Sets the userid of the current process\n\n    :param user: User id to change privileges to\n    """'
newline|'\n'
name|'user'
op|'='
name|'pwd'
op|'.'
name|'getpwnam'
op|'('
name|'user'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'setgid'
op|'('
name|'user'
op|'['
number|'3'
op|']'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'setuid'
op|'('
name|'user'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|NamedLogger
dedent|''
name|'class'
name|'NamedLogger'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Cheesy version of the LoggerAdapter available in Python 3"""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'server'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'server'
op|'='
name|'server'
newline|'\n'
name|'for'
name|'proxied_method'
name|'in'
op|'('
string|"'debug'"
op|','
string|"'info'"
op|','
string|"'log'"
op|','
string|"'warn'"
op|','
string|"'warning'"
op|','
nl|'\n'
string|"'error'"
op|','
string|"'critical'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'setattr'
op|'('
name|'self'
op|','
name|'proxied_method'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_proxy'
op|'('
name|'getattr'
op|'('
name|'logger'
op|','
name|'proxied_method'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_proxy
dedent|''
dedent|''
name|'def'
name|'_proxy'
op|'('
name|'self'
op|','
name|'logger_meth'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|_inner_proxy
indent|'        '
name|'def'
name|'_inner_proxy'
op|'('
name|'msg'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"'%s %s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'server'
op|','
name|'msg'
op|')'
newline|'\n'
name|'logger_meth'
op|'('
name|'msg'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'_inner_proxy'
newline|'\n'
nl|'\n'
DECL|member|getEffectiveLevel
dedent|''
name|'def'
name|'getEffectiveLevel'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'getEffectiveLevel'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|exception
dedent|''
name|'def'
name|'exception'
op|'('
name|'self'
op|','
name|'msg'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'_'
op|','
name|'exc'
op|','
name|'_'
op|'='
name|'sys'
op|'.'
name|'exc_info'
op|'('
op|')'
newline|'\n'
name|'call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
newline|'\n'
name|'emsg'
op|'='
string|"''"
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'exc'
op|','
name|'OSError'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'exc'
op|'.'
name|'errno'
name|'in'
op|'('
name|'errno'
op|'.'
name|'EIO'
op|','
name|'errno'
op|'.'
name|'ENOSPC'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'emsg'
op|'='
name|'str'
op|'('
name|'exc'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'isinstance'
op|'('
name|'exc'
op|','
name|'socket'
op|'.'
name|'error'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'exc'
op|'.'
name|'errno'
op|'=='
name|'errno'
op|'.'
name|'ECONNREFUSED'
op|':'
newline|'\n'
indent|'                '
name|'emsg'
op|'='
string|"'Connection refused'"
newline|'\n'
dedent|''
name|'elif'
name|'exc'
op|'.'
name|'errno'
op|'=='
name|'errno'
op|'.'
name|'EHOSTUNREACH'
op|':'
newline|'\n'
indent|'                '
name|'emsg'
op|'='
string|"'Host unreachable'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'isinstance'
op|'('
name|'exc'
op|','
name|'eventlet'
op|'.'
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'emsg'
op|'='
name|'exc'
op|'.'
name|'__class__'
op|'.'
name|'__name__'
newline|'\n'
name|'if'
name|'hasattr'
op|'('
name|'exc'
op|','
string|"'seconds'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'emsg'
op|'+='
string|"' (%ss)'"
op|'%'
name|'exc'
op|'.'
name|'seconds'
newline|'\n'
dedent|''
name|'if'
name|'isinstance'
op|'('
name|'exc'
op|','
name|'MessageTimeout'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'exc'
op|'.'
name|'msg'
op|':'
newline|'\n'
indent|'                    '
name|'emsg'
op|'+='
string|"' %s'"
op|'%'
name|'exc'
op|'.'
name|'msg'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
newline|'\n'
dedent|''
name|'call'
op|'('
string|"'%s %s: %s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'server'
op|','
name|'msg'
op|','
name|'emsg'
op|')'
op|','
op|'*'
name|'args'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_logger
dedent|''
dedent|''
name|'def'
name|'get_logger'
op|'('
name|'conf'
op|','
name|'name'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get the current system logger using config settings.\n\n    **Log config and defaults**::\n\n        log_facility = LOG_LOCAL0\n        log_level = INFO\n\n    :param conf: Configuration dict to read settings from\n    :param name: Name of the logger\n    """'
newline|'\n'
name|'root_logger'
op|'='
name|'logging'
op|'.'
name|'getLogger'
op|'('
op|')'
newline|'\n'
name|'if'
name|'hasattr'
op|'('
name|'get_logger'
op|','
string|"'handler'"
op|')'
name|'and'
name|'get_logger'
op|'.'
name|'handler'
op|':'
newline|'\n'
indent|'        '
name|'root_logger'
op|'.'
name|'removeHandler'
op|'('
name|'get_logger'
op|'.'
name|'handler'
op|')'
newline|'\n'
name|'get_logger'
op|'.'
name|'handler'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'conf'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'root_logger'
op|'.'
name|'setLevel'
op|'('
name|'logging'
op|'.'
name|'INFO'
op|')'
newline|'\n'
name|'return'
name|'NamedLogger'
op|'('
name|'root_logger'
op|','
name|'name'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'name'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'name'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_name'"
op|','
string|"'swift'"
op|')'
newline|'\n'
dedent|''
name|'get_logger'
op|'.'
name|'handler'
op|'='
name|'SysLogHandler'
op|'('
name|'address'
op|'='
string|"'/dev/log'"
op|','
nl|'\n'
name|'facility'
op|'='
name|'getattr'
op|'('
name|'SysLogHandler'
op|','
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_facility'"
op|','
string|"'LOG_LOCAL0'"
op|')'
op|','
nl|'\n'
name|'SysLogHandler'
op|'.'
name|'LOG_LOCAL0'
op|')'
op|')'
newline|'\n'
name|'root_logger'
op|'.'
name|'addHandler'
op|'('
name|'get_logger'
op|'.'
name|'handler'
op|')'
newline|'\n'
name|'root_logger'
op|'.'
name|'setLevel'
op|'('
nl|'\n'
name|'getattr'
op|'('
name|'logging'
op|','
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_level'"
op|','
string|"'INFO'"
op|')'
op|'.'
name|'upper'
op|'('
op|')'
op|','
name|'logging'
op|'.'
name|'INFO'
op|')'
op|')'
newline|'\n'
name|'return'
name|'NamedLogger'
op|'('
name|'root_logger'
op|','
name|'name'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|whataremyips
dedent|''
name|'def'
name|'whataremyips'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get the machine\'s ip addresses using ifconfig\n\n    :returns: list of Strings of IPv4 ip addresses\n    """'
newline|'\n'
name|'proc'
op|'='
name|'subprocess'
op|'.'
name|'Popen'
op|'('
op|'['
string|"'/sbin/ifconfig'"
op|']'
op|','
name|'stdout'
op|'='
name|'subprocess'
op|'.'
name|'PIPE'
op|','
nl|'\n'
name|'stderr'
op|'='
name|'subprocess'
op|'.'
name|'STDOUT'
op|')'
newline|'\n'
name|'ret_val'
op|'='
name|'proc'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
name|'results'
op|'='
name|'proc'
op|'.'
name|'stdout'
op|'.'
name|'read'
op|'('
op|')'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
newline|'\n'
name|'return'
op|'['
name|'x'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'1'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
name|'for'
name|'x'
name|'in'
name|'results'
name|'if'
string|"'inet addr'"
name|'in'
name|'x'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|storage_directory
dedent|''
name|'def'
name|'storage_directory'
op|'('
name|'datadir'
op|','
name|'partition'
op|','
name|'hash'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get the storage directory\n\n    :param datadir: Base data directory\n    :param partition: Partition\n    :param hash: Account, container or object hash\n    :returns: Storage directory\n    """'
newline|'\n'
name|'return'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'datadir'
op|','
name|'partition'
op|','
name|'hash'
op|'['
op|'-'
number|'3'
op|':'
op|']'
op|','
name|'hash'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|hash_path
dedent|''
name|'def'
name|'hash_path'
op|'('
name|'account'
op|','
name|'container'
op|'='
name|'None'
op|','
name|'object'
op|'='
name|'None'
op|','
name|'raw_digest'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get the connonical hash for an account/container/object\n\n    :param account: Account\n    :param container: Container\n    :param object: Object\n    :param raw_digest: If True, return the raw version rather than a hex digest\n    :returns: hash string\n    """'
newline|'\n'
name|'if'
name|'object'
name|'and'
name|'not'
name|'container'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|"'container is required if object is provided'"
op|')'
newline|'\n'
dedent|''
name|'paths'
op|'='
op|'['
name|'account'
op|']'
newline|'\n'
name|'if'
name|'container'
op|':'
newline|'\n'
indent|'        '
name|'paths'
op|'.'
name|'append'
op|'('
name|'container'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'object'
op|':'
newline|'\n'
indent|'        '
name|'paths'
op|'.'
name|'append'
op|'('
name|'object'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'raw_digest'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'md5'
op|'('
string|"'/'"
op|'+'
string|"'/'"
op|'.'
name|'join'
op|'('
name|'paths'
op|')'
op|'+'
name|'HASH_PATH_SUFFIX'
op|')'
op|'.'
name|'digest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'md5'
op|'('
string|"'/'"
op|'+'
string|"'/'"
op|'.'
name|'join'
op|'('
name|'paths'
op|')'
op|'+'
name|'HASH_PATH_SUFFIX'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|lock_path
name|'def'
name|'lock_path'
op|'('
name|'directory'
op|','
name|'timeout'
op|'='
number|'10'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Context manager that acquires a lock on a directory.  This will block until\n    the lock can be acquired, or the timeout time has expired (whichever occurs\n    first).\n\n    :param directory: directory to be locked\n    :param timeout: timeout (in seconds)\n    """'
newline|'\n'
name|'mkdirs'
op|'('
name|'directory'
op|')'
newline|'\n'
name|'fd'
op|'='
name|'os'
op|'.'
name|'open'
op|'('
name|'directory'
op|','
name|'os'
op|'.'
name|'O_RDONLY'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'with'
name|'LockTimeout'
op|'('
name|'timeout'
op|','
name|'directory'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'fcntl'
op|'.'
name|'flock'
op|'('
name|'fd'
op|','
name|'fcntl'
op|'.'
name|'LOCK_EX'
op|'|'
name|'fcntl'
op|'.'
name|'LOCK_NB'
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'err'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'EAGAIN'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'sleep'
op|'('
number|'0.01'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'yield'
name|'True'
newline|'\n'
dedent|''
name|'finally'
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
nl|'\n'
nl|'\n'
DECL|function|lock_parent_directory
dedent|''
dedent|''
name|'def'
name|'lock_parent_directory'
op|'('
name|'filename'
op|','
name|'timeout'
op|'='
number|'10'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Context manager that acquires a lock on the parent directory of the given\n    file path.  This will block until the lock can be acquired, or the timeout\n    time has expired (whichever occurs first).\n\n    :param filename: file path of the parent directory to be locked\n    :param timeout: timeout (in seconds)\n    """'
newline|'\n'
name|'return'
name|'lock_path'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'filename'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_time_units
dedent|''
name|'def'
name|'get_time_units'
op|'('
name|'time_amount'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get a nomralized length of time in the largest unit of time (hours,\n    minutes, or seconds.)\n\n    :param time_amount: length of time in seconds\n    :returns: A touple of (length of time, unit of time) where unit of time is\n              one of (\'h\', \'m\', \'s\')\n    """'
newline|'\n'
name|'time_unit'
op|'='
string|"'s'"
newline|'\n'
name|'if'
name|'time_amount'
op|'>'
number|'60'
op|':'
newline|'\n'
indent|'        '
name|'time_amount'
op|'/='
number|'60'
newline|'\n'
name|'time_unit'
op|'='
string|"'m'"
newline|'\n'
name|'if'
name|'time_amount'
op|'>'
number|'60'
op|':'
newline|'\n'
indent|'            '
name|'time_amount'
op|'/='
number|'60'
newline|'\n'
name|'time_unit'
op|'='
string|"'h'"
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'time_amount'
op|','
name|'time_unit'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|compute_eta
dedent|''
name|'def'
name|'compute_eta'
op|'('
name|'start_time'
op|','
name|'current_value'
op|','
name|'final_value'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Compute an ETA.  Now only if we could also have a progress bar...\n\n    :param start_time: Unix timestamp when the operation began\n    :param current_value: Current value\n    :param final_value: Final value\n    :returns: ETA as a tuple of (length of time, unit of time) where unit of\n              time is one of (\'h\', \'m\', \'s\')\n    """'
newline|'\n'
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start_time'
newline|'\n'
name|'completion'
op|'='
op|'('
name|'float'
op|'('
name|'current_value'
op|')'
op|'/'
name|'final_value'
op|')'
name|'or'
number|'0.00001'
newline|'\n'
name|'return'
name|'get_time_units'
op|'('
number|'1.0'
op|'/'
name|'completion'
op|'*'
name|'elapsed'
op|'-'
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|iter_devices_partitions
dedent|''
name|'def'
name|'iter_devices_partitions'
op|'('
name|'devices_dir'
op|','
name|'item_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Iterate over partitions accross all devices.\n\n    :param devices_dir: Path to devices\n    :param item_type: One of \'accounts\', \'containers\', or \'objects\'\n    :returns: Each iteration returns a tuple of (device, partition)\n    """'
newline|'\n'
name|'devices'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'devices_dir'
op|')'
newline|'\n'
name|'shuffle'
op|'('
name|'devices'
op|')'
newline|'\n'
name|'devices_partitions'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'device'
name|'in'
name|'devices'
op|':'
newline|'\n'
indent|'        '
name|'partitions'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'devices_dir'
op|','
name|'device'
op|','
name|'item_type'
op|')'
op|')'
newline|'\n'
name|'shuffle'
op|'('
name|'partitions'
op|')'
newline|'\n'
name|'devices_partitions'
op|'.'
name|'append'
op|'('
op|'('
name|'device'
op|','
name|'iter'
op|'('
name|'partitions'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'yielded'
op|'='
name|'True'
newline|'\n'
name|'while'
name|'yielded'
op|':'
newline|'\n'
indent|'        '
name|'yielded'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'device'
op|','
name|'partitions'
name|'in'
name|'devices_partitions'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'device'
op|','
name|'partitions'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'yielded'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'except'
name|'StopIteration'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|unlink_older_than
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'unlink_older_than'
op|'('
name|'path'
op|','
name|'mtime'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Remove any file in a given path that that was last modified before mtime.\n\n    :param path: Path to remove file from\n    :mtime: Timestamp of oldest file to keep\n    """'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'fname'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'path'
op|','
name|'fname'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getmtime'
op|'('
name|'fpath'
op|')'
op|'<'
name|'mtime'
op|':'
newline|'\n'
indent|'                    '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'fpath'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|function|item_from_env
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'item_from_env'
op|'('
name|'env'
op|','
name|'item_name'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'item'
op|'='
name|'env'
op|'.'
name|'get'
op|'('
name|'item_name'
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
name|'item'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'logging'
op|'.'
name|'error'
op|'('
string|'"ERROR: %s could not be found in env!"'
op|'%'
name|'item_name'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'item'
newline|'\n'
nl|'\n'
DECL|function|cache_from_env
dedent|''
name|'def'
name|'cache_from_env'
op|'('
name|'env'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'return'
name|'item_from_env'
op|'('
name|'env'
op|','
string|"'swift.cache'"
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
