begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack, LLC.'
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
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
newline|'\n'
name|'import'
name|'optparse'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|tiers_for_dev
name|'def'
name|'tiers_for_dev'
op|'('
name|'dev'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns a tuple of tiers for a given device in ascending order by\n    length.\n\n    :returns: tuple of tiers\n    """'
newline|'\n'
name|'t1'
op|'='
name|'dev'
op|'['
string|"'region'"
op|']'
newline|'\n'
name|'t2'
op|'='
name|'dev'
op|'['
string|"'zone'"
op|']'
newline|'\n'
name|'t3'
op|'='
string|'"{ip}:{port}"'
op|'.'
name|'format'
op|'('
name|'ip'
op|'='
name|'dev'
op|'.'
name|'get'
op|'('
string|"'ip'"
op|')'
op|','
name|'port'
op|'='
name|'dev'
op|'.'
name|'get'
op|'('
string|"'port'"
op|')'
op|')'
newline|'\n'
name|'t4'
op|'='
name|'dev'
op|'['
string|"'id'"
op|']'
newline|'\n'
nl|'\n'
name|'return'
op|'('
op|'('
name|'t1'
op|','
op|')'
op|','
nl|'\n'
op|'('
name|'t1'
op|','
name|'t2'
op|')'
op|','
nl|'\n'
op|'('
name|'t1'
op|','
name|'t2'
op|','
name|'t3'
op|')'
op|','
nl|'\n'
op|'('
name|'t1'
op|','
name|'t2'
op|','
name|'t3'
op|','
name|'t4'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|build_tier_tree
dedent|''
name|'def'
name|'build_tier_tree'
op|'('
name|'devices'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Construct the tier tree from the zone layout.\n\n    The tier tree is a dictionary that maps tiers to their child tiers.\n    A synthetic root node of () is generated so that there\'s one tree,\n    not a forest.\n\n    Example:\n\n    region 1 -+---- zone 1 -+---- 192.168.101.1:6000 -+---- device id 0\n              |             |                         |\n              |             |                         +---- device id 1\n              |             |                         |\n              |             |                         +---- device id 2\n              |             |\n              |             +---- 192.168.101.2:6000 -+---- device id 3\n              |                                       |\n              |                                       +---- device id 4\n              |                                       |\n              |                                       +---- device id 5\n              |\n              +---- zone 2 -+---- 192.168.102.1:6000 -+---- device id 6\n                            |                         |\n                            |                         +---- device id 7\n                            |                         |\n                            |                         +---- device id 8\n                            |\n                            +---- 192.168.102.2:6000 -+---- device id 9\n                                                      |\n                                                      +---- device id 10\n\n\n    region 2 -+---- zone 1 -+---- 192.168.201.1:6000 -+---- device id 12\n                            |                         |\n                            |                         +---- device id 13\n                            |                         |\n                            |                         +---- device id 14\n                            |\n                            +---- 192.168.201.2:6000 -+---- device id 15\n                                                      |\n                                                      +---- device id 16\n                                                      |\n                                                      +---- device id 17\n\n    The tier tree would look like:\n    {\n      (): [(1,), (2,)],\n\n      (1,): [(1, 1), (1, 2)],\n      (2,): [(2, 1)],\n\n      (1, 1): [(1, 1, 192.168.101.1:6000),\n               (1, 1, 192.168.101.2:6000)],\n      (1, 2): [(1, 2, 192.168.102.1:6000),\n               (1, 2, 192.168.102.2:6000)],\n      (2, 1): [(2, 1, 192.168.201.1:6000),\n               (2, 1, 192.168.201.2:6000)],\n\n      (1, 1, 192.168.101.1:6000): [(1, 1, 192.168.101.1:6000, 0),\n                                   (1, 1, 192.168.101.1:6000, 1),\n                                   (1, 1, 192.168.101.1:6000, 2)],\n      (1, 1, 192.168.101.2:6000): [(1, 1, 192.168.101.2:6000, 3),\n                                   (1, 1, 192.168.101.2:6000, 4),\n                                   (1, 1, 192.168.101.2:6000, 5)],\n      (1, 2, 192.168.102.1:6000): [(1, 2, 192.168.102.1:6000, 6),\n                                   (1, 2, 192.168.102.1:6000, 7),\n                                   (1, 2, 192.168.102.1:6000, 8)],\n      (1, 2, 192.168.102.2:6000): [(1, 2, 192.168.102.2:6000, 9),\n                                   (1, 2, 192.168.102.2:6000, 10)],\n      (2, 1, 192.168.201.1:6000): [(2, 1, 192.168.201.1:6000, 12),\n                                   (2, 1, 192.168.201.1:6000, 13),\n                                   (2, 1, 192.168.201.1:6000, 14)],\n      (2, 1, 192.168.201.2:6000): [(2, 1, 192.168.201.2:6000, 15),\n                                   (2, 1, 192.168.201.2:6000, 16),\n                                   (2, 1, 192.168.201.2:6000, 17)],\n    }\n\n    :devices: device dicts from which to generate the tree\n    :returns: tier tree\n\n    """'
newline|'\n'
name|'tier2children'
op|'='
name|'defaultdict'
op|'('
name|'set'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'devices'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'tier'
name|'in'
name|'tiers_for_dev'
op|'('
name|'dev'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'len'
op|'('
name|'tier'
op|')'
op|'>'
number|'1'
op|':'
newline|'\n'
indent|'                '
name|'tier2children'
op|'['
name|'tier'
op|'['
number|'0'
op|':'
op|'-'
number|'1'
op|']'
op|']'
op|'.'
name|'add'
op|'('
name|'tier'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'tier2children'
op|'['
op|'('
op|')'
op|']'
op|'.'
name|'add'
op|'('
name|'tier'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'tier2children'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|parse_search_value
dedent|''
name|'def'
name|'parse_search_value'
op|'('
name|'search_value'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""The <search-value> can be of the form::\n\n        d<device_id>r<region>z<zone>-<ip>:<port>[R<r_ip>:<r_port>]/\n         <device_name>_<meta>\n\n    Where <r_ip> and <r_port> are replication ip and port.\n\n    Any part is optional, but you must include at least one part.\n\n    Examples::\n\n        d74              Matches the device id 74\n        r4               Matches devices in region 4\n        z1               Matches devices in zone 1\n        z1-1.2.3.4       Matches devices in zone 1 with the ip 1.2.3.4\n        1.2.3.4          Matches devices in any zone with the ip 1.2.3.4\n        z1:5678          Matches devices in zone 1 using port 5678\n        :5678            Matches devices that use port 5678\n        R5.6.7.8         Matches devices that use replication ip 5.6.7.8\n        R:5678           Matches devices that use replication port 5678\n        1.2.3.4R5.6.7.8  Matches devices that use ip 1.2.3.4 and replication ip\n                         5.6.7.8\n        /sdb1            Matches devices with the device name sdb1\n        _shiny           Matches devices with shiny in the meta data\n        _"snet: 5.6.7.8" Matches devices with snet: 5.6.7.8 in the meta data\n        [::1]            Matches devices in any zone with the ip ::1\n        z1-[::1]:5678    Matches devices in zone 1 with ip ::1 and port 5678\n\n    Most specific example::\n\n        d74r4z1-1.2.3.4:5678/sdb1_"snet: 5.6.7.8"\n\n    Nerd explanation:\n\n        All items require their single character prefix except the ip, in which\n        case the - is optional unless the device id or zone is also included.\n    """'
newline|'\n'
name|'orig_search_value'
op|'='
name|'search_value'
newline|'\n'
name|'match'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'d'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'id'"
op|']'
op|'='
name|'int'
op|'('
name|'search_value'
op|'['
number|'1'
op|':'
name|'i'
op|']'
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'r'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'region'"
op|']'
op|'='
name|'int'
op|'('
name|'search_value'
op|'['
number|'1'
op|':'
name|'i'
op|']'
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'z'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'zone'"
op|']'
op|'='
name|'int'
op|'('
name|'search_value'
op|'['
number|'1'
op|':'
name|'i'
op|']'
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'-'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'search_value'
op|'='
name|'search_value'
op|'['
number|'1'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
number|'0'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
name|'in'
string|"'0123456789.'"
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'ip'"
op|']'
op|'='
name|'search_value'
op|'['
op|':'
name|'i'
op|']'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'elif'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
number|'0'
op|']'
op|'=='
string|"'['"
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'!='
string|"']'"
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'i'
op|'+='
number|'1'
newline|'\n'
name|'match'
op|'['
string|"'ip'"
op|']'
op|'='
name|'search_value'
op|'['
op|':'
name|'i'
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'['"
op|')'
op|'.'
name|'rstrip'
op|'('
string|"']'"
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"':'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'port'"
op|']'
op|'='
name|'int'
op|'('
name|'search_value'
op|'['
number|'1'
op|':'
name|'i'
op|']'
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
comment|'# replication parameters'
nl|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'R'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'search_value'
op|'='
name|'search_value'
op|'['
number|'1'
op|':'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
number|'0'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
op|'('
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
nl|'\n'
name|'search_value'
op|'['
name|'i'
op|']'
name|'in'
string|"'0123456789.'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'replication_ip'"
op|']'
op|'='
name|'search_value'
op|'['
op|':'
name|'i'
op|']'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'elif'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
number|'0'
op|']'
op|'=='
string|"'['"
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'!='
string|"']'"
op|':'
newline|'\n'
indent|'                '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'i'
op|'+='
number|'1'
newline|'\n'
name|'match'
op|'['
string|"'replication_ip'"
op|']'
op|'='
name|'search_value'
op|'['
op|':'
name|'i'
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'['"
op|')'
op|'.'
name|'rstrip'
op|'('
string|"']'"
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"':'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'replication_port'"
op|']'
op|'='
name|'int'
op|'('
name|'search_value'
op|'['
number|'1'
op|':'
name|'i'
op|']'
op|')'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'i'
op|'='
number|'1'
newline|'\n'
name|'while'
name|'i'
op|'<'
name|'len'
op|'('
name|'search_value'
op|')'
name|'and'
name|'search_value'
op|'['
name|'i'
op|']'
op|'!='
string|"'_'"
op|':'
newline|'\n'
indent|'            '
name|'i'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'match'
op|'['
string|"'device'"
op|']'
op|'='
name|'search_value'
op|'['
number|'1'
op|':'
name|'i'
op|']'
newline|'\n'
name|'search_value'
op|'='
name|'search_value'
op|'['
name|'i'
op|':'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|'.'
name|'startswith'
op|'('
string|"'_'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'match'
op|'['
string|"'meta'"
op|']'
op|'='
name|'search_value'
op|'['
number|'1'
op|':'
op|']'
newline|'\n'
name|'search_value'
op|'='
string|"''"
newline|'\n'
dedent|''
name|'if'
name|'search_value'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|"'Invalid <search-value>: %s'"
op|'%'
nl|'\n'
name|'repr'
op|'('
name|'orig_search_value'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'match'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|parse_args
dedent|''
name|'def'
name|'parse_args'
op|'('
name|'argvish'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Build OptionParser and evaluate command line arguments.\n    """'
newline|'\n'
name|'parser'
op|'='
name|'optparse'
op|'.'
name|'OptionParser'
op|'('
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-r'"
op|','
string|"'--region'"
op|','
name|'type'
op|'='
string|'"int"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Region"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-z'"
op|','
string|"'--zone'"
op|','
name|'type'
op|'='
string|'"int"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Zone"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-i'"
op|','
string|"'--ip'"
op|','
name|'type'
op|'='
string|'"string"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"IP address"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-p'"
op|','
string|"'--port'"
op|','
name|'type'
op|'='
string|'"int"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Port number"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-j'"
op|','
string|"'--replication-ip'"
op|','
name|'type'
op|'='
string|'"string"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Replication IP address"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-q'"
op|','
string|"'--replication-port'"
op|','
name|'type'
op|'='
string|'"int"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Replication port number"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-d'"
op|','
string|"'--device'"
op|','
name|'type'
op|'='
string|'"string"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Device name (e.g. md0, sdb1)"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-w'"
op|','
string|"'--weight'"
op|','
name|'type'
op|'='
string|'"float"'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Device weight"'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-m'"
op|','
string|"'--meta'"
op|','
name|'type'
op|'='
string|'"string"'
op|','
name|'default'
op|'='
string|'""'
op|','
nl|'\n'
name|'help'
op|'='
string|'"Extra device info (just a string)"'
op|')'
newline|'\n'
name|'return'
name|'parser'
op|'.'
name|'parse_args'
op|'('
name|'argvish'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|build_dev_from_opts
dedent|''
name|'def'
name|'build_dev_from_opts'
op|'('
name|'opts'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Convert optparse stype options into a device dictionary.\n    """'
newline|'\n'
name|'for'
name|'attribute'
op|','
name|'shortopt'
op|','
name|'longopt'
name|'in'
op|'('
op|'['
string|"'region'"
op|','
string|"'-r'"
op|','
string|"'--region'"
op|']'
op|','
nl|'\n'
op|'['
string|"'zone'"
op|','
string|"'-z'"
op|','
string|"'--zone'"
op|']'
op|','
nl|'\n'
op|'['
string|"'ip'"
op|','
string|"'-i'"
op|','
string|"'--ip'"
op|']'
op|','
nl|'\n'
op|'['
string|"'port'"
op|','
string|"'-p'"
op|','
string|"'--port'"
op|']'
op|','
nl|'\n'
op|'['
string|"'device'"
op|','
string|"'-d'"
op|','
string|"'--device'"
op|']'
op|','
nl|'\n'
op|'['
string|"'weight'"
op|','
string|"'-w'"
op|','
string|"'--weight'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'getattr'
op|'('
name|'opts'
op|','
name|'attribute'
op|','
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|"'Required argument %s/%s not specified.'"
op|'%'
nl|'\n'
op|'('
name|'shortopt'
op|','
name|'longopt'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'replication_ip'
op|'='
name|'opts'
op|'.'
name|'replication_ip'
name|'or'
name|'opts'
op|'.'
name|'ip'
newline|'\n'
name|'replication_port'
op|'='
name|'opts'
op|'.'
name|'replication_port'
name|'or'
name|'opts'
op|'.'
name|'port'
newline|'\n'
nl|'\n'
name|'return'
op|'{'
string|"'region'"
op|':'
name|'opts'
op|'.'
name|'region'
op|','
string|"'zone'"
op|':'
name|'opts'
op|'.'
name|'zone'
op|','
string|"'ip'"
op|':'
name|'opts'
op|'.'
name|'ip'
op|','
nl|'\n'
string|"'port'"
op|':'
name|'opts'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'opts'
op|'.'
name|'device'
op|','
string|"'meta'"
op|':'
name|'opts'
op|'.'
name|'meta'
op|','
nl|'\n'
string|"'replication_ip'"
op|':'
name|'replication_ip'
op|','
nl|'\n'
string|"'replication_port'"
op|':'
name|'replication_port'
op|','
string|"'weight'"
op|':'
name|'opts'
op|'.'
name|'weight'
op|'}'
newline|'\n'
dedent|''
endmarker|''
end_unit
