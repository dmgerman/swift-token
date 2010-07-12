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
name|'ConfigParser'
name|'import'
name|'ConfigParser'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'run_wsgi'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'auth'
name|'import'
name|'DevAuthMiddleware'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'memcached'
name|'import'
name|'MemcacheRing'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'server'
name|'import'
name|'Application'
newline|'\n'
nl|'\n'
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
DECL|variable|c
indent|'    '
name|'c'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'c'
op|'.'
name|'read'
op|'('
name|'sys'
op|'.'
name|'argv'
op|'['
number|'1'
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|'"Unable to read config file."'
newline|'\n'
name|'sys'
op|'.'
name|'exit'
op|'('
number|'1'
op|')'
newline|'\n'
DECL|variable|conf
dedent|''
name|'conf'
op|'='
name|'dict'
op|'('
name|'c'
op|'.'
name|'items'
op|'('
string|"'proxy-server'"
op|')'
op|')'
newline|'\n'
DECL|variable|swift_dir
name|'swift_dir'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'swift_dir'"
op|','
string|"'/etc/swift'"
op|')'
newline|'\n'
DECL|variable|c
name|'c'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'c'
op|'.'
name|'read'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'auth-server.conf'"
op|')'
op|')'
newline|'\n'
DECL|variable|auth_conf
name|'auth_conf'
op|'='
name|'dict'
op|'('
name|'c'
op|'.'
name|'items'
op|'('
string|"'auth-server'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|variable|memcache
name|'memcache'
op|'='
name|'MemcacheRing'
op|'('
op|'['
name|'s'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'s'
name|'in'
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'memcache_servers'"
op|','
string|"'127.0.0.1:11211'"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
nl|'\n'
name|'if'
name|'s'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
op|')'
newline|'\n'
DECL|variable|logger
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
string|"'proxy'"
op|')'
newline|'\n'
DECL|variable|app
name|'app'
op|'='
name|'Application'
op|'('
name|'conf'
op|','
name|'memcache'
op|','
name|'logger'
op|')'
newline|'\n'
comment|'# Wrap the app with auth'
nl|'\n'
DECL|variable|app
name|'app'
op|'='
name|'DevAuthMiddleware'
op|'('
name|'app'
op|','
name|'auth_conf'
op|','
name|'memcache'
op|','
name|'logger'
op|')'
newline|'\n'
name|'run_wsgi'
op|'('
name|'app'
op|','
name|'conf'
op|','
name|'logger'
op|'='
name|'logger'
op|','
name|'default_port'
op|'='
number|'80'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
