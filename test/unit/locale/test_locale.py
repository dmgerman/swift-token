begin_unit
comment|'#!/usr/bin/env python'
nl|'\n'
comment|'#-*- coding:utf-8 -*-'
nl|'\n'
comment|'# Copyright (c) 2013 OpenStack Foundation'
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
name|'os'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'string'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'threading'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'    '
name|'from'
name|'subprocess'
name|'import'
name|'check_output'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
indent|'    '
name|'from'
name|'subprocess'
name|'import'
name|'Popen'
op|','
name|'PIPE'
op|','
name|'CalledProcessError'
newline|'\n'
nl|'\n'
DECL|function|check_output
name|'def'
name|'check_output'
op|'('
op|'*'
name|'popenargs'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Lifted from python 2.7 stdlib."""'
newline|'\n'
name|'if'
string|"'stdout'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|"'stdout argument not allowed, it will be '"
nl|'\n'
string|"'overridden.'"
op|')'
newline|'\n'
dedent|''
name|'process'
op|'='
name|'Popen'
op|'('
name|'stdout'
op|'='
name|'PIPE'
op|','
op|'*'
name|'popenargs'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'output'
op|','
name|'unused_err'
op|'='
name|'process'
op|'.'
name|'communicate'
op|'('
op|')'
newline|'\n'
name|'retcode'
op|'='
name|'process'
op|'.'
name|'poll'
op|'('
op|')'
newline|'\n'
name|'if'
name|'retcode'
op|':'
newline|'\n'
indent|'            '
name|'cmd'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|'"args"'
op|')'
newline|'\n'
name|'if'
name|'cmd'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'cmd'
op|'='
name|'popenargs'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'raise'
name|'CalledProcessError'
op|'('
name|'retcode'
op|','
name|'cmd'
op|','
name|'output'
op|'='
name|'output'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'output'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestTranslations
dedent|''
dedent|''
name|'class'
name|'TestTranslations'
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
name|'self'
op|'.'
name|'orig_env'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'var'
name|'in'
string|"'LC_ALL'"
op|','
string|"'SWIFT_LOCALEDIR'"
op|','
string|"'LANGUAGE'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'orig_env'
op|'['
name|'var'
op|']'
op|'='
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
name|'var'
op|')'
newline|'\n'
dedent|''
name|'os'
op|'.'
name|'environ'
op|'['
string|"'LC_ALL'"
op|']'
op|'='
string|"'eo'"
newline|'\n'
name|'os'
op|'.'
name|'environ'
op|'['
string|"'SWIFT_LOCALEDIR'"
op|']'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'__file__'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'environ'
op|'['
string|"'LANGUAGE'"
op|']'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'orig_stop'
op|'='
name|'threading'
op|'.'
name|'_DummyThread'
op|'.'
name|'_Thread__stop'
newline|'\n'
comment|'# See http://stackoverflow.com/questions/13193278/\\'
nl|'\n'
comment|'#     understand-python-threading-bug'
nl|'\n'
name|'threading'
op|'.'
name|'_DummyThread'
op|'.'
name|'_Thread__stop'
op|'='
name|'lambda'
name|'x'
op|':'
number|'42'
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
name|'for'
name|'var'
op|','
name|'val'
name|'in'
name|'self'
op|'.'
name|'orig_env'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'val'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'environ'
op|'['
name|'var'
op|']'
op|'='
name|'val'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'os'
op|'.'
name|'environ'
op|'['
name|'var'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'threading'
op|'.'
name|'_DummyThread'
op|'.'
name|'_Thread__stop'
op|'='
name|'self'
op|'.'
name|'orig_stop'
newline|'\n'
nl|'\n'
DECL|member|test_translations
dedent|''
name|'def'
name|'test_translations'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'path'
op|'='
string|"':'"
op|'.'
name|'join'
op|'('
name|'sys'
op|'.'
name|'path'
op|')'
newline|'\n'
name|'translated_message'
op|'='
name|'check_output'
op|'('
op|'['
string|"'python'"
op|','
name|'__file__'
op|','
name|'path'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'translated_message'
op|','
string|"'prova mesa\xc4\x9do\\n'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|'"__main__"'
op|':'
newline|'\n'
indent|'    '
name|'os'
op|'.'
name|'environ'
op|'['
string|"'LC_ALL'"
op|']'
op|'='
string|"'eo'"
newline|'\n'
name|'os'
op|'.'
name|'environ'
op|'['
string|"'SWIFT_LOCALEDIR'"
op|']'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'__file__'
op|')'
newline|'\n'
name|'sys'
op|'.'
name|'path'
op|'='
name|'string'
op|'.'
name|'split'
op|'('
name|'sys'
op|'.'
name|'argv'
op|'['
number|'1'
op|']'
op|','
string|"':'"
op|')'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'print'
name|'_'
op|'('
string|"'test message'"
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
