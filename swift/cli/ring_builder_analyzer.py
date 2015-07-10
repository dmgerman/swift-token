begin_unit
comment|'#! /usr/bin/env python'
nl|'\n'
comment|'# Copyright (c) 2015 Samuel Merritt <sam@swiftstack.com>'
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
string|'"""\nThis is a tool for analyzing how well the ring builder performs its job\nin a particular scenario. It is intended to help developers quantify any\nimprovements or regressions in the ring builder; it is probably not useful\nto others.\n\nThe ring builder analyzer takes a scenario file containing some initial\nparameters for a ring builder plus a certain number of rounds. In each\nround, some modifications are made to the builder, e.g. add a device, remove\na device, change a device\'s weight. Then, the builder is repeatedly\nrebalanced until it settles down. Data about that round is printed, and the\nnext round begins.\n\nScenarios are specified in JSON. Example scenario for a gradual device\naddition::\n\n    {\n        "part_power": 12,\n        "replicas": 3,\n        "overload": 0.1,\n        "random_seed": 203488,\n\n        "rounds": [\n            [\n                ["add", "r1z2-10.20.30.40:6000/sda", 8000],\n                ["add", "r1z2-10.20.30.40:6000/sdb", 8000],\n                ["add", "r1z2-10.20.30.40:6000/sdc", 8000],\n                ["add", "r1z2-10.20.30.40:6000/sdd", 8000],\n\n                ["add", "r1z2-10.20.30.41:6000/sda", 8000],\n                ["add", "r1z2-10.20.30.41:6000/sdb", 8000],\n                ["add", "r1z2-10.20.30.41:6000/sdc", 8000],\n                ["add", "r1z2-10.20.30.41:6000/sdd", 8000],\n\n                ["add", "r1z2-10.20.30.43:6000/sda", 8000],\n                ["add", "r1z2-10.20.30.43:6000/sdb", 8000],\n                ["add", "r1z2-10.20.30.43:6000/sdc", 8000],\n                ["add", "r1z2-10.20.30.43:6000/sdd", 8000],\n\n                ["add", "r1z2-10.20.30.44:6000/sda", 8000],\n                ["add", "r1z2-10.20.30.44:6000/sdb", 8000],\n                ["add", "r1z2-10.20.30.44:6000/sdc", 8000]\n            ], [\n                ["add", "r1z2-10.20.30.44:6000/sdd", 1000]\n            ], [\n                ["set_weight", 15, 2000]\n            ], [\n                ["remove", 3],\n                ["set_weight", 15, 3000]\n            ], [\n                ["set_weight", 15, 4000]\n            ], [\n                ["set_weight", 15, 5000]\n            ], [\n                ["set_weight", 15, 6000]\n            ], [\n                ["set_weight", 15, 7000]\n            ], [\n                ["set_weight", 15, 8000]\n            ]]\n    }\n\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'argparse'
newline|'\n'
name|'import'
name|'json'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'builder'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
op|'.'
name|'utils'
name|'import'
name|'parse_add_value'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|ARG_PARSER
name|'ARG_PARSER'
op|'='
name|'argparse'
op|'.'
name|'ArgumentParser'
op|'('
nl|'\n'
DECL|variable|description
name|'description'
op|'='
string|"'Put the ring builder through its paces'"
op|')'
newline|'\n'
name|'ARG_PARSER'
op|'.'
name|'add_argument'
op|'('
nl|'\n'
string|"'--check'"
op|','
string|"'-c'"
op|','
name|'action'
op|'='
string|"'store_true'"
op|','
nl|'\n'
DECL|variable|help
name|'help'
op|'='
string|'"Just check the scenario, don\'t execute it."'
op|')'
newline|'\n'
name|'ARG_PARSER'
op|'.'
name|'add_argument'
op|'('
nl|'\n'
string|"'scenario_path'"
op|','
nl|'\n'
DECL|variable|help
name|'help'
op|'='
string|'"Path to the scenario file"'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_parse_weight
name|'def'
name|'_parse_weight'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'weight_str'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'weight'
op|'='
name|'float'
op|'('
name|'weight_str'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid weight %r (round %d, command %d): %s"'
nl|'\n'
op|'%'
op|'('
name|'weight_str'
op|','
name|'round_index'
op|','
name|'command_index'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'weight'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Negative weight (round %d, command %d)"'
nl|'\n'
op|'%'
op|'('
name|'round_index'
op|','
name|'command_index'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'weight'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_parse_add_command
dedent|''
name|'def'
name|'_parse_add_command'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'command'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'len'
op|'('
name|'command'
op|')'
op|'!='
number|'3'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid add command (round %d, command %d): expected array of "'
nl|'\n'
string|'"length 3, but got %d"'
nl|'\n'
op|'%'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'len'
op|'('
name|'command'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'dev_str'
op|'='
name|'command'
op|'['
number|'1'
op|']'
newline|'\n'
name|'weight_str'
op|'='
name|'command'
op|'['
number|'2'
op|']'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'dev'
op|'='
name|'parse_add_value'
op|'('
name|'dev_str'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid device specifier \'%s\' in add (round %d, command %d): %s"'
nl|'\n'
op|'%'
op|'('
name|'dev_str'
op|','
name|'round_index'
op|','
name|'command_index'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'dev'
op|'['
string|"'weight'"
op|']'
op|'='
name|'_parse_weight'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'weight_str'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'dev'
op|'['
string|"'region'"
op|']'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'dev'
op|'['
string|"'region'"
op|']'
op|'='
number|'1'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
op|'['
string|"'add'"
op|','
name|'dev'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_parse_remove_command
dedent|''
name|'def'
name|'_parse_remove_command'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'command'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'len'
op|'('
name|'command'
op|')'
op|'!='
number|'2'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid remove command (round %d, command %d): expected array of "'
nl|'\n'
string|'"length 2, but got %d"'
nl|'\n'
op|'%'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'len'
op|'('
name|'command'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'dev_str'
op|'='
name|'command'
op|'['
number|'1'
op|']'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'dev_id'
op|'='
name|'int'
op|'('
name|'dev_str'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid device ID \'%s\' in remove (round %d, command %d): %s"'
nl|'\n'
op|'%'
op|'('
name|'dev_str'
op|','
name|'round_index'
op|','
name|'command_index'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
op|'['
string|"'remove'"
op|','
name|'dev_id'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_parse_set_weight_command
dedent|''
name|'def'
name|'_parse_set_weight_command'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'command'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'len'
op|'('
name|'command'
op|')'
op|'!='
number|'3'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid remove command (round %d, command %d): expected array of "'
nl|'\n'
string|'"length 3, but got %d"'
nl|'\n'
op|'%'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'len'
op|'('
name|'command'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'dev_str'
op|'='
name|'command'
op|'['
number|'1'
op|']'
newline|'\n'
name|'weight_str'
op|'='
name|'command'
op|'['
number|'2'
op|']'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'dev_id'
op|'='
name|'int'
op|'('
name|'dev_str'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Invalid device ID \'%s\' in set_weight (round %d, command %d): %s"'
nl|'\n'
op|'%'
op|'('
name|'dev_str'
op|','
name|'round_index'
op|','
name|'command_index'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'weight'
op|'='
name|'_parse_weight'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'weight_str'
op|')'
newline|'\n'
name|'return'
op|'['
string|"'set_weight'"
op|','
name|'dev_id'
op|','
name|'weight'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|parse_scenario
dedent|''
name|'def'
name|'parse_scenario'
op|'('
name|'scenario_data'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Takes a serialized scenario and turns it into a data structure suitable\n    for feeding to run_scenario().\n\n    :returns: scenario\n    :raises: ValueError on invalid scenario\n    """'
newline|'\n'
nl|'\n'
name|'parsed_scenario'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'raw_scenario'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'scenario_data'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"Invalid JSON in scenario file: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'raw_scenario'
op|','
name|'dict'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"Scenario must be a JSON object, not array or string"'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'part_power'"
name|'not'
name|'in'
name|'raw_scenario'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"part_power missing"'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'parsed_scenario'
op|'['
string|"'part_power'"
op|']'
op|'='
name|'int'
op|'('
name|'raw_scenario'
op|'['
string|"'part_power'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"part_power not an integer: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
number|'1'
op|'<='
name|'parsed_scenario'
op|'['
string|"'part_power'"
op|']'
op|'<='
number|'32'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"part_power must be between 1 and 32, but was %d"'
nl|'\n'
op|'%'
name|'raw_scenario'
op|'['
string|"'part_power'"
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'replicas'"
name|'not'
name|'in'
name|'raw_scenario'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"replicas missing"'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'parsed_scenario'
op|'['
string|"'replicas'"
op|']'
op|'='
name|'float'
op|'('
name|'raw_scenario'
op|'['
string|"'replicas'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"replicas not a float: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'parsed_scenario'
op|'['
string|"'replicas'"
op|']'
op|'<'
number|'1'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"replicas must be at least 1, but is %f"'
nl|'\n'
op|'%'
name|'parsed_scenario'
op|'['
string|"'replicas'"
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'overload'"
name|'not'
name|'in'
name|'raw_scenario'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"overload missing"'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'parsed_scenario'
op|'['
string|"'overload'"
op|']'
op|'='
name|'float'
op|'('
name|'raw_scenario'
op|'['
string|"'overload'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"overload not a float: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'parsed_scenario'
op|'['
string|"'overload'"
op|']'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"overload must be non-negative, but is %f"'
nl|'\n'
op|'%'
name|'parsed_scenario'
op|'['
string|"'overload'"
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'random_seed'"
name|'not'
name|'in'
name|'raw_scenario'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"random_seed missing"'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'parsed_scenario'
op|'['
string|"'random_seed'"
op|']'
op|'='
name|'int'
op|'('
name|'raw_scenario'
op|'['
string|"'random_seed'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"replicas not an integer: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'rounds'"
name|'not'
name|'in'
name|'raw_scenario'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"rounds missing"'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'raw_scenario'
op|'['
string|"'rounds'"
op|']'
op|','
name|'list'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ValueError'
op|'('
string|'"rounds must be an array"'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'parser_for_command'
op|'='
op|'{'
string|"'add'"
op|':'
name|'_parse_add_command'
op|','
nl|'\n'
string|"'remove'"
op|':'
name|'_parse_remove_command'
op|','
nl|'\n'
string|"'set_weight'"
op|':'
name|'_parse_set_weight_command'
op|'}'
newline|'\n'
nl|'\n'
name|'parsed_scenario'
op|'['
string|"'rounds'"
op|']'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'round_index'
op|','
name|'raw_round'
name|'in'
name|'enumerate'
op|'('
name|'raw_scenario'
op|'['
string|"'rounds'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'raw_round'
op|','
name|'list'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|'"round %d not an array"'
op|'%'
name|'round_index'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'parsed_round'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'command_index'
op|','
name|'command'
name|'in'
name|'enumerate'
op|'('
name|'raw_round'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'command'
op|'['
number|'0'
op|']'
name|'not'
name|'in'
name|'parser_for_command'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|'"Unknown command (round %d, command %d): "'
nl|'\n'
string|'"\'%s\' should be one of %s"'
op|'%'
nl|'\n'
op|'('
name|'round_index'
op|','
name|'command_index'
op|','
name|'command'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'parser_for_command'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'parsed_round'
op|'.'
name|'append'
op|'('
nl|'\n'
name|'parser_for_command'
op|'['
name|'command'
op|'['
number|'0'
op|']'
op|']'
op|'('
nl|'\n'
name|'round_index'
op|','
name|'command_index'
op|','
name|'command'
op|')'
op|')'
newline|'\n'
dedent|''
name|'parsed_scenario'
op|'['
string|"'rounds'"
op|']'
op|'.'
name|'append'
op|'('
name|'parsed_round'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'parsed_scenario'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|run_scenario
dedent|''
name|'def'
name|'run_scenario'
op|'('
name|'scenario'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Takes a parsed scenario (like from parse_scenario()) and runs it.\n    """'
newline|'\n'
name|'seed'
op|'='
name|'scenario'
op|'['
string|"'random_seed'"
op|']'
newline|'\n'
nl|'\n'
name|'rb'
op|'='
name|'builder'
op|'.'
name|'RingBuilder'
op|'('
name|'scenario'
op|'['
string|"'part_power'"
op|']'
op|','
name|'scenario'
op|'['
string|"'replicas'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'set_overload'
op|'('
name|'scenario'
op|'['
string|"'overload'"
op|']'
op|')'
newline|'\n'
name|'for'
name|'round_index'
op|','
name|'commands'
name|'in'
name|'enumerate'
op|'('
name|'scenario'
op|'['
string|"'rounds'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|'"Round %d"'
op|'%'
op|'('
name|'round_index'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'command'
name|'in'
name|'commands'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'command'
op|'['
number|'0'
op|']'
op|'=='
string|"'add'"
op|':'
newline|'\n'
indent|'                '
name|'rb'
op|'.'
name|'add_dev'
op|'('
name|'command'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'command'
op|'['
number|'0'
op|']'
op|'=='
string|"'remove'"
op|':'
newline|'\n'
indent|'                '
name|'rb'
op|'.'
name|'remove_dev'
op|'('
name|'command'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'command'
op|'['
number|'0'
op|']'
op|'=='
string|"'set_weight'"
op|':'
newline|'\n'
indent|'                '
name|'rb'
op|'.'
name|'set_dev_weight'
op|'('
name|'command'
op|'['
number|'1'
op|']'
op|','
name|'command'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'ValueError'
op|'('
string|'"unknown command %r"'
op|'%'
op|'('
name|'command'
op|'['
number|'0'
op|']'
op|','
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'rebalance_number'
op|'='
number|'1'
newline|'\n'
name|'parts_moved'
op|','
name|'old_balance'
op|'='
name|'rb'
op|'.'
name|'rebalance'
op|'('
name|'seed'
op|'='
name|'seed'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'pretend_min_part_hours_passed'
op|'('
op|')'
newline|'\n'
name|'print'
string|'"\\tRebalance 1: moved %d parts, balance is %.6f"'
op|'%'
op|'('
nl|'\n'
name|'parts_moved'
op|','
name|'old_balance'
op|')'
newline|'\n'
nl|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'rebalance_number'
op|'+='
number|'1'
newline|'\n'
name|'parts_moved'
op|','
name|'new_balance'
op|'='
name|'rb'
op|'.'
name|'rebalance'
op|'('
name|'seed'
op|'='
name|'seed'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'pretend_min_part_hours_passed'
op|'('
op|')'
newline|'\n'
name|'print'
string|'"\\tRebalance %d: moved %d parts, balance is %.6f"'
op|'%'
op|'('
nl|'\n'
name|'rebalance_number'
op|','
name|'parts_moved'
op|','
name|'new_balance'
op|')'
newline|'\n'
name|'if'
name|'parts_moved'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'abs'
op|'('
name|'new_balance'
op|'-'
name|'old_balance'
op|')'
op|'<'
number|'1'
name|'and'
name|'not'
op|'('
nl|'\n'
name|'old_balance'
op|'=='
name|'builder'
op|'.'
name|'MAX_BALANCE'
name|'and'
nl|'\n'
name|'new_balance'
op|'=='
name|'builder'
op|'.'
name|'MAX_BALANCE'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'old_balance'
op|'='
name|'new_balance'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|main
dedent|''
dedent|''
dedent|''
name|'def'
name|'main'
op|'('
name|'argv'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'args'
op|'='
name|'ARG_PARSER'
op|'.'
name|'parse_args'
op|'('
name|'argv'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'with'
name|'open'
op|'('
name|'args'
op|'.'
name|'scenario_path'
op|')'
name|'as'
name|'sfh'
op|':'
newline|'\n'
indent|'            '
name|'scenario_data'
op|'='
name|'sfh'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'OSError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'sys'
op|'.'
name|'stderr'
op|'.'
name|'write'
op|'('
string|'"Error opening scenario %s: %s\\n"'
op|'%'
nl|'\n'
op|'('
name|'args'
op|'.'
name|'scenario_path'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
name|'return'
number|'1'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'scenario'
op|'='
name|'parse_scenario'
op|'('
name|'scenario_data'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'sys'
op|'.'
name|'stderr'
op|'.'
name|'write'
op|'('
string|'"Invalid scenario %s: %s\\n"'
op|'%'
nl|'\n'
op|'('
name|'args'
op|'.'
name|'scenario_path'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
name|'return'
number|'1'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'args'
op|'.'
name|'check'
op|':'
newline|'\n'
indent|'        '
name|'run_scenario'
op|'('
name|'scenario'
op|')'
newline|'\n'
dedent|''
name|'return'
number|'0'
newline|'\n'
dedent|''
endmarker|''
end_unit
