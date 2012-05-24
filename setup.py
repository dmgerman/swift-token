begin_unit
comment|'#!/usr/bin/python'
nl|'\n'
comment|'# Copyright (c) 2010-2012 OpenStack, LLC.'
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
name|'from'
name|'setuptools'
name|'import'
name|'setup'
op|','
name|'find_packages'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
name|'import'
name|'__canonical_version__'
name|'as'
name|'version'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|name
name|'name'
op|'='
string|"'swift'"
newline|'\n'
nl|'\n'
nl|'\n'
name|'setup'
op|'('
nl|'\n'
DECL|variable|name
name|'name'
op|'='
name|'name'
op|','
nl|'\n'
DECL|variable|version
name|'version'
op|'='
name|'version'
op|','
nl|'\n'
DECL|variable|description
name|'description'
op|'='
string|"'Swift'"
op|','
nl|'\n'
DECL|variable|license
name|'license'
op|'='
string|"'Apache License (2.0)'"
op|','
nl|'\n'
DECL|variable|author
name|'author'
op|'='
string|"'OpenStack, LLC.'"
op|','
nl|'\n'
DECL|variable|author_email
name|'author_email'
op|'='
string|"'openstack-admins@lists.launchpad.net'"
op|','
nl|'\n'
DECL|variable|url
name|'url'
op|'='
string|"'https://launchpad.net/swift'"
op|','
nl|'\n'
DECL|variable|packages
name|'packages'
op|'='
name|'find_packages'
op|'('
name|'exclude'
op|'='
op|'['
string|"'test'"
op|','
string|"'bin'"
op|']'
op|')'
op|','
nl|'\n'
DECL|variable|test_suite
name|'test_suite'
op|'='
string|"'nose.collector'"
op|','
nl|'\n'
DECL|variable|classifiers
name|'classifiers'
op|'='
op|'['
nl|'\n'
string|"'Development Status :: 4 - Beta'"
op|','
nl|'\n'
string|"'License :: OSI Approved :: Apache Software License'"
op|','
nl|'\n'
string|"'Operating System :: POSIX :: Linux'"
op|','
nl|'\n'
string|"'Programming Language :: Python :: 2.6'"
op|','
nl|'\n'
string|"'Environment :: No Input/Output (Daemon)'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
DECL|variable|install_requires
name|'install_requires'
op|'='
op|'['
op|']'
op|','
comment|'# removed for better compat'
nl|'\n'
DECL|variable|scripts
name|'scripts'
op|'='
op|'['
nl|'\n'
string|"'bin/swift'"
op|','
nl|'\n'
string|"'bin/swift-account-audit'"
op|','
nl|'\n'
string|"'bin/swift-account-auditor'"
op|','
nl|'\n'
string|"'bin/swift-account-reaper'"
op|','
nl|'\n'
string|"'bin/swift-account-replicator'"
op|','
nl|'\n'
string|"'bin/swift-account-server'"
op|','
nl|'\n'
string|"'bin/swift-bench'"
op|','
nl|'\n'
string|"'bin/swift-container-auditor'"
op|','
nl|'\n'
string|"'bin/swift-container-replicator'"
op|','
nl|'\n'
string|"'bin/swift-container-server'"
op|','
nl|'\n'
string|"'bin/swift-container-sync'"
op|','
nl|'\n'
string|"'bin/swift-container-updater'"
op|','
nl|'\n'
string|"'bin/swift-dispersion-populate'"
op|','
nl|'\n'
string|"'bin/swift-dispersion-report'"
op|','
nl|'\n'
string|"'bin/swift-drive-audit'"
op|','
nl|'\n'
string|"'bin/swift-form-signature'"
op|','
nl|'\n'
string|"'bin/swift-get-nodes'"
op|','
nl|'\n'
string|"'bin/swift-init'"
op|','
nl|'\n'
string|"'bin/swift-object-auditor'"
op|','
nl|'\n'
string|"'bin/swift-object-expirer'"
op|','
nl|'\n'
string|"'bin/swift-object-info'"
op|','
nl|'\n'
string|"'bin/swift-object-replicator'"
op|','
nl|'\n'
string|"'bin/swift-object-server'"
op|','
nl|'\n'
string|"'bin/swift-object-updater'"
op|','
nl|'\n'
string|"'bin/swift-oldies'"
op|','
nl|'\n'
string|"'bin/swift-orphans'"
op|','
nl|'\n'
string|"'bin/swift-proxy-server'"
op|','
nl|'\n'
string|"'bin/swift-recon'"
op|','
nl|'\n'
string|"'bin/swift-recon-cron'"
op|','
nl|'\n'
string|"'bin/swift-ring-builder'"
op|','
nl|'\n'
string|"'bin/swift-temp-url'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
DECL|variable|entry_points
name|'entry_points'
op|'='
op|'{'
nl|'\n'
string|"'paste.app_factory'"
op|':'
op|'['
nl|'\n'
string|"'proxy=swift.proxy.server:app_factory'"
op|','
nl|'\n'
string|"'object=swift.obj.server:app_factory'"
op|','
nl|'\n'
string|"'container=swift.container.server:app_factory'"
op|','
nl|'\n'
string|"'account=swift.account.server:app_factory'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
string|"'paste.filter_factory'"
op|':'
op|'['
nl|'\n'
string|"'healthcheck=swift.common.middleware.healthcheck:filter_factory'"
op|','
nl|'\n'
string|"'memcache=swift.common.middleware.memcache:filter_factory'"
op|','
nl|'\n'
string|"'ratelimit=swift.common.middleware.ratelimit:filter_factory'"
op|','
nl|'\n'
string|"'cname_lookup=swift.common.middleware.cname_lookup:filter_factory'"
op|','
nl|'\n'
string|"'catch_errors=swift.common.middleware.catch_errors:filter_factory'"
op|','
nl|'\n'
string|"'domain_remap=swift.common.middleware.domain_remap:filter_factory'"
op|','
nl|'\n'
string|"'staticweb=swift.common.middleware.staticweb:filter_factory'"
op|','
nl|'\n'
string|"'tempauth=swift.common.middleware.tempauth:filter_factory'"
op|','
nl|'\n'
string|"'recon=swift.common.middleware.recon:filter_factory'"
op|','
nl|'\n'
string|"'tempurl=swift.common.middleware.tempurl:filter_factory'"
op|','
nl|'\n'
string|"'formpost=swift.common.middleware.formpost:filter_factory'"
op|','
nl|'\n'
string|"'name_check=swift.common.middleware.name_check:filter_factory'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
op|'}'
op|','
nl|'\n'
op|')'
newline|'\n'
endmarker|''
end_unit
