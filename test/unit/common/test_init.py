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
name|'re'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'swift'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestVersioning
name|'class'
name|'TestVersioning'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
DECL|member|test_canonical_version_is_clean
indent|'    '
name|'def'
name|'test_canonical_version_is_clean'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Ensure that a non-clean canonical_version never happens"""'
newline|'\n'
name|'pattern'
op|'='
name|'re'
op|'.'
name|'compile'
op|'('
string|"'^\\d+(\\.\\d+)*$'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'pattern'
op|'.'
name|'match'
op|'('
name|'swift'
op|'.'
name|'__canonical_version__'
op|')'
name|'is'
name|'not'
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_canonical_version_equals_version_for_final
dedent|''
name|'def'
name|'test_canonical_version_equals_version_for_final'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'version'
op|'='
name|'swift'
op|'.'
name|'Version'
op|'('
string|"'7.8.9'"
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'version'
op|'.'
name|'pretty_version'
op|','
string|"'7.8.9'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'version'
op|'.'
name|'canonical_version'
op|','
string|"'7.8.9'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_version_has_dev_suffix_for_non_final
dedent|''
name|'def'
name|'test_version_has_dev_suffix_for_non_final'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'version'
op|'='
name|'swift'
op|'.'
name|'Version'
op|'('
string|"'7.8.9'"
op|','
name|'False'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'version'
op|'.'
name|'pretty_version'
op|','
string|"'7.8.9-dev'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'version'
op|'.'
name|'canonical_version'
op|','
string|"'7.8.9'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
