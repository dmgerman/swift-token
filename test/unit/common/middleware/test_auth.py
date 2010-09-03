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
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'auth'
newline|'\n'
nl|'\n'
comment|'# mocks'
nl|'\n'
name|'logging'
op|'.'
name|'getLogger'
op|'('
op|')'
op|'.'
name|'addHandler'
op|'('
name|'logging'
op|'.'
name|'StreamHandler'
op|'('
name|'sys'
op|'.'
name|'stdout'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeMemcache
name|'class'
name|'FakeMemcache'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
name|'def'
name|'get'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'store'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
newline|'\n'
nl|'\n'
DECL|member|set
dedent|''
name|'def'
name|'set'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'value'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|incr
dedent|''
name|'def'
name|'incr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'self'
op|'.'
name|'store'
op|'.'
name|'setdefault'
op|'('
name|'key'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|soft_lock
name|'def'
name|'soft_lock'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'0'
op|','
name|'retries'
op|'='
number|'5'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|delete
dedent|''
name|'def'
name|'delete'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|mock_http_connect
dedent|''
dedent|''
name|'def'
name|'mock_http_connect'
op|'('
name|'response'
op|','
name|'headers'
op|'='
name|'None'
op|','
name|'with_exc'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
DECL|class|FakeConn
indent|'    '
name|'class'
name|'FakeConn'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'        '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'status'
op|','
name|'headers'
op|','
name|'with_exc'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'status'
op|'='
name|'status'
newline|'\n'
name|'self'
op|'.'
name|'reason'
op|'='
string|"'Fake'"
newline|'\n'
name|'self'
op|'.'
name|'host'
op|'='
string|"'1.2.3.4'"
newline|'\n'
name|'self'
op|'.'
name|'port'
op|'='
string|"'1234'"
newline|'\n'
name|'self'
op|'.'
name|'with_exc'
op|'='
name|'with_exc'
newline|'\n'
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
DECL|member|getresponse
dedent|''
dedent|''
name|'def'
name|'getresponse'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'with_exc'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'test'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
newline|'\n'
DECL|member|getheader
dedent|''
name|'def'
name|'getheader'
op|'('
name|'self'
op|','
name|'header'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
newline|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'amt'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"''"
newline|'\n'
DECL|member|close
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'lambda'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|':'
name|'FakeConn'
op|'('
name|'response'
op|','
name|'headers'
op|','
name|'with_exc'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Logger
dedent|''
name|'class'
name|'Logger'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'error_value'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'exception_value'
op|'='
name|'None'
newline|'\n'
DECL|member|error
dedent|''
name|'def'
name|'error'
op|'('
name|'self'
op|','
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
indent|'        '
name|'self'
op|'.'
name|'error_value'
op|'='
op|'('
name|'msg'
op|','
name|'args'
op|','
name|'kwargs'
op|')'
newline|'\n'
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
op|','
op|'**'
name|'kwargs'
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
name|'self'
op|'.'
name|'exception_value'
op|'='
op|'('
name|'msg'
op|','
nl|'\n'
string|"'%s %s'"
op|'%'
op|'('
name|'exc'
op|'.'
name|'__class__'
op|'.'
name|'__name__'
op|','
name|'str'
op|'('
name|'exc'
op|')'
op|')'
op|','
name|'args'
op|','
name|'kwargs'
op|')'
newline|'\n'
comment|'# tests'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
dedent|''
dedent|''
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__call__
indent|'    '
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
string|'"OK"'
newline|'\n'
nl|'\n'
DECL|function|start_response
dedent|''
dedent|''
name|'def'
name|'start_response'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|TestAuth
dedent|''
name|'class'
name|'TestAuth'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
comment|'# TODO: With the auth refactor, these tests have to be refactored as well.'
nl|'\n'
comment|"# I brought some over from another refactor I've been trying, but these"
nl|'\n'
comment|'# also need work.'
nl|'\n'
nl|'\n'
DECL|member|test_clean_acl
indent|'    '
name|'def'
name|'test_clean_acl'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'devauth'
op|'='
name|'auth'
op|'.'
name|'DevAuthorization'
op|'('
name|'None'
op|','
name|'None'
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:any'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:any'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:specific.host'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:specific.host'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:.ending.with'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:.ending.with'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:one,.ref:two'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:one,.ref:two'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:any,.ref:-specific.host'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:any,.ref:-specific.host'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:any,.ref:-.ending.with'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:any,.ref:-.ending.with'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:one,.ref:-two'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:one,.ref:-two'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'devauth'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
nl|'\n'
string|"' .ref : one , ,, .ref:two , .ref : - three '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.ref:one,.ref:two,.ref:-three'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'devauth'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.ref:'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'devauth'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"' .ref : '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'devauth'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
nl|'\n'
string|"'user , .ref : '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'devauth'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.ref:-'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'devauth'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
nl|'\n'
string|"' .ref : - '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'devauth'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
nl|'\n'
string|"'user , .ref : - '"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_acl
dedent|''
name|'def'
name|'test_parse_acl'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'devauth'
op|'='
name|'auth'
op|'.'
name|'DevAuthorization'
op|'('
name|'None'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
name|'None'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
string|"''"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
string|"'.ref:ref1'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
string|"'ref1'"
op|']'
op|','
op|'['
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
string|"'.ref:-ref1'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
string|"'-ref1'"
op|']'
op|','
op|'['
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
string|"'account:user'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
op|']'
op|','
op|'['
op|']'
op|','
op|'['
string|"'account:user'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
string|"'account'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
op|']'
op|','
op|'['
string|"'account'"
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
string|"'acc1,acc2:usr2,.ref:ref3,.ref:-ref4'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
string|"'ref3'"
op|','
string|"'-ref4'"
op|']'
op|','
op|'['
string|"'acc1'"
op|']'
op|','
op|'['
string|"'acc2:usr2'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'devauth'
op|'.'
name|'parse_acl'
op|'('
nl|'\n'
string|"'acc1,acc2:usr2,.ref:ref3,acc3,acc4:usr4,.ref:ref5,.ref:-ref6'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
string|"'ref3'"
op|','
string|"'ref5'"
op|','
string|"'-ref6'"
op|']'
op|','
op|'['
string|"'acc1'"
op|','
string|"'acc3'"
op|']'
op|','
nl|'\n'
op|'['
string|"'acc2:usr2'"
op|','
string|"'acc4:usr4'"
op|']'
op|')'
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
