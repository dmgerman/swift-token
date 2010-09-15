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
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
newline|'\n'
nl|'\n'
DECL|class|Daemon
name|'class'
name|'Daemon'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Daemon base class"""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'utils'
op|'.'
name|'get_logger'
op|'('
name|'conf'
op|','
string|"'swift-daemon'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Override this to run the script once"""'
newline|'\n'
name|'raise'
name|'NotImplementedError'
op|'('
string|"'run_once not implemented'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
name|'def'
name|'run_forever'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Override this to run forever"""'
newline|'\n'
name|'raise'
name|'NotImplementedError'
op|'('
string|"'run_forever not implemented'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|','
name|'once'
op|'='
name|'False'
op|','
name|'capture_stdout'
op|'='
name|'True'
op|','
name|'capture_stderr'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Run the daemon"""'
newline|'\n'
comment|'# log uncaught exceptions'
nl|'\n'
name|'sys'
op|'.'
name|'excepthook'
op|'='
name|'lambda'
op|'*'
name|'exc_info'
op|':'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'critical'
op|'('
string|"'UNCAUGHT EXCEPTION'"
op|','
name|'exc_info'
op|'='
name|'exc_info'
op|')'
newline|'\n'
name|'if'
name|'capture_stdout'
op|':'
newline|'\n'
indent|'            '
name|'sys'
op|'.'
name|'stdout'
op|'='
name|'utils'
op|'.'
name|'LoggerFileObject'
op|'('
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'capture_stderr'
op|':'
newline|'\n'
indent|'            '
name|'sys'
op|'.'
name|'stderr'
op|'='
name|'utils'
op|'.'
name|'LoggerFileObject'
op|'('
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'utils'
op|'.'
name|'drop_privileges'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'user'"
op|','
string|"'swift'"
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'setsid'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
nl|'\n'
DECL|function|kill_children
dedent|''
name|'def'
name|'kill_children'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_IGN'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'killpg'
op|'('
number|'0'
op|','
name|'signal'
op|'.'
name|'SIGTERM'
op|')'
newline|'\n'
name|'sys'
op|'.'
name|'exit'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'kill_children'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'once'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'run_forever'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
