begin_unit
comment|'#!/usr/bin/python'
nl|'\n'
nl|'\n'
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
name|'json'
newline|'\n'
name|'from'
name|'nose'
name|'import'
name|'SkipTest'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'MAX_META_COUNT'
op|','
name|'MAX_META_NAME_LENGTH'
op|','
name|'MAX_META_OVERALL_SIZE'
op|','
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
op|'.'
name|'acl'
name|'import'
name|'format_acl'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'functional'
op|'.'
name|'swift_test_client'
name|'import'
name|'Connection'
newline|'\n'
name|'from'
name|'test'
name|'import'
name|'get_config'
newline|'\n'
name|'from'
name|'swift_testing'
name|'import'
name|'check_response'
op|','
name|'retry'
op|','
name|'skip'
op|','
name|'web_front_end'
newline|'\n'
name|'import'
name|'swift_testing'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccount
name|'class'
name|'TestAccount'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_metadata
indent|'    '
name|'def'
name|'test_metadata'
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
nl|'\n'
DECL|function|post
dedent|''
name|'def'
name|'post'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'value'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'POST'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
nl|'\n'
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|','
string|"'X-Account-Meta-Test'"
op|':'
name|'value'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|head
dedent|''
name|'def'
name|'head'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'HEAD'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|get
dedent|''
name|'def'
name|'get'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'GET'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
string|"''"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-test'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'get'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-test'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
string|"'Value'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-test'"
op|')'
op|','
string|"'Value'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'get'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-test'"
op|')'
op|','
string|"'Value'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_tempauth_account_acls
dedent|''
name|'def'
name|'test_tempauth_account_acls'
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
nl|'\n'
comment|'# Determine whether this cluster has account ACLs; if not, skip test'
nl|'\n'
dedent|''
name|'conn'
op|'='
name|'Connection'
op|'('
name|'get_config'
op|'('
string|"'func_test'"
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'authenticate'
op|'('
op|')'
newline|'\n'
name|'status'
op|'='
name|'conn'
op|'.'
name|'make_request'
op|'('
nl|'\n'
string|"'GET'"
op|','
string|"'/info'"
op|','
name|'cfg'
op|'='
op|'{'
string|"'verbatim_path'"
op|':'
name|'True'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'status'
op|'//'
number|'100'
op|'!='
number|'2'
op|':'
newline|'\n'
comment|"# Can't tell if account ACLs are enabled; skip tests proactively."
nl|'\n'
indent|'            '
name|'raise'
name|'SkipTest'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'cluster_info'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'conn'
op|'.'
name|'response'
op|'.'
name|'read'
op|'('
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'cluster_info'
op|'.'
name|'get'
op|'('
string|"'tempauth'"
op|','
op|'{'
op|'}'
op|')'
op|'.'
name|'get'
op|'('
string|"'account_acls'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'SkipTest'
newline|'\n'
dedent|''
name|'if'
string|"'keystoneauth'"
name|'in'
name|'cluster_info'
op|':'
newline|'\n'
comment|'# Unfortunate hack -- tempauth (with account ACLs) is expected'
nl|'\n'
comment|'# to play nice with Keystone (without account ACLs), but Zuul'
nl|'\n'
comment|"# functest framework doesn't give us an easy way to get a"
nl|'\n'
comment|'# tempauth user.'
nl|'\n'
indent|'                '
name|'raise'
name|'SkipTest'
newline|'\n'
nl|'\n'
DECL|function|post
dedent|''
dedent|''
name|'def'
name|'post'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'new_headers'
op|'='
name|'dict'
op|'('
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|','
op|'**'
name|'headers'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'POST'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
name|'new_headers'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|put
dedent|''
name|'def'
name|'put'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'new_headers'
op|'='
name|'dict'
op|'('
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|','
op|'**'
name|'headers'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'PUT'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
name|'new_headers'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|delete
dedent|''
name|'def'
name|'delete'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'new_headers'
op|'='
name|'dict'
op|'('
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|','
op|'**'
name|'headers'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'DELETE'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
name|'new_headers'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|head
dedent|''
name|'def'
name|'head'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'HEAD'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|get
dedent|''
name|'def'
name|'get'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'GET'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
comment|'# User1 can POST to their own account (and reset the ACLs)'
nl|'\n'
indent|'            '
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|'='
op|'{'
string|"'X-Account-Access-Control'"
op|':'
string|"'{}'"
op|'}'
op|','
nl|'\n'
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'X-Account-Access-Control'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
comment|'# User1 can GET their own empty account'
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'get'
op|','
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|'//'
number|'100'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'X-Account-Access-Control'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
comment|"# User2 can't GET User1's account"
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'get'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'403'
op|')'
newline|'\n'
nl|'\n'
comment|'# User1 is swift_owner of their own account, so they can POST an'
nl|'\n'
comment|"# ACL -- let's do this and make User2 (test_user[1]) an admin"
nl|'\n'
name|'acl_user'
op|'='
name|'swift_testing'
op|'.'
name|'swift_test_user'
op|'['
number|'1'
op|']'
newline|'\n'
name|'acl'
op|'='
op|'{'
string|"'admin'"
op|':'
op|'['
name|'acl_user'
op|']'
op|'}'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-account-access-control'"
op|':'
name|'format_acl'
op|'('
nl|'\n'
name|'version'
op|'='
number|'2'
op|','
name|'acl_dict'
op|'='
name|'acl'
op|')'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|'='
name|'headers'
op|','
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
nl|'\n'
comment|'# User1 can see the new header'
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'get'
op|','
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|'//'
number|'100'
op|','
number|'2'
op|')'
newline|'\n'
name|'data_from_headers'
op|'='
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-access-control'"
op|')'
newline|'\n'
name|'expected'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'acl'
op|','
name|'separators'
op|'='
op|'('
string|"','"
op|','
string|"':'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'data_from_headers'
op|','
name|'expected'
op|')'
newline|'\n'
nl|'\n'
comment|'# Now User2 should be able to GET the account and see the ACL'
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'data_from_headers'
op|'='
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-access-control'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'data_from_headers'
op|','
name|'expected'
op|')'
newline|'\n'
nl|'\n'
comment|"# Revoke User2's admin access, grant User2 read-write access"
nl|'\n'
name|'acl'
op|'='
op|'{'
string|"'read-write'"
op|':'
op|'['
name|'acl_user'
op|']'
op|'}'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-account-access-control'"
op|':'
name|'format_acl'
op|'('
nl|'\n'
name|'version'
op|'='
number|'2'
op|','
name|'acl_dict'
op|'='
name|'acl'
op|')'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|'='
name|'headers'
op|','
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
nl|'\n'
comment|'# User2 can still GET the account, but not see the ACL'
nl|'\n'
comment|"# (since it's privileged data)"
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-access-control'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
comment|'# User2 can PUT and DELETE a container'
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'put'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|','
nl|'\n'
name|'resource'
op|'='
string|"'%(storage_url)s/mycontainer'"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'201'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'delete'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|','
nl|'\n'
name|'resource'
op|'='
string|"'%(storage_url)s/mycontainer'"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
nl|'\n'
comment|"# Revoke User2's read-write access, grant User2 read-only access"
nl|'\n'
name|'acl'
op|'='
op|'{'
string|"'read-only'"
op|':'
op|'['
name|'acl_user'
op|']'
op|'}'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-account-access-control'"
op|':'
name|'format_acl'
op|'('
nl|'\n'
name|'version'
op|'='
number|'2'
op|','
name|'acl_dict'
op|'='
name|'acl'
op|')'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|'='
name|'headers'
op|','
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
nl|'\n'
comment|'# User2 can still GET the account, but not see the ACL'
nl|'\n'
comment|"# (since it's privileged data)"
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-access-control'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
comment|"# User2 can't PUT a container"
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'put'
op|','
name|'use_account'
op|'='
number|'2'
op|','
name|'url_account'
op|'='
number|'1'
op|','
nl|'\n'
name|'resource'
op|'='
string|"'%(storage_url)s/mycontainer'"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'403'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
comment|'# Make sure to clean up even if tests fail -- User2 should not'
nl|'\n'
comment|"# have access to User1's account in other functional tests!"
nl|'\n'
indent|'            '
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|'='
op|'{'
string|"'X-Account-Access-Control'"
op|':'
string|"'{}'"
op|'}'
op|','
nl|'\n'
name|'use_account'
op|'='
number|'1'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_unicode_metadata
dedent|''
dedent|''
name|'def'
name|'test_unicode_metadata'
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
nl|'\n'
DECL|function|post
dedent|''
name|'def'
name|'post'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'name'
op|','
name|'value'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'POST'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
nl|'\n'
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|','
name|'name'
op|':'
name|'value'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|head
dedent|''
name|'def'
name|'head'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'HEAD'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'uni_key'
op|'='
string|"u'X-Account-Meta-uni\\u0E12'"
newline|'\n'
name|'uni_value'
op|'='
string|"u'uni\\u0E12'"
newline|'\n'
name|'if'
op|'('
name|'web_front_end'
op|'=='
string|"'integral'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'uni_key'
op|','
string|"'1'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'201'
op|','
number|'204'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
name|'uni_key'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
op|')'
op|','
string|"'1'"
op|')'
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
string|"'X-Account-Meta-uni'"
op|','
name|'uni_value'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'X-Account-Meta-uni'"
op|')'
op|','
nl|'\n'
name|'uni_value'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
op|')'
newline|'\n'
name|'if'
op|'('
name|'web_front_end'
op|'=='
string|"'integral'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'uni_key'
op|','
name|'uni_value'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
name|'uni_key'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
op|')'
op|','
nl|'\n'
name|'uni_value'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_multi_metadata
dedent|''
dedent|''
name|'def'
name|'test_multi_metadata'
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
nl|'\n'
DECL|function|post
dedent|''
name|'def'
name|'post'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'name'
op|','
name|'value'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'POST'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
nl|'\n'
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|','
name|'name'
op|':'
name|'value'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|function|head
dedent|''
name|'def'
name|'head'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'request'
op|'('
string|"'HEAD'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
string|"'X-Account-Meta-One'"
op|','
string|"'1'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-one'"
op|')'
op|','
string|"'1'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
string|"'X-Account-Meta-Two'"
op|','
string|"'2'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'head'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'status'
name|'in'
op|'('
number|'200'
op|','
number|'204'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-one'"
op|')'
op|','
string|"'1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-account-meta-two'"
op|')'
op|','
string|"'2'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_bad_metadata
dedent|''
name|'def'
name|'test_bad_metadata'
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
nl|'\n'
DECL|function|post
dedent|''
name|'def'
name|'post'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
op|','
name|'extra_headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
op|'{'
string|"'X-Auth-Token'"
op|':'
name|'token'
op|'}'
newline|'\n'
name|'headers'
op|'.'
name|'update'
op|'('
name|'extra_headers'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'POST'"
op|','
name|'parsed'
op|'.'
name|'path'
op|','
string|"''"
op|','
name|'headers'
op|')'
newline|'\n'
name|'return'
name|'check_response'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
nl|'\n'
op|'{'
string|"'X-Account-Meta-'"
op|'+'
op|'('
string|"'k'"
op|'*'
name|'MAX_META_NAME_LENGTH'
op|')'
op|':'
string|"'v'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
nl|'\n'
name|'post'
op|','
nl|'\n'
op|'{'
string|"'X-Account-Meta-'"
op|'+'
op|'('
string|"'k'"
op|'*'
op|'('
name|'MAX_META_NAME_LENGTH'
op|'+'
number|'1'
op|')'
op|')'
op|':'
string|"'v'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'400'
op|')'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
nl|'\n'
op|'{'
string|"'X-Account-Meta-Too-Long'"
op|':'
string|"'k'"
op|'*'
name|'MAX_META_VALUE_LENGTH'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
nl|'\n'
name|'post'
op|','
nl|'\n'
op|'{'
string|"'X-Account-Meta-Too-Long'"
op|':'
string|"'k'"
op|'*'
op|'('
name|'MAX_META_VALUE_LENGTH'
op|'+'
number|'1'
op|')'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'400'
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'x'
name|'in'
name|'xrange'
op|'('
name|'MAX_META_COUNT'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'['
string|"'X-Account-Meta-%d'"
op|'%'
name|'x'
op|']'
op|'='
string|"'v'"
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'x'
name|'in'
name|'xrange'
op|'('
name|'MAX_META_COUNT'
op|'+'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'['
string|"'X-Account-Meta-%d'"
op|'%'
name|'x'
op|']'
op|'='
string|"'v'"
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'400'
op|')'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'header_value'
op|'='
string|"'k'"
op|'*'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'size'
op|'='
number|'0'
newline|'\n'
name|'x'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'size'
op|'<'
name|'MAX_META_OVERALL_SIZE'
op|'-'
number|'4'
op|'-'
name|'MAX_META_VALUE_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'size'
op|'+='
number|'4'
op|'+'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'headers'
op|'['
string|"'X-Account-Meta-%04d'"
op|'%'
name|'x'
op|']'
op|'='
name|'header_value'
newline|'\n'
name|'x'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'if'
name|'MAX_META_OVERALL_SIZE'
op|'-'
name|'size'
op|'>'
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'['
string|"'X-Account-Meta-k'"
op|']'
op|'='
string|"'v'"
op|'*'
op|'('
name|'MAX_META_OVERALL_SIZE'
op|'-'
name|'size'
op|'-'
number|'1'
op|')'
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'204'
op|')'
newline|'\n'
name|'headers'
op|'['
string|"'X-Account-Meta-k'"
op|']'
op|'='
string|"'v'"
op|'*'
op|'('
name|'MAX_META_OVERALL_SIZE'
op|'-'
name|'size'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'retry'
op|'('
name|'post'
op|','
name|'headers'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
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
number|'400'
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
