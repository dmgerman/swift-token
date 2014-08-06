begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack Foundation'
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
string|'"""\nScript for generating a form signature for use with FormPost middleware.\n"""'
newline|'\n'
name|'import'
name|'hmac'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'sha1'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'basename'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|main
name|'def'
name|'main'
op|'('
name|'argv'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'len'
op|'('
name|'argv'
op|')'
op|'!='
number|'7'
op|':'
newline|'\n'
indent|'        '
name|'prog'
op|'='
name|'basename'
op|'('
name|'argv'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'print'
string|"'Syntax: %s <path> <redirect> <max_file_size> '"
string|"'<max_file_count> <seconds> <key>'"
op|'%'
name|'prog'
newline|'\n'
name|'print'
newline|'\n'
name|'print'
string|"'Where:'"
newline|'\n'
name|'print'
string|"'  <path>            The prefix to use for form uploaded'"
newline|'\n'
name|'print'
string|"'                    objects. For example:'"
newline|'\n'
name|'print'
string|"'                    /v1/account/container/object_prefix_ would'"
newline|'\n'
name|'print'
string|"'                    ensure all form uploads have that path'"
newline|'\n'
name|'print'
string|"'                    prepended to the browser-given file name.'"
newline|'\n'
name|'print'
string|"'  <redirect>        The URL to redirect the browser to after'"
newline|'\n'
name|'print'
string|"'                    the uploads have completed.'"
newline|'\n'
name|'print'
string|"'  <max_file_size>   The maximum file size per file uploaded.'"
newline|'\n'
name|'print'
string|"'  <max_file_count>  The maximum number of uploaded files'"
newline|'\n'
name|'print'
string|"'                    allowed.'"
newline|'\n'
name|'print'
string|"'  <seconds>         The number of seconds from now to allow'"
newline|'\n'
name|'print'
string|"'                    the form post to begin.'"
newline|'\n'
name|'print'
string|"'  <key>             The X-Account-Meta-Temp-URL-Key for the'"
newline|'\n'
name|'print'
string|"'                    account.'"
newline|'\n'
name|'print'
newline|'\n'
name|'print'
string|"'Example output:'"
newline|'\n'
name|'print'
string|"'    Expires: 1323842228'"
newline|'\n'
name|'print'
string|"'  Signature: 18de97e47345a82c4dbfb3b06a640dbb'"
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'path'
op|','
name|'redirect'
op|','
name|'max_file_size'
op|','
name|'max_file_count'
op|','
name|'seconds'
op|','
name|'key'
op|'='
name|'argv'
op|'['
number|'1'
op|':'
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'max_file_size'
op|'='
name|'int'
op|'('
name|'max_file_size'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'        '
name|'max_file_size'
op|'='
op|'-'
number|'1'
newline|'\n'
dedent|''
name|'if'
name|'max_file_size'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|"'Please use a <max_file_size> value greater than or equal to 0.'"
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'max_file_count'
op|'='
name|'int'
op|'('
name|'max_file_count'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'        '
name|'max_file_count'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'max_file_count'
op|'<'
number|'1'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|"'Please use a positive <max_file_count> value.'"
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'expires'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'+'
name|'int'
op|'('
name|'seconds'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'        '
name|'expires'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'expires'
op|'<'
number|'1'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|"'Please use a positive <seconds> value.'"
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'parts'
op|'='
name|'path'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'4'
op|')'
newline|'\n'
comment|"# Must be four parts, ['', 'v1', 'a', 'c'], must be a v1 request, have"
nl|'\n'
comment|'# account and container values, and optionally have an object prefix.'
nl|'\n'
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'<'
number|'4'
name|'or'
name|'parts'
op|'['
number|'0'
op|']'
name|'or'
name|'parts'
op|'['
number|'1'
op|']'
op|'!='
string|"'v1'"
name|'or'
name|'not'
name|'parts'
op|'['
number|'2'
op|']'
name|'or'
name|'not'
name|'parts'
op|'['
number|'3'
op|']'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|"'<path> must point to a container at least.'"
newline|'\n'
name|'print'
string|"'For example: /v1/account/container'"
newline|'\n'
name|'print'
string|"'         Or: /v1/account/container/object_prefix'"
newline|'\n'
name|'return'
number|'1'
newline|'\n'
dedent|''
name|'sig'
op|'='
name|'hmac'
op|'.'
name|'new'
op|'('
name|'key'
op|','
string|"'%s\\n%s\\n%s\\n%s\\n%s'"
op|'%'
op|'('
name|'path'
op|','
name|'redirect'
op|','
name|'max_file_size'
op|','
nl|'\n'
name|'max_file_count'
op|','
name|'expires'
op|')'
op|','
nl|'\n'
name|'sha1'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'print'
string|"'  Expires:'"
op|','
name|'expires'
newline|'\n'
name|'print'
string|"'Signature:'"
op|','
name|'sig'
newline|'\n'
name|'return'
number|'0'
newline|'\n'
dedent|''
endmarker|''
end_unit
