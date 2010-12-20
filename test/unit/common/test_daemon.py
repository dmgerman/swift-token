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
comment|'# TODO: Test kill_children signal handlers'
nl|'\n'
nl|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'getpass'
name|'import'
name|'getuser'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'from'
name|'StringIO'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'tmpfile'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'daemon'
op|','
name|'utils'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MyDaemon
name|'class'
name|'MyDaemon'
op|'('
name|'daemon'
op|'.'
name|'Daemon'
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
name|'None'
op|')'
newline|'\n'
name|'MyDaemon'
op|'.'
name|'forever_called'
op|'='
name|'False'
newline|'\n'
name|'MyDaemon'
op|'.'
name|'once_called'
op|'='
name|'False'
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
name|'MyDaemon'
op|'.'
name|'forever_called'
op|'='
name|'True'
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
name|'MyDaemon'
op|'.'
name|'once_called'
op|'='
name|'True'
newline|'\n'
nl|'\n'
DECL|member|run_raise
dedent|''
name|'def'
name|'run_raise'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'OSError'
newline|'\n'
nl|'\n'
DECL|member|run_quit
dedent|''
name|'def'
name|'run_quit'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'KeyboardInterrupt'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestDaemon
dedent|''
dedent|''
name|'class'
name|'TestDaemon'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_create
indent|'    '
name|'def'
name|'test_create'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'d'
op|'='
name|'daemon'
op|'.'
name|'Daemon'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'d'
op|'.'
name|'conf'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'d'
op|'.'
name|'logger'
op|','
name|'utils'
op|'.'
name|'LogAdapter'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_stubs
dedent|''
name|'def'
name|'test_stubs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'d'
op|'='
name|'daemon'
op|'.'
name|'Daemon'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'NotImplementedError'
op|','
name|'d'
op|'.'
name|'run_once'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'NotImplementedError'
op|','
name|'d'
op|'.'
name|'run_forever'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestRunDaemon
dedent|''
dedent|''
name|'class'
name|'TestRunDaemon'
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
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
op|'='
string|"'endcap'"
newline|'\n'
name|'utils'
op|'.'
name|'drop_privileges'
op|'='
name|'lambda'
op|'*'
name|'args'
op|':'
name|'None'
newline|'\n'
name|'utils'
op|'.'
name|'capture_stdio'
op|'='
name|'lambda'
op|'*'
name|'args'
op|':'
name|'None'
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
name|'reload'
op|'('
name|'utils'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run
dedent|''
name|'def'
name|'test_run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'d'
op|'='
name|'MyDaemon'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'MyDaemon'
op|'.'
name|'forever_called'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'MyDaemon'
op|'.'
name|'once_called'
op|')'
newline|'\n'
comment|'# test default'
nl|'\n'
name|'d'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'d'
op|'.'
name|'forever_called'
op|','
name|'True'
op|')'
newline|'\n'
comment|'# test once'
nl|'\n'
name|'d'
op|'.'
name|'run'
op|'('
name|'once'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'d'
op|'.'
name|'once_called'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_run_daemon
dedent|''
name|'def'
name|'test_run_daemon'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sample_conf'
op|'='
string|'"""[my-daemon]\nuser = %s\n"""'
op|'%'
name|'getuser'
op|'('
op|')'
newline|'\n'
name|'with'
name|'tmpfile'
op|'('
name|'sample_conf'
op|')'
name|'as'
name|'conf_file'
op|':'
newline|'\n'
indent|'            '
name|'daemon'
op|'.'
name|'run_daemon'
op|'('
name|'MyDaemon'
op|','
name|'conf_file'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'MyDaemon'
op|'.'
name|'forever_called'
op|','
name|'True'
op|')'
newline|'\n'
name|'daemon'
op|'.'
name|'run_daemon'
op|'('
name|'MyDaemon'
op|','
name|'conf_file'
op|','
name|'once'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'MyDaemon'
op|'.'
name|'once_called'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
comment|'# test raise in daemon code'
nl|'\n'
name|'MyDaemon'
op|'.'
name|'run_once'
op|'='
name|'MyDaemon'
op|'.'
name|'run_raise'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'OSError'
op|','
name|'daemon'
op|'.'
name|'run_daemon'
op|','
name|'MyDaemon'
op|','
nl|'\n'
name|'conf_file'
op|','
name|'once'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
comment|'# test user quit'
nl|'\n'
name|'MyDaemon'
op|'.'
name|'run_forever'
op|'='
name|'MyDaemon'
op|'.'
name|'run_quit'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'logger'
op|'='
name|'logging'
op|'.'
name|'getLogger'
op|'('
op|')'
newline|'\n'
name|'logger'
op|'.'
name|'addHandler'
op|'('
name|'logging'
op|'.'
name|'StreamHandler'
op|'('
name|'sio'
op|')'
op|')'
newline|'\n'
name|'logger'
op|'='
name|'utils'
op|'.'
name|'get_logger'
op|'('
name|'None'
op|','
string|"'server'"
op|')'
newline|'\n'
name|'daemon'
op|'.'
name|'run_daemon'
op|'('
name|'MyDaemon'
op|','
name|'conf_file'
op|','
name|'logger'
op|'='
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
string|"'user quit'"
name|'in'
name|'sio'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'lower'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
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
