begin_unit
comment|'# Licensed under the Apache License, Version 2.0 (the "License"); you may not'
nl|'\n'
comment|'# use this file except in compliance with the License. You may obtain a copy'
nl|'\n'
comment|'# of the License at'
nl|'\n'
comment|'#'
nl|'\n'
comment|'#      http://www.apache.org/licenses/LICENSE-2.0'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Unless required by applicable law or agreed to in writing, software'
nl|'\n'
comment|'# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT'
nl|'\n'
comment|'# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the'
nl|'\n'
comment|'# License for the specific language governing permissions and limitations'
nl|'\n'
comment|'# under the License.'
nl|'\n'
nl|'\n'
string|'"""Tests for swift.cli.info"""'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'mock'
newline|'\n'
name|'from'
name|'cStringIO'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'write_fake_ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'ring'
op|','
name|'utils'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'cli'
op|'.'
name|'info'
name|'import'
name|'print_db_info_metadata'
op|','
name|'print_ring_locations'
op|','
name|'print_info'
op|','
name|'InfoSystemExit'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
op|'.'
name|'server'
name|'import'
name|'AccountController'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'server'
name|'import'
name|'ContainerController'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestCliInfo
name|'class'
name|'TestCliInfo'
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
name|'orig_hp'
op|'='
name|'utils'
op|'.'
name|'HASH_PATH_PREFIX'
op|','
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
newline|'\n'
name|'utils'
op|'.'
name|'HASH_PATH_PREFIX'
op|'='
string|"'info'"
newline|'\n'
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
op|'='
string|"'info'"
newline|'\n'
name|'self'
op|'.'
name|'testdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'mkdtemp'
op|'('
op|')'
op|','
string|"'tmp_test_cli_info'"
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'mkdirs'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
newline|'\n'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sda1'"
op|')'
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sda1'"
op|','
string|"'tmp'"
op|')'
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sdb1'"
op|')'
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sdb1'"
op|','
string|"'tmp'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'account.ring.gz'"
op|')'
newline|'\n'
name|'account_devs'
op|'='
op|'['
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'42'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.2'"
op|','
string|"'port'"
op|':'
number|'43'
op|'}'
op|']'
newline|'\n'
name|'write_fake_ring'
op|'('
name|'self'
op|'.'
name|'account_ring_path'
op|','
op|'*'
name|'account_devs'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'container.ring.gz'"
op|')'
newline|'\n'
name|'container_devs'
op|'='
op|'['
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.3'"
op|','
string|"'port'"
op|':'
number|'42'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.4'"
op|','
string|"'port'"
op|':'
number|'43'
op|'}'
op|']'
newline|'\n'
name|'write_fake_ring'
op|'('
name|'self'
op|'.'
name|'container_ring_path'
op|','
op|'*'
name|'container_devs'
op|')'
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
name|'utils'
op|'.'
name|'HASH_PATH_PREFIX'
op|','
name|'utils'
op|'.'
name|'HASH_PATH_SUFFIX'
op|'='
name|'self'
op|'.'
name|'orig_hp'
newline|'\n'
name|'rmtree'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|assertRaisesMessage
dedent|''
name|'def'
name|'assertRaisesMessage'
op|'('
name|'self'
op|','
name|'exc'
op|','
name|'msg'
op|','
name|'func'
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
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'func'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'msg'
op|','
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'isinstance'
op|'('
name|'e'
op|','
name|'exc'
op|')'
op|','
nl|'\n'
string|'"Expected %s, got %s"'
op|'%'
op|'('
name|'exc'
op|','
name|'type'
op|'('
name|'e'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_print_db_info_metadata
dedent|''
dedent|''
name|'def'
name|'test_print_db_info_metadata'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'Wrong DB type'"
op|','
nl|'\n'
name|'print_db_info_metadata'
op|','
string|"'t'"
op|','
op|'{'
op|'}'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'DB info is None'"
op|','
nl|'\n'
name|'print_db_info_metadata'
op|','
string|"'container'"
op|','
name|'None'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'Info is incomplete'"
op|','
nl|'\n'
name|'print_db_info_metadata'
op|','
string|"'container'"
op|','
op|'{'
op|'}'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
nl|'\n'
name|'info'
op|'='
name|'dict'
op|'('
nl|'\n'
name|'account'
op|'='
string|"'acct'"
op|','
nl|'\n'
name|'created_at'
op|'='
number|'100.1'
op|','
nl|'\n'
name|'put_timestamp'
op|'='
number|'106.3'
op|','
nl|'\n'
name|'delete_timestamp'
op|'='
number|'107.9'
op|','
nl|'\n'
name|'container_count'
op|'='
string|"'3'"
op|','
nl|'\n'
name|'object_count'
op|'='
string|"'20'"
op|','
nl|'\n'
name|'bytes_used'
op|'='
string|"'42'"
op|')'
newline|'\n'
name|'info'
op|'['
string|"'hash'"
op|']'
op|'='
string|"'abaddeadbeefcafe'"
newline|'\n'
name|'info'
op|'['
string|"'id'"
op|']'
op|'='
string|"'abadf100d0ddba11'"
newline|'\n'
name|'md'
op|'='
op|'{'
string|"'x-account-meta-mydata'"
op|':'
op|'('
string|"'swift'"
op|','
string|"'0000000000.00000'"
op|')'
op|','
nl|'\n'
string|"'x-other-something'"
op|':'
op|'('
string|"'boo'"
op|','
string|"'0000000000.00000'"
op|')'
op|'}'
newline|'\n'
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'print_db_info_metadata'
op|'('
string|"'account'"
op|','
name|'info'
op|','
name|'md'
op|')'
newline|'\n'
dedent|''
name|'exp_out'
op|'='
string|"'''Path: /acct\n  Account: acct\n  Account Hash: dc5be2aa4347a22a0fee6bc7de505b47\nMetadata:\n  Created at: 1970-01-01 00:01:40.100000 (100.1)\n  Put Timestamp: 1970-01-01 00:01:46.300000 (106.3)\n  Delete Timestamp: 1970-01-01 00:01:47.900000 (107.9)\n  Container Count: 3\n  Object Count: 20\n  Bytes Used: 42\n  Chexor: abaddeadbeefcafe\n  UUID: abadf100d0ddba11\n  X-Other-Something: boo\nNo system metadata found in db file\n  User Metadata: {'mydata': 'swift'}'''"
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'sorted'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
op|')'
op|','
nl|'\n'
name|'sorted'
op|'('
name|'exp_out'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'info'
op|'='
name|'dict'
op|'('
nl|'\n'
name|'account'
op|'='
string|"'acct'"
op|','
nl|'\n'
name|'container'
op|'='
string|"'cont'"
op|','
nl|'\n'
name|'created_at'
op|'='
string|"'0000000100.10000'"
op|','
nl|'\n'
name|'put_timestamp'
op|'='
string|"'0000000106.30000'"
op|','
nl|'\n'
name|'delete_timestamp'
op|'='
string|"'0000000107.90000'"
op|','
nl|'\n'
name|'object_count'
op|'='
string|"'20'"
op|','
nl|'\n'
name|'bytes_used'
op|'='
string|"'42'"
op|','
nl|'\n'
name|'reported_put_timestamp'
op|'='
string|"'0000010106.30000'"
op|','
nl|'\n'
name|'reported_delete_timestamp'
op|'='
string|"'0000010107.90000'"
op|','
nl|'\n'
name|'reported_object_count'
op|'='
string|"'20'"
op|','
nl|'\n'
name|'reported_bytes_used'
op|'='
string|"'42'"
op|','
nl|'\n'
name|'x_container_foo'
op|'='
string|"'bar'"
op|','
nl|'\n'
name|'x_container_bar'
op|'='
string|"'goo'"
op|')'
newline|'\n'
name|'info'
op|'['
string|"'hash'"
op|']'
op|'='
string|"'abaddeadbeefcafe'"
newline|'\n'
name|'info'
op|'['
string|"'id'"
op|']'
op|'='
string|"'abadf100d0ddba11'"
newline|'\n'
name|'md'
op|'='
op|'{'
string|"'x-container-sysmeta-mydata'"
op|':'
op|'('
string|"'swift'"
op|','
string|"'0000000000.00000'"
op|')'
op|'}'
newline|'\n'
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'print_db_info_metadata'
op|'('
string|"'container'"
op|','
name|'info'
op|','
name|'md'
op|')'
newline|'\n'
dedent|''
name|'exp_out'
op|'='
string|"'''Path: /acct/cont\n  Account: acct\n  Container: cont\n  Container Hash: d49d0ecbb53be1fcc49624f2f7c7ccae\nMetadata:\n  Created at: 1970-01-01 00:01:40.100000 (0000000100.10000)\n  Put Timestamp: 1970-01-01 00:01:46.300000 (0000000106.30000)\n  Delete Timestamp: 1970-01-01 00:01:47.900000 (0000000107.90000)\n  Object Count: 20\n  Bytes Used: 42\n  Reported Put Timestamp: 1970-01-01 02:48:26.300000 (0000010106.30000)\n  Reported Delete Timestamp: 1970-01-01 02:48:27.900000 (0000010107.90000)\n  Reported Object Count: 20\n  Reported Bytes Used: 42\n  Chexor: abaddeadbeefcafe\n  UUID: abadf100d0ddba11\n  X-Container-Bar: goo\n  X-Container-Foo: bar\n  System Metadata: {'mydata': 'swift'}\nNo user metadata found in db file'''"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'sorted'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
op|')'
op|','
nl|'\n'
name|'sorted'
op|'('
name|'exp_out'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_print_ring_locations
dedent|''
name|'def'
name|'test_print_ring_locations'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'None type'"
op|','
name|'print_ring_locations'
op|','
nl|'\n'
name|'None'
op|','
string|"'dir'"
op|','
string|"'acct'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'None type'"
op|','
name|'print_ring_locations'
op|','
nl|'\n'
op|'['
op|']'
op|','
name|'None'
op|','
string|"'acct'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'None type'"
op|','
name|'print_ring_locations'
op|','
nl|'\n'
op|'['
op|']'
op|','
string|"'dir'"
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaisesMessage'
op|'('
name|'ValueError'
op|','
string|"'Ring error'"
op|','
nl|'\n'
name|'print_ring_locations'
op|','
nl|'\n'
op|'['
op|']'
op|','
string|"'dir'"
op|','
string|"'acct'"
op|','
string|"'con'"
op|')'
newline|'\n'
nl|'\n'
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'acctring'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ring_name'
op|'='
string|"'account'"
op|')'
newline|'\n'
name|'print_ring_locations'
op|'('
name|'acctring'
op|','
string|"'dir'"
op|','
string|"'acct'"
op|')'
newline|'\n'
dedent|''
name|'exp_db2'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
string|"'/srv'"
op|','
string|"'node'"
op|','
string|"'sdb1'"
op|','
string|"'dir'"
op|','
string|"'3'"
op|','
string|"'b47'"
op|','
nl|'\n'
string|"'dc5be2aa4347a22a0fee6bc7de505b47'"
op|','
nl|'\n'
string|"'dc5be2aa4347a22a0fee6bc7de505b47.db'"
op|')'
newline|'\n'
name|'exp_db1'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
string|"'/srv'"
op|','
string|"'node'"
op|','
string|"'sda1'"
op|','
string|"'dir'"
op|','
string|"'3'"
op|','
string|"'b47'"
op|','
nl|'\n'
string|"'dc5be2aa4347a22a0fee6bc7de505b47'"
op|','
nl|'\n'
string|"'dc5be2aa4347a22a0fee6bc7de505b47.db'"
op|')'
newline|'\n'
name|'exp_out'
op|'='
op|'('
string|"'Ring locations:\\n  127.0.0.2:43 - %s\\n'"
nl|'\n'
string|"'  127.0.0.1:42 - %s\\n'"
nl|'\n'
string|"'\\nnote: /srv/node is used as default value of `devices`,'"
nl|'\n'
string|"' the real value is set in the account config file on'"
nl|'\n'
string|"' each storage node.'"
op|'%'
op|'('
name|'exp_db2'
op|','
name|'exp_db1'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|','
name|'exp_out'
op|')'
newline|'\n'
nl|'\n'
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'contring'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ring_name'
op|'='
string|"'container'"
op|')'
newline|'\n'
name|'print_ring_locations'
op|'('
name|'contring'
op|','
string|"'dir'"
op|','
string|"'acct'"
op|','
string|"'con'"
op|')'
newline|'\n'
dedent|''
name|'exp_db4'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
string|"'/srv'"
op|','
string|"'node'"
op|','
string|"'sdb1'"
op|','
string|"'dir'"
op|','
string|"'1'"
op|','
string|"'fe6'"
op|','
nl|'\n'
string|"'63e70955d78dfc62821edc07d6ec1fe6'"
op|','
nl|'\n'
string|"'63e70955d78dfc62821edc07d6ec1fe6.db'"
op|')'
newline|'\n'
name|'exp_db3'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
string|"'/srv'"
op|','
string|"'node'"
op|','
string|"'sda1'"
op|','
string|"'dir'"
op|','
string|"'1'"
op|','
string|"'fe6'"
op|','
nl|'\n'
string|"'63e70955d78dfc62821edc07d6ec1fe6'"
op|','
nl|'\n'
string|"'63e70955d78dfc62821edc07d6ec1fe6.db'"
op|')'
newline|'\n'
name|'exp_out'
op|'='
op|'('
string|"'Ring locations:\\n  127.0.0.4:43 - %s\\n'"
nl|'\n'
string|"'  127.0.0.3:42 - %s\\n'"
nl|'\n'
string|"'\\nnote: /srv/node is used as default value of `devices`,'"
nl|'\n'
string|"' the real value is set in the container config file on'"
nl|'\n'
string|"' each storage node.'"
op|'%'
op|'('
name|'exp_db4'
op|','
name|'exp_db3'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|','
name|'exp_out'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_print_info
dedent|''
name|'def'
name|'test_print_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'db_file'
op|'='
string|"'foo'"
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'InfoSystemExit'
op|','
name|'print_info'
op|','
string|"'object'"
op|','
name|'db_file'
op|')'
newline|'\n'
name|'db_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'./acct.db'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'InfoSystemExit'
op|','
name|'print_info'
op|','
string|"'account'"
op|','
name|'db_file'
op|')'
newline|'\n'
nl|'\n'
name|'controller'
op|'='
name|'AccountController'
op|'('
nl|'\n'
op|'{'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
string|"'mount_check'"
op|':'
string|"'false'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/sda1/1/acct'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
nl|'\n'
string|"'HTTP_X_TIMESTAMP'"
op|':'
string|"'0'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'controller'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
number|'201'
op|')'
newline|'\n'
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'exp_raised'
op|'='
name|'False'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'db_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sda1'"
op|','
string|"'accounts'"
op|','
nl|'\n'
string|"'1'"
op|','
string|"'b47'"
op|','
nl|'\n'
string|"'dc5be2aa4347a22a0fee6bc7de505b47'"
op|','
nl|'\n'
string|"'dc5be2aa4347a22a0fee6bc7de505b47.db'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'print_info'
op|'('
string|"'account'"
op|','
name|'db_file'
op|','
name|'swift_dir'
op|'='
name|'self'
op|'.'
name|'testdir'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                '
name|'exp_raised'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'exp_raised'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|'"Unexpected exception raised"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'len'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|')'
op|'>'
number|'800'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'controller'
op|'='
name|'ContainerController'
op|'('
nl|'\n'
op|'{'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
string|"'mount_check'"
op|':'
string|"'false'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/sda1/1/acct/cont'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
nl|'\n'
string|"'HTTP_X_TIMESTAMP'"
op|':'
string|"'0'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'controller'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
number|'201'
op|')'
newline|'\n'
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'exp_raised'
op|'='
name|'False'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'db_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sda1'"
op|','
string|"'containers'"
op|','
nl|'\n'
string|"'1'"
op|','
string|"'cae'"
op|','
nl|'\n'
string|"'d49d0ecbb53be1fcc49624f2f7c7ccae'"
op|','
nl|'\n'
string|"'d49d0ecbb53be1fcc49624f2f7c7ccae.db'"
op|')'
newline|'\n'
name|'orig_cwd'
op|'='
name|'os'
op|'.'
name|'getcwd'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'chdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'db_file'
op|')'
op|')'
newline|'\n'
name|'print_info'
op|'('
string|"'container'"
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'db_file'
op|')'
op|','
nl|'\n'
name|'swift_dir'
op|'='
string|"'/dev/null'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                '
name|'exp_raised'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'chdir'
op|'('
name|'orig_cwd'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'exp_raised'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|'"Unexpected exception raised"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'len'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|')'
op|'>'
number|'600'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'out'
op|'='
name|'StringIO'
op|'('
op|')'
newline|'\n'
name|'exp_raised'
op|'='
name|'False'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'sys.stdout'"
op|','
name|'out'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'db_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sda1'"
op|','
string|"'containers'"
op|','
nl|'\n'
string|"'1'"
op|','
string|"'cae'"
op|','
nl|'\n'
string|"'d49d0ecbb53be1fcc49624f2f7c7ccae'"
op|','
nl|'\n'
string|"'d49d0ecbb53be1fcc49624f2f7c7ccae.db'"
op|')'
newline|'\n'
name|'orig_cwd'
op|'='
name|'os'
op|'.'
name|'getcwd'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'chdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'db_file'
op|')'
op|')'
newline|'\n'
name|'print_info'
op|'('
string|"'account'"
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'db_file'
op|')'
op|','
nl|'\n'
name|'swift_dir'
op|'='
string|"'/dev/null'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'InfoSystemExit'
op|':'
newline|'\n'
indent|'                '
name|'exp_raised'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'chdir'
op|'('
name|'orig_cwd'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'exp_raised'
op|':'
newline|'\n'
indent|'            '
name|'exp_out'
op|'='
string|'\'Does not appear to be a DB of type "account":\''
string|"' ./d49d0ecbb53be1fcc49624f2f7c7ccae.db'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'out'
op|'.'
name|'getvalue'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|','
name|'exp_out'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|'"Expected an InfoSystemExit exception to be raised"'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
