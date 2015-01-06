begin_unit
comment|'# Copyright 2012 OpenStack Foundation'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Licensed under the Apache License, Version 2.0 (the "License"); you may'
nl|'\n'
comment|'# not use this file except in compliance with the License. You may obtain'
nl|'\n'
comment|'# a copy of the License at'
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
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
name|'as'
name|'swift_utils'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'is_success'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'acl'
name|'as'
name|'swift_acl'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'get_sys_meta_prefix'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPNotFound'
op|','
name|'HTTPForbidden'
op|','
name|'HTTPUnauthorized'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'register_swift_info'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
name|'import'
name|'get_account_info'
newline|'\n'
name|'import'
name|'functools'
newline|'\n'
nl|'\n'
DECL|variable|PROJECT_DOMAIN_ID_HEADER
name|'PROJECT_DOMAIN_ID_HEADER'
op|'='
string|"'x-account-project-domain-id'"
newline|'\n'
name|'PROJECT_DOMAIN_ID_SYSMETA_HEADER'
op|'='
DECL|variable|PROJECT_DOMAIN_ID_SYSMETA_HEADER
name|'get_sys_meta_prefix'
op|'('
string|"'account'"
op|')'
op|'+'
string|"'project-domain-id'"
newline|'\n'
comment|'# a string that is unique w.r.t valid ids'
nl|'\n'
DECL|variable|UNKNOWN_ID
name|'UNKNOWN_ID'
op|'='
string|"'_unknown'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|KeystoneAuth
name|'class'
name|'KeystoneAuth'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Swift middleware to Keystone authorization system.\n\n    In Swift\'s proxy-server.conf add this middleware to your pipeline::\n\n        [pipeline:main]\n        pipeline = catch_errors cache authtoken keystoneauth proxy-server\n\n    Make sure you have the authtoken middleware before the\n    keystoneauth middleware.\n\n    The authtoken middleware will take care of validating the user and\n    keystoneauth will authorize access.\n\n    The authtoken middleware is shipped with keystonemiddleware - it\n    does not have any other dependencies than itself so you can either\n    install it by copying the file directly in your python path or by\n    installing keystonemiddleware.\n\n    If support is required for unvalidated users (as with anonymous\n    access) or for formpost/staticweb/tempurl middleware, authtoken will\n    need to be configured with ``delay_auth_decision`` set to true.  See\n    the Keystone documentation for more detail on how to configure the\n    authtoken middleware.\n\n    In proxy-server.conf you will need to have the setting account\n    auto creation to true::\n\n        [app:proxy-server]\n        account_autocreate = true\n\n    And add a swift authorization filter section, such as::\n\n        [filter:keystoneauth]\n        use = egg:swift#keystoneauth\n        operator_roles = admin, swiftoperator\n\n    This maps tenants to account in Swift.\n\n    The user whose able to give ACL / create Containers permissions\n    will be the one that are inside the ``operator_roles``\n    setting which by default includes the admin and the swiftoperator\n    roles.\n\n    If the ``is_admin`` option is ``true``, a user whose username is the same\n    as the project name and who has any role on the project will have access\n    rights elevated to be the same as if the user had one of the\n    ``operator_roles``. Note that the condition compares names rather than\n    UUIDs. This option is deprecated. It is ``false`` by default.\n\n    If you need to have a different reseller_prefix to be able to\n    mix different auth servers you can configure the option\n    ``reseller_prefix`` in your keystoneauth entry like this::\n\n        reseller_prefix = NEWAUTH\n\n    The keystoneauth middleware supports cross-tenant access control using\n    the syntax ``<tenant>:<user>`` to specify a grantee in container Access\n    Control Lists (ACLs). For a request to be granted by an ACL, the grantee\n    ``<tenant>`` must match the UUID of the tenant to which the request\n    token is scoped and the grantee ``<user>`` must match the UUID of the\n    user authenticated by the request token.\n\n    Note that names must no longer be used in cross-tenant ACLs because with\n    the introduction of domains in keystone names are no longer globally\n    unique.\n\n    For backwards compatibility, ACLs using names will be granted by\n    keystoneauth when it can be established that the grantee tenant,\n    the grantee user and the tenant being accessed are either not yet in a\n    domain (e.g. the request token has been obtained via the keystone v2\n    API) or are all in the default domain to which legacy accounts would\n    have been migrated. The default domain is identified by its UUID,\n    which by default has the value ``default``. This can be changed by\n    setting the ``default_domain_id`` option in the keystoneauth\n    configuration::\n\n        default_domain_id = default\n\n    The backwards compatible behavior can be disabled by setting the config\n    option ``allow_names_in_acls`` to false::\n\n        allow_names_in_acls = false\n\n    To enable this backwards compatibility, keystoneauth will attempt to\n    determine the domain id of a tenant when any new account is created,\n    and persist this as account metadata. If an account is created for a tenant\n    using a token with reselleradmin role that is not scoped on that tenant,\n    keystoneauth is unable to determine the domain id of the tenant;\n    keystoneauth will assume that the tenant may not be in the default domain\n    and therefore not match names in ACLs for that account.\n\n    By default, middleware higher in the WSGI pipeline may override auth\n    processing, useful for middleware such as tempurl and formpost. If you know\n    you\'re not going to use such middleware and you want a bit of extra\n    security you can disable this behaviour by setting the ``allow_overrides``\n    option to ``false``::\n\n        allow_overrides = false\n\n    :param app: The next WSGI app in the pipeline\n    :param conf: The dict of configuration values\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
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
name|'swift_utils'
op|'.'
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'keystoneauth'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reseller_prefix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'reseller_prefix'"
op|','
string|"'AUTH_'"
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'reseller_prefix'
name|'and'
name|'self'
op|'.'
name|'reseller_prefix'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'_'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'reseller_prefix'
op|'+='
string|"'_'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'operator_roles'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'operator_roles'"
op|','
nl|'\n'
string|"'admin, swiftoperator'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reseller_admin_role'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'reseller_admin_role'"
op|','
nl|'\n'
string|"'ResellerAdmin'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'config_is_admin'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'is_admin'"
op|','
string|'"false"'
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'is_admin'
op|'='
name|'swift_utils'
op|'.'
name|'config_true_value'
op|'('
name|'config_is_admin'
op|')'
newline|'\n'
name|'config_overrides'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_overrides'"
op|','
string|"'t'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'allow_overrides'
op|'='
name|'swift_utils'
op|'.'
name|'config_true_value'
op|'('
name|'config_overrides'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'default_domain_id'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'default_domain_id'"
op|','
string|"'default'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'allow_names_in_acls'
op|'='
name|'swift_utils'
op|'.'
name|'config_true_value'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_names_in_acls'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'environ'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'identity'
op|'='
name|'self'
op|'.'
name|'_keystone_identity'
op|'('
name|'environ'
op|')'
newline|'\n'
nl|'\n'
comment|'# Check if one of the middleware like tempurl or formpost have'
nl|'\n'
comment|'# set the swift.authorize_override environ and want to control the'
nl|'\n'
comment|'# authentication'
nl|'\n'
name|'if'
op|'('
name|'self'
op|'.'
name|'allow_overrides'
name|'and'
nl|'\n'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.authorize_override'"
op|','
name|'False'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"'Authorizing from an overriding middleware (i.e: tempurl)'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'msg'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'identity'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Using identity: %r'"
op|','
name|'identity'
op|')'
newline|'\n'
name|'environ'
op|'['
string|"'keystone.identity'"
op|']'
op|'='
name|'identity'
newline|'\n'
name|'environ'
op|'['
string|"'REMOTE_USER'"
op|']'
op|'='
name|'identity'
op|'.'
name|'get'
op|'('
string|"'tenant'"
op|')'
newline|'\n'
name|'env_identity'
op|'='
name|'self'
op|'.'
name|'_integral_keystone_identity'
op|'('
name|'environ'
op|')'
newline|'\n'
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'functools'
op|'.'
name|'partial'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'authorize'
op|','
name|'env_identity'
op|')'
newline|'\n'
name|'user_roles'
op|'='
op|'('
name|'r'
op|'.'
name|'lower'
op|'('
op|')'
name|'for'
name|'r'
name|'in'
name|'identity'
op|'.'
name|'get'
op|'('
string|"'roles'"
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'reseller_admin_role'
name|'in'
name|'user_roles'
op|':'
newline|'\n'
indent|'                '
name|'environ'
op|'['
string|"'reseller_request'"
op|']'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Authorizing as anonymous'"
op|')'
newline|'\n'
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'self'
op|'.'
name|'authorize_anonymous'
newline|'\n'
nl|'\n'
dedent|''
name|'environ'
op|'['
string|"'swift.clean_acl'"
op|']'
op|'='
name|'swift_acl'
op|'.'
name|'clean_acl'
newline|'\n'
nl|'\n'
DECL|function|keystone_start_response
name|'def'
name|'keystone_start_response'
op|'('
name|'status'
op|','
name|'response_headers'
op|','
name|'exc_info'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'project_domain_id'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'key'
op|','
name|'val'
name|'in'
name|'response_headers'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
name|'PROJECT_DOMAIN_ID_SYSMETA_HEADER'
op|':'
newline|'\n'
indent|'                    '
name|'project_domain_id'
op|'='
name|'val'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'project_domain_id'
op|':'
newline|'\n'
indent|'                '
name|'response_headers'
op|'.'
name|'append'
op|'('
op|'('
name|'PROJECT_DOMAIN_ID_HEADER'
op|','
nl|'\n'
name|'project_domain_id'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'start_response'
op|'('
name|'status'
op|','
name|'response_headers'
op|','
name|'exc_info'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'environ'
op|','
name|'keystone_start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_keystone_identity
dedent|''
name|'def'
name|'_keystone_identity'
op|'('
name|'self'
op|','
name|'environ'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Extract the identity from the Keystone auth component."""'
newline|'\n'
comment|"# In next release, we would add user id in env['keystone.identity'] by"
nl|'\n'
comment|'# using _integral_keystone_identity to replace current'
nl|'\n'
comment|'# _keystone_identity. The purpose of keeping it in this release it for'
nl|'\n'
comment|'# back compatibility.'
nl|'\n'
name|'if'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_IDENTITY_STATUS'"
op|')'
op|'!='
string|"'Confirmed'"
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'roles'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
string|"'HTTP_X_ROLES'"
name|'in'
name|'environ'
op|':'
newline|'\n'
indent|'            '
name|'roles'
op|'='
name|'environ'
op|'['
string|"'HTTP_X_ROLES'"
op|']'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
newline|'\n'
dedent|''
name|'identity'
op|'='
op|'{'
string|"'user'"
op|':'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_USER_NAME'"
op|')'
op|','
nl|'\n'
string|"'tenant'"
op|':'
op|'('
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_TENANT_ID'"
op|')'
op|','
nl|'\n'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_TENANT_NAME'"
op|')'
op|')'
op|','
nl|'\n'
string|"'roles'"
op|':'
name|'roles'
op|'}'
newline|'\n'
name|'return'
name|'identity'
newline|'\n'
nl|'\n'
DECL|member|_integral_keystone_identity
dedent|''
name|'def'
name|'_integral_keystone_identity'
op|'('
name|'self'
op|','
name|'environ'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Extract the identity from the Keystone auth component."""'
newline|'\n'
name|'if'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_IDENTITY_STATUS'"
op|')'
op|'!='
string|"'Confirmed'"
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'roles'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
string|"'HTTP_X_ROLES'"
name|'in'
name|'environ'
op|':'
newline|'\n'
indent|'            '
name|'roles'
op|'='
name|'environ'
op|'['
string|"'HTTP_X_ROLES'"
op|']'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
newline|'\n'
dedent|''
name|'identity'
op|'='
op|'{'
string|"'user'"
op|':'
op|'('
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_USER_ID'"
op|')'
op|','
nl|'\n'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_USER_NAME'"
op|')'
op|')'
op|','
nl|'\n'
string|"'tenant'"
op|':'
op|'('
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_TENANT_ID'"
op|')'
op|','
nl|'\n'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_TENANT_NAME'"
op|')'
op|')'
op|','
nl|'\n'
string|"'roles'"
op|':'
name|'roles'
op|'}'
newline|'\n'
name|'token_info'
op|'='
name|'environ'
op|'.'
name|'get'
op|'('
string|"'keystone.token_info'"
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'auth_version'
op|'='
number|'0'
newline|'\n'
name|'user_domain'
op|'='
name|'project_domain'
op|'='
op|'('
name|'None'
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
string|"'access'"
name|'in'
name|'token_info'
op|':'
newline|'\n'
comment|'# ignore any domain id headers that authtoken may have set'
nl|'\n'
indent|'            '
name|'auth_version'
op|'='
number|'2'
newline|'\n'
dedent|''
name|'elif'
string|"'token'"
name|'in'
name|'token_info'
op|':'
newline|'\n'
indent|'            '
name|'auth_version'
op|'='
number|'3'
newline|'\n'
name|'user_domain'
op|'='
op|'('
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_USER_DOMAIN_ID'"
op|')'
op|','
nl|'\n'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_USER_DOMAIN_NAME'"
op|')'
op|')'
newline|'\n'
name|'project_domain'
op|'='
op|'('
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_PROJECT_DOMAIN_ID'"
op|')'
op|','
nl|'\n'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'HTTP_X_PROJECT_DOMAIN_NAME'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'identity'
op|'['
string|"'user_domain'"
op|']'
op|'='
name|'user_domain'
newline|'\n'
name|'identity'
op|'['
string|"'project_domain'"
op|']'
op|'='
name|'project_domain'
newline|'\n'
name|'identity'
op|'['
string|"'auth_version'"
op|']'
op|'='
name|'auth_version'
newline|'\n'
name|'return'
name|'identity'
newline|'\n'
nl|'\n'
DECL|member|_get_account_for_tenant
dedent|''
name|'def'
name|'_get_account_for_tenant'
op|'('
name|'self'
op|','
name|'tenant_id'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
string|"'%s%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'reseller_prefix'
op|','
name|'tenant_id'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_reseller_check
dedent|''
name|'def'
name|'_reseller_check'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'tenant_id'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Check reseller prefix."""'
newline|'\n'
name|'return'
name|'account'
op|'=='
name|'self'
op|'.'
name|'_get_account_for_tenant'
op|'('
name|'tenant_id'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_project_domain_id
dedent|''
name|'def'
name|'_get_project_domain_id'
op|'('
name|'self'
op|','
name|'environ'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'info'
op|'='
name|'get_account_info'
op|'('
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|','
string|"'KS'"
op|')'
newline|'\n'
name|'domain_id'
op|'='
name|'info'
op|'.'
name|'get'
op|'('
string|"'sysmeta'"
op|','
op|'{'
op|'}'
op|')'
op|'.'
name|'get'
op|'('
string|"'project-domain-id'"
op|')'
newline|'\n'
name|'exists'
op|'='
name|'is_success'
op|'('
name|'info'
op|'.'
name|'get'
op|'('
string|"'status'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'return'
name|'exists'
op|','
name|'domain_id'
newline|'\n'
nl|'\n'
DECL|member|_set_project_domain_id
dedent|''
name|'def'
name|'_set_project_domain_id'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'path_parts'
op|','
name|'env_identity'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Try to determine the project domain id and save it as\n        account metadata. Do this for a PUT or POST to the\n        account, and also for a container PUT in case that\n        causes the account to be auto-created.\n        '''"
newline|'\n'
name|'if'
name|'PROJECT_DOMAIN_ID_SYSMETA_HEADER'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'path_parts'
newline|'\n'
name|'method'
op|'='
name|'req'
op|'.'
name|'method'
newline|'\n'
name|'if'
op|'('
name|'obj'
name|'or'
op|'('
name|'container'
name|'and'
name|'method'
op|'!='
string|"'PUT'"
op|')'
nl|'\n'
name|'or'
name|'method'
name|'not'
name|'in'
op|'['
string|"'PUT'"
op|','
string|"'POST'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'tenant_id'
op|','
name|'tenant_name'
op|'='
name|'env_identity'
op|'['
string|"'tenant'"
op|']'
newline|'\n'
name|'exists'
op|','
name|'sysmeta_id'
op|'='
name|'self'
op|'.'
name|'_get_project_domain_id'
op|'('
name|'req'
op|'.'
name|'environ'
op|')'
newline|'\n'
name|'req_has_id'
op|','
name|'req_id'
op|','
name|'new_id'
op|'='
name|'False'
op|','
name|'None'
op|','
name|'None'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_reseller_check'
op|'('
name|'account'
op|','
name|'tenant_id'
op|')'
op|':'
newline|'\n'
comment|'# domain id can be inferred from request (may be None)'
nl|'\n'
indent|'            '
name|'req_has_id'
op|'='
name|'True'
newline|'\n'
name|'req_id'
op|'='
name|'env_identity'
op|'['
string|"'project_domain'"
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'exists'
op|':'
newline|'\n'
comment|'# new account so set a domain id'
nl|'\n'
indent|'            '
name|'new_id'
op|'='
name|'req_id'
name|'if'
name|'req_has_id'
name|'else'
name|'UNKNOWN_ID'
newline|'\n'
dedent|''
name|'elif'
name|'sysmeta_id'
name|'is'
name|'None'
name|'and'
name|'req_id'
op|'=='
name|'self'
op|'.'
name|'default_domain_id'
op|':'
newline|'\n'
comment|'# legacy account, update if default domain id in req'
nl|'\n'
indent|'            '
name|'new_id'
op|'='
name|'req_id'
newline|'\n'
dedent|''
name|'elif'
name|'sysmeta_id'
op|'=='
name|'UNKNOWN_ID'
name|'and'
name|'req_has_id'
op|':'
newline|'\n'
comment|'# unknown domain, update if req confirms domain'
nl|'\n'
indent|'            '
name|'new_id'
op|'='
name|'req_id'
name|'or'
string|"''"
newline|'\n'
dedent|''
name|'elif'
name|'req_has_id'
name|'and'
name|'sysmeta_id'
op|'!='
name|'req_id'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warn'
op|'('
string|'"Inconsistent project domain id: "'
op|'+'
nl|'\n'
string|'"%s in token vs %s in account metadata."'
nl|'\n'
op|'%'
op|'('
name|'req_id'
op|','
name|'sysmeta_id'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'new_id'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'headers'
op|'['
name|'PROJECT_DOMAIN_ID_SYSMETA_HEADER'
op|']'
op|'='
name|'new_id'
newline|'\n'
nl|'\n'
DECL|member|_is_name_allowed_in_acl
dedent|''
dedent|''
name|'def'
name|'_is_name_allowed_in_acl'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'path_parts'
op|','
name|'identity'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'allow_names_in_acls'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'user_domain_id'
op|'='
name|'identity'
op|'['
string|"'user_domain'"
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'user_domain_id'
name|'and'
name|'user_domain_id'
op|'!='
name|'self'
op|'.'
name|'default_domain_id'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
dedent|''
name|'proj_domain_id'
op|'='
name|'identity'
op|'['
string|"'project_domain'"
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'proj_domain_id'
name|'and'
name|'proj_domain_id'
op|'!='
name|'self'
op|'.'
name|'default_domain_id'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
comment|'# request user and scoped project are both in default domain'
nl|'\n'
dedent|''
name|'tenant_id'
op|','
name|'tenant_name'
op|'='
name|'identity'
op|'['
string|"'tenant'"
op|']'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'path_parts'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_reseller_check'
op|'('
name|'account'
op|','
name|'tenant_id'
op|')'
op|':'
newline|'\n'
comment|'# account == scoped project, so account is also in default domain'
nl|'\n'
indent|'            '
name|'allow'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# retrieve account project domain id from account sysmeta'
nl|'\n'
indent|'            '
name|'exists'
op|','
name|'acc_domain_id'
op|'='
name|'self'
op|'.'
name|'_get_project_domain_id'
op|'('
name|'req'
op|'.'
name|'environ'
op|')'
newline|'\n'
name|'allow'
op|'='
name|'exists'
name|'and'
name|'acc_domain_id'
name|'in'
op|'['
name|'self'
op|'.'
name|'default_domain_id'
op|','
name|'None'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'allow'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|'"Names allowed in acls."'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'allow'
newline|'\n'
nl|'\n'
DECL|member|_authorize_cross_tenant
dedent|''
name|'def'
name|'_authorize_cross_tenant'
op|'('
name|'self'
op|','
name|'user_id'
op|','
name|'user_name'
op|','
nl|'\n'
name|'tenant_id'
op|','
name|'tenant_name'
op|','
name|'roles'
op|','
nl|'\n'
name|'allow_names'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Check cross-tenant ACLs.\n\n        Match tenant:user, tenant and user could be its id, name or \'*\'\n\n        :param user_id: The user id from the identity token.\n        :param user_name: The user name from the identity token.\n        :param tenant_id: The tenant ID from the identity token.\n        :param tenant_name: The tenant name from the identity token.\n        :param roles: The given container ACL.\n        :param allow_names: If True then attempt to match tenant and user names\n                            as well as id\'s.\n\n        :returns: matched string if tenant(name/id/*):user(name/id/*) matches\n                  the given ACL.\n                  None otherwise.\n\n        """'
newline|'\n'
name|'tenant_match'
op|'='
op|'['
name|'tenant_id'
op|','
string|"'*'"
op|']'
newline|'\n'
name|'user_match'
op|'='
op|'['
name|'user_id'
op|','
string|"'*'"
op|']'
newline|'\n'
name|'if'
name|'allow_names'
op|':'
newline|'\n'
indent|'            '
name|'tenant_match'
op|'='
name|'tenant_match'
op|'+'
op|'['
name|'tenant_name'
op|']'
newline|'\n'
name|'user_match'
op|'='
name|'user_match'
op|'+'
op|'['
name|'user_name'
op|']'
newline|'\n'
dedent|''
name|'for'
name|'tenant'
name|'in'
name|'tenant_match'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'user'
name|'in'
name|'user_match'
op|':'
newline|'\n'
indent|'                '
name|'s'
op|'='
string|"'%s:%s'"
op|'%'
op|'('
name|'tenant'
op|','
name|'user'
op|')'
newline|'\n'
name|'if'
name|'s'
name|'in'
name|'roles'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'s'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|authorize
dedent|''
name|'def'
name|'authorize'
op|'('
name|'self'
op|','
name|'env_identity'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'tenant_id'
op|','
name|'tenant_name'
op|'='
name|'env_identity'
op|'['
string|"'tenant'"
op|']'
newline|'\n'
name|'user_id'
op|','
name|'user_name'
op|'='
name|'env_identity'
op|'['
string|"'user'"
op|']'
newline|'\n'
name|'referrers'
op|','
name|'roles'
op|'='
name|'swift_acl'
op|'.'
name|'parse_acl'
op|'('
name|'getattr'
op|'('
name|'req'
op|','
string|"'acl'"
op|','
name|'None'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'#allow OPTIONS requests to proceed as normal'
nl|'\n'
name|'if'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'OPTIONS'"
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'part'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'1'
op|','
number|'4'
op|','
name|'True'
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
name|'part'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'_set_project_domain_id'
op|'('
name|'req'
op|','
name|'part'
op|','
name|'env_identity'
op|')'
newline|'\n'
nl|'\n'
name|'user_roles'
op|'='
op|'['
name|'r'
op|'.'
name|'lower'
op|'('
op|')'
name|'for'
name|'r'
name|'in'
name|'env_identity'
op|'.'
name|'get'
op|'('
string|"'roles'"
op|','
op|'['
op|']'
op|')'
op|']'
newline|'\n'
nl|'\n'
comment|'# Give unconditional access to a user with the reseller_admin'
nl|'\n'
comment|'# role.'
nl|'\n'
name|'if'
name|'self'
op|'.'
name|'reseller_admin_role'
name|'in'
name|'user_roles'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"'User %s has reseller admin authorizing'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'msg'
op|','
name|'tenant_id'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift_owner'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
comment|'# If we are not reseller admin and user is trying to delete its own'
nl|'\n'
comment|'# account then deny it.'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'container'
name|'and'
name|'not'
name|'obj'
name|'and'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'DELETE'"
op|':'
newline|'\n'
comment|'# User is not allowed to issue a DELETE on its own account'
nl|'\n'
indent|'            '
name|'msg'
op|'='
string|"'User %s:%s is not allowed to delete its own account'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'msg'
op|','
name|'tenant_name'
op|','
name|'user_name'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
comment|'# cross-tenant authorization'
nl|'\n'
dedent|''
name|'matched_acl'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'roles'
op|':'
newline|'\n'
indent|'            '
name|'allow_names'
op|'='
name|'self'
op|'.'
name|'_is_name_allowed_in_acl'
op|'('
name|'req'
op|','
name|'part'
op|','
name|'env_identity'
op|')'
newline|'\n'
name|'matched_acl'
op|'='
name|'self'
op|'.'
name|'_authorize_cross_tenant'
op|'('
name|'user_id'
op|','
name|'user_name'
op|','
nl|'\n'
name|'tenant_id'
op|','
name|'tenant_name'
op|','
nl|'\n'
name|'roles'
op|','
name|'allow_names'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'matched_acl'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'log_msg'
op|'='
string|"'user %s allowed in ACL authorizing.'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_msg'
op|','
name|'matched_acl'
op|')'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'acl_authorized'
op|'='
name|'self'
op|'.'
name|'_authorize_unconfirmed_identity'
op|'('
name|'req'
op|','
name|'obj'
op|','
nl|'\n'
name|'referrers'
op|','
nl|'\n'
name|'roles'
op|')'
newline|'\n'
name|'if'
name|'acl_authorized'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
comment|'# Check if a user tries to access an account that does not match their'
nl|'\n'
comment|'# token'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'_reseller_check'
op|'('
name|'account'
op|','
name|'tenant_id'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'log_msg'
op|'='
string|"'tenant mismatch: %s != %s'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_msg'
op|','
name|'account'
op|','
name|'tenant_id'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
comment|'# Check the roles the user is belonging to. If the user is'
nl|'\n'
comment|'# part of the role defined in the config variable'
nl|'\n'
comment|'# operator_roles (like admin) then it will be'
nl|'\n'
comment|'# promoted as an admin of the account/tenant.'
nl|'\n'
dedent|''
name|'for'
name|'role'
name|'in'
name|'self'
op|'.'
name|'operator_roles'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'role'
op|'='
name|'role'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'role'
name|'in'
name|'user_roles'
op|':'
newline|'\n'
indent|'                '
name|'log_msg'
op|'='
string|"'allow user with role %s as account admin'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_msg'
op|','
name|'role'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift_owner'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
comment|'# If user is of the same name of the tenant then make owner of it.'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'self'
op|'.'
name|'is_admin'
name|'and'
name|'user_name'
op|'=='
name|'tenant_name'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warning'
op|'('
string|'"the is_admin feature has been deprecated "'
nl|'\n'
string|'"and will be removed in the future "'
nl|'\n'
string|'"update your config file"'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift_owner'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'acl_authorized'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
comment|'# Check if we have the role in the userroles and allow it'
nl|'\n'
dedent|''
name|'for'
name|'user_role'
name|'in'
name|'user_roles'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'user_role'
name|'in'
op|'('
name|'r'
op|'.'
name|'lower'
op|'('
op|')'
name|'for'
name|'r'
name|'in'
name|'roles'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'log_msg'
op|'='
string|"'user %s:%s allowed in ACL: %s authorizing'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_msg'
op|','
name|'tenant_name'
op|','
name|'user_name'
op|','
nl|'\n'
name|'user_role'
op|')'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|authorize_anonymous
dedent|''
name|'def'
name|'authorize_anonymous'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Authorize an anonymous request.\n\n        :returns: None if authorization is granted, an error page otherwise.\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'part'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'1'
op|','
number|'4'
op|','
name|'True'
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
name|'part'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
comment|'#allow OPTIONS requests to proceed as normal'
nl|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'OPTIONS'"
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'is_authoritative_authz'
op|'='
op|'('
name|'account'
name|'and'
nl|'\n'
name|'account'
op|'.'
name|'startswith'
op|'('
name|'self'
op|'.'
name|'reseller_prefix'
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_authoritative_authz'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'referrers'
op|','
name|'roles'
op|'='
name|'swift_acl'
op|'.'
name|'parse_acl'
op|'('
name|'getattr'
op|'('
name|'req'
op|','
string|"'acl'"
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'authorized'
op|'='
name|'self'
op|'.'
name|'_authorize_unconfirmed_identity'
op|'('
name|'req'
op|','
name|'obj'
op|','
name|'referrers'
op|','
nl|'\n'
name|'roles'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'authorized'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'denied_response'
op|'('
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_authorize_unconfirmed_identity
dedent|''
dedent|''
name|'def'
name|'_authorize_unconfirmed_identity'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'obj'
op|','
name|'referrers'
op|','
name|'roles'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'""""\n        Perform authorization for access that does not require a\n        confirmed identity.\n\n        :returns: A boolean if authorization is granted or denied.  None if\n                  a determination could not be made.\n        """'
newline|'\n'
comment|'# Allow container sync.'
nl|'\n'
name|'if'
op|'('
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift_sync_key'"
op|')'
nl|'\n'
name|'and'
op|'('
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift_sync_key'"
op|']'
op|'=='
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-container-sync-key'"
op|','
name|'None'
op|')'
op|')'
nl|'\n'
name|'and'
string|"'x-timestamp'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'log_msg'
op|'='
string|"'allowing proxy %s for container-sync'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_msg'
op|','
name|'req'
op|'.'
name|'remote_addr'
op|')'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
nl|'\n'
comment|'# Check if referrer is allowed.'
nl|'\n'
dedent|''
name|'if'
name|'swift_acl'
op|'.'
name|'referrer_allowed'
op|'('
name|'req'
op|'.'
name|'referer'
op|','
name|'referrers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj'
name|'or'
string|"'.rlistings'"
name|'in'
name|'roles'
op|':'
newline|'\n'
indent|'                '
name|'log_msg'
op|'='
string|"'authorizing %s via referer ACL'"
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_msg'
op|','
name|'req'
op|'.'
name|'referrer'
op|')'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'return'
name|'False'
newline|'\n'
nl|'\n'
DECL|member|denied_response
dedent|''
dedent|''
name|'def'
name|'denied_response'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Deny WSGI Response.\n\n        Returns a standard WSGI response callable with the status of 403 or 401\n        depending on whether the REMOTE_USER is set or not.\n        """'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'remote_user'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPForbidden'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPUnauthorized'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
dedent|''
dedent|''
dedent|''
name|'def'
name|'filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Returns a WSGI filter app for use with paste.deploy."""'
newline|'\n'
name|'conf'
op|'='
name|'global_conf'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'.'
name|'update'
op|'('
name|'local_conf'
op|')'
newline|'\n'
name|'register_swift_info'
op|'('
string|"'keystoneauth'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|auth_filter
name|'def'
name|'auth_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'KeystoneAuth'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'auth_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
