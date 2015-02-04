begin_unit
comment|'# Copyright (c) 2010-2014 OpenStack Foundation'
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
name|'inspect'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'__version__'
name|'as'
name|'swift_version'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'public'
op|','
name|'timing_stats'
op|','
name|'config_true_value'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Response'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BaseStorageServer
name|'class'
name|'BaseStorageServer'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Implements common OPTIONS method for object, account, container servers.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_allowed_methods'
op|'='
name|'None'
newline|'\n'
name|'replication_server'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'replication_server'"
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
name|'replication_server'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'replication_server'
op|'='
name|'config_true_value'
op|'('
name|'replication_server'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'replication_server'
op|'='
name|'replication_server'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|server_type
name|'def'
name|'server_type'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'NotImplementedError'
op|'('
nl|'\n'
string|"'Storage nodes have not implemented the Server type.'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|allowed_methods
name|'def'
name|'allowed_methods'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_allowed_methods'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_allowed_methods'
op|'='
op|'['
op|']'
newline|'\n'
name|'all_methods'
op|'='
name|'inspect'
op|'.'
name|'getmembers'
op|'('
name|'self'
op|','
name|'predicate'
op|'='
name|'callable'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'self'
op|'.'
name|'replication_server'
name|'is'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'name'
op|','
name|'m'
name|'in'
name|'all_methods'
op|':'
newline|'\n'
indent|'                    '
name|'if'
op|'('
name|'getattr'
op|'('
name|'m'
op|','
string|"'publicly_accessible'"
op|','
name|'False'
op|')'
name|'and'
nl|'\n'
name|'getattr'
op|'('
name|'m'
op|','
string|"'replication'"
op|','
name|'False'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_allowed_methods'
op|'.'
name|'append'
op|'('
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'elif'
name|'self'
op|'.'
name|'replication_server'
name|'is'
name|'False'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'name'
op|','
name|'m'
name|'in'
name|'all_methods'
op|':'
newline|'\n'
indent|'                    '
name|'if'
op|'('
name|'getattr'
op|'('
name|'m'
op|','
string|"'publicly_accessible'"
op|','
name|'False'
op|')'
name|'and'
name|'not'
nl|'\n'
name|'getattr'
op|'('
name|'m'
op|','
string|"'replication'"
op|','
name|'False'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_allowed_methods'
op|'.'
name|'append'
op|'('
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'elif'
name|'self'
op|'.'
name|'replication_server'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'name'
op|','
name|'m'
name|'in'
name|'all_methods'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'getattr'
op|'('
name|'m'
op|','
string|"'publicly_accessible'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_allowed_methods'
op|'.'
name|'append'
op|'('
name|'name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'self'
op|'.'
name|'_allowed_methods'
op|'.'
name|'sort'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'_allowed_methods'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|OPTIONS
name|'def'
name|'OPTIONS'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Base handler for OPTIONS requests\n\n        :param req: swob.Request object\n        :returns: swob.Response object\n        """'
newline|'\n'
comment|'# Prepare the default response'
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Allow'"
op|':'
string|"', '"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'allowed_methods'
op|')'
op|','
nl|'\n'
string|"'Server'"
op|':'
string|"'%s/%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'server_type'
op|','
name|'swift_version'
op|')'
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit