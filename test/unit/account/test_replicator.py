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
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
name|'import'
name|'replicator'
op|','
name|'backend'
op|','
name|'server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'normalize_timestamp'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
op|'.'
name|'common'
name|'import'
name|'test_db_replicator'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestReplicatorSync
name|'class'
name|'TestReplicatorSync'
op|'('
name|'test_db_replicator'
op|'.'
name|'TestReplicatorSync'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|variable|backend
indent|'    '
name|'backend'
op|'='
name|'backend'
op|'.'
name|'AccountBroker'
newline|'\n'
DECL|variable|datadir
name|'datadir'
op|'='
name|'server'
op|'.'
name|'DATADIR'
newline|'\n'
DECL|variable|replicator_daemon
name|'replicator_daemon'
op|'='
name|'replicator'
op|'.'
name|'AccountReplicator'
newline|'\n'
nl|'\n'
DECL|member|test_sync
name|'def'
name|'test_sync'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
newline|'\n'
name|'put_timestamp'
op|'='
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'put_timestamp'
op|')'
newline|'\n'
comment|'# "replicate" to same database'
nl|'\n'
name|'daemon'
op|'='
name|'replicator'
op|'.'
name|'AccountReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'part'
op|','
name|'node'
op|'='
name|'self'
op|'.'
name|'_get_broker_part_node'
op|'('
name|'broker'
op|')'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_replication_info'
op|'('
op|')'
newline|'\n'
name|'success'
op|'='
name|'daemon'
op|'.'
name|'_repl_to_node'
op|'('
name|'node'
op|','
name|'broker'
op|','
name|'part'
op|','
name|'info'
op|')'
newline|'\n'
comment|'# nothing to do'
nl|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'success'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'1'
op|','
name|'daemon'
op|'.'
name|'stats'
op|'['
string|"'no_change'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sync_remote_missing
dedent|''
name|'def'
name|'test_sync_remote_missing'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
newline|'\n'
name|'put_timestamp'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'put_timestamp'
op|')'
newline|'\n'
comment|'# "replicate" to all other nodes'
nl|'\n'
name|'part'
op|','
name|'node'
op|'='
name|'self'
op|'.'
name|'_get_broker_part_node'
op|'('
name|'broker'
op|')'
newline|'\n'
name|'daemon'
op|'='
name|'self'
op|'.'
name|'_run_once'
op|'('
name|'node'
op|')'
newline|'\n'
comment|'# complete rsync'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'2'
op|','
name|'daemon'
op|'.'
name|'stats'
op|'['
string|"'rsync'"
op|']'
op|')'
newline|'\n'
name|'local_info'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
nl|'\n'
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
number|'1'
op|','
number|'3'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remote_broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
name|'i'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'remote_broker'
op|'.'
name|'db_file'
op|')'
op|')'
newline|'\n'
name|'remote_info'
op|'='
name|'remote_broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'local_info'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'k'
op|'=='
string|"'id'"
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'remote_info'
op|'['
name|'k'
op|']'
op|','
name|'v'
op|','
nl|'\n'
string|'"mismatch remote %s %r != %r"'
op|'%'
op|'('
nl|'\n'
name|'k'
op|','
name|'remote_info'
op|'['
name|'k'
op|']'
op|','
name|'v'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sync_remote_missing_most_rows
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_sync_remote_missing_most_rows'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'put_timestamp'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
comment|'# create "local" broker'
nl|'\n'
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'put_timestamp'
op|')'
newline|'\n'
comment|'# create "remote" broker'
nl|'\n'
name|'remote_broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
number|'1'
op|')'
newline|'\n'
name|'remote_broker'
op|'.'
name|'initialize'
op|'('
name|'put_timestamp'
op|')'
newline|'\n'
comment|'# add a row to "local" db'
nl|'\n'
name|'broker'
op|'.'
name|'put_container'
op|'('
string|"'/a/c'"
op|','
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|','
number|'0'
op|','
number|'0'
op|','
number|'0'
op|','
nl|'\n'
name|'POLICIES'
op|'.'
name|'default'
op|'.'
name|'idx'
op|')'
newline|'\n'
comment|'# replicate'
nl|'\n'
name|'daemon'
op|'='
name|'replicator'
op|'.'
name|'AccountReplicator'
op|'('
op|'{'
string|"'per_diff'"
op|':'
number|'1'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|_rsync_file
name|'def'
name|'_rsync_file'
op|'('
name|'db_file'
op|','
name|'remote_file'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remote_server'
op|','
name|'remote_path'
op|'='
name|'remote_file'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'1'
op|')'
newline|'\n'
name|'dest_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'remote_path'
op|')'
newline|'\n'
name|'shutil'
op|'.'
name|'copy'
op|'('
name|'db_file'
op|','
name|'dest_path'
op|')'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'daemon'
op|'.'
name|'_rsync_file'
op|'='
name|'_rsync_file'
newline|'\n'
name|'part'
op|','
name|'node'
op|'='
name|'self'
op|'.'
name|'_get_broker_part_node'
op|'('
name|'remote_broker'
op|')'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_replication_info'
op|'('
op|')'
newline|'\n'
name|'success'
op|'='
name|'daemon'
op|'.'
name|'_repl_to_node'
op|'('
name|'node'
op|','
name|'broker'
op|','
name|'part'
op|','
name|'info'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'success'
op|')'
newline|'\n'
comment|'# row merge'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'1'
op|','
name|'daemon'
op|'.'
name|'stats'
op|'['
string|"'remote_merge'"
op|']'
op|')'
newline|'\n'
name|'local_info'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
nl|'\n'
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'remote_info'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
nl|'\n'
string|"'a'"
op|','
name|'node_index'
op|'='
number|'1'
op|')'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'local_info'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'k'
op|'=='
string|"'id'"
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'remote_info'
op|'['
name|'k'
op|']'
op|','
name|'v'
op|','
nl|'\n'
string|'"mismatch remote %s %r != %r"'
op|'%'
op|'('
nl|'\n'
name|'k'
op|','
name|'remote_info'
op|'['
name|'k'
op|']'
op|','
name|'v'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sync_remote_missing_one_rows
dedent|''
dedent|''
name|'def'
name|'test_sync_remote_missing_one_rows'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'put_timestamp'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
comment|'# create "local" broker'
nl|'\n'
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'put_timestamp'
op|')'
newline|'\n'
comment|'# create "remote" broker'
nl|'\n'
name|'remote_broker'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
string|"'a'"
op|','
name|'node_index'
op|'='
number|'1'
op|')'
newline|'\n'
name|'remote_broker'
op|'.'
name|'initialize'
op|'('
name|'put_timestamp'
op|')'
newline|'\n'
comment|'# add some rows to both db'
nl|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
number|'10'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'put_timestamp'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'for'
name|'db'
name|'in'
op|'('
name|'broker'
op|','
name|'remote_broker'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'path'
op|'='
string|"'/a/c_%s'"
op|'%'
name|'i'
newline|'\n'
name|'db'
op|'.'
name|'put_container'
op|'('
name|'path'
op|','
name|'put_timestamp'
op|','
number|'0'
op|','
number|'0'
op|','
number|'0'
op|','
nl|'\n'
name|'POLICIES'
op|'.'
name|'default'
op|'.'
name|'idx'
op|')'
newline|'\n'
comment|'# now a row to the "local" broker only'
nl|'\n'
dedent|''
dedent|''
name|'broker'
op|'.'
name|'put_container'
op|'('
string|"'/a/c_missing'"
op|','
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|','
number|'0'
op|','
number|'0'
op|','
number|'0'
op|','
nl|'\n'
name|'POLICIES'
op|'.'
name|'default'
op|'.'
name|'idx'
op|')'
newline|'\n'
comment|'# replicate'
nl|'\n'
name|'daemon'
op|'='
name|'replicator'
op|'.'
name|'AccountReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'part'
op|','
name|'node'
op|'='
name|'self'
op|'.'
name|'_get_broker_part_node'
op|'('
name|'remote_broker'
op|')'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_replication_info'
op|'('
op|')'
newline|'\n'
name|'success'
op|'='
name|'daemon'
op|'.'
name|'_repl_to_node'
op|'('
name|'node'
op|','
name|'broker'
op|','
name|'part'
op|','
name|'info'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'success'
op|')'
newline|'\n'
comment|'# row merge'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'1'
op|','
name|'daemon'
op|'.'
name|'stats'
op|'['
string|"'diff'"
op|']'
op|')'
newline|'\n'
name|'local_info'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
nl|'\n'
string|"'a'"
op|','
name|'node_index'
op|'='
number|'0'
op|')'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'remote_info'
op|'='
name|'self'
op|'.'
name|'_get_broker'
op|'('
nl|'\n'
string|"'a'"
op|','
name|'node_index'
op|'='
number|'1'
op|')'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'local_info'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'k'
op|'=='
string|"'id'"
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'remote_info'
op|'['
name|'k'
op|']'
op|','
name|'v'
op|','
nl|'\n'
string|'"mismatch remote %s %r != %r"'
op|'%'
op|'('
nl|'\n'
name|'k'
op|','
name|'remote_info'
op|'['
name|'k'
op|']'
op|','
name|'v'
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
