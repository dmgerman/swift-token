begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack Foundation'
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
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'from'
name|'re'
name|'import'
name|'sub'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
op|'.'
name|'debug'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'ondisk'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Daemon
name|'class'
name|'Daemon'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Daemon base class"""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'utils'
op|'.'
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'daemon'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Override this to run the script once"""'
newline|'\n'
name|'raise'
name|'NotImplementedError'
op|'('
string|"'run_once not implemented'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
name|'def'
name|'run_forever'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Override this to run forever"""'
newline|'\n'
name|'raise'
name|'NotImplementedError'
op|'('
string|"'run_forever not implemented'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|','
name|'once'
op|'='
name|'False'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Run the daemon"""'
newline|'\n'
name|'ondisk'
op|'.'
name|'validate_configuration'
op|'('
op|')'
newline|'\n'
name|'utils'
op|'.'
name|'drop_privileges'
op|'('
name|'self'
op|'.'
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
name|'utils'
op|'.'
name|'capture_stdio'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
nl|'\n'
DECL|function|kill_children
name|'def'
name|'kill_children'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
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
name|'sys'
op|'.'
name|'exit'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
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
name|'if'
name|'once'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'run_once'
op|'('
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'run_forever'
op|'('
op|'**'
name|'kwargs'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|run_daemon
dedent|''
dedent|''
dedent|''
name|'def'
name|'run_daemon'
op|'('
name|'klass'
op|','
name|'conf_file'
op|','
name|'section_name'
op|'='
string|"''"
op|','
name|'once'
op|'='
name|'False'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Loads settings from conf, then instantiates daemon "klass" and runs the\n    daemon with the specified once kwarg.  The section_name will be derived\n    from the daemon "klass" if not provided (e.g. ObjectReplicator =>\n    object-replicator).\n\n    :param klass: Class to instantiate, subclass of common.daemon.Daemon\n    :param conf_file: Path to configuration file\n    :param section_name: Section name from conf file to load config from\n    :param once: Passed to daemon run method\n    """'
newline|'\n'
comment|'# very often the config section_name is based on the class name'
nl|'\n'
comment|'# the None singleton will be passed through to readconf as is'
nl|'\n'
name|'if'
name|'section_name'
name|'is'
string|"''"
op|':'
newline|'\n'
indent|'        '
name|'section_name'
op|'='
name|'sub'
op|'('
string|"r'([a-z])([A-Z])'"
op|','
string|"r'\\1-\\2'"
op|','
nl|'\n'
name|'klass'
op|'.'
name|'__name__'
op|')'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
dedent|''
name|'conf'
op|'='
name|'utils'
op|'.'
name|'readconf'
op|'('
name|'conf_file'
op|','
name|'section_name'
op|','
nl|'\n'
name|'log_name'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'log_name'"
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# once on command line (i.e. daemonize=false) will over-ride config'
nl|'\n'
name|'once'
op|'='
name|'once'
name|'or'
name|'not'
name|'utils'
op|'.'
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'daemonize'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# pre-configure logger'
nl|'\n'
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
name|'utils'
op|'.'
name|'get_logger'
op|'('
name|'conf'
op|','
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_name'"
op|','
name|'section_name'
op|')'
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
nl|'\n'
name|'log_route'
op|'='
name|'section_name'
op|')'
newline|'\n'
nl|'\n'
comment|'# disable fallocate if desired'
nl|'\n'
dedent|''
name|'if'
name|'utils'
op|'.'
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'disable_fallocate'"
op|','
string|"'no'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'utils'
op|'.'
name|'disable_fallocate'
op|'('
op|')'
newline|'\n'
comment|'# set utils.FALLOCATE_RESERVE if desired'
nl|'\n'
dedent|''
name|'reserve'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'fallocate_reserve'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
name|'if'
name|'reserve'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'utils'
op|'.'
name|'FALLOCATE_RESERVE'
op|'='
name|'reserve'
newline|'\n'
nl|'\n'
comment|'# By default, disable eventlet printing stacktraces'
nl|'\n'
dedent|''
name|'eventlet_debug'
op|'='
name|'utils'
op|'.'
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'eventlet_debug'"
op|','
string|"'no'"
op|')'
op|')'
newline|'\n'
name|'eventlet'
op|'.'
name|'debug'
op|'.'
name|'hub_exceptions'
op|'('
name|'eventlet_debug'
op|')'
newline|'\n'
nl|'\n'
comment|"# Ensure TZ environment variable exists to avoid stat('/etc/localtime') on"
nl|'\n'
comment|'# some platforms. This locks in reported times to the timezone in which'
nl|'\n'
comment|'# the server first starts running in locations that periodically change'
nl|'\n'
comment|'# timezones.'
nl|'\n'
name|'os'
op|'.'
name|'environ'
op|'['
string|"'TZ'"
op|']'
op|'='
name|'time'
op|'.'
name|'strftime'
op|'('
string|'"%z"'
op|','
name|'time'
op|'.'
name|'gmtime'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'klass'
op|'('
name|'conf'
op|')'
op|'.'
name|'run'
op|'('
name|'once'
op|'='
name|'once'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'KeyboardInterrupt'
op|':'
newline|'\n'
indent|'        '
name|'logger'
op|'.'
name|'info'
op|'('
string|"'User quit'"
op|')'
newline|'\n'
dedent|''
name|'logger'
op|'.'
name|'info'
op|'('
string|"'Exited'"
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
