begin_unit
string|'""" Swift tests """'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'NamedTemporaryFile'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
name|'import'
name|'socket'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|readuntil2crlfs
name|'def'
name|'readuntil2crlfs'
op|'('
name|'fd'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'rv'
op|'='
string|"''"
newline|'\n'
name|'lc'
op|'='
string|"''"
newline|'\n'
name|'crlfs'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'crlfs'
op|'<'
number|'2'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'='
name|'fd'
op|'.'
name|'read'
op|'('
number|'1'
op|')'
newline|'\n'
name|'rv'
op|'='
name|'rv'
op|'+'
name|'c'
newline|'\n'
name|'if'
name|'c'
op|'=='
string|"'\\r'"
name|'and'
name|'lc'
op|'!='
string|"'\\n'"
op|':'
newline|'\n'
indent|'            '
name|'crlfs'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'lc'
op|'=='
string|"'\\r'"
name|'and'
name|'c'
op|'=='
string|"'\\n'"
op|':'
newline|'\n'
indent|'            '
name|'crlfs'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'lc'
op|'='
name|'c'
newline|'\n'
dedent|''
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|connect_tcp
dedent|''
name|'def'
name|'connect_tcp'
op|'('
name|'hostport'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'rv'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
op|')'
newline|'\n'
name|'rv'
op|'.'
name|'connect'
op|'('
name|'hostport'
op|')'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|tmpfile
name|'def'
name|'tmpfile'
op|'('
name|'content'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'with'
name|'NamedTemporaryFile'
op|'('
string|"'w'"
op|','
name|'delete'
op|'='
name|'False'
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'        '
name|'file_name'
op|'='
name|'f'
op|'.'
name|'name'
newline|'\n'
name|'f'
op|'.'
name|'write'
op|'('
name|'str'
op|'('
name|'content'
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'file_name'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'file_name'
op|')'
newline|'\n'
nl|'\n'
DECL|variable|xattr_data
dedent|''
dedent|''
name|'xattr_data'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|function|_get_inode
name|'def'
name|'_get_inode'
op|'('
name|'fd'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'fd'
op|','
name|'int'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'fd'
op|'='
name|'fd'
op|'.'
name|'fileno'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'os'
op|'.'
name|'stat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_ino'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_ino'
newline|'\n'
nl|'\n'
DECL|function|_setxattr
dedent|''
name|'def'
name|'_setxattr'
op|'('
name|'fd'
op|','
name|'k'
op|','
name|'v'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'inode'
op|'='
name|'_get_inode'
op|'('
name|'fd'
op|')'
newline|'\n'
name|'data'
op|'='
name|'xattr_data'
op|'.'
name|'get'
op|'('
name|'inode'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'data'
op|'['
name|'k'
op|']'
op|'='
name|'v'
newline|'\n'
name|'xattr_data'
op|'['
name|'inode'
op|']'
op|'='
name|'data'
newline|'\n'
nl|'\n'
DECL|function|_getxattr
dedent|''
name|'def'
name|'_getxattr'
op|'('
name|'fd'
op|','
name|'k'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'inode'
op|'='
name|'_get_inode'
op|'('
name|'fd'
op|')'
newline|'\n'
name|'data'
op|'='
name|'xattr_data'
op|'.'
name|'get'
op|'('
name|'inode'
op|','
op|'{'
op|'}'
op|')'
op|'.'
name|'get'
op|'('
name|'k'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'data'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
newline|'\n'
dedent|''
name|'return'
name|'data'
newline|'\n'
nl|'\n'
dedent|''
name|'import'
name|'xattr'
newline|'\n'
name|'xattr'
op|'.'
name|'setxattr'
op|'='
name|'_setxattr'
newline|'\n'
name|'xattr'
op|'.'
name|'getxattr'
op|'='
name|'_getxattr'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MockTrue
name|'class'
name|'MockTrue'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Instances of MockTrue evaluate like True\n    Any attr accessed on an instance of MockTrue will return a MockTrue instance\n    Any method called on an instance of MockTrue will return a MockTrue instance\n\n    >>> thing = MockTrue()\n    >>> thing\n    True\n    >>> thing == True # True == True\n    True\n    >>> thing == False # True == False\n    False\n    >>> thing != True # True != True\n    False\n    >>> thing != False # True != False\n    True\n    >>> thing.attribute\n    True\n    >>> thing.method()\n    True\n    >>> thing.attribute.method()\n    True\n    >>> thing.method().attribute\n    True\n\n    """'
newline|'\n'
nl|'\n'
DECL|member|__getattribute__
name|'def'
name|'__getattribute__'
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
name|'return'
name|'self'
newline|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
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
name|'return'
name|'self'
newline|'\n'
DECL|member|__repr__
dedent|''
name|'def'
name|'__repr__'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'repr'
op|'('
name|'True'
op|')'
newline|'\n'
DECL|member|__eq__
dedent|''
name|'def'
name|'__eq__'
op|'('
name|'self'
op|','
name|'other'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'other'
op|'=='
name|'True'
newline|'\n'
DECL|member|__ne__
dedent|''
name|'def'
name|'__ne__'
op|'('
name|'self'
op|','
name|'other'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'other'
op|'!='
name|'True'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
