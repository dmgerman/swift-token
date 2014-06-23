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
name|'urllib'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'import'
name|'eventlet'
op|'.'
name|'wsgi'
newline|'\n'
name|'import'
name|'eventlet'
op|'.'
name|'greenio'
newline|'\n'
nl|'\n'
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
name|'import'
name|'exceptions'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'http'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'swob'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Receiver
name|'class'
name|'Receiver'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Handles incoming REPLICATION requests to the object server.\n\n    These requests come from the object-replicator daemon that uses\n    :py:mod:`.ssync_sender`.\n\n    The number of concurrent REPLICATION requests is restricted by\n    use of a replication_semaphore and can be configured with the\n    object-server.conf [object-server] replication_concurrency\n    setting.\n\n    A REPLICATION request is really just an HTTP conduit for\n    sender/receiver replication communication. The overall\n    REPLICATION request should always succeed, but it will contain\n    multiple requests within its request and response bodies. This\n    "hack" is done so that replication concurrency can be managed.\n\n    The general process inside a REPLICATION request is:\n\n        1. Initialize the request: Basic request validation, mount check,\n           acquire semaphore lock, etc..\n\n        2. Missing check: Sender sends the hashes and timestamps of\n           the object information it can send, receiver sends back\n           the hashes it wants (doesn\'t have or has an older\n           timestamp).\n\n        3. Updates: Sender sends the object information requested.\n\n        4. Close down: Release semaphore lock, etc.\n    """'
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
name|'request'
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
name|'request'
op|'='
name|'request'
newline|'\n'
name|'self'
op|'.'
name|'device'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'partition'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'fp'
op|'='
name|'None'
newline|'\n'
comment|'# We default to dropping the connection in case there is any exception'
nl|'\n'
comment|'# raised during processing because otherwise the sender could send for'
nl|'\n'
comment|'# quite some time before realizing it was all in vain.'
nl|'\n'
name|'self'
op|'.'
name|'disconnect'
op|'='
name|'True'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Processes a REPLICATION request.\n\n        Acquires a semaphore lock and then proceeds through the steps\n        of the REPLICATION process.\n        """'
newline|'\n'
comment|'# The general theme for functions __call__ calls is that they should'
nl|'\n'
comment|'# raise exceptions.MessageTimeout for client timeouts (logged locally),'
nl|'\n'
comment|'# swob.HTTPException classes for exceptions to return to the caller but'
nl|'\n'
comment|'# not log locally (unmounted, for example), and any other Exceptions'
nl|'\n'
comment|'# will be logged with a full stack trace.'
nl|'\n'
comment|'#       This is because the client is never just some random user but'
nl|'\n'
comment|'# is instead also our code and we definitely want to know if our code'
nl|'\n'
comment|'# is broken or doing something unexpected.'
nl|'\n'
name|'try'
op|':'
newline|'\n'
comment|'# Double try blocks in case our main error handlers fail.'
nl|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
comment|'# intialize_request is for preamble items that can be done'
nl|'\n'
comment|'# outside a replication semaphore lock.'
nl|'\n'
indent|'                '
name|'for'
name|'data'
name|'in'
name|'self'
op|'.'
name|'initialize_request'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'yield'
name|'data'
newline|'\n'
comment|'# If semaphore is in use, try to acquire it, non-blocking, and'
nl|'\n'
comment|'# return a 503 if it fails.'
nl|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'replication_semaphore'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'not'
name|'self'
op|'.'
name|'app'
op|'.'
name|'replication_semaphore'
op|'.'
name|'acquire'
op|'('
name|'False'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
name|'swob'
op|'.'
name|'HTTPServiceUnavailable'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'with'
name|'self'
op|'.'
name|'app'
op|'.'
name|'_diskfile_mgr'
op|'.'
name|'replication_lock'
op|'('
name|'self'
op|'.'
name|'device'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'for'
name|'data'
name|'in'
name|'self'
op|'.'
name|'missing_check'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'yield'
name|'data'
newline|'\n'
dedent|''
name|'for'
name|'data'
name|'in'
name|'self'
op|'.'
name|'updates'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'yield'
name|'data'
newline|'\n'
comment|"# We didn't raise an exception, so end the request"
nl|'\n'
comment|'# normally.'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'disconnect'
op|'='
name|'False'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'replication_semaphore'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'app'
op|'.'
name|'replication_semaphore'
op|'.'
name|'release'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'ReplicationLockTimeout'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'app'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
string|"'%s/%s/%s REPLICATION LOCK TIMEOUT: %s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'request'
op|'.'
name|'remote_addr'
op|','
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|','
nl|'\n'
name|'err'
op|')'
op|')'
newline|'\n'
name|'yield'
string|"':ERROR: %d %r\\n'"
op|'%'
op|'('
number|'0'
op|','
name|'str'
op|'('
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'MessageTimeout'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'app'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
nl|'\n'
string|"'%s/%s/%s TIMEOUT in replication.Receiver: %s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'request'
op|'.'
name|'remote_addr'
op|','
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|','
nl|'\n'
name|'err'
op|')'
op|')'
newline|'\n'
name|'yield'
string|"':ERROR: %d %r\\n'"
op|'%'
op|'('
number|'408'
op|','
name|'str'
op|'('
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'swob'
op|'.'
name|'HTTPException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'body'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'err'
op|'('
op|'{'
op|'}'
op|','
name|'lambda'
op|'*'
name|'args'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'yield'
string|"':ERROR: %d %r\\n'"
op|'%'
op|'('
name|'err'
op|'.'
name|'status_int'
op|','
name|'body'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'app'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
string|"'%s/%s/%s EXCEPTION in replication.Receiver'"
op|'%'
nl|'\n'
op|'('
name|'self'
op|'.'
name|'request'
op|'.'
name|'remote_addr'
op|','
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|')'
op|')'
newline|'\n'
name|'yield'
string|"':ERROR: %d %r\\n'"
op|'%'
op|'('
number|'0'
op|','
name|'str'
op|'('
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'app'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'EXCEPTION in replication.Receiver'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'disconnect'
op|':'
newline|'\n'
comment|"# This makes the socket close early so the remote side doesn't have"
nl|'\n'
comment|'# to send its whole request while the lower Eventlet-level just'
nl|'\n'
comment|'# reads it and throws it away. Instead, the connection is dropped'
nl|'\n'
comment|'# and the remote side will get a broken-pipe exception.'
nl|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'socket'
op|'='
name|'self'
op|'.'
name|'request'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'get_socket'
op|'('
op|')'
newline|'\n'
name|'eventlet'
op|'.'
name|'greenio'
op|'.'
name|'shutdown_safe'
op|'('
name|'socket'
op|')'
newline|'\n'
name|'socket'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                '
name|'pass'
comment|"# We're okay with the above failing."
newline|'\n'
nl|'\n'
DECL|member|_ensure_flush
dedent|''
dedent|''
dedent|''
name|'def'
name|'_ensure_flush'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sends a blank line sufficient to flush buffers.\n\n        This is to ensure Eventlet versions that don\'t support\n        eventlet.minimum_write_chunk_size will send any previous data\n        buffered.\n\n        If https://bitbucket.org/eventlet/eventlet/pull-request/37\n        ever gets released in an Eventlet version, we should make\n        this yield only for versions older than that.\n        """'
newline|'\n'
name|'yield'
string|"' '"
op|'*'
name|'eventlet'
op|'.'
name|'wsgi'
op|'.'
name|'MINIMUM_CHUNK_SIZE'
op|'+'
string|"'\\r\\n'"
newline|'\n'
nl|'\n'
DECL|member|initialize_request
dedent|''
name|'def'
name|'initialize_request'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Basic validation of request and mount check.\n\n        This function will be called before attempting to acquire a\n        replication semaphore lock, so contains only quick checks.\n        """'
newline|'\n'
comment|'# The following is the setting we talk about above in _ensure_flush.'
nl|'\n'
name|'self'
op|'.'
name|'request'
op|'.'
name|'environ'
op|'['
string|"'eventlet.minimum_write_chunk_size'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|'='
name|'utils'
op|'.'
name|'split_path'
op|'('
nl|'\n'
name|'urllib'
op|'.'
name|'unquote'
op|'('
name|'self'
op|'.'
name|'request'
op|'.'
name|'path'
op|')'
op|','
number|'2'
op|','
number|'2'
op|','
name|'False'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'policy_idx'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Backend-Storage-Policy-Index'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'validate_device_partition'
op|'('
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'app'
op|'.'
name|'_diskfile_mgr'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'constraints'
op|'.'
name|'check_mount'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'_diskfile_mgr'
op|'.'
name|'devices'
op|','
name|'self'
op|'.'
name|'device'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'swob'
op|'.'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'self'
op|'.'
name|'device'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'fp'
op|'='
name|'self'
op|'.'
name|'request'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
newline|'\n'
name|'for'
name|'data'
name|'in'
name|'self'
op|'.'
name|'_ensure_flush'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'yield'
name|'data'
newline|'\n'
nl|'\n'
DECL|member|missing_check
dedent|''
dedent|''
name|'def'
name|'missing_check'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles the receiver-side of the MISSING_CHECK step of a\n        REPLICATION request.\n\n        Receives a list of hashes and timestamps of object\n        information the sender can provide and responds with a list\n        of hashes desired, either because they\'re missing or have an\n        older timestamp locally.\n\n        The process is generally:\n\n            1. Sender sends `:MISSING_CHECK: START` and begins\n               sending `hash timestamp` lines.\n\n            2. Receiver gets `:MISSING_CHECK: START` and begins\n               reading the `hash timestamp` lines, collecting the\n               hashes of those it desires.\n\n            3. Sender sends `:MISSING_CHECK: END`.\n\n            4. Receiver gets `:MISSING_CHECK: END`, responds with\n               `:MISSING_CHECK: START`, followed by the list of\n               hashes it collected as being wanted (one per line),\n               `:MISSING_CHECK: END`, and flushes any buffers.\n\n            5. Sender gets `:MISSING_CHECK: START` and reads the list\n               of hashes desired by the receiver until reading\n               `:MISSING_CHECK: END`.\n\n        The collection and then response is so the sender doesn\'t\n        have to read while it writes to ensure network buffers don\'t\n        fill up and block everything.\n        """'
newline|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'client_timeout'
op|','
string|"'missing_check start'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'line'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'network_chunk_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|'!='
string|"':MISSING_CHECK: START'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Looking for :MISSING_CHECK: START got %r'"
op|'%'
name|'line'
op|'['
op|':'
number|'1024'
op|']'
op|')'
newline|'\n'
dedent|''
name|'object_hashes'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'client_timeout'
op|','
string|"'missing_check line'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'network_chunk_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
name|'or'
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|'=='
string|"':MISSING_CHECK: END'"
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'object_hash'
op|','
name|'timestamp'
op|'='
op|'['
name|'urllib'
op|'.'
name|'unquote'
op|'('
name|'v'
op|')'
name|'for'
name|'v'
name|'in'
name|'line'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
name|'want'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'df'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'_diskfile_mgr'
op|'.'
name|'get_diskfile_from_hash'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|','
name|'object_hash'
op|','
name|'self'
op|'.'
name|'policy_idx'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'DiskFileNotExist'
op|':'
newline|'\n'
indent|'                '
name|'want'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'df'
op|'.'
name|'open'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'DiskFileDeleted'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'want'
op|'='
name|'err'
op|'.'
name|'timestamp'
op|'<'
name|'timestamp'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'DiskFileError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'want'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'want'
op|'='
name|'df'
op|'.'
name|'timestamp'
op|'<'
name|'timestamp'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'want'
op|':'
newline|'\n'
indent|'                '
name|'object_hashes'
op|'.'
name|'append'
op|'('
name|'object_hash'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'yield'
string|"':MISSING_CHECK: START\\r\\n'"
newline|'\n'
name|'yield'
string|"'\\r\\n'"
op|'.'
name|'join'
op|'('
name|'object_hashes'
op|')'
newline|'\n'
name|'yield'
string|"'\\r\\n'"
newline|'\n'
name|'yield'
string|"':MISSING_CHECK: END\\r\\n'"
newline|'\n'
name|'for'
name|'data'
name|'in'
name|'self'
op|'.'
name|'_ensure_flush'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'yield'
name|'data'
newline|'\n'
nl|'\n'
DECL|member|updates
dedent|''
dedent|''
name|'def'
name|'updates'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles the UPDATES step of a REPLICATION request.\n\n        Receives a set of PUT and DELETE subrequests that will be\n        routed to the object server itself for processing. These\n        contain the information requested by the MISSING_CHECK step.\n\n        The PUT and DELETE subrequests are formatted pretty much\n        exactly like regular HTTP requests, excepting the HTTP\n        version on the first request line.\n\n        The process is generally:\n\n            1. Sender sends `:UPDATES: START` and begins sending the\n               PUT and DELETE subrequests.\n\n            2. Receiver gets `:UPDATES: START` and begins routing the\n               subrequests to the object server.\n\n            3. Sender sends `:UPDATES: END`.\n\n            4. Receiver gets `:UPDATES: END` and sends `:UPDATES:\n               START` and `:UPDATES: END` (assuming no errors).\n\n            5. Sender gets `:UPDATES: START` and `:UPDATES: END`.\n\n        If too many subrequests fail, as configured by\n        replication_failure_threshold and replication_failure_ratio,\n        the receiver will hang up the request early so as to not\n        waste any more time.\n\n        At step 4, the receiver will send back an error if there were\n        any failures (that didn\'t cause a hangup due to the above\n        thresholds) so the sender knows the whole was not entirely a\n        success. This is so the sender knows if it can remove an out\n        of place partition, for example.\n        """'
newline|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'client_timeout'
op|','
string|"'updates start'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'line'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'network_chunk_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|'!='
string|"':UPDATES: START'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Looking for :UPDATES: START got %r'"
op|'%'
name|'line'
op|'['
op|':'
number|'1024'
op|']'
op|')'
newline|'\n'
dedent|''
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'client_timeout'
op|','
string|"'updates line'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'network_chunk_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
name|'or'
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|'=='
string|"':UPDATES: END'"
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
comment|'# Read first line METHOD PATH of subrequest.'
nl|'\n'
dedent|''
name|'method'
op|','
name|'path'
op|'='
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
string|"' '"
op|','
number|'1'
op|')'
newline|'\n'
name|'subreq'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'device'
op|','
name|'self'
op|'.'
name|'partition'
op|','
name|'path'
op|')'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
name|'method'
op|'}'
op|')'
newline|'\n'
comment|'# Read header lines.'
nl|'\n'
name|'content_length'
op|'='
name|'None'
newline|'\n'
name|'replication_headers'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'client_timeout'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'line'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'network_chunk_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Got no headers for %s %s'"
op|'%'
op|'('
name|'method'
op|','
name|'path'
op|')'
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'line'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'header'
op|','
name|'value'
op|'='
name|'line'
op|'.'
name|'split'
op|'('
string|"':'"
op|','
number|'1'
op|')'
newline|'\n'
name|'header'
op|'='
name|'header'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'value'
op|'='
name|'value'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'subreq'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
op|'='
name|'value'
newline|'\n'
name|'replication_headers'
op|'.'
name|'append'
op|'('
name|'header'
op|')'
newline|'\n'
name|'if'
name|'header'
op|'=='
string|"'content-length'"
op|':'
newline|'\n'
indent|'                    '
name|'content_length'
op|'='
name|'int'
op|'('
name|'value'
op|')'
newline|'\n'
comment|'# Establish subrequest body, if needed.'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'method'
op|'=='
string|"'DELETE'"
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'content_length'
name|'not'
name|'in'
op|'('
name|'None'
op|','
number|'0'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'DELETE subrequest with content-length %s'"
op|'%'
name|'path'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'method'
op|'=='
string|"'PUT'"
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'content_length'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'No content-length sent for %s %s'"
op|'%'
op|'('
name|'method'
op|','
name|'path'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|subreq_iter
dedent|''
name|'def'
name|'subreq_iter'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'left'
op|'='
name|'content_length'
newline|'\n'
name|'while'
name|'left'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'client_timeout'
op|','
nl|'\n'
string|"'updates content'"
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'chunk'
op|'='
name|'self'
op|'.'
name|'fp'
op|'.'
name|'read'
op|'('
nl|'\n'
name|'min'
op|'('
name|'left'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'network_chunk_size'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'chunk'
op|':'
newline|'\n'
indent|'                            '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Early termination for %s %s'"
op|'%'
op|'('
name|'method'
op|','
name|'path'
op|')'
op|')'
newline|'\n'
dedent|''
name|'left'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'yield'
name|'chunk'
newline|'\n'
dedent|''
dedent|''
name|'subreq'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
op|'='
name|'utils'
op|'.'
name|'FileLikeIter'
op|'('
nl|'\n'
name|'subreq_iter'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'Invalid subrequest method %s'"
op|'%'
name|'method'
op|')'
newline|'\n'
dedent|''
name|'subreq'
op|'.'
name|'headers'
op|'['
string|"'X-Backend-Storage-Policy-Index'"
op|']'
op|'='
name|'self'
op|'.'
name|'policy_idx'
newline|'\n'
name|'subreq'
op|'.'
name|'headers'
op|'['
string|"'X-Backend-Replication'"
op|']'
op|'='
string|"'True'"
newline|'\n'
name|'if'
name|'replication_headers'
op|':'
newline|'\n'
indent|'                '
name|'subreq'
op|'.'
name|'headers'
op|'['
string|"'X-Backend-Replication-Headers'"
op|']'
op|'='
string|"' '"
op|'.'
name|'join'
op|'('
name|'replication_headers'
op|')'
newline|'\n'
comment|'# Route subrequest and translate response.'
nl|'\n'
dedent|''
name|'resp'
op|'='
name|'subreq'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'http'
op|'.'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|')'
name|'or'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'http'
op|'.'
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                '
name|'successes'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'if'
name|'failures'
op|'>='
name|'self'
op|'.'
name|'app'
op|'.'
name|'replication_failure_threshold'
name|'and'
op|'('
nl|'\n'
name|'not'
name|'successes'
name|'or'
nl|'\n'
name|'float'
op|'('
name|'failures'
op|')'
op|'/'
name|'successes'
op|'>'
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'replication_failure_ratio'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Too many %d failures to %d successes'"
op|'%'
nl|'\n'
op|'('
name|'failures'
op|','
name|'successes'
op|')'
op|')'
newline|'\n'
comment|'# The subreq may have failed, but we want to read the rest of the'
nl|'\n'
comment|'# body from the remote side so we can continue on with the next'
nl|'\n'
comment|'# subreq.'
nl|'\n'
dedent|''
name|'for'
name|'junk'
name|'in'
name|'subreq'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'failures'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'swob'
op|'.'
name|'HTTPInternalServerError'
op|'('
nl|'\n'
string|"'ERROR: With :UPDATES: %d failures to %d successes'"
op|'%'
nl|'\n'
op|'('
name|'failures'
op|','
name|'successes'
op|')'
op|')'
newline|'\n'
dedent|''
name|'yield'
string|"':UPDATES: START\\r\\n'"
newline|'\n'
name|'yield'
string|"':UPDATES: END\\r\\n'"
newline|'\n'
name|'for'
name|'data'
name|'in'
name|'self'
op|'.'
name|'_ensure_flush'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'yield'
name|'data'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
