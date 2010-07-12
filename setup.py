begin_unit
comment|'#!/usr/bin/python'
nl|'\n'
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
name|'from'
name|'distutils'
op|'.'
name|'core'
name|'import'
name|'setup'
newline|'\n'
nl|'\n'
name|'setup'
op|'('
nl|'\n'
DECL|variable|name
name|'name'
op|'='
string|"'swift'"
op|','
nl|'\n'
DECL|variable|version
name|'version'
op|'='
string|"'1.0.0-1'"
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
nl|'\n'
DECL|variable|author
name|'author'
op|'='
string|"'OpenStack, LLC.'"
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
op|'['
string|"'swift'"
op|','
string|"'swift.common'"
op|']'
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
DECL|variable|scripts
name|'scripts'
op|'='
op|'['
string|"'bin/st.py'"
op|','
string|"'bin/swift-account-auditor.py'"
op|','
nl|'\n'
string|"'bin/swift-account-audit.py'"
op|','
string|"'bin/swift-account-reaper.py'"
op|','
nl|'\n'
string|"'bin/swift-account-replicator.py'"
op|','
string|"'bin/swift-account-server.py'"
op|','
nl|'\n'
string|"'bin/swift-auth-create-account.py'"
op|','
nl|'\n'
string|"'bin/swift-auth-recreate-accounts.py'"
op|','
string|"'bin/swift-auth-server.py'"
op|','
nl|'\n'
string|"'bin/swift-container-auditor.py'"
op|','
nl|'\n'
string|"'bin/swift-container-replicator.py'"
op|','
nl|'\n'
string|"'bin/swift-container-server.py'"
op|','
string|"'bin/swift-container-updater.py'"
op|','
nl|'\n'
string|"'bin/swift-drive-audit.py'"
op|','
string|"'bin/swift-get-nodes.py'"
op|','
nl|'\n'
string|"'bin/swift-init.py'"
op|','
string|"'bin/swift-object-auditor.py'"
op|','
nl|'\n'
string|"'bin/swift-object-info.py'"
op|','
string|"'bin/swift-object-server.py'"
op|','
nl|'\n'
string|"'bin/swift-object-updater.py'"
op|','
string|"'bin/swift-proxy-server.py'"
op|','
nl|'\n'
string|"'bin/swift-ring-builder.py'"
op|','
string|"'bin/swift-stats-populate.py'"
op|','
nl|'\n'
string|"'bin/swift-stats-report.py'"
op|']'
nl|'\n'
op|')'
newline|'\n'
endmarker|''
end_unit
