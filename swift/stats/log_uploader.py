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
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'gzip'
newline|'\n'
name|'import'
name|'glob'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'appconfig'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'internal_proxy'
name|'import'
name|'InternalProxy'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'daemon'
name|'import'
name|'Daemon'
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
DECL|class|LogUploader
name|'class'
name|'LogUploader'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''\n    Given a local directory, a swift account, and a container name, LogParser\n    will upload all files in the local directory to the given account/\n    container.  All but the newest files will be uploaded, and the files' md5\n    sum will be computed. The hash is used to prevent duplicate data from\n    being uploaded multiple times in different files (ex: log lines). Since\n    the hash is computed, it is also used as the uploaded object's etag to\n    ensure data integrity.\n\n    Note that after the file is successfully uploaded, it will be unlinked.\n\n    The given proxy server config is used to instantiate a proxy server for\n    the object uploads.\n    '''"
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'uploader_conf'
op|','
name|'plugin_name'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'LogUploader'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'uploader_conf'
op|')'
newline|'\n'
name|'log_dir'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'log_dir'"
op|','
string|"'/var/log/swift/'"
op|')'
newline|'\n'
name|'swift_account'
op|'='
name|'uploader_conf'
op|'['
string|"'swift_account'"
op|']'
newline|'\n'
name|'container_name'
op|'='
name|'uploader_conf'
op|'['
string|"'container_name'"
op|']'
newline|'\n'
name|'source_filename_format'
op|'='
name|'uploader_conf'
op|'['
string|"'source_filename_format'"
op|']'
newline|'\n'
name|'proxy_server_conf_loc'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'proxy_server_conf'"
op|','
nl|'\n'
string|"'/etc/swift/proxy-server.conf'"
op|')'
newline|'\n'
name|'proxy_server_conf'
op|'='
name|'appconfig'
op|'('
string|"'config:%s'"
op|'%'
name|'proxy_server_conf_loc'
op|','
nl|'\n'
name|'name'
op|'='
string|"'proxy-server'"
op|')'
newline|'\n'
name|'new_log_cutoff'
op|'='
name|'int'
op|'('
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'new_log_cutoff'"
op|','
string|"'7200'"
op|')'
op|')'
newline|'\n'
name|'unlink_log'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'unlink_log'"
op|','
string|"'True'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'true'"
op|','
string|"'on'"
op|','
string|"'1'"
op|','
string|"'yes'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'unlink_log'
op|'='
name|'unlink_log'
newline|'\n'
name|'self'
op|'.'
name|'new_log_cutoff'
op|'='
name|'new_log_cutoff'
newline|'\n'
name|'if'
name|'not'
name|'log_dir'
op|'.'
name|'endswith'
op|'('
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'log_dir'
op|'='
name|'log_dir'
op|'+'
string|"'/'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'log_dir'
op|'='
name|'log_dir'
newline|'\n'
name|'self'
op|'.'
name|'swift_account'
op|'='
name|'swift_account'
newline|'\n'
name|'self'
op|'.'
name|'container_name'
op|'='
name|'container_name'
newline|'\n'
name|'self'
op|'.'
name|'filename_format'
op|'='
name|'source_filename_format'
newline|'\n'
name|'self'
op|'.'
name|'internal_proxy'
op|'='
name|'InternalProxy'
op|'('
name|'proxy_server_conf'
op|')'
newline|'\n'
name|'log_name'
op|'='
string|"'swift-log-uploader-%s'"
op|'%'
name|'plugin_name'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'utils'
op|'.'
name|'get_logger'
op|'('
name|'uploader_conf'
op|','
name|'plugin_name'
op|','
name|'log_route'
op|'='
name|'plugin_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Uploading logs"'
op|')'
op|')'
newline|'\n'
name|'start'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'upload_all_logs'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Uploading logs complete (%0.2f minutes)"'
op|')'
op|'%'
nl|'\n'
op|'('
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
op|')'
op|'/'
number|'60'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|upload_all_logs
dedent|''
name|'def'
name|'upload_all_logs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
op|'['
op|'('
name|'self'
op|'.'
name|'filename_format'
op|'.'
name|'index'
op|'('
name|'c'
op|')'
op|','
name|'c'
op|')'
name|'for'
name|'c'
name|'in'
string|"'%Y %m %d %H'"
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
name|'i'
op|'.'
name|'sort'
op|'('
op|')'
newline|'\n'
name|'year_offset'
op|'='
name|'month_offset'
op|'='
name|'day_offset'
op|'='
name|'hour_offset'
op|'='
name|'None'
newline|'\n'
name|'base_offset'
op|'='
name|'len'
op|'('
name|'self'
op|'.'
name|'log_dir'
op|')'
newline|'\n'
name|'for'
name|'start'
op|','
name|'c'
name|'in'
name|'i'
op|':'
newline|'\n'
indent|'            '
name|'offset'
op|'='
name|'base_offset'
op|'+'
name|'start'
newline|'\n'
name|'if'
name|'c'
op|'=='
string|"'%Y'"
op|':'
newline|'\n'
indent|'                '
name|'year_offset'
op|'='
name|'offset'
op|','
name|'offset'
op|'+'
number|'4'
newline|'\n'
comment|'# Add in the difference between len(%Y) and the expanded'
nl|'\n'
comment|'# version of %Y (????). This makes sure the codes after this'
nl|'\n'
comment|'# one will align properly in the final filename.'
nl|'\n'
name|'base_offset'
op|'+='
number|'2'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'=='
string|"'%m'"
op|':'
newline|'\n'
indent|'                '
name|'month_offset'
op|'='
name|'offset'
op|','
name|'offset'
op|'+'
number|'2'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'=='
string|"'%d'"
op|':'
newline|'\n'
indent|'                '
name|'day_offset'
op|'='
name|'offset'
op|','
name|'offset'
op|'+'
number|'2'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|'=='
string|"'%H'"
op|':'
newline|'\n'
indent|'                '
name|'hour_offset'
op|'='
name|'offset'
op|','
name|'offset'
op|'+'
number|'2'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
op|'('
name|'year_offset'
name|'and'
name|'month_offset'
name|'and'
name|'day_offset'
name|'and'
name|'hour_offset'
op|')'
op|':'
newline|'\n'
comment|"# don't have all the parts, can't upload anything"
nl|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'glob_pattern'
op|'='
name|'self'
op|'.'
name|'filename_format'
newline|'\n'
name|'glob_pattern'
op|'='
name|'glob_pattern'
op|'.'
name|'replace'
op|'('
string|"'%Y'"
op|','
string|"'????'"
op|','
number|'1'
op|')'
newline|'\n'
name|'glob_pattern'
op|'='
name|'glob_pattern'
op|'.'
name|'replace'
op|'('
string|"'%m'"
op|','
string|"'??'"
op|','
number|'1'
op|')'
newline|'\n'
name|'glob_pattern'
op|'='
name|'glob_pattern'
op|'.'
name|'replace'
op|'('
string|"'%d'"
op|','
string|"'??'"
op|','
number|'1'
op|')'
newline|'\n'
name|'glob_pattern'
op|'='
name|'glob_pattern'
op|'.'
name|'replace'
op|'('
string|"'%H'"
op|','
string|"'??'"
op|','
number|'1'
op|')'
newline|'\n'
name|'filelist'
op|'='
name|'glob'
op|'.'
name|'iglob'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'log_dir'
op|','
name|'glob_pattern'
op|')'
op|')'
newline|'\n'
name|'current_hour'
op|'='
name|'int'
op|'('
name|'time'
op|'.'
name|'strftime'
op|'('
string|"'%H'"
op|')'
op|')'
newline|'\n'
name|'today'
op|'='
name|'int'
op|'('
name|'time'
op|'.'
name|'strftime'
op|'('
string|"'%Y%m%d'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'create_container'
op|'('
name|'self'
op|'.'
name|'swift_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'for'
name|'filename'
name|'in'
name|'filelist'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
comment|'# From the filename, we need to derive the year, month, day,'
nl|'\n'
comment|'# and hour for the file. These values are used in the uploaded'
nl|'\n'
comment|"# object's name, so they should be a reasonably accurate"
nl|'\n'
comment|'# representation of the time for which the data in the file was'
nl|'\n'
comment|"# collected. The file's last modified time is not a reliable"
nl|'\n'
comment|'# representation of the data in the file. For example, an old'
nl|'\n'
comment|'# log file (from hour A) may be uploaded or moved into the'
nl|'\n'
comment|"# log_dir in hour Z. The file's modified time will be for hour"
nl|'\n'
comment|"# Z, and therefore the object's name in the system will not"
nl|'\n'
comment|'# represent the data in it.'
nl|'\n'
comment|"# If the filename doesn't match the format, it shouldn't be"
nl|'\n'
comment|'# uploaded.'
nl|'\n'
indent|'                '
name|'year'
op|'='
name|'filename'
op|'['
name|'slice'
op|'('
op|'*'
name|'year_offset'
op|')'
op|']'
newline|'\n'
name|'month'
op|'='
name|'filename'
op|'['
name|'slice'
op|'('
op|'*'
name|'month_offset'
op|')'
op|']'
newline|'\n'
name|'day'
op|'='
name|'filename'
op|'['
name|'slice'
op|'('
op|'*'
name|'day_offset'
op|')'
op|']'
newline|'\n'
name|'hour'
op|'='
name|'filename'
op|'['
name|'slice'
op|'('
op|'*'
name|'hour_offset'
op|')'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'IndexError'
op|':'
newline|'\n'
comment|'# unexpected filename format, move on'
nl|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|'"Unexpected log: %s"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'if'
op|'('
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'os'
op|'.'
name|'stat'
op|'('
name|'filename'
op|')'
op|'.'
name|'st_mtime'
op|')'
op|'<'
nl|'\n'
name|'self'
op|'.'
name|'new_log_cutoff'
op|')'
op|':'
newline|'\n'
comment|"# don't process very new logs"
nl|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
name|'_'
op|'('
string|'"Skipping log: %(file)s (< %(cutoff)d seconds old)"'
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'file'"
op|':'
name|'filename'
op|','
string|"'cutoff'"
op|':'
name|'self'
op|'.'
name|'new_log_cutoff'
op|'}'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'upload_one_log'
op|'('
name|'filename'
op|','
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|')'
newline|'\n'
nl|'\n'
DECL|member|upload_one_log
dedent|''
dedent|''
name|'def'
name|'upload_one_log'
op|'('
name|'self'
op|','
name|'filename'
op|','
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'filename'
op|')'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Log %s is 0 length, skipping"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Processing log: %s"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
name|'filehash'
op|'='
name|'hashlib'
op|'.'
name|'md5'
op|'('
op|')'
newline|'\n'
name|'already_compressed'
op|'='
name|'True'
name|'if'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.gz'"
op|')'
name|'else'
name|'False'
newline|'\n'
name|'opener'
op|'='
name|'gzip'
op|'.'
name|'open'
name|'if'
name|'already_compressed'
name|'else'
name|'open'
newline|'\n'
name|'f'
op|'='
name|'opener'
op|'('
name|'filename'
op|','
string|"'rb'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'line'
name|'in'
name|'f'
op|':'
newline|'\n'
comment|'# filter out bad lines here?'
nl|'\n'
indent|'                '
name|'filehash'
op|'.'
name|'update'
op|'('
name|'line'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'filehash'
op|'='
name|'filehash'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
comment|'# By adding a hash to the filename, we ensure that uploaded files'
nl|'\n'
comment|'# have unique filenames and protect against uploading one file'
nl|'\n'
comment|'# more than one time. By using md5, we get an etag for free.'
nl|'\n'
name|'target_filename'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|','
name|'filehash'
op|'+'
string|"'.gz'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'upload_file'
op|'('
name|'filename'
op|','
nl|'\n'
name|'self'
op|'.'
name|'swift_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'target_filename'
op|','
nl|'\n'
name|'compress'
op|'='
op|'('
name|'not'
name|'already_compressed'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Uploaded log %(file)s to %(target)s"'
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'file'"
op|':'
name|'filename'
op|','
string|"'target'"
op|':'
name|'target_filename'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'unlink_log'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'filename'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|'"ERROR: Upload of log %s failed!"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
