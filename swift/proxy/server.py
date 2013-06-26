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
comment|'# NOTE: swift_conn'
nl|'\n'
comment|"# You'll see swift_conn passed around a few places in this file. This is the"
nl|'\n'
comment|'# source httplib connection of whatever it is attached to.'
nl|'\n'
comment|'#   It is used when early termination of reading from the connection should'
nl|'\n'
comment|"# happen, such as when a range request is satisfied but there's still more the"
nl|'\n'
comment|'# source connection would like to send. To prevent having to read all the data'
nl|'\n'
comment|'# that could be left, the source connection can be .close() and then reads'
nl|'\n'
comment|'# commence to empty out any buffers.'
nl|'\n'
comment|'#   These shenanigans are to ensure all related objects can be garbage'
nl|'\n'
comment|"# collected. We've seen objects hang around forever otherwise."
nl|'\n'
nl|'\n'
name|'import'
name|'mimetypes'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'ConfigParser'
name|'import'
name|'ConfigParser'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'shuffle'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'Ring'
newline|'\n'
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
op|','
name|'get_remote_client'
op|','
name|'split_path'
op|','
name|'config_true_value'
op|','
name|'generate_trans_id'
op|','
name|'affinity_key_function'
op|','
name|'affinity_locality_predicate'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_utf8'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
name|'import'
name|'AccountController'
op|','
name|'ObjectController'
op|','
name|'ContainerController'
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
name|'HTTPForbidden'
op|','
name|'HTTPMethodNotAllowed'
op|','
name|'HTTPNotFound'
op|','
name|'HTTPPreconditionFailed'
op|','
name|'HTTPServerError'
op|','
name|'Request'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Application
name|'class'
name|'Application'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""WSGI application for the proxy server."""'
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
name|'memcache'
op|'='
name|'None'
op|','
name|'logger'
op|'='
name|'None'
op|','
name|'account_ring'
op|'='
name|'None'
op|','
nl|'\n'
name|'container_ring'
op|'='
name|'None'
op|','
name|'object_ring'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'conf'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'conf'
op|'='
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'if'
name|'logger'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
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
string|"'proxy-server'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
nl|'\n'
dedent|''
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
name|'self'
op|'.'
name|'node_timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'node_timeout'"
op|','
number|'10'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn_timeout'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'conn_timeout'"
op|','
number|'0.5'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'client_timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'client_timeout'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'put_queue_depth'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'put_queue_depth'"
op|','
number|'10'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_chunk_size'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'object_chunk_size'"
op|','
number|'65536'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'client_chunk_size'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'client_chunk_size'"
op|','
number|'65536'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'trans_id_suffix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'trans_id_suffix'"
op|','
string|"''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'error_suppression_interval'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'error_suppression_interval'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'error_suppression_limit'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'error_suppression_limit'"
op|','
number|'10'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'recheck_container_existence'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'recheck_container_existence'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'recheck_account_existence'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'recheck_account_existence'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'allow_account_management'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_account_management'"
op|','
string|"'no'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_post_as_copy'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'object_post_as_copy'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'resellers_conf'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'resellers_conf'
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
string|"'resellers.conf'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_ring'
op|'='
name|'object_ring'
name|'or'
name|'Ring'
op|'('
name|'swift_dir'
op|','
name|'ring_name'
op|'='
string|"'object'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'container_ring'
name|'or'
name|'Ring'
op|'('
name|'swift_dir'
op|','
nl|'\n'
name|'ring_name'
op|'='
string|"'container'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'account_ring'
name|'or'
name|'Ring'
op|'('
name|'swift_dir'
op|','
nl|'\n'
name|'ring_name'
op|'='
string|"'account'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'memcache'
op|'='
name|'memcache'
newline|'\n'
name|'mimetypes'
op|'.'
name|'init'
op|'('
name|'mimetypes'
op|'.'
name|'knownfiles'
op|'+'
nl|'\n'
op|'['
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'mime.types'"
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_autocreate'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'account_autocreate'"
op|','
string|"'no'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'expiring_objects_account'
op|'='
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'auto_create_account_prefix'"
op|')'
name|'or'
string|"'.'"
op|')'
op|'+'
string|"'expiring_objects'"
newline|'\n'
name|'self'
op|'.'
name|'expiring_objects_container_divisor'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'expiring_objects_container_divisor'"
op|')'
name|'or'
number|'86400'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_containers_per_account'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_containers_per_account'"
op|')'
name|'or'
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_containers_whitelist'
op|'='
op|'['
nl|'\n'
name|'a'
op|'.'
name|'strip'
op|'('
op|')'
nl|'\n'
name|'for'
name|'a'
name|'in'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_containers_whitelist'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
nl|'\n'
name|'if'
name|'a'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'deny_host_headers'
op|'='
op|'['
nl|'\n'
name|'host'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'host'
name|'in'
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'deny_host_headers'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
name|'if'
name|'host'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
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
string|"'rate_limit_after_segment'"
op|','
number|'10'
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
string|"'rate_limit_segments_per_sec'"
op|','
number|'1'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_handoffs'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_handoffs'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'cors_allow_origin'
op|'='
op|'['
nl|'\n'
name|'a'
op|'.'
name|'strip'
op|'('
op|')'
nl|'\n'
name|'for'
name|'a'
name|'in'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'cors_allow_origin'"
op|','
string|"''"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
nl|'\n'
name|'if'
name|'a'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'node_timings'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'timing_expiry'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'timing_expiry'"
op|','
number|'300'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'sorting_method'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'sorting_method'"
op|','
string|"'shuffle'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'allow_static_large_object'
op|'='
name|'config_true_value'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_static_large_object'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_large_object_get_time'
op|'='
name|'float'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_large_object_get_time'"
op|','
string|"'86400'"
op|')'
op|')'
newline|'\n'
name|'value'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'request_node_count'"
op|','
string|"'2 * replicas'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'value'
op|')'
op|'=='
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'int'
op|'('
name|'value'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'request_node_count'
op|'='
name|'lambda'
name|'r'
op|':'
name|'value'
newline|'\n'
dedent|''
name|'elif'
name|'len'
op|'('
name|'value'
op|')'
op|'=='
number|'3'
name|'and'
name|'value'
op|'['
number|'1'
op|']'
op|'=='
string|"'*'"
name|'and'
name|'value'
op|'['
number|'2'
op|']'
op|'=='
string|"'replicas'"
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'int'
op|'('
name|'value'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'request_node_count'
op|'='
name|'lambda'
name|'r'
op|':'
name|'value'
op|'*'
name|'r'
op|'.'
name|'replica_count'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'Invalid request_node_count value: %r'"
op|'%'
string|"''"
op|'.'
name|'join'
op|'('
name|'value'
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'read_affinity'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'read_affinity'"
op|','
string|"''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'read_affinity_sort_key'
op|'='
name|'affinity_key_function'
op|'('
name|'read_affinity'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
comment|'# make the message a little more useful'
nl|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|'"Invalid read_affinity value: %r (%s)"'
op|'%'
nl|'\n'
op|'('
name|'read_affinity'
op|','
name|'err'
op|'.'
name|'message'
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'write_affinity'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'write_affinity'"
op|','
string|"''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'write_affinity_is_local_fn'
op|'='
name|'affinity_locality_predicate'
op|'('
name|'write_affinity'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
comment|'# make the message a little more useful'
nl|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|'"Invalid write_affinity value: %r (%s)"'
op|'%'
nl|'\n'
op|'('
name|'write_affinity'
op|','
name|'err'
op|'.'
name|'message'
op|')'
op|')'
newline|'\n'
dedent|''
name|'value'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'write_affinity_node_count'"
op|','
nl|'\n'
string|"'2 * replicas'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'value'
op|')'
op|'=='
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'int'
op|'('
name|'value'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'write_affinity_node_count'
op|'='
name|'lambda'
name|'r'
op|':'
name|'value'
newline|'\n'
dedent|''
name|'elif'
name|'len'
op|'('
name|'value'
op|')'
op|'=='
number|'3'
name|'and'
name|'value'
op|'['
number|'1'
op|']'
op|'=='
string|"'*'"
name|'and'
name|'value'
op|'['
number|'2'
op|']'
op|'=='
string|"'replicas'"
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'int'
op|'('
name|'value'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'write_affinity_node_count'
op|'='
name|'lambda'
name|'r'
op|':'
name|'value'
op|'*'
name|'r'
op|'.'
name|'replica_count'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'Invalid write_affinity_node_count value: %r'"
op|'%'
string|"''"
op|'.'
name|'join'
op|'('
name|'value'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_controller
dedent|''
dedent|''
name|'def'
name|'get_controller'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get the controller to handle a request.\n\n        :param path: path from request\n        :returns: tuple of (controller class, path dictionary)\n\n        :raises: ValueError (thrown by split_path) if given invalid path\n        """'
newline|'\n'
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'path'
op|','
number|'1'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
name|'d'
op|'='
name|'dict'
op|'('
name|'version'
op|'='
name|'version'
op|','
nl|'\n'
name|'account_name'
op|'='
name|'account'
op|','
nl|'\n'
name|'container_name'
op|'='
name|'container'
op|','
nl|'\n'
name|'object_name'
op|'='
name|'obj'
op|')'
newline|'\n'
name|'if'
name|'obj'
name|'and'
name|'container'
name|'and'
name|'account'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'ObjectController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'elif'
name|'container'
name|'and'
name|'account'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'ContainerController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'elif'
name|'account'
name|'and'
name|'not'
name|'container'
name|'and'
name|'not'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'AccountController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'return'
name|'None'
op|','
name|'d'
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
string|'"""\n        WSGI entry point.\n        Wraps env in swob.Request object and passes it down.\n\n        :param env: WSGI environment dictionary\n        :param start_response: WSGI callable\n        """'
newline|'\n'
name|'try'
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
name|'req'
op|'='
name|'self'
op|'.'
name|'update_request'
op|'('
name|'Request'
op|'('
name|'env'
op|')'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'handle_request'
op|'('
name|'req'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'UnicodeError'
op|':'
newline|'\n'
indent|'            '
name|'err'
op|'='
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid UTF8 or contains NULL'"
op|')'
newline|'\n'
name|'return'
name|'err'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
string|"'500 Server Error'"
op|','
nl|'\n'
op|'['
op|'('
string|"'Content-Type'"
op|','
string|"'text/plain'"
op|')'
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
string|"'Internal server error.\\n'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|update_request
dedent|''
dedent|''
name|'def'
name|'update_request'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
string|"'x-storage-token'"
name|'in'
name|'req'
op|'.'
name|'headers'
name|'and'
string|"'x-auth-token'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-auth-token'"
op|']'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-storage-token'"
op|']'
newline|'\n'
dedent|''
name|'return'
name|'req'
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
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Entry point for proxy server.\n        Should return a WSGI-style callable (such as swob.Response).\n\n        :param req: swob.Request object\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'set_statsd_prefix'
op|'('
string|"'proxy-server'"
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'content_length'
name|'and'
name|'req'
op|'.'
name|'content_length'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'Invalid Content-Length'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'req'
op|'.'
name|'path_info'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'return'
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid UTF8 or contains NULL'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'UnicodeError'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'return'
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid UTF8 or contains NULL'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'controller'
op|','
name|'path_parts'
op|'='
name|'self'
op|'.'
name|'get_controller'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
newline|'\n'
name|'p'
op|'='
name|'req'
op|'.'
name|'path_info'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'p'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'p'
op|'='
name|'p'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'controller'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'return'
name|'HTTPPreconditionFailed'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Bad URL'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'deny_host_headers'
name|'and'
name|'req'
op|'.'
name|'host'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
op|'['
number|'0'
op|']'
name|'in'
name|'self'
op|'.'
name|'deny_host_headers'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPForbidden'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid host header'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'set_statsd_prefix'
op|'('
string|"'proxy-server.'"
op|'+'
nl|'\n'
name|'controller'
op|'.'
name|'server_type'
op|'.'
name|'lower'
op|'('
op|')'
op|')'
newline|'\n'
name|'controller'
op|'='
name|'controller'
op|'('
name|'self'
op|','
op|'**'
name|'path_parts'
op|')'
newline|'\n'
name|'if'
string|"'swift.trans_id'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'environ'
op|':'
newline|'\n'
comment|"# if this wasn't set by an earlier middleware, set it now"
nl|'\n'
indent|'                '
name|'trans_id'
op|'='
name|'generate_trans_id'
op|'('
name|'self'
op|'.'
name|'trans_id_suffix'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.trans_id'"
op|']'
op|'='
name|'trans_id'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'txn_id'
op|'='
name|'trans_id'
newline|'\n'
dedent|''
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-trans-id'"
op|']'
op|'='
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.trans_id'"
op|']'
newline|'\n'
name|'controller'
op|'.'
name|'trans_id'
op|'='
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.trans_id'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'client_ip'
op|'='
name|'get_remote_client'
op|'('
name|'req'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'handler'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
name|'req'
op|'.'
name|'method'
op|')'
newline|'\n'
name|'getattr'
op|'('
name|'handler'
op|','
string|"'publicly_accessible'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'                '
name|'allowed_methods'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
string|"'allowed_methods'"
op|','
name|'set'
op|'('
op|')'
op|')'
newline|'\n'
name|'return'
name|'HTTPMethodNotAllowed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
op|'{'
string|"'Allow'"
op|':'
string|"', '"
op|'.'
name|'join'
op|'('
name|'allowed_methods'
op|')'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'path_parts'
op|'['
string|"'version'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'req'
op|'.'
name|'path_info_pop'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'swift.authorize'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|':'
newline|'\n'
comment|'# We call authorize before the handler, always. If authorized,'
nl|'\n'
comment|"# we remove the swift.authorize hook so isn't ever called"
nl|'\n'
comment|'# again. If not authorized, we return the denial unless the'
nl|'\n'
comment|"# controller's method indicates it'd like to gather more"
nl|'\n'
comment|'# information and try again later.'
nl|'\n'
indent|'                '
name|'resp'
op|'='
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
op|'('
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'resp'
op|':'
newline|'\n'
comment|'# No resp means authorized, no delayed recheck required.'
nl|'\n'
indent|'                    '
name|'del'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# Response indicates denial, but we might delay the denial'
nl|'\n'
comment|'# and recheck later. If not delayed, return the error now.'
nl|'\n'
indent|'                    '
name|'if'
name|'not'
name|'getattr'
op|'('
name|'handler'
op|','
string|"'delay_denial'"
op|','
name|'None'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'return'
name|'resp'
newline|'\n'
comment|'# Save off original request method (GET, POST, etc.) in case it'
nl|'\n'
comment|'# gets mutated during handling.  This way logging can display the'
nl|'\n'
comment|'# method the client actually sent.'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.orig_req_method'"
op|']'
op|'='
name|'req'
op|'.'
name|'method'
newline|'\n'
name|'return'
name|'handler'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR Unhandled exception in request'"
op|')'
op|')'
newline|'\n'
name|'return'
name|'HTTPServerError'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|sort_nodes
dedent|''
dedent|''
name|'def'
name|'sort_nodes'
op|'('
name|'self'
op|','
name|'nodes'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'\'\'\'\n        Sorts nodes in-place (and returns the sorted list) according to\n        the configured strategy. The default "sorting" is to randomly\n        shuffle the nodes. If the "timing" strategy is chosen, the nodes\n        are sorted according to the stored timing data.\n        \'\'\''
newline|'\n'
comment|'# In the case of timing sorting, shuffling ensures that close timings'
nl|'\n'
comment|"# (ie within the rounding resolution) won't prefer one over another."
nl|'\n'
comment|"# Python's sort is stable (http://wiki.python.org/moin/HowTo/Sorting/)"
nl|'\n'
name|'shuffle'
op|'('
name|'nodes'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'sorting_method'
op|'=='
string|"'timing'"
op|':'
newline|'\n'
indent|'            '
name|'now'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|function|key_func
name|'def'
name|'key_func'
op|'('
name|'node'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'timing'
op|','
name|'expires'
op|'='
name|'self'
op|'.'
name|'node_timings'
op|'.'
name|'get'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
op|'('
op|'-'
number|'1.0'
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'return'
name|'timing'
name|'if'
name|'expires'
op|'>'
name|'now'
name|'else'
op|'-'
number|'1.0'
newline|'\n'
dedent|''
name|'nodes'
op|'.'
name|'sort'
op|'('
name|'key'
op|'='
name|'key_func'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'sorting_method'
op|'=='
string|"'affinity'"
op|':'
newline|'\n'
indent|'            '
name|'nodes'
op|'.'
name|'sort'
op|'('
name|'key'
op|'='
name|'self'
op|'.'
name|'read_affinity_sort_key'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'nodes'
newline|'\n'
nl|'\n'
DECL|member|set_node_timing
dedent|''
name|'def'
name|'set_node_timing'
op|'('
name|'self'
op|','
name|'node'
op|','
name|'timing'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'sorting_method'
op|'!='
string|"'timing'"
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'now'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'timing'
op|'='
name|'round'
op|'('
name|'timing'
op|','
number|'3'
op|')'
comment|'# sort timings to the millisecond'
newline|'\n'
name|'self'
op|'.'
name|'node_timings'
op|'['
name|'node'
op|'['
string|"'ip'"
op|']'
op|']'
op|'='
op|'('
name|'timing'
op|','
name|'now'
op|'+'
name|'self'
op|'.'
name|'timing_expiry'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|app_factory
dedent|''
dedent|''
name|'def'
name|'app_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""paste.deploy app factory for creating WSGI proxy apps."""'
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
name|'return'
name|'Application'
op|'('
name|'conf'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
