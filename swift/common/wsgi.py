begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
string|'"""WSGI tools for use with swift."""'
newline|'\n'
nl|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'mimetools'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'greenio'
op|','
name|'GreenPool'
op|','
name|'sleep'
op|','
name|'wsgi'
op|','
name|'listen'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'loadapp'
op|','
name|'appconfig'
newline|'\n'
nl|'\n'
comment|"# Hook to ensure connection resets don't blow up our servers."
nl|'\n'
comment|'# Remove with next release of Eventlet that has it in the set already.'
nl|'\n'
name|'from'
name|'errno'
name|'import'
name|'ECONNRESET'
newline|'\n'
name|'wsgi'
op|'.'
name|'ACCEPT_ERRNO'
op|'.'
name|'add'
op|'('
name|'ECONNRESET'
op|')'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
name|'import'
name|'socket'
op|','
name|'ssl'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'drop_privileges'
op|','
name|'validate_configuration'
op|','
name|'capture_stdio'
op|','
name|'NullLogger'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|monkey_patch_mimetools
name|'def'
name|'monkey_patch_mimetools'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    mimetools.Message defaults content-type to "text/plain"\n    This changes it to default to None, so we can detect missing headers.\n    """'
newline|'\n'
nl|'\n'
name|'orig_parsetype'
op|'='
name|'mimetools'
op|'.'
name|'Message'
op|'.'
name|'parsetype'
newline|'\n'
nl|'\n'
DECL|function|parsetype
name|'def'
name|'parsetype'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'typeheader'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'type'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'maintype'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'subtype'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'plisttext'
op|'='
string|"''"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'orig_parsetype'
op|'('
name|'self'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'mimetools'
op|'.'
name|'Message'
op|'.'
name|'parsetype'
op|'='
name|'parsetype'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_socket
dedent|''
name|'def'
name|'get_socket'
op|'('
name|'conf'
op|','
name|'default_port'
op|'='
number|'8080'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Bind socket to bind ip:port in conf\n\n    :param conf: Configuration dict to read settings from\n    :param default_port: port to use if not specified in conf\n\n    :returns : a socket object as returned from socket.listen or\n               ssl.wrap_socket if conf specifies cert_file\n    """'
newline|'\n'
name|'bind_addr'
op|'='
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bind_ip'"
op|','
string|"'0.0.0.0'"
op|')'
op|','
nl|'\n'
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bind_port'"
op|','
name|'default_port'
op|')'
op|')'
op|')'
newline|'\n'
name|'address_family'
op|'='
op|'['
name|'addr'
op|'['
number|'0'
op|']'
name|'for'
name|'addr'
name|'in'
name|'socket'
op|'.'
name|'getaddrinfo'
op|'('
name|'bind_addr'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'bind_addr'
op|'['
number|'1'
op|']'
op|','
name|'socket'
op|'.'
name|'AF_UNSPEC'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
nl|'\n'
name|'if'
name|'addr'
op|'['
number|'0'
op|']'
name|'in'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'AF_INET6'
op|')'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'sock'
op|'='
name|'None'
newline|'\n'
name|'retry_until'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
number|'30'
newline|'\n'
name|'while'
name|'not'
name|'sock'
name|'and'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'<'
name|'retry_until'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'sock'
op|'='
name|'listen'
op|'('
name|'bind_addr'
op|','
name|'backlog'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'backlog'"
op|','
number|'4096'
op|')'
op|')'
op|','
nl|'\n'
name|'family'
op|'='
name|'address_family'
op|')'
newline|'\n'
name|'if'
string|"'cert_file'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'='
name|'ssl'
op|'.'
name|'wrap_socket'
op|'('
name|'sock'
op|','
name|'certfile'
op|'='
name|'conf'
op|'['
string|"'cert_file'"
op|']'
op|','
nl|'\n'
name|'keyfile'
op|'='
name|'conf'
op|'['
string|"'key_file'"
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'args'
op|'['
number|'0'
op|']'
op|'!='
name|'errno'
op|'.'
name|'EADDRINUSE'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'sock'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'Could not bind to %s:%s after trying for 30 seconds'"
op|'%'
nl|'\n'
name|'bind_addr'
op|')'
newline|'\n'
dedent|''
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'SOL_SOCKET'
op|','
name|'socket'
op|'.'
name|'SO_REUSEADDR'
op|','
number|'1'
op|')'
newline|'\n'
comment|'# in my experience, sockets can hang around forever without keepalive'
nl|'\n'
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'SOL_SOCKET'
op|','
name|'socket'
op|'.'
name|'SO_KEEPALIVE'
op|','
number|'1'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'IPPROTO_TCP'
op|','
name|'socket'
op|'.'
name|'TCP_KEEPIDLE'
op|','
number|'600'
op|')'
newline|'\n'
name|'return'
name|'sock'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'# TODO: pull pieces of this out to test'
nl|'\n'
DECL|function|run_wsgi
dedent|''
name|'def'
name|'run_wsgi'
op|'('
name|'conf_file'
op|','
name|'app_section'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Loads common settings from conf, then instantiates app and runs\n    the server using the specified number of workers.\n\n    :param conf_file: Path to paste.deploy style configuration file\n    :param app_section: App name from conf file to load config from\n    """'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
name|'appconfig'
op|'('
string|"'config:%s'"
op|'%'
name|'conf_file'
op|','
name|'name'
op|'='
name|'app_section'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|'"Error trying to load config %s: %s"'
op|'%'
op|'('
name|'conf_file'
op|','
name|'e'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'validate_configuration'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# pre-configure logger'
nl|'\n'
name|'log_name'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_name'"
op|','
name|'app_section'
op|')'
newline|'\n'
name|'if'
string|"'logger'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'        '
name|'logger'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'logger'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_name'
op|','
nl|'\n'
name|'log_to_console'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'verbose'"
op|','
name|'False'
op|')'
op|','
name|'log_route'
op|'='
string|"'wsgi'"
op|')'
newline|'\n'
nl|'\n'
comment|'# redirect errors to logger and close stdio'
nl|'\n'
dedent|''
name|'capture_stdio'
op|'('
name|'logger'
op|')'
newline|'\n'
comment|'# bind to address and port'
nl|'\n'
name|'sock'
op|'='
name|'get_socket'
op|'('
name|'conf'
op|','
name|'default_port'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'default_port'"
op|','
number|'8080'
op|')'
op|')'
newline|'\n'
comment|'# remaining tasks should not require elevated privileges'
nl|'\n'
name|'drop_privileges'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'user'"
op|','
string|"'swift'"
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# finally after binding to ports and privilege drop, run app __init__ code'
nl|'\n'
name|'app'
op|'='
name|'loadapp'
op|'('
string|"'config:%s'"
op|'%'
name|'conf_file'
op|','
name|'global_conf'
op|'='
op|'{'
string|"'log_name'"
op|':'
name|'log_name'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|run_server
name|'def'
name|'run_server'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'wsgi'
op|'.'
name|'HttpProtocol'
op|'.'
name|'default_request_version'
op|'='
string|'"HTTP/1.0"'
newline|'\n'
name|'eventlet'
op|'.'
name|'hubs'
op|'.'
name|'use_hub'
op|'('
string|"'poll'"
op|')'
newline|'\n'
name|'eventlet'
op|'.'
name|'patcher'
op|'.'
name|'monkey_patch'
op|'('
name|'all'
op|'='
name|'False'
op|','
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
name|'monkey_patch_mimetools'
op|'('
op|')'
newline|'\n'
name|'pool'
op|'='
name|'GreenPool'
op|'('
name|'size'
op|'='
number|'1024'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'wsgi'
op|'.'
name|'server'
op|'('
name|'sock'
op|','
name|'app'
op|','
name|'NullLogger'
op|'('
op|')'
op|','
name|'custom_pool'
op|'='
name|'pool'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'['
number|'0'
op|']'
op|'!='
name|'errno'
op|'.'
name|'EINVAL'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'worker_count'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'workers'"
op|','
string|"'1'"
op|')'
op|')'
newline|'\n'
comment|'# Useful for profiling [no forks].'
nl|'\n'
name|'if'
name|'worker_count'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'run_server'
op|'('
op|')'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
DECL|function|kill_children
dedent|''
name|'def'
name|'kill_children'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Kills the entire process group."""'
newline|'\n'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'SIGTERM received'"
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_IGN'
op|')'
newline|'\n'
name|'running'
op|'['
number|'0'
op|']'
op|'='
name|'False'
newline|'\n'
name|'os'
op|'.'
name|'killpg'
op|'('
number|'0'
op|','
name|'signal'
op|'.'
name|'SIGTERM'
op|')'
newline|'\n'
nl|'\n'
DECL|function|hup
dedent|''
name|'def'
name|'hup'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Shuts down the server, but allows running requests to complete"""'
newline|'\n'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'SIGHUP received'"
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGHUP'
op|','
name|'signal'
op|'.'
name|'SIG_IGN'
op|')'
newline|'\n'
name|'running'
op|'['
number|'0'
op|']'
op|'='
name|'False'
newline|'\n'
nl|'\n'
dedent|''
name|'running'
op|'='
op|'['
name|'True'
op|']'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'kill_children'
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGHUP'
op|','
name|'hup'
op|')'
newline|'\n'
name|'children'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'running'
op|'['
number|'0'
op|']'
op|':'
newline|'\n'
indent|'        '
name|'while'
name|'len'
op|'('
name|'children'
op|')'
op|'<'
name|'worker_count'
op|':'
newline|'\n'
indent|'            '
name|'pid'
op|'='
name|'os'
op|'.'
name|'fork'
op|'('
op|')'
newline|'\n'
name|'if'
name|'pid'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGHUP'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'run_server'
op|'('
op|')'
newline|'\n'
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'Child %d exiting normally'"
op|'%'
name|'os'
op|'.'
name|'getpid'
op|'('
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'Started child %s'"
op|'%'
name|'pid'
op|')'
newline|'\n'
name|'children'
op|'.'
name|'append'
op|'('
name|'pid'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'pid'
op|','
name|'status'
op|'='
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'WIFEXITED'
op|'('
name|'status'
op|')'
name|'or'
name|'os'
op|'.'
name|'WIFSIGNALED'
op|'('
name|'status'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'logger'
op|'.'
name|'error'
op|'('
string|"'Removing dead child %s'"
op|'%'
name|'pid'
op|')'
newline|'\n'
name|'children'
op|'.'
name|'remove'
op|'('
name|'pid'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'OSError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'errno'
name|'not'
name|'in'
op|'('
name|'errno'
op|'.'
name|'EINTR'
op|','
name|'errno'
op|'.'
name|'ECHILD'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'KeyboardInterrupt'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'User quit'"
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'greenio'
op|'.'
name|'shutdown_safe'
op|'('
name|'sock'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'Exited'"
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
