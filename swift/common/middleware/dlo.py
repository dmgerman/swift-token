begin_unit
comment|'# Copyright (c) 2013 OpenStack Foundation'
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
nl|'\n'
name|'import'
name|'six'
newline|'\n'
name|'from'
name|'six'
op|'.'
name|'moves'
op|'.'
name|'configparser'
name|'import'
name|'ConfigParser'
op|','
name|'NoSectionError'
op|','
name|'NoOptionError'
newline|'\n'
name|'from'
name|'six'
op|'.'
name|'moves'
op|'.'
name|'urllib'
op|'.'
name|'parse'
name|'import'
name|'unquote'
newline|'\n'
nl|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'constraints'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'ListingIterError'
op|','
name|'SegmentError'
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
name|'swob'
name|'import'
name|'Request'
op|','
name|'Response'
op|','
name|'HTTPRequestedRangeNotSatisfiable'
op|','
name|'HTTPBadRequest'
op|','
name|'HTTPConflict'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'json'
op|','
name|'RateLimitedIterator'
op|','
name|'read_conf_dir'
op|','
name|'quote'
op|','
name|'close_if_possible'
op|','
name|'closing_if_possible'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'SegmentedIterable'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'WSGIContext'
op|','
name|'make_subrequest'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|GetContext
name|'class'
name|'GetContext'
op|'('
name|'WSGIContext'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'dlo'
op|','
name|'logger'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'GetContext'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'dlo'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'dlo'
op|'='
name|'dlo'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
nl|'\n'
DECL|member|_get_container_listing
dedent|''
name|'def'
name|'_get_container_listing'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
nl|'\n'
name|'prefix'
op|','
name|'marker'
op|'='
string|"''"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'con_req'
op|'='
name|'make_subrequest'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'path'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
string|"''"
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|']'
op|')'
op|','
nl|'\n'
name|'method'
op|'='
string|"'GET'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-auth-token'"
op|':'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-token'"
op|')'
op|'}'
op|','
nl|'\n'
name|'agent'
op|'='
op|'('
string|"'%(orig)s '"
op|'+'
string|"'DLO MultipartGET'"
op|')'
op|','
name|'swift_source'
op|'='
string|"'DLO'"
op|')'
newline|'\n'
name|'con_req'
op|'.'
name|'query_string'
op|'='
string|"'format=json&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'prefix'
op|')'
newline|'\n'
name|'if'
name|'marker'
op|':'
newline|'\n'
indent|'            '
name|'con_req'
op|'.'
name|'query_string'
op|'+='
string|"'&marker=%s'"
op|'%'
name|'quote'
op|'('
name|'marker'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'con_resp'
op|'='
name|'con_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'dlo'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_success'
op|'('
name|'con_resp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'con_resp'
op|','
name|'None'
newline|'\n'
dedent|''
name|'with'
name|'closing_if_possible'
op|'('
name|'con_resp'
op|'.'
name|'app_iter'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
op|','
name|'json'
op|'.'
name|'loads'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'con_resp'
op|'.'
name|'app_iter'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_segment_listing_iterator
dedent|''
dedent|''
name|'def'
name|'_segment_listing_iterator'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
nl|'\n'
name|'prefix'
op|','
name|'segments'
op|','
name|'first_byte'
op|'='
name|'None'
op|','
nl|'\n'
name|'last_byte'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
comment|"# It's sort of hokey that this thing takes in the first page of"
nl|'\n'
comment|'# segments as an argument, but we need to compute the etag and content'
nl|'\n'
comment|"# length from the first page, and it's better to have a hokey"
nl|'\n'
comment|'# interface than to make redundant requests.'
nl|'\n'
indent|'        '
name|'if'
name|'first_byte'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'first_byte'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'last_byte'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'last_byte'
op|'='
name|'float'
op|'('
string|'"inf"'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'marker'
op|'='
string|"''"
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'segment'
name|'in'
name|'segments'
op|':'
newline|'\n'
indent|'                '
name|'seg_length'
op|'='
name|'int'
op|'('
name|'segment'
op|'['
string|"'bytes'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'first_byte'
op|'>='
name|'seg_length'
op|':'
newline|'\n'
comment|"# don't need any bytes from this segment"
nl|'\n'
indent|'                    '
name|'first_byte'
op|'='
name|'max'
op|'('
name|'first_byte'
op|'-'
name|'seg_length'
op|','
op|'-'
number|'1'
op|')'
newline|'\n'
name|'last_byte'
op|'='
name|'max'
op|'('
name|'last_byte'
op|'-'
name|'seg_length'
op|','
op|'-'
number|'1'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'elif'
name|'last_byte'
op|'<'
number|'0'
op|':'
newline|'\n'
comment|'# no bytes are needed from this or any future segment'
nl|'\n'
indent|'                    '
name|'break'
newline|'\n'
nl|'\n'
dedent|''
name|'seg_name'
op|'='
name|'segment'
op|'['
string|"'name'"
op|']'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'seg_name'
op|','
name|'six'
op|'.'
name|'text_type'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'seg_name'
op|'='
name|'seg_name'
op|'.'
name|'encode'
op|'('
string|'"utf-8"'
op|')'
newline|'\n'
nl|'\n'
comment|'# (obj path, etag, size, first byte, last byte)'
nl|'\n'
dedent|''
name|'yield'
op|'('
string|'"/"'
op|'+'
string|'"/"'
op|'.'
name|'join'
op|'('
op|'('
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
nl|'\n'
name|'seg_name'
op|')'
op|')'
op|','
nl|'\n'
comment|'# We deliberately omit the etag and size here;'
nl|'\n'
comment|'# SegmentedIterable will check size and etag if'
nl|'\n'
comment|"# specified, but we don't want it to. DLOs only care"
nl|'\n'
comment|"# that the objects' names match the specified prefix."
nl|'\n'
name|'None'
op|','
name|'None'
op|','
nl|'\n'
op|'('
name|'None'
name|'if'
name|'first_byte'
op|'<='
number|'0'
name|'else'
name|'first_byte'
op|')'
op|','
nl|'\n'
op|'('
name|'None'
name|'if'
name|'last_byte'
op|'>='
name|'seg_length'
op|'-'
number|'1'
name|'else'
name|'last_byte'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'first_byte'
op|'='
name|'max'
op|'('
name|'first_byte'
op|'-'
name|'seg_length'
op|','
op|'-'
number|'1'
op|')'
newline|'\n'
name|'last_byte'
op|'='
name|'max'
op|'('
name|'last_byte'
op|'-'
name|'seg_length'
op|','
op|'-'
number|'1'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'segments'
op|')'
op|'<'
name|'constraints'
op|'.'
name|'CONTAINER_LISTING_LIMIT'
op|':'
newline|'\n'
comment|"# a short page means that we're done with the listing"
nl|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'elif'
name|'last_byte'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
nl|'\n'
dedent|''
name|'marker'
op|'='
name|'segments'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'name'"
op|']'
newline|'\n'
name|'error_response'
op|','
name|'segments'
op|'='
name|'self'
op|'.'
name|'_get_container_listing'
op|'('
nl|'\n'
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'prefix'
op|','
name|'marker'
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
comment|"# we've already started sending the response body to the"
nl|'\n'
comment|'# client, so all we can do is raise an exception to make the'
nl|'\n'
comment|'# WSGI server close the connection early'
nl|'\n'
indent|'                '
name|'close_if_possible'
op|'('
name|'error_response'
op|'.'
name|'app_iter'
op|')'
newline|'\n'
name|'raise'
name|'ListingIterError'
op|'('
nl|'\n'
string|'"Got status %d listing container /%s/%s"'
op|'%'
nl|'\n'
op|'('
name|'error_response'
op|'.'
name|'status_int'
op|','
name|'account'
op|','
name|'container'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_or_head_response
dedent|''
dedent|''
dedent|''
name|'def'
name|'get_or_head_response'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'x_object_manifest'
op|','
nl|'\n'
name|'response_headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'response_headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'response_headers'
op|'='
name|'self'
op|'.'
name|'_response_headers'
newline|'\n'
nl|'\n'
dedent|''
name|'container'
op|','
name|'obj_prefix'
op|'='
name|'x_object_manifest'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'1'
op|')'
newline|'\n'
name|'container'
op|'='
name|'unquote'
op|'('
name|'container'
op|')'
newline|'\n'
name|'obj_prefix'
op|'='
name|'unquote'
op|'('
name|'obj_prefix'
op|')'
newline|'\n'
nl|'\n'
comment|'# manifest might point to a different container'
nl|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
name|'None'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'_junk'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'2'
op|','
number|'3'
op|','
name|'True'
op|')'
newline|'\n'
name|'error_response'
op|','
name|'segments'
op|'='
name|'self'
op|'.'
name|'_get_container_listing'
op|'('
nl|'\n'
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj_prefix'
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'error_response'
newline|'\n'
dedent|''
name|'have_complete_listing'
op|'='
name|'len'
op|'('
name|'segments'
op|')'
op|'<'
name|'constraints'
op|'.'
name|'CONTAINER_LISTING_LIMIT'
newline|'\n'
nl|'\n'
name|'first_byte'
op|'='
name|'last_byte'
op|'='
name|'None'
newline|'\n'
name|'actual_content_length'
op|'='
name|'None'
newline|'\n'
name|'content_length_for_swob_range'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'range'
name|'and'
name|'len'
op|'('
name|'req'
op|'.'
name|'range'
op|'.'
name|'ranges'
op|')'
op|'=='
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'content_length_for_swob_range'
op|'='
name|'sum'
op|'('
name|'o'
op|'['
string|"'bytes'"
op|']'
name|'for'
name|'o'
name|'in'
name|'segments'
op|')'
newline|'\n'
nl|'\n'
comment|'# This is a hack to handle suffix byte ranges (e.g. "bytes=-5"),'
nl|'\n'
comment|"# which we can't honor unless we have a complete listing."
nl|'\n'
name|'_junk'
op|','
name|'range_end'
op|'='
name|'req'
op|'.'
name|'range'
op|'.'
name|'ranges_for_length'
op|'('
name|'float'
op|'('
string|'"inf"'
op|')'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
nl|'\n'
comment|'# If this is all the segments, we know whether or not this'
nl|'\n'
comment|'# range request is satisfiable.'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Alternately, we may not have all the segments, but this range'
nl|'\n'
comment|"# falls entirely within the first page's segments, so we know"
nl|'\n'
comment|'# that it is satisfiable.'
nl|'\n'
name|'if'
op|'('
name|'have_complete_listing'
nl|'\n'
name|'or'
name|'range_end'
op|'<'
name|'content_length_for_swob_range'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'byteranges'
op|'='
name|'req'
op|'.'
name|'range'
op|'.'
name|'ranges_for_length'
op|'('
nl|'\n'
name|'content_length_for_swob_range'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'byteranges'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'HTTPRequestedRangeNotSatisfiable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'first_byte'
op|','
name|'last_byte'
op|'='
name|'byteranges'
op|'['
number|'0'
op|']'
newline|'\n'
comment|'# For some reason, swob.Range.ranges_for_length adds 1 to the'
nl|'\n'
comment|"# last byte's position."
nl|'\n'
name|'last_byte'
op|'-='
number|'1'
newline|'\n'
name|'actual_content_length'
op|'='
name|'last_byte'
op|'-'
name|'first_byte'
op|'+'
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|"# The range may or may not be satisfiable, but we can't tell"
nl|'\n'
comment|"# based on just one page of listing, and we're not going to go"
nl|'\n'
comment|'# get more pages because that would use up too many resources,'
nl|'\n'
comment|'# so we ignore the Range header and return the whole object.'
nl|'\n'
indent|'                '
name|'actual_content_length'
op|'='
name|'None'
newline|'\n'
name|'content_length_for_swob_range'
op|'='
name|'None'
newline|'\n'
name|'req'
op|'.'
name|'range'
op|'='
name|'None'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'response_headers'
op|'='
op|'['
nl|'\n'
op|'('
name|'h'
op|','
name|'v'
op|')'
name|'for'
name|'h'
op|','
name|'v'
name|'in'
name|'response_headers'
nl|'\n'
name|'if'
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
name|'not'
name|'in'
op|'('
string|'"content-length"'
op|','
string|'"content-range"'
op|')'
op|']'
newline|'\n'
nl|'\n'
name|'if'
name|'content_length_for_swob_range'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
comment|'# Here, we have to give swob a big-enough content length so that'
nl|'\n'
comment|'# it can compute the actual content length based on the Range'
nl|'\n'
comment|'# header. This value will not be visible to the client; swob will'
nl|'\n'
comment|'# substitute its own Content-Length.'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Note: if the manifest points to at least CONTAINER_LISTING_LIMIT'
nl|'\n'
comment|"# segments, this may be less than the sum of all the segments'"
nl|'\n'
comment|"# sizes. However, it'll still be greater than the last byte in the"
nl|'\n'
comment|"# Range header, so it's good enough for swob."
nl|'\n'
indent|'            '
name|'response_headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'Content-Length'"
op|','
nl|'\n'
name|'str'
op|'('
name|'content_length_for_swob_range'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'have_complete_listing'
op|':'
newline|'\n'
indent|'            '
name|'actual_content_length'
op|'='
name|'sum'
op|'('
name|'o'
op|'['
string|"'bytes'"
op|']'
name|'for'
name|'o'
name|'in'
name|'segments'
op|')'
newline|'\n'
name|'response_headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'Content-Length'"
op|','
nl|'\n'
name|'str'
op|'('
name|'actual_content_length'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'have_complete_listing'
op|':'
newline|'\n'
indent|'            '
name|'response_headers'
op|'='
op|'['
op|'('
name|'h'
op|','
name|'v'
op|')'
name|'for'
name|'h'
op|','
name|'v'
name|'in'
name|'response_headers'
nl|'\n'
name|'if'
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
op|'!='
string|'"etag"'
op|']'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'seg_dict'
name|'in'
name|'segments'
op|':'
newline|'\n'
indent|'                '
name|'etag'
op|'.'
name|'update'
op|'('
name|'seg_dict'
op|'['
string|"'hash'"
op|']'
op|'.'
name|'strip'
op|'('
string|'\'"\''
op|')'
op|')'
newline|'\n'
dedent|''
name|'response_headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'Etag'"
op|','
string|'\'"%s"\''
op|'%'
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'app_iter'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'GET'"
op|':'
newline|'\n'
indent|'            '
name|'listing_iter'
op|'='
name|'RateLimitedIterator'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_segment_listing_iterator'
op|'('
nl|'\n'
name|'req'
op|','
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj_prefix'
op|','
name|'segments'
op|','
nl|'\n'
name|'first_byte'
op|'='
name|'first_byte'
op|','
name|'last_byte'
op|'='
name|'last_byte'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'dlo'
op|'.'
name|'rate_limit_segments_per_sec'
op|','
nl|'\n'
name|'limit_after'
op|'='
name|'self'
op|'.'
name|'dlo'
op|'.'
name|'rate_limit_after_segment'
op|')'
newline|'\n'
nl|'\n'
name|'app_iter'
op|'='
name|'SegmentedIterable'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'dlo'
op|'.'
name|'app'
op|','
name|'listing_iter'
op|','
name|'ua_suffix'
op|'='
string|'"DLO MultipartGET"'
op|','
nl|'\n'
name|'swift_source'
op|'='
string|'"DLO"'
op|','
name|'name'
op|'='
name|'req'
op|'.'
name|'path'
op|','
name|'logger'
op|'='
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'max_get_time'
op|'='
name|'self'
op|'.'
name|'dlo'
op|'.'
name|'max_get_time'
op|','
nl|'\n'
name|'response_body_length'
op|'='
name|'actual_content_length'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'app_iter'
op|'.'
name|'validate_first_segment'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'SegmentError'
op|','
name|'ListingIterError'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPConflict'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'response_headers'
op|','
nl|'\n'
name|'conditional_response'
op|'='
name|'True'
op|','
nl|'\n'
name|'app_iter'
op|'='
name|'app_iter'
op|')'
newline|'\n'
nl|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|handle_request
dedent|''
name|'def'
name|'handle_request'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Take a GET or HEAD request, and if it is for a dynamic large object\n        manifest, return an appropriate response.\n\n        Otherwise, simply pass it through.\n        """'
newline|'\n'
name|'resp_iter'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'req'
op|'.'
name|'environ'
op|')'
newline|'\n'
nl|'\n'
comment|'# make sure this response is for a dynamic large object manifest'
nl|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'self'
op|'.'
name|'_response_headers'
op|':'
newline|'\n'
indent|'            '
name|'if'
op|'('
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'x-object-manifest'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'close_if_possible'
op|'('
name|'resp_iter'
op|')'
newline|'\n'
name|'response'
op|'='
name|'self'
op|'.'
name|'get_or_head_response'
op|'('
name|'req'
op|','
name|'value'
op|')'
newline|'\n'
name|'return'
name|'response'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# Not a dynamic large object manifest; just pass it through.'
nl|'\n'
indent|'            '
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_headers'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|')'
newline|'\n'
name|'return'
name|'resp_iter'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DynamicLargeObject
dedent|''
dedent|''
dedent|''
name|'class'
name|'DynamicLargeObject'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
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
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'dlo'"
op|')'
newline|'\n'
nl|'\n'
comment|'# DLO functionality used to live in the proxy server, not middleware,'
nl|'\n'
comment|"# so let's try to go find config values in the proxy's config section"
nl|'\n'
comment|'# to ease cluster upgrades.'
nl|'\n'
name|'self'
op|'.'
name|'_populate_config_from_old_location'
op|'('
name|'conf'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'max_get_time'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_get_time'"
op|','
string|"'86400'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'rate_limit_after_segment'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'rate_limit_after_segment'"
op|','
string|"'10'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'rate_limit_segments_per_sec'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'rate_limit_segments_per_sec'"
op|','
string|"'1'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_populate_config_from_old_location
dedent|''
name|'def'
name|'_populate_config_from_old_location'
op|'('
name|'self'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
op|'('
string|"'rate_limit_after_segment'"
name|'in'
name|'conf'
name|'or'
nl|'\n'
string|"'rate_limit_segments_per_sec'"
name|'in'
name|'conf'
name|'or'
nl|'\n'
string|"'max_get_time'"
name|'in'
name|'conf'
name|'or'
nl|'\n'
string|"'__file__'"
name|'not'
name|'in'
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'cp'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'conf'
op|'['
string|"'__file__'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'read_conf_dir'
op|'('
name|'cp'
op|','
name|'conf'
op|'['
string|"'__file__'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'cp'
op|'.'
name|'read'
op|'('
name|'conf'
op|'['
string|"'__file__'"
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'pipe'
op|'='
name|'cp'
op|'.'
name|'get'
op|'('
string|'"pipeline:main"'
op|','
string|'"pipeline"'
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
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'proxy_name'
op|'='
name|'pipe'
op|'.'
name|'rsplit'
op|'('
name|'None'
op|','
number|'1'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'proxy_section'
op|'='
string|'"app:"'
op|'+'
name|'proxy_name'
newline|'\n'
name|'for'
name|'setting'
name|'in'
op|'('
string|"'rate_limit_after_segment'"
op|','
nl|'\n'
string|"'rate_limit_segments_per_sec'"
op|','
nl|'\n'
string|"'max_get_time'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conf'
op|'['
name|'setting'
op|']'
op|'='
name|'cp'
op|'.'
name|'get'
op|'('
name|'proxy_section'
op|','
name|'setting'
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
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
dedent|''
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
string|'"""\n        WSGI entry point\n        """'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'vrs'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'4'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
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
nl|'\n'
comment|'# install our COPY-callback hook'
nl|'\n'
dedent|''
name|'env'
op|'['
string|"'swift.copy_hook'"
op|']'
op|'='
name|'self'
op|'.'
name|'copy_hook'
op|'('
nl|'\n'
name|'env'
op|'.'
name|'get'
op|'('
string|"'swift.copy_hook'"
op|','
nl|'\n'
name|'lambda'
name|'src_req'
op|','
name|'src_resp'
op|','
name|'sink_req'
op|':'
name|'src_resp'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'if'
op|'('
op|'('
name|'req'
op|'.'
name|'method'
op|'=='
string|"'GET'"
name|'or'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'HEAD'"
op|')'
name|'and'
nl|'\n'
name|'req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
string|"'multipart-manifest'"
op|')'
op|'!='
string|"'get'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'GetContext'
op|'('
name|'self'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
op|'.'
name|'handle_request'
op|'('
name|'req'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'PUT'"
op|':'
newline|'\n'
indent|'            '
name|'error_response'
op|'='
name|'self'
op|'.'
name|'validate_x_object_manifest_header'
op|'('
nl|'\n'
name|'req'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'error_response'
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
DECL|member|validate_x_object_manifest_header
dedent|''
name|'def'
name|'validate_x_object_manifest_header'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Make sure that X-Object-Manifest is valid if present.\n        """'
newline|'\n'
name|'if'
string|"'X-Object-Manifest'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'X-Object-Manifest'"
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
indent|'                '
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
indent|'                '
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
indent|'                '
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
op|'('
string|"'X-Object-Manifest must be in the '"
nl|'\n'
string|"'format container/prefix'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|copy_hook
dedent|''
dedent|''
dedent|''
name|'def'
name|'copy_hook'
op|'('
name|'self'
op|','
name|'inner_hook'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|dlo_copy_hook
indent|'        '
name|'def'
name|'dlo_copy_hook'
op|'('
name|'source_req'
op|','
name|'source_resp'
op|','
name|'sink_req'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'x_o_m'
op|'='
name|'source_resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Object-Manifest'"
op|')'
newline|'\n'
name|'if'
name|'x_o_m'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'source_req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
string|"'multipart-manifest'"
op|')'
op|'=='
string|"'get'"
op|':'
newline|'\n'
comment|'# To copy the manifest, we let the copy proceed as normal,'
nl|'\n'
comment|'# but ensure that X-Object-Manifest is set on the new'
nl|'\n'
comment|'# object.'
nl|'\n'
indent|'                    '
name|'sink_req'
op|'.'
name|'headers'
op|'['
string|"'X-Object-Manifest'"
op|']'
op|'='
name|'x_o_m'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'ctx'
op|'='
name|'GetContext'
op|'('
name|'self'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'source_resp'
op|'='
name|'ctx'
op|'.'
name|'get_or_head_response'
op|'('
nl|'\n'
name|'source_req'
op|','
name|'x_o_m'
op|','
name|'source_resp'
op|'.'
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'inner_hook'
op|'('
name|'source_req'
op|','
name|'source_resp'
op|','
name|'sink_req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'dlo_copy_hook'
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
DECL|function|dlo_filter
name|'def'
name|'dlo_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'DynamicLargeObject'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'dlo_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
