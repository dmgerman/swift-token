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
nl|'\n'
DECL|class|MockTrue
dedent|''
dedent|''
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
