begin_unit
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
name|'webob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPBadRequest'
newline|'\n'
name|'import'
name|'dns'
op|'.'
name|'resolver'
newline|'\n'
name|'from'
name|'dns'
op|'.'
name|'exception'
name|'import'
name|'DNSException'
newline|'\n'
name|'from'
name|'dns'
op|'.'
name|'resolver'
name|'import'
name|'NXDOMAIN'
op|','
name|'NoAnswer'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'cache_from_env'
op|','
name|'get_logger'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|lookup_cname
name|'def'
name|'lookup_cname'
op|'('
name|'domain'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'    '
string|'"""\n    Given a domain, returns its DNS CNAME mapping and DNS ttl.\n\n    :param domain: domain to query on\n    :returns: (ttl, result)\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'answer'
op|'='
name|'dns'
op|'.'
name|'resolver'
op|'.'
name|'query'
op|'('
name|'domain'
op|','
string|"'CNAME'"
op|')'
op|'.'
name|'rrset'
newline|'\n'
name|'ttl'
op|'='
name|'answer'
op|'.'
name|'ttl'
newline|'\n'
name|'result'
op|'='
name|'answer'
op|'.'
name|'items'
op|'['
number|'0'
op|']'
op|'.'
name|'to_text'
op|'('
op|')'
newline|'\n'
name|'result'
op|'='
name|'result'
op|'.'
name|'rstrip'
op|'('
string|"'.'"
op|')'
newline|'\n'
name|'return'
name|'ttl'
op|','
name|'result'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'DNSException'
op|','
name|'NXDOMAIN'
op|','
name|'NoAnswer'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
number|'0'
op|','
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|CNAMELookupMiddleware
dedent|''
dedent|''
name|'class'
name|'CNAMELookupMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Middleware that translates a unknown domain in the host header to\n    something that ends with the configured storage_domain by looking up\n    the given domain\'s CNAME record in DNS.\n    """'
newline|'\n'
nl|'\n'
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
name|'storage_domain'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'storage_domain'"
op|','
string|"'example.com'"
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'storage_domain'
name|'and'
name|'self'
op|'.'
name|'storage_domain'
op|'['
number|'0'
op|']'
op|'!='
string|"'.'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'storage_domain'
op|'='
string|"'.'"
op|'+'
name|'self'
op|'.'
name|'storage_domain'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'lookup_depth'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'lookup_depth'"
op|','
string|"'1'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'memcache'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'cname-lookup'"
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
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'storage_domain'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'given_domain'
op|'='
name|'env'
op|'['
string|"'HTTP_HOST'"
op|']'
newline|'\n'
name|'port'
op|'='
string|"''"
newline|'\n'
name|'if'
string|"':'"
name|'in'
name|'given_domain'
op|':'
newline|'\n'
indent|'            '
name|'given_domain'
op|','
name|'port'
op|'='
name|'given_domain'
op|'.'
name|'rsplit'
op|'('
string|"':'"
op|','
number|'1'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'given_domain'
op|'=='
name|'self'
op|'.'
name|'storage_domain'
op|'['
number|'1'
op|':'
op|']'
op|':'
comment|"# strip initial '.'"
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'a_domain'
op|'='
name|'given_domain'
newline|'\n'
name|'if'
name|'not'
name|'a_domain'
op|'.'
name|'endswith'
op|'('
name|'self'
op|'.'
name|'storage_domain'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'memcache'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'memcache'
op|'='
name|'cache_from_env'
op|'('
name|'env'
op|')'
newline|'\n'
dedent|''
name|'error'
op|'='
name|'True'
newline|'\n'
name|'for'
name|'tries'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'lookup_depth'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'found_domain'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'memcache'
op|':'
newline|'\n'
indent|'                    '
name|'memcache_key'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
op|'['
string|"'cname-'"
op|','
name|'a_domain'
op|']'
op|')'
newline|'\n'
name|'found_domain'
op|'='
name|'self'
op|'.'
name|'memcache'
op|'.'
name|'get'
op|'('
name|'memcache_key'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'found_domain'
op|':'
newline|'\n'
indent|'                    '
name|'ttl'
op|','
name|'found_domain'
op|'='
name|'lookup_cname'
op|'('
name|'a_domain'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'memcache'
op|':'
newline|'\n'
indent|'                        '
name|'memcache_key'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
op|'['
string|"'cname-'"
op|','
name|'given_domain'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'memcache'
op|'.'
name|'set'
op|'('
name|'memcache_key'
op|','
name|'found_domain'
op|','
nl|'\n'
name|'timeout'
op|'='
name|'ttl'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'found_domain'
name|'is'
name|'None'
name|'or'
name|'found_domain'
op|'=='
name|'a_domain'
op|':'
newline|'\n'
comment|"# no CNAME records or we're at the last lookup"
nl|'\n'
indent|'                    '
name|'error'
op|'='
name|'True'
newline|'\n'
name|'found_domain'
op|'='
name|'None'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
name|'elif'
name|'found_domain'
op|'.'
name|'endswith'
op|'('
name|'self'
op|'.'
name|'storage_domain'
op|')'
op|':'
newline|'\n'
comment|'# Found it!'
nl|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Mapped %(given_domain)s to %(found_domain)s'"
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'given_domain'"
op|':'
name|'given_domain'
op|','
nl|'\n'
string|"'found_domain'"
op|':'
name|'found_domain'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'port'
op|':'
newline|'\n'
indent|'                        '
name|'env'
op|'['
string|"'HTTP_HOST'"
op|']'
op|'='
string|"':'"
op|'.'
name|'join'
op|'('
op|'['
name|'found_domain'
op|','
name|'port'
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'env'
op|'['
string|"'HTTP_HOST'"
op|']'
op|'='
name|'found_domain'
newline|'\n'
dedent|''
name|'error'
op|'='
name|'False'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# try one more deep in the chain'
nl|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Following CNAME chain for  '"
string|"'%(given_domain)s to %(found_domain)s'"
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'given_domain'"
op|':'
name|'given_domain'
op|','
nl|'\n'
string|"'found_domain'"
op|':'
name|'found_domain'
op|'}'
op|')'
newline|'\n'
name|'a_domain'
op|'='
name|'found_domain'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'error'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'found_domain'
op|':'
newline|'\n'
indent|'                    '
name|'msg'
op|'='
string|"'CNAME lookup failed after %d tries'"
op|'%'
name|'self'
op|'.'
name|'lookup_depth'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'msg'
op|'='
string|"'CNAME lookup failed to resolve to a valid domain'"
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
op|','
name|'body'
op|'='
name|'msg'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
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
comment|'# pragma: no cover'
newline|'\n'
indent|'    '
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
nl|'\n'
DECL|function|cname_filter
name|'def'
name|'cname_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'CNAMELookupMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'cname_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
