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
name|'swob'
name|'import'
name|'Request'
op|','
name|'HTTPServerError'
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
name|'generate_trans_id'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'WSGIContext'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|CatchErrorsContext
name|'class'
name|'CatchErrorsContext'
op|'('
name|'WSGIContext'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'logger'
op|','
name|'trans_id_suffix'
op|'='
string|"''"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'CatchErrorsContext'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'trans_id_suffix'
op|'='
name|'trans_id_suffix'
newline|'\n'
nl|'\n'
DECL|member|handle_request
dedent|''
name|'def'
name|'handle_request'
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
name|'trans_id'
op|'='
name|'generate_trans_id'
op|'('
name|'self'
op|'.'
name|'trans_id_suffix'
op|')'
newline|'\n'
name|'env'
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
name|'try'
op|':'
newline|'\n'
comment|'# catch any errors in the pipeline'
nl|'\n'
indent|'            '
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'env'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|','
name|'err'
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
string|"'Error: %s'"
op|')'
op|','
name|'err'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'HTTPServerError'
op|'('
name|'request'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
op|','
nl|'\n'
name|'body'
op|'='
string|"'An error occurred'"
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'headers'
op|'['
string|"'x-trans-id'"
op|']'
op|'='
name|'trans_id'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
comment|'# make sure the response has the trans_id'
nl|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'_response_headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_response_headers'
op|'='
op|'['
op|']'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_response_headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'x-trans-id'"
op|','
name|'trans_id'
op|')'
op|')'
newline|'\n'
name|'start_response'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|','
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
name|'resp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|CatchErrorMiddleware
dedent|''
dedent|''
name|'class'
name|'CatchErrorMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Middleware that provides high-level error handling and ensures that a\n    transaction id will be set for every request.\n    """'
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
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'catch-errors'"
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
string|'"""\n        If used, this should be the first middleware in pipeline.\n        """'
newline|'\n'
name|'context'
op|'='
name|'CatchErrorsContext'
op|'('
name|'self'
op|'.'
name|'app'
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'self'
op|'.'
name|'trans_id_suffix'
op|')'
newline|'\n'
name|'return'
name|'context'
op|'.'
name|'handle_request'
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
DECL|function|except_filter
name|'def'
name|'except_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'CatchErrorMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'except_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
