begin_unit
comment|'# Copyright (c) 2012 OpenStack, LLC.'
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
name|'unittest'
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
name|'json'
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
DECL|class|TestListEndpoints
dedent|''
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
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'__file__'
op|')'
op|','
string|"'ring'"
op|')'
newline|'\n'
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
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'testdir'
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
DECL|member|test_get_endpoint
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
comment|"# Here, 'o1/' is the object name."
nl|'\n'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
string|"'FakeApp'"
op|')'
newline|'\n'
nl|'\n'
comment|'# test custom path with trailing slash'
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
name|'self'
op|'.'
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
comment|'# test ustom path without trailing slash'
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
name|'self'
op|'.'
name|'assertEquals'
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
name|'assertEquals'
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
name|'assertEquals'
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
