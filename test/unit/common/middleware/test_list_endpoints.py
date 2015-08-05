begin_unit
comment|'# Copyright (c) 2012 OpenStack Foundation'
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
name|'array'
newline|'\n'
name|'import'
name|'json'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'mock'
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
name|'utils'
name|'import'
name|'split_path'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
op|','
name|'Response'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'list_endpoints'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'StoragePolicy'
op|','
name|'POLICIES'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'patch_policies'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
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
name|'Response'
op|'('
name|'body'
op|'='
string|'"FakeApp"'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
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
nl|'\n'
dedent|''
op|'@'
name|'patch_policies'
op|'('
op|'['
name|'StoragePolicy'
op|'('
number|'0'
op|','
string|"'zero'"
op|','
name|'False'
op|')'
op|','
nl|'\n'
name|'StoragePolicy'
op|'('
number|'1'
op|','
string|"'one'"
op|','
name|'True'
op|')'
op|']'
op|')'
newline|'\n'
DECL|class|TestListEndpoints
name|'class'
name|'TestListEndpoints'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
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
name|'HASH_PATH_PREFIX'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'testdir'
op|'='
name|'mkdtemp'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'accountgz'
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
name|'containergz'
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
string|"'container.ring.gz'"
op|')'
newline|'\n'
name|'objectgz'
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
string|"'object.ring.gz'"
op|')'
newline|'\n'
name|'objectgz_1'
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
string|"'object-1.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'policy_to_test'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'expected_path'
op|'='
op|'('
string|"'v1'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o1'"
op|')'
newline|'\n'
nl|'\n'
comment|"# Let's make the rings slightly different so we can test"
nl|'\n'
comment|"# that the correct ring is consulted (e.g. we don't consult"
nl|'\n'
comment|'# the object ring to get nodes for a container)'
nl|'\n'
name|'intended_replica2part2dev_id_a'
op|'='
op|'['
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'3'
op|','
number|'1'
op|','
number|'3'
op|','
number|'1'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'0'
op|','
number|'3'
op|','
number|'1'
op|','
number|'4'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'1'
op|','
number|'4'
op|','
number|'0'
op|','
number|'3'
op|']'
op|')'
op|']'
newline|'\n'
name|'intended_replica2part2dev_id_c'
op|'='
op|'['
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'4'
op|','
number|'3'
op|','
number|'0'
op|','
number|'1'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'0'
op|','
number|'1'
op|','
number|'3'
op|','
number|'4'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'3'
op|','
number|'4'
op|','
number|'0'
op|','
number|'1'
op|']'
op|')'
op|']'
newline|'\n'
name|'intended_replica2part2dev_id_o'
op|'='
op|'['
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'0'
op|','
number|'1'
op|','
number|'0'
op|','
number|'1'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'3'
op|','
number|'4'
op|','
number|'3'
op|','
number|'4'
op|']'
op|')'
op|']'
newline|'\n'
name|'intended_replica2part2dev_id_o_1'
op|'='
op|'['
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'1'
op|','
number|'0'
op|','
number|'1'
op|','
number|'0'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'1'
op|','
number|'0'
op|','
number|'1'
op|','
number|'0'
op|']'
op|')'
op|','
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
op|'['
number|'4'
op|','
number|'3'
op|','
number|'4'
op|','
number|'3'
op|']'
op|')'
op|']'
newline|'\n'
name|'intended_devs'
op|'='
op|'['
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.1.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.1.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sdb1'"
op|'}'
op|','
nl|'\n'
name|'None'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.2.1'"
op|','
string|"'port'"
op|':'
number|'6000'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sdc1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
number|'4'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'10.1.2.2'"
op|','
string|"'port'"
op|':'
number|'6000'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sdd1'"
op|'}'
op|']'
newline|'\n'
name|'intended_part_shift'
op|'='
number|'30'
newline|'\n'
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'intended_replica2part2dev_id_a'
op|','
nl|'\n'
name|'intended_devs'
op|','
name|'intended_part_shift'
op|')'
op|'.'
name|'save'
op|'('
name|'accountgz'
op|')'
newline|'\n'
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'intended_replica2part2dev_id_c'
op|','
nl|'\n'
name|'intended_devs'
op|','
name|'intended_part_shift'
op|')'
op|'.'
name|'save'
op|'('
name|'containergz'
op|')'
newline|'\n'
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'intended_replica2part2dev_id_o'
op|','
nl|'\n'
name|'intended_devs'
op|','
name|'intended_part_shift'
op|')'
op|'.'
name|'save'
op|'('
name|'objectgz'
op|')'
newline|'\n'
name|'ring'
op|'.'
name|'RingData'
op|'('
name|'intended_replica2part2dev_id_o_1'
op|','
nl|'\n'
name|'intended_devs'
op|','
name|'intended_part_shift'
op|')'
op|'.'
name|'save'
op|'('
name|'objectgz_1'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'FakeApp'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'list_endpoints'
op|'='
name|'list_endpoints'
op|'.'
name|'filter_factory'
op|'('
nl|'\n'
op|'{'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|'}'
op|')'
op|'('
name|'self'
op|'.'
name|'app'
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
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|FakeGetInfo
dedent|''
name|'def'
name|'FakeGetInfo'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'app'
op|','
name|'swift_source'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'info'
op|'='
op|'{'
string|"'status'"
op|':'
number|'0'
op|','
string|"'sync_key'"
op|':'
name|'None'
op|','
string|"'meta'"
op|':'
op|'{'
op|'}'
op|','
nl|'\n'
string|"'cors'"
op|':'
op|'{'
string|"'allow_origin'"
op|':'
name|'None'
op|','
string|"'expose_headers'"
op|':'
name|'None'
op|','
nl|'\n'
string|"'max_age'"
op|':'
name|'None'
op|'}'
op|','
nl|'\n'
string|"'sysmeta'"
op|':'
op|'{'
op|'}'
op|','
string|"'read_acl'"
op|':'
name|'None'
op|','
nl|'\n'
string|"'object_count'"
op|':'
name|'None'
op|','
string|"'write_acl'"
op|':'
name|'None'
op|','
string|"'versions'"
op|':'
name|'None'
op|','
nl|'\n'
string|"'bytes'"
op|':'
name|'None'
op|'}'
newline|'\n'
name|'info'
op|'['
string|"'storage_policy'"
op|']'
op|'='
name|'self'
op|'.'
name|'policy_to_test'
newline|'\n'
op|'('
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'unused'
op|')'
op|'='
name|'split_path'
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
number|'3'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
op|'('
name|'version'
op|','
name|'account'
op|','
name|'container'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'expected_path'
op|'['
op|':'
number|'3'
op|']'
op|')'
newline|'\n'
name|'return'
name|'info'
newline|'\n'
nl|'\n'
DECL|member|test_parse_response_version
dedent|''
name|'def'
name|'test_parse_response_version'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'expectations'
op|'='
op|'{'
nl|'\n'
string|"''"
op|':'
number|'1.0'
op|','
comment|'# legacy compat'
nl|'\n'
string|"'/1'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'/v1'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'/1.0'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'/v1.0'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'/2'"
op|':'
number|'2.0'
op|','
nl|'\n'
string|"'/v2'"
op|':'
number|'2.0'
op|','
nl|'\n'
string|"'/2.0'"
op|':'
number|'2.0'
op|','
nl|'\n'
string|"'/v2.0'"
op|':'
number|'2.0'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'accounts'
op|'='
op|'('
nl|'\n'
string|"'AUTH_test'"
op|','
nl|'\n'
string|"'test'"
op|','
nl|'\n'
string|"'verybadreseller_prefix'"
nl|'\n'
string|"'verybadaccount'"
nl|'\n'
op|')'
newline|'\n'
name|'for'
name|'expected_account'
name|'in'
name|'accounts'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'version'
op|','
name|'expected'
name|'in'
name|'expectations'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'path'
op|'='
string|"'/endpoints%s/%s/c/o'"
op|'%'
op|'('
name|'version'
op|','
name|'expected_account'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|')'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|'('
name|'req'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'version'
op|','
name|'expected'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'account'
op|','
name|'expected_account'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AssertionError'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Unexpected result from parse path %r: %r != %r'"
nl|'\n'
op|'%'
op|'('
name|'path'
op|','
op|'('
name|'version'
op|','
name|'account'
op|')'
op|','
nl|'\n'
op|'('
name|'expected'
op|','
name|'expected_account'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_version_that_looks_like_account
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_parse_version_that_looks_like_account'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Demonstrate the failure mode for versions that look like accounts,\n        if you can make _parse_path better and this is the *only* test that\n        fails you can delete it ;)\n        """'
newline|'\n'
name|'bad_versions'
op|'='
op|'('
nl|'\n'
string|"'v_3'"
op|','
nl|'\n'
string|"'verybadreseller_prefix'"
op|','
nl|'\n'
op|')'
newline|'\n'
name|'for'
name|'bad_version'
name|'in'
name|'bad_versions'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/%s/a/c/o'"
op|'%'
name|'bad_version'
op|')'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'version'
op|','
number|'1.0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'account'
op|','
name|'bad_version'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'container'
op|','
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'obj'
op|','
string|"'c/o'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_account_that_looks_like_version
dedent|''
dedent|''
name|'def'
name|'test_parse_account_that_looks_like_version'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Demonstrate the failure mode for accounts that looks like versions,\n        if you can make _parse_path better and this is the *only* test that\n        fails you can delete it ;)\n        """'
newline|'\n'
name|'bad_accounts'
op|'='
op|'('
nl|'\n'
string|"'v3.0'"
op|','
string|"'verybaddaccountwithnoprefix'"
op|','
nl|'\n'
op|')'
newline|'\n'
name|'for'
name|'bad_account'
name|'in'
name|'bad_accounts'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/%s/c/o'"
op|'%'
name|'bad_account'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|','
name|'req'
op|')'
newline|'\n'
dedent|''
name|'even_worse_accounts'
op|'='
op|'{'
nl|'\n'
string|"'v1'"
op|':'
number|'1.0'
op|','
nl|'\n'
string|"'v2.0'"
op|':'
number|'2.0'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'for'
name|'bad_account'
op|','
name|'guessed_version'
name|'in'
name|'even_worse_accounts'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/%s/c/o'"
op|'%'
name|'bad_account'
op|')'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'version'
op|','
name|'guessed_version'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'account'
op|','
string|"'c'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'container'
op|','
string|"'o'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'obj'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_object_ring
dedent|''
dedent|''
name|'def'
name|'test_get_object_ring'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'isinstance'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'get_object_ring'
op|'('
number|'0'
op|')'
op|','
nl|'\n'
name|'ring'
op|'.'
name|'Ring'
op|')'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'isinstance'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'get_object_ring'
op|'('
number|'1'
op|')'
op|','
nl|'\n'
name|'ring'
op|'.'
name|'Ring'
op|')'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'get_object_ring'
op|','
number|'99'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_path_no_version_specified
dedent|''
name|'def'
name|'test_parse_path_no_version_specified'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c/o1'"
op|')'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'account'
op|','
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'container'
op|','
string|"'c'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'obj'
op|','
string|"'o1'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_path_with_valid_version
dedent|''
name|'def'
name|'test_parse_path_with_valid_version'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v2/a/c/o1'"
op|')'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'version'
op|','
number|'2.0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'account'
op|','
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'container'
op|','
string|"'c'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'obj'
op|','
string|"'o1'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_path_with_invalid_version
dedent|''
name|'def'
name|'test_parse_path_with_invalid_version'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v3/a/c/o1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|','
nl|'\n'
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_path_with_no_account
dedent|''
name|'def'
name|'test_parse_path_with_no_account'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'bad_paths'
op|'='
op|'('
string|"'v1'"
op|','
string|"'v2'"
op|','
string|"''"
op|')'
newline|'\n'
name|'for'
name|'path'
name|'in'
name|'bad_paths'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/%s'"
op|'%'
name|'path'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'list_endpoints'
op|'.'
name|'_parse_path'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Expected ValueError to be raised'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'str'
op|'('
name|'err'
op|')'
op|','
string|"'No account specified'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_endpoint
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_get_endpoint'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Expected results for objects taken from test_ring'
nl|'\n'
comment|'# Expected results for others computed by manually invoking'
nl|'\n'
comment|'# ring.get_nodes().'
nl|'\n'
indent|'        '
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c/o1'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'content_type'
op|','
string|"'application/json'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/1/a/c/o1"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/1/a/c/o1"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# test policies with no version endpoint name'
nl|'\n'
name|'expected'
op|'='
op|'['
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/1/a/c/o1"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/1/a/c/o1"'
op|']'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/1/a/c/o1"'
op|','
nl|'\n'
string|'"http://10.1.2.1:6000/sdc1/1/a/c/o1"'
nl|'\n'
op|']'
op|']'
newline|'\n'
name|'PATCHGI'
op|'='
string|"'swift.common.middleware.list_endpoints.get_container_info'"
newline|'\n'
name|'for'
name|'pol'
name|'in'
name|'POLICIES'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'policy_to_test'
op|'='
name|'pol'
op|'.'
name|'idx'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
name|'PATCHGI'
op|','
name|'self'
op|'.'
name|'FakeGetInfo'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c/o1'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'content_type'
op|','
string|"'application/json'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
name|'expected'
op|'['
name|'pol'
op|'.'
name|'idx'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|"# Here, 'o1/' is the object name."
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c/o1/'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/3/a/c/o1/"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/3/a/c/o1/"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c2'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/2/a/c2"'
op|','
nl|'\n'
string|'"http://10.1.2.1:6000/sdc1/2/a/c2"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a1'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.2.1:6000/sdc1/0/a1"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/0/a1"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/0/a1"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'400'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c 2'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/3/a/c%202"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/3/a/c%202"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c%202'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/3/a/c%202"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/3/a/c%202"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/ac%20count/con%20tainer/ob%20ject'"
op|')'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
op|'['
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/3/ac%20count/con%20tainer/ob%20ject"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/3/ac%20count/con%20tainer/ob%20ject"'
nl|'\n'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a/c/o1'"
op|','
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|'}'
op|')'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
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
number|'405'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'405 Method Not Allowed'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'headers'
op|'['
string|"'allow'"
op|']'
op|','
string|"'GET'"
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/not-endpoints'"
op|')'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'list_endpoints'
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
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
string|"'FakeApp'"
op|')'
newline|'\n'
nl|'\n'
comment|'# test policies with custom endpoint name'
nl|'\n'
name|'for'
name|'pol'
name|'in'
name|'POLICIES'
op|':'
newline|'\n'
comment|'# test custom path with trailing slash'
nl|'\n'
indent|'            '
name|'custom_path_le'
op|'='
name|'list_endpoints'
op|'.'
name|'filter_factory'
op|'('
op|'{'
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'list_endpoints_path'"
op|':'
string|"'/some/another/path/'"
nl|'\n'
op|'}'
op|')'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'policy_to_test'
op|'='
name|'pol'
op|'.'
name|'idx'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
name|'PATCHGI'
op|','
name|'self'
op|'.'
name|'FakeGetInfo'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/some/another/path/a/c/o1'"
op|')'
op|'.'
name|'get_response'
op|'('
name|'custom_path_le'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'content_type'
op|','
string|"'application/json'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
name|'expected'
op|'['
name|'pol'
op|'.'
name|'idx'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# test custom path without trailing slash'
nl|'\n'
name|'custom_path_le'
op|'='
name|'list_endpoints'
op|'.'
name|'filter_factory'
op|'('
op|'{'
nl|'\n'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
nl|'\n'
string|"'list_endpoints_path'"
op|':'
string|"'/some/another/path'"
nl|'\n'
op|'}'
op|')'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'policy_to_test'
op|'='
name|'pol'
op|'.'
name|'idx'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
name|'PATCHGI'
op|','
name|'self'
op|'.'
name|'FakeGetInfo'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/some/another/path/a/c/o1'"
op|')'
op|'.'
name|'get_response'
op|'('
name|'custom_path_le'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'content_type'
op|','
string|"'application/json'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
op|','
name|'expected'
op|'['
name|'pol'
op|'.'
name|'idx'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_v1_response
dedent|''
dedent|''
name|'def'
name|'test_v1_response'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v1/a/c/o1'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
string|'"http://10.1.1.1:6000/sdb1/1/a/c/o1"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/1/a/c/o1"'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_v2_obj_response
dedent|''
name|'def'
name|'test_v2_obj_response'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v2/a/c/o1'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
nl|'\n'
string|"'endpoints'"
op|':'
op|'['
string|'"http://10.1.1.1:6000/sdb1/1/a/c/o1"'
op|','
nl|'\n'
string|'"http://10.1.2.2:6000/sdd1/1/a/c/o1"'
op|']'
op|','
nl|'\n'
string|"'headers'"
op|':'
op|'{'
string|"'X-Backend-Storage-Policy-Index'"
op|':'
string|'"0"'
op|'}'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
name|'for'
name|'policy'
name|'in'
name|'POLICIES'
op|':'
newline|'\n'
indent|'            '
name|'patch_path'
op|'='
string|"'swift.common.middleware.list_endpoints'"
string|"'.get_container_info'"
newline|'\n'
name|'mock_get_container_info'
op|'='
name|'lambda'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|':'
op|'{'
string|"'storage_policy'"
op|':'
name|'int'
op|'('
name|'policy'
op|')'
op|'}'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
name|'patch_path'
op|','
name|'mock_get_container_info'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
dedent|''
name|'part'
op|','
name|'nodes'
op|'='
name|'policy'
op|'.'
name|'object_ring'
op|'.'
name|'get_nodes'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o1'"
op|')'
newline|'\n'
op|'['
name|'node'
op|'.'
name|'update'
op|'('
op|'{'
string|"'part'"
op|':'
name|'part'
op|'}'
op|')'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|']'
newline|'\n'
name|'path'
op|'='
string|"'http://%(ip)s:%(port)s/%(device)s/%(part)s/a/c/o1'"
newline|'\n'
name|'expected'
op|'='
op|'{'
nl|'\n'
string|"'headers'"
op|':'
op|'{'
nl|'\n'
string|"'X-Backend-Storage-Policy-Index'"
op|':'
name|'str'
op|'('
name|'int'
op|'('
name|'policy'
op|')'
op|')'
op|'}'
op|','
nl|'\n'
string|"'endpoints'"
op|':'
op|'['
name|'path'
op|'%'
name|'node'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|']'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_v2_non_obj_response
dedent|''
dedent|''
name|'def'
name|'test_v2_non_obj_response'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# account'
nl|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v2/a'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
nl|'\n'
string|"'endpoints'"
op|':'
op|'['
string|'"http://10.1.2.1:6000/sdc1/0/a"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/0/a"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/0/a"'
op|']'
op|','
nl|'\n'
string|"'headers'"
op|':'
op|'{'
op|'}'
op|','
nl|'\n'
op|'}'
newline|'\n'
comment|'# container'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v2/a/c'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
nl|'\n'
string|"'endpoints'"
op|':'
op|'['
string|'"http://10.1.2.2:6000/sdd1/0/a/c"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/0/a/c"'
op|','
nl|'\n'
string|'"http://10.1.2.1:6000/sdc1/0/a/c"'
op|']'
op|','
nl|'\n'
string|"'headers'"
op|':'
op|'{'
op|'}'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_version_account_response
dedent|''
name|'def'
name|'test_version_account_response'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/a'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
string|'"http://10.1.2.1:6000/sdc1/0/a"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/0/a"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/0/a"'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v1.0/a'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/endpoints/v2/a'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'list_endpoints'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
nl|'\n'
string|"'endpoints'"
op|':'
op|'['
string|'"http://10.1.2.1:6000/sdc1/0/a"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sda1/0/a"'
op|','
nl|'\n'
string|'"http://10.1.1.1:6000/sdb1/0/a"'
op|']'
op|','
nl|'\n'
string|"'headers'"
op|':'
op|'{'
op|'}'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'expected'
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
