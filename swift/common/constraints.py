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
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'urllib'
newline|'\n'
name|'from'
name|'ConfigParser'
name|'import'
name|'ConfigParser'
op|','
name|'NoSectionError'
op|','
name|'NoOptionError'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPBadRequest'
op|','
name|'HTTPLengthRequired'
op|','
name|'HTTPRequestEntityTooLarge'
newline|'\n'
nl|'\n'
DECL|variable|constraints_conf
name|'constraints_conf'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'constraints_conf'
op|'.'
name|'read'
op|'('
string|"'/etc/swift/swift.conf'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|constraints_conf_int
name|'def'
name|'constraints_conf_int'
op|'('
name|'name'
op|','
name|'default'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'int'
op|'('
name|'constraints_conf'
op|'.'
name|'get'
op|'('
string|"'swift-constraints'"
op|','
name|'name'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'NoSectionError'
op|','
name|'NoOptionError'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'default'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#: Max file size allowed for objects'
nl|'\n'
DECL|variable|MAX_FILE_SIZE
dedent|''
dedent|''
name|'MAX_FILE_SIZE'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_file_size'"
op|','
nl|'\n'
number|'5368709122'
op|')'
comment|'# 5 * 1024 * 1024 * 1024 + 2'
newline|'\n'
comment|'#: Max length of the name of a key for metadata'
nl|'\n'
DECL|variable|MAX_META_NAME_LENGTH
name|'MAX_META_NAME_LENGTH'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_meta_name_length'"
op|','
number|'128'
op|')'
newline|'\n'
comment|'#: Max length of the value of a key for metadata'
nl|'\n'
DECL|variable|MAX_META_VALUE_LENGTH
name|'MAX_META_VALUE_LENGTH'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_meta_value_length'"
op|','
number|'256'
op|')'
newline|'\n'
comment|'#: Max number of metadata items'
nl|'\n'
DECL|variable|MAX_META_COUNT
name|'MAX_META_COUNT'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_meta_count'"
op|','
number|'90'
op|')'
newline|'\n'
comment|'#: Max overall size of metadata'
nl|'\n'
DECL|variable|MAX_META_OVERALL_SIZE
name|'MAX_META_OVERALL_SIZE'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_meta_overall_size'"
op|','
number|'4096'
op|')'
newline|'\n'
comment|'#: Max object name length'
nl|'\n'
DECL|variable|MAX_OBJECT_NAME_LENGTH
name|'MAX_OBJECT_NAME_LENGTH'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_object_name_length'"
op|','
number|'1024'
op|')'
newline|'\n'
comment|'#: Max object list length of a get request for a container'
nl|'\n'
DECL|variable|CONTAINER_LISTING_LIMIT
name|'CONTAINER_LISTING_LIMIT'
op|'='
name|'constraints_conf_int'
op|'('
string|"'container_listing_limit'"
op|','
nl|'\n'
number|'10000'
op|')'
newline|'\n'
comment|'#: Max container list length of a get request for an account'
nl|'\n'
DECL|variable|ACCOUNT_LISTING_LIMIT
name|'ACCOUNT_LISTING_LIMIT'
op|'='
name|'constraints_conf_int'
op|'('
string|"'account_listing_limit'"
op|','
number|'10000'
op|')'
newline|'\n'
comment|'#: Max account name length'
nl|'\n'
DECL|variable|MAX_ACCOUNT_NAME_LENGTH
name|'MAX_ACCOUNT_NAME_LENGTH'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_account_name_length'"
op|','
number|'256'
op|')'
newline|'\n'
comment|'#: Max container name length'
nl|'\n'
DECL|variable|MAX_CONTAINER_NAME_LENGTH
name|'MAX_CONTAINER_NAME_LENGTH'
op|'='
name|'constraints_conf_int'
op|'('
string|"'max_container_name_length'"
op|','
nl|'\n'
number|'256'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#: Query string format= values to their corresponding content-type values'
nl|'\n'
DECL|variable|FORMAT2CONTENT_TYPE
name|'FORMAT2CONTENT_TYPE'
op|'='
op|'{'
string|"'plain'"
op|':'
string|"'text/plain'"
op|','
string|"'json'"
op|':'
string|"'application/json'"
op|','
nl|'\n'
string|"'xml'"
op|':'
string|"'application/xml'"
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_metadata
name|'def'
name|'check_metadata'
op|'('
name|'req'
op|','
name|'target_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Check metadata sent in the request headers.\n\n    :param req: request object\n    :param target_type: str: one of: object, container, or account: indicates\n                        which type the target storage for the metadata is\n    :raises HTTPBadRequest: bad metadata\n    """'
newline|'\n'
name|'prefix'
op|'='
string|"'x-%s-meta-'"
op|'%'
name|'target_type'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'meta_count'
op|'='
number|'0'
newline|'\n'
name|'meta_size'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
name|'prefix'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'continue'
newline|'\n'
dedent|''
name|'key'
op|'='
name|'key'
op|'['
name|'len'
op|'('
name|'prefix'
op|')'
op|':'
op|']'
newline|'\n'
name|'if'
name|'not'
name|'key'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Metadata name cannot be empty'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'meta_count'
op|'+='
number|'1'
newline|'\n'
name|'meta_size'
op|'+='
name|'len'
op|'('
name|'key'
op|')'
op|'+'
name|'len'
op|'('
name|'value'
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'key'
op|')'
op|'>'
name|'MAX_META_NAME_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Metadata name too long; max %d'"
op|'%'
name|'MAX_META_NAME_LENGTH'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'len'
op|'('
name|'value'
op|')'
op|'>'
name|'MAX_META_VALUE_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Metadata value too long; max %d'"
op|'%'
name|'MAX_META_VALUE_LENGTH'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'meta_count'
op|'>'
name|'MAX_META_COUNT'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Too many metadata items; max %d'"
op|'%'
name|'MAX_META_COUNT'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'meta_size'
op|'>'
name|'MAX_META_OVERALL_SIZE'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Total metadata too large; max %d'"
nl|'\n'
op|'%'
name|'MAX_META_OVERALL_SIZE'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_object_creation
dedent|''
name|'def'
name|'check_object_creation'
op|'('
name|'req'
op|','
name|'object_name'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Check to ensure that everything is alright about an object to be created.\n\n    :param req: HTTP request object\n    :param object_name: name of object to be created\n    :raises HTTPRequestEntityTooLarge: the object is too large\n    :raises HTTPLengthRequered: missing content-length header and not\n                                a chunked request\n    :raises HTTPBadRequest: missing or bad content-type header, or\n                            bad metadata\n    """'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'content_length'
name|'and'
name|'req'
op|'.'
name|'content_length'
op|'>'
name|'MAX_FILE_SIZE'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPRequestEntityTooLarge'
op|'('
name|'body'
op|'='
string|"'Your request is too large.'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'content_length'
name|'is'
name|'None'
name|'and'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'transfer-encoding'"
op|')'
op|'!='
string|"'chunked'"
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPLengthRequired'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'X-Copy-From'"
name|'in'
name|'req'
op|'.'
name|'headers'
name|'and'
name|'req'
op|'.'
name|'content_length'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Copy requests require a zero byte body'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'object_name'
op|')'
op|'>'
name|'MAX_OBJECT_NAME_LENGTH'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Object name length of %d longer than %d'"
op|'%'
nl|'\n'
op|'('
name|'len'
op|'('
name|'object_name'
op|')'
op|','
name|'MAX_OBJECT_NAME_LENGTH'
op|')'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'Content-Type'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
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
string|"'No content type'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'Content-Type'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid Content-Type'"
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'x-object-manifest'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-object-manifest'"
op|']'
newline|'\n'
name|'container'
op|'='
name|'prefix'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'container'
op|','
name|'prefix'
op|'='
name|'value'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'1'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'container'
name|'or'
name|'not'
name|'prefix'
name|'or'
string|"'?'"
name|'in'
name|'value'
name|'or'
string|"'&'"
name|'in'
name|'value'
name|'or'
name|'prefix'
op|'['
number|'0'
op|']'
op|'=='
string|"'/'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'X-Object-Manifest must in the format container/prefix'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'check_metadata'
op|'('
name|'req'
op|','
string|"'object'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_mount
dedent|''
name|'def'
name|'check_mount'
op|'('
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Verify that the path to the device is a mount point and mounted.  This\n    allows us to fast fail on drives that have been unmounted because of\n    issues, and also prevents us for accidentally filling up the root\n    partition.\n\n    :param root:  base path where the devices are mounted\n    :param drive: drive name to be checked\n    :returns: True if it is a valid mounted device, False otherwise\n    """'
newline|'\n'
name|'if'
name|'not'
op|'('
name|'urllib'
op|'.'
name|'quote_plus'
op|'('
name|'drive'
op|')'
op|'=='
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'root'
op|','
name|'drive'
op|')'
newline|'\n'
name|'return'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'path'
op|')'
name|'and'
name|'os'
op|'.'
name|'path'
op|'.'
name|'ismount'
op|'('
name|'path'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_float
dedent|''
name|'def'
name|'check_float'
op|'('
name|'string'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function for checking if a string can be converted to a float.\n\n    :param string: string to be verified as a float\n    :returns: True if the string can be converted to a float, False otherwise\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'float'
op|'('
name|'string'
op|')'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_utf8
dedent|''
dedent|''
name|'def'
name|'check_utf8'
op|'('
name|'string'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Validate if a string is valid UTF-8 str or unicode and that it\n    does not contain any null character.\n\n    :param string: string to be validated\n    :returns: True if the string is valid utf-8 str or unicode and\n              contains no null characters, False otherwise\n    """'
newline|'\n'
name|'if'
name|'not'
name|'string'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'isinstance'
op|'('
name|'string'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'string'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'string'
op|'.'
name|'decode'
op|'('
string|"'UTF-8'"
op|')'
newline|'\n'
dedent|''
name|'return'
string|"'\\x00'"
name|'not'
name|'in'
name|'string'
newline|'\n'
comment|'# If string is unicode, decode() will raise UnicodeEncodeError'
nl|'\n'
comment|'# So, we should catch both UnicodeDecodeError & UnicodeEncodeError'
nl|'\n'
dedent|''
name|'except'
name|'UnicodeError'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
