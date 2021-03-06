begin_unit
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
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
nl|'\n'
name|'from'
name|'mock'
name|'import'
name|'patch'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'container_sync_realms'
name|'import'
name|'ContainerSyncRealms'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeLogger'
op|','
name|'temptree'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestUtils
name|'class'
name|'TestUtils'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_no_file_there
indent|'    '
name|'def'
name|'test_no_file_there'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'unique'
op|'='
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|'.'
name|'hex'
newline|'\n'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'unique'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'debug'"
op|':'
op|'['
nl|'\n'
string|'"Could not load \'%s\': [Errno 2] No such file or directory: "'
nl|'\n'
string|'"\'%s\'"'
op|'%'
op|'('
name|'unique'
op|','
name|'unique'
op|')'
op|']'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_os_error
dedent|''
name|'def'
name|'test_os_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
nl|'\n'
DECL|function|_mock_getmtime
name|'def'
name|'_mock_getmtime'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'OSError'
op|'('
name|'errno'
op|'.'
name|'EACCES'
op|','
nl|'\n'
name|'os'
op|'.'
name|'strerror'
op|'('
name|'errno'
op|'.'
name|'EACCES'
op|')'
op|'+'
nl|'\n'
string|'": \'%s\'"'
op|'%'
op|'('
name|'fpath'
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'patch'
op|'('
string|"'os.path.getmtime'"
op|','
name|'_mock_getmtime'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'error'"
op|':'
op|'['
nl|'\n'
string|'"Could not load \'%s\': [Errno 13] Permission denied: "'
nl|'\n'
string|'"\'%s\'"'
op|'%'
op|'('
name|'fpath'
op|','
name|'fpath'
op|')'
op|']'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_empty
dedent|''
dedent|''
name|'def'
name|'test_empty'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_error_parsing
dedent|''
dedent|''
name|'def'
name|'test_error_parsing'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"'invalid'"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'error'"
op|':'
op|'['
nl|'\n'
string|'"Could not load \'%s\': File contains no section headers.\\n"'
nl|'\n'
string|'"file: %s, line: 1\\n"'
nl|'\n'
string|'"\'invalid\'"'
op|'%'
op|'('
name|'fpath'
op|','
name|'fpath'
op|')'
op|']'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_one_realm
dedent|''
dedent|''
name|'def'
name|'test_one_realm'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"'''\n[US]\nkey = 9ff3b71c849749dbaec4ccdd3cbab62b\ncluster_dfw1 = http://dfw1.host/v1/\n'''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|','
op|'['
string|"'US'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key'
op|'('
string|"'US'"
op|')'
op|','
string|"'9ff3b71c849749dbaec4ccdd3cbab62b'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key2'
op|'('
string|"'US'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'clusters'
op|'('
string|"'US'"
op|')'
op|','
op|'['
string|"'DFW1'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'csr'
op|'.'
name|'endpoint'
op|'('
string|"'US'"
op|','
string|"'DFW1'"
op|')'
op|','
string|"'http://dfw1.host/v1/'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_two_realms_and_change_a_default
dedent|''
dedent|''
name|'def'
name|'test_two_realms_and_change_a_default'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"'''\n[DEFAULT]\nmtime_check_interval = 60\n\n[US]\nkey = 9ff3b71c849749dbaec4ccdd3cbab62b\ncluster_dfw1 = http://dfw1.host/v1/\n\n[UK]\nkey = e9569809dc8b4951accc1487aa788012\nkey2 = f6351bd1cc36413baa43f7ba1b45e51d\ncluster_lon3 = http://lon3.host/v1/\n'''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'60'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'sorted'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|')'
op|','
op|'['
string|"'UK'"
op|','
string|"'US'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key'
op|'('
string|"'US'"
op|')'
op|','
string|"'9ff3b71c849749dbaec4ccdd3cbab62b'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key2'
op|'('
string|"'US'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'clusters'
op|'('
string|"'US'"
op|')'
op|','
op|'['
string|"'DFW1'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'csr'
op|'.'
name|'endpoint'
op|'('
string|"'US'"
op|','
string|"'DFW1'"
op|')'
op|','
string|"'http://dfw1.host/v1/'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key'
op|'('
string|"'UK'"
op|')'
op|','
string|"'e9569809dc8b4951accc1487aa788012'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'csr'
op|'.'
name|'key2'
op|'('
string|"'UK'"
op|')'
op|','
string|"'f6351bd1cc36413baa43f7ba1b45e51d'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'clusters'
op|'('
string|"'UK'"
op|')'
op|','
op|'['
string|"'LON3'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'csr'
op|'.'
name|'endpoint'
op|'('
string|"'UK'"
op|','
string|"'LON3'"
op|')'
op|','
string|"'http://lon3.host/v1/'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_empty_realm
dedent|''
dedent|''
name|'def'
name|'test_empty_realm'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"'''\n[US]\n'''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'realms'
op|'('
op|')'
op|','
op|'['
string|"'US'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key'
op|'('
string|"'US'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'key2'
op|'('
string|"'US'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'clusters'
op|'('
string|"'US'"
op|')'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'endpoint'
op|'('
string|"'US'"
op|','
string|"'JUST_TESTING'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_bad_mtime_check_interval
dedent|''
dedent|''
name|'def'
name|'test_bad_mtime_check_interval'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"'''\n[DEFAULT]\nmtime_check_interval = invalid\n'''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'logger'
op|'.'
name|'all_log_lines'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'error'"
op|':'
op|'['
nl|'\n'
string|'"Error in \'%s\' with mtime_check_interval: invalid literal "'
nl|'\n'
string|'"for int() with base 10: \'invalid\'"'
op|'%'
name|'fpath'
op|']'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'csr'
op|'.'
name|'mtime_check_interval'
op|','
number|'300'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_sig
dedent|''
dedent|''
name|'def'
name|'test_get_sig'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fname'
op|'='
string|"'container-sync-realms.conf'"
newline|'\n'
name|'fcontents'
op|'='
string|"''"
newline|'\n'
name|'with'
name|'temptree'
op|'('
op|'['
name|'fname'
op|']'
op|','
op|'['
name|'fcontents'
op|']'
op|')'
name|'as'
name|'tempdir'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'fname'
op|')'
newline|'\n'
name|'csr'
op|'='
name|'ContainerSyncRealms'
op|'('
name|'fpath'
op|','
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'csr'
op|'.'
name|'get_sig'
op|'('
nl|'\n'
string|"'GET'"
op|','
string|"'/some/path'"
op|','
string|"'1387212345.67890'"
op|','
string|"'my_nonce'"
op|','
nl|'\n'
string|"'realm_key'"
op|','
string|"'user_key'"
op|')'
op|','
nl|'\n'
string|"'5a6eb486eb7b44ae1b1f014187a94529c3f9c8f9'"
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
