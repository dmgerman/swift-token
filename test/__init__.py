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
comment|'# See http://code.google.com/p/python-nose/issues/detail?id=373'
nl|'\n'
comment|'# The code below enables nosetests to work with i18n _() blocks'
nl|'\n'
name|'from'
name|'__future__'
name|'import'
name|'print_function'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'    '
name|'from'
name|'unittest'
op|'.'
name|'util'
name|'import'
name|'safe_repr'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
comment|'# Probably py26'
nl|'\n'
DECL|variable|_MAX_LENGTH
indent|'    '
name|'_MAX_LENGTH'
op|'='
number|'80'
newline|'\n'
nl|'\n'
DECL|function|safe_repr
name|'def'
name|'safe_repr'
op|'('
name|'obj'
op|','
name|'short'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'result'
op|'='
name|'repr'
op|'('
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'result'
op|'='
name|'object'
op|'.'
name|'__repr__'
op|'('
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'short'
name|'or'
name|'len'
op|'('
name|'result'
op|')'
op|'<'
name|'_MAX_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'result'
newline|'\n'
dedent|''
name|'return'
name|'result'
op|'['
op|':'
name|'_MAX_LENGTH'
op|']'
op|'+'
string|"' [truncated]...'"
newline|'\n'
nl|'\n'
comment|'# make unittests pass on all locale'
nl|'\n'
dedent|''
dedent|''
name|'import'
name|'swift'
newline|'\n'
name|'setattr'
op|'('
name|'swift'
op|','
string|"'gettext_'"
op|','
name|'lambda'
name|'x'
op|':'
name|'x'
op|')'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'readconf'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'# Work around what seems to be a Python bug.'
nl|'\n'
comment|'# c.f. https://bugs.launchpad.net/swift/+bug/820185.'
nl|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'logging'
op|'.'
name|'raiseExceptions'
op|'='
name|'False'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_config
name|'def'
name|'get_config'
op|'('
name|'section_name'
op|'='
name|'None'
op|','
name|'defaults'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Attempt to get a test config dictionary.\n\n    :param section_name: the section to read (all sections if not defined)\n    :param defaults: an optional dictionary namespace of defaults\n    """'
newline|'\n'
name|'config'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'if'
name|'defaults'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'config'
op|'.'
name|'update'
op|'('
name|'defaults'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'config_file'
op|'='
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_TEST_CONFIG_FILE'"
op|','
nl|'\n'
string|"'/etc/swift/test.conf'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'config'
op|'='
name|'readconf'
op|'('
name|'config_file'
op|','
name|'section_name'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'SystemExit'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'config_file'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'print'
op|'('
string|"'Unable to read test config %s - file not found'"
nl|'\n'
op|'%'
name|'config_file'
op|','
name|'file'
op|'='
name|'sys'
op|'.'
name|'stderr'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'not'
name|'os'
op|'.'
name|'access'
op|'('
name|'config_file'
op|','
name|'os'
op|'.'
name|'R_OK'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'print'
op|'('
string|"'Unable to read test config %s - permission denied'"
nl|'\n'
op|'%'
name|'config_file'
op|','
name|'file'
op|'='
name|'sys'
op|'.'
name|'stderr'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'print'
op|'('
string|"'Unable to read test config %s - section %s not found'"
nl|'\n'
op|'%'
op|'('
name|'config_file'
op|','
name|'section_name'
op|')'
op|','
name|'file'
op|'='
name|'sys'
op|'.'
name|'stderr'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'config'
newline|'\n'
dedent|''
endmarker|''
end_unit
