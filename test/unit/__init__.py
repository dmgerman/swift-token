begin_unit
string|'""" Swift tests """'
newline|'\n'
nl|'\n'
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
dedent|''
endmarker|''
end_unit
