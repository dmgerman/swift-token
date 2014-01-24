begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack Foundation'
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
string|'"""\nMiscellaneous utility functions for use in generating responses.\n\nWhy not swift.common.utils, you ask? Because this way we can import things\nfrom swob in here without creating circular imports.\n"""'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'FORMAT2CONTENT_TYPE'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPBadRequest'
op|','
name|'HTTPNotAcceptable'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
op|','
name|'validate_device_partition'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_param
name|'def'
name|'get_param'
op|'('
name|'req'
op|','
name|'name'
op|','
name|'default'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get parameters from an HTTP request ensuring proper handling UTF-8\n    encoding.\n\n    :param req: request object\n    :param name: parameter name\n    :param default: result to return if the parameter is not found\n    :returns: HTTP request parameter value\n              (as UTF-8 encoded str, not unicode object)\n    :raises: HTTPBadRequest if param not valid UTF-8 byte sequence\n    """'
newline|'\n'
name|'value'
op|'='
name|'req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
name|'name'
op|','
name|'default'
op|')'
newline|'\n'
name|'if'
name|'value'
name|'and'
name|'not'
name|'isinstance'
op|'('
name|'value'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'.'
name|'decode'
op|'('
string|"'utf8'"
op|')'
comment|'# Ensure UTF8ness'
newline|'\n'
dedent|''
name|'except'
name|'UnicodeDecodeError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|'\'"%s" parameter not valid UTF-8\''
op|'%'
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'value'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_listing_content_type
dedent|''
name|'def'
name|'get_listing_content_type'
op|'('
name|'req'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Determine the content type to use for an account or container listing\n    response.\n\n    :param req: request object\n    :returns: content type as a string (e.g. text/plain, application/json)\n    :raises: HTTPNotAcceptable if the requested content type is not acceptable\n    :raises: HTTPBadRequest if the \'format\' query param is provided and\n             not valid UTF-8\n    """'
newline|'\n'
name|'query_format'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'format'"
op|')'
newline|'\n'
name|'if'
name|'query_format'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'.'
name|'accept'
op|'='
name|'FORMAT2CONTENT_TYPE'
op|'.'
name|'get'
op|'('
nl|'\n'
name|'query_format'
op|'.'
name|'lower'
op|'('
op|')'
op|','
name|'FORMAT2CONTENT_TYPE'
op|'['
string|"'plain'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'out_content_type'
op|'='
name|'req'
op|'.'
name|'accept'
op|'.'
name|'best_match'
op|'('
nl|'\n'
op|'['
string|"'text/plain'"
op|','
string|"'application/json'"
op|','
string|"'application/xml'"
op|','
string|"'text/xml'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'out_content_type'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPNotAcceptable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'out_content_type'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|split_and_validate_path
dedent|''
name|'def'
name|'split_and_validate_path'
op|'('
name|'request'
op|','
name|'minsegs'
op|'='
number|'1'
op|','
name|'maxsegs'
op|'='
name|'None'
op|','
nl|'\n'
name|'rest_with_last'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Utility function to split and validate the request path.\n\n    :returns: result of split_path if everything\'s okay\n    :raises: HTTPBadRequest if something\'s not okay\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'segs'
op|'='
name|'split_path'
op|'('
name|'unquote'
op|'('
name|'request'
op|'.'
name|'path'
op|')'
op|','
nl|'\n'
name|'minsegs'
op|','
name|'maxsegs'
op|','
name|'rest_with_last'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'segs'
op|'['
number|'0'
op|']'
op|','
name|'segs'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
name|'return'
name|'segs'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'request'
op|'='
name|'request'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|is_user_meta
dedent|''
dedent|''
name|'def'
name|'is_user_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Tests if a header key starts with and is longer than the user\n    metadata prefix for given server type.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: True if the key satisfies the test, False otherwise\n    """'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'key'
op|')'
op|'<='
number|'8'
op|'+'
name|'len'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
name|'get_user_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|is_sys_meta
dedent|''
name|'def'
name|'is_sys_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Tests if a header key starts with and is longer than the system\n    metadata prefix for given server type.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: True if the key satisfies the test, False otherwise\n    """'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'key'
op|')'
op|'<='
number|'11'
op|'+'
name|'len'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
name|'get_sys_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|is_sys_or_user_meta
dedent|''
name|'def'
name|'is_sys_or_user_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Tests if a header key starts with and is longer than the user or system\n    metadata prefix for given server type.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: True if the key satisfies the test, False otherwise\n    """'
newline|'\n'
name|'return'
name|'is_user_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
name|'or'
name|'is_sys_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|strip_user_meta_prefix
dedent|''
name|'def'
name|'strip_user_meta_prefix'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes the user metadata prefix for a given server type from the start\n    of a header key.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: stripped header key\n    """'
newline|'\n'
name|'return'
name|'key'
op|'['
name|'len'
op|'('
name|'get_user_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
op|':'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|strip_sys_meta_prefix
dedent|''
name|'def'
name|'strip_sys_meta_prefix'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes the system metadata prefix for a given server type from the start\n    of a header key.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: stripped header key\n    """'
newline|'\n'
name|'return'
name|'key'
op|'['
name|'len'
op|'('
name|'get_sys_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
op|':'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_user_meta_prefix
dedent|''
name|'def'
name|'get_user_meta_prefix'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns the prefix for user metadata headers for given server type.\n\n    This prefix defines the namespace for headers that will be persisted\n    by backend servers.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :returns: prefix string for server type\'s user metadata headers\n    """'
newline|'\n'
name|'return'
string|"'x-%s-%s-'"
op|'%'
op|'('
name|'server_type'
op|'.'
name|'lower'
op|'('
op|')'
op|','
string|"'meta'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_sys_meta_prefix
dedent|''
name|'def'
name|'get_sys_meta_prefix'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns the prefix for system metadata headers for given server type.\n\n    This prefix defines the namespace for headers that will be persisted\n    by backend servers.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :returns: prefix string for server type\'s system metadata headers\n    """'
newline|'\n'
name|'return'
string|"'x-%s-%s-'"
op|'%'
op|'('
name|'server_type'
op|'.'
name|'lower'
op|'('
op|')'
op|','
string|"'sysmeta'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|remove_items
dedent|''
name|'def'
name|'remove_items'
op|'('
name|'headers'
op|','
name|'condition'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes items from a dict whose keys satisfy\n    the given condition.\n\n    :param headers: a dict of headers\n    :param condition: a function that will be passed the header key as a\n                      single argument and should return True if the header\n                      is to be removed.\n    :returns: a dict, possibly empty, of headers that have been removed\n    """'
newline|'\n'
name|'removed'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'keys'
op|'='
name|'filter'
op|'('
name|'condition'
op|','
name|'headers'
op|')'
newline|'\n'
name|'removed'
op|'.'
name|'update'
op|'('
op|'('
name|'key'
op|','
name|'headers'
op|'.'
name|'pop'
op|'('
name|'key'
op|')'
op|')'
name|'for'
name|'key'
name|'in'
name|'keys'
op|')'
newline|'\n'
name|'return'
name|'removed'
newline|'\n'
dedent|''
endmarker|''
end_unit
