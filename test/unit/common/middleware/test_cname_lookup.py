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
name|'unittest'
newline|'\n'
name|'import'
name|'mock'
newline|'\n'
name|'from'
name|'nose'
name|'import'
name|'SkipTest'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
comment|'# this test requires the dnspython package to be installed'
nl|'\n'
indent|'    '
name|'import'
name|'dns'
op|'.'
name|'resolver'
comment|'# noqa'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
DECL|variable|skip
indent|'    '
name|'skip'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
comment|'# executed if the try has no errors'
newline|'\n'
DECL|variable|skip
indent|'    '
name|'skip'
op|'='
name|'False'
newline|'\n'
dedent|''
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'cname_lookup'
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
nl|'\n'
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
string|'"FAKE APP"'
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
DECL|variable|original_lookup
dedent|''
name|'original_lookup'
op|'='
name|'cname_lookup'
op|'.'
name|'lookup_cname'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestCNAMELookup
name|'class'
name|'TestCNAMELookup'
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
name|'if'
name|'skip'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'SkipTest'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'CNAMELookupMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'lookup_depth'"
op|':'
number|'2'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pass_ip_addresses
dedent|''
name|'def'
name|'test_pass_ip_addresses'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'original_lookup'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'10.134.23.198'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'fc00:7ea1:f155::6321:8841'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_passthrough
dedent|''
name|'def'
name|'test_passthrough'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
indent|'        '
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
name|'d'
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'foo.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'foo.example.com:8080'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'SERVER_NAME'"
op|':'
string|"'foo.example.com'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
name|'None'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_good_lookup
dedent|''
name|'def'
name|'test_good_lookup'
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
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
string|"'%s.example.com'"
op|'%'
name|'d'
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com:8080'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'SERVER_NAME'"
op|':'
string|"'mysite.com'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
name|'None'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_lookup_chain_too_long
dedent|''
name|'def'
name|'test_lookup_chain_too_long'
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
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'d'
op|'=='
string|"'mysite.com'"
op|':'
newline|'\n'
indent|'                '
name|'site'
op|'='
string|"'level1.foo.com'"
newline|'\n'
dedent|''
name|'elif'
name|'d'
op|'=='
string|"'level1.foo.com'"
op|':'
newline|'\n'
indent|'                '
name|'site'
op|'='
string|"'level2.foo.com'"
newline|'\n'
dedent|''
name|'elif'
name|'d'
op|'=='
string|"'level2.foo.com'"
op|':'
newline|'\n'
indent|'                '
name|'site'
op|'='
string|"'bar.example.com'"
newline|'\n'
dedent|''
name|'return'
number|'0'
op|','
name|'site'
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
op|'['
string|"'CNAME lookup failed after 2 tries'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_lookup_chain_bad_target
dedent|''
name|'def'
name|'test_lookup_chain_bad_target'
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
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
string|"'some.invalid.site.com'"
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
nl|'\n'
op|'['
string|"'CNAME lookup failed to resolve to a valid domain'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_something_weird
dedent|''
name|'def'
name|'test_something_weird'
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
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
name|'None'
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
nl|'\n'
op|'['
string|"'CNAME lookup failed to resolve to a valid domain'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_with_memcache
dedent|''
name|'def'
name|'test_with_memcache'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|function|my_lookup
indent|'        '
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
string|"'%s.example.com'"
op|'%'
name|'d'
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
DECL|class|memcache_stub
name|'class'
name|'memcache_stub'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'cache'
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
indent|'                '
name|'return'
name|'self'
op|'.'
name|'cache'
op|'.'
name|'get'
op|'('
name|'key'
op|','
name|'None'
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
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'cache'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
dedent|''
name|'memcache'
op|'='
name|'memcache_stub'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'memcache'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'memcache'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'mysite.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_cname_matching_ending_not_domain
dedent|''
name|'def'
name|'test_cname_matching_ending_not_domain'
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
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'foo.com'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
string|"'c.aexample.com'"
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
nl|'\n'
op|'['
string|"'CNAME lookup failed to resolve to a valid domain'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_cname_configured_with_empty_storage_domain
dedent|''
name|'def'
name|'test_cname_configured_with_empty_storage_domain'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'CNAMELookupMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'storage_domain'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'lookup_depth'"
op|':'
number|'2'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.a.example.com'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|my_lookup
name|'def'
name|'my_lookup'
op|'('
name|'d'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
number|'0'
op|','
name|'None'
newline|'\n'
dedent|''
name|'cname_lookup'
op|'.'
name|'lookup_cname'
op|'='
name|'my_lookup'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_storage_domains_conf_format
dedent|''
name|'def'
name|'test_storage_domains_conf_format'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
op|'{'
string|"'storage_domain'"
op|':'
string|"'foo.com'"
op|'}'
newline|'\n'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'filter_factory'
op|'('
name|'conf'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'app'
op|'.'
name|'storage_domain'
op|','
op|'['
string|"'.foo.com'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'conf'
op|'='
op|'{'
string|"'storage_domain'"
op|':'
string|"'foo.com, '"
op|'}'
newline|'\n'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'filter_factory'
op|'('
name|'conf'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'app'
op|'.'
name|'storage_domain'
op|','
op|'['
string|"'.foo.com'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'conf'
op|'='
op|'{'
string|"'storage_domain'"
op|':'
string|"'foo.com, bar.com'"
op|'}'
newline|'\n'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'filter_factory'
op|'('
name|'conf'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'app'
op|'.'
name|'storage_domain'
op|','
op|'['
string|"'.foo.com'"
op|','
string|"'.bar.com'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'conf'
op|'='
op|'{'
string|"'storage_domain'"
op|':'
string|"'foo.com, .bar.com'"
op|'}'
newline|'\n'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'filter_factory'
op|'('
name|'conf'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'app'
op|'.'
name|'storage_domain'
op|','
op|'['
string|"'.foo.com'"
op|','
string|"'.bar.com'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'conf'
op|'='
op|'{'
string|"'storage_domain'"
op|':'
string|"'.foo.com, .bar.com'"
op|'}'
newline|'\n'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'filter_factory'
op|'('
name|'conf'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'app'
op|'.'
name|'storage_domain'
op|','
op|'['
string|"'.foo.com'"
op|','
string|"'.bar.com'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_multiple_storage_domains
dedent|''
name|'def'
name|'test_multiple_storage_domains'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
op|'{'
string|"'storage_domain'"
op|':'
string|"'storage1.com, storage2.com'"
op|','
nl|'\n'
string|"'lookup_depth'"
op|':'
number|'2'
op|'}'
newline|'\n'
name|'app'
op|'='
name|'cname_lookup'
op|'.'
name|'CNAMELookupMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
name|'conf'
op|')'
newline|'\n'
nl|'\n'
DECL|function|do_test
name|'def'
name|'do_test'
op|'('
name|'lookup_back'
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
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'module'
op|'='
string|"'swift.common.middleware.cname_lookup.lookup_cname'"
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
name|'module'
op|','
name|'lambda'
name|'x'
op|':'
op|'('
number|'0'
op|','
name|'lookup_back'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'do_test'
op|'('
string|"'c.storage1.com'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'do_test'
op|'('
string|"'c.storage2.com'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
string|"'FAKE APP'"
op|')'
newline|'\n'
nl|'\n'
name|'bad_domain'
op|'='
op|'['
string|"'CNAME lookup failed to resolve to a valid domain'"
op|']'
newline|'\n'
name|'resp'
op|'='
name|'do_test'
op|'('
string|"'c.badtest.com'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|','
name|'bad_domain'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
