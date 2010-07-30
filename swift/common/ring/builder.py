begin_unit
comment|'# Copyright (c) 2010 OpenStack, LLC.'
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
name|'array'
name|'import'
name|'array'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'randint'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'RingData'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|RingBuilder
name|'class'
name|'RingBuilder'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Used to build swift.common.RingData instances to be written to disk and\n    used with swift.common.ring.Ring instances. See bin/ring-builder.py for\n    example usage.\n\n    The instance variable devs_changed indicates if the device information has\n    changed since the last balancing. This can be used by tools to know whether\n    a rebalance request is an isolated request or due to added, changed, or\n    removed devices.\n\n    :param part_power: number of partitions = 2**part_power\n    :param replicas: number of replicas for each partition\n    :param min_part_hours: minimum number of hours between partition changes\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'part_power'
op|','
name|'replicas'
op|','
name|'min_part_hours'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'part_power'
op|'='
name|'part_power'
newline|'\n'
name|'self'
op|'.'
name|'replicas'
op|'='
name|'replicas'
newline|'\n'
name|'self'
op|'.'
name|'min_part_hours'
op|'='
name|'min_part_hours'
newline|'\n'
name|'self'
op|'.'
name|'parts'
op|'='
number|'2'
op|'**'
name|'self'
op|'.'
name|'part_power'
newline|'\n'
name|'self'
op|'.'
name|'devs'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'devs_changed'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'='
number|'0'
newline|'\n'
nl|'\n'
comment|'# _replica2part2dev maps from replica number to partition number to'
nl|'\n'
comment|"# device id. So, for a three replica, 2**23 ring, it's an array of"
nl|'\n'
comment|'# three 2**23 arrays of device ids (unsigned shorts). This can work a'
nl|'\n'
comment|'# bit faster than the 2**23 array of triplet arrays of device ids in'
nl|'\n'
comment|"# many circumstances. Making one big 2**23 * 3 array didn't seem to"
nl|'\n'
comment|"# have any speed change; though you're welcome to try it again (it was"
nl|'\n'
comment|'# a while ago, code-wise, when I last tried it).'
nl|'\n'
name|'self'
op|'.'
name|'_replica2part2dev'
op|'='
name|'None'
newline|'\n'
nl|'\n'
comment|'# _last_part_moves is a 2**23 array of unsigned bytes representing the'
nl|'\n'
comment|'# number of hours since a given partition was last moved. This is used'
nl|'\n'
comment|"# to guarantee we don't move a partition twice within a given number of"
nl|'\n'
comment|"# hours (24 is my usual test). Removing a device or setting it's weight"
nl|'\n'
comment|"# to 0 overrides this behavior as it's assumed those actions are done"
nl|'\n'
comment|'# because of device failure.'
nl|'\n'
comment|'# _last_part_moves_epoch indicates the time the offsets in'
nl|'\n'
comment|'# _last_part_moves is based on.'
nl|'\n'
name|'self'
op|'.'
name|'_last_part_moves_epoch'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'_last_part_moves'
op|'='
name|'None'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'_last_part_gather_start'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'_remove_devs'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'_ring'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|change_min_part_hours
dedent|''
name|'def'
name|'change_min_part_hours'
op|'('
name|'self'
op|','
name|'min_part_hours'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Changes the value used to decide if a given partition can be moved\n        again. This restriction is to give the overall system enough time to\n        settle a partition to its new location before moving it to yet another\n        location. While no data would be lost if a partition is moved several\n        times quickly, it could make that data unreachable for a short period\n        of time.\n\n        This should be set to at least the average full partition replication\n        time. Starting it at 24 hours and then lowering it to what the\n        replicator reports as the longest partition cycle is best.\n\n        :param min_part_hours: new value for min_part_hours\n        """'
newline|'\n'
name|'self'
op|'.'
name|'min_part_hours'
op|'='
name|'min_part_hours'
newline|'\n'
nl|'\n'
DECL|member|get_ring
dedent|''
name|'def'
name|'get_ring'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get the ring, or more specifically, the swift.common.ring.RingData.\n        This ring data is the minimum required for use of the ring. The ring\n        builder itself keeps additional data such as when partitions were last\n        moved.\n        """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'_ring'
op|':'
newline|'\n'
indent|'            '
name|'devs'
op|'='
op|'['
name|'None'
op|']'
op|'*'
name|'len'
op|'('
name|'self'
op|'.'
name|'devs'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'dev'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'devs'
op|'['
name|'dev'
op|'['
string|"'id'"
op|']'
op|']'
op|'='
name|'dict'
op|'('
op|'('
name|'k'
op|','
name|'v'
op|')'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'dev'
op|'.'
name|'items'
op|'('
op|')'
nl|'\n'
name|'if'
name|'k'
name|'not'
name|'in'
op|'('
string|"'parts'"
op|','
string|"'parts_wanted'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_ring'
op|'='
name|'RingData'
op|'('
op|'['
name|'array'
op|'('
string|"'H'"
op|','
name|'p2d'
op|')'
name|'for'
name|'p2d'
name|'in'
name|'self'
op|'.'
name|'_replica2part2dev'
op|']'
op|','
nl|'\n'
name|'devs'
op|','
number|'32'
op|'-'
name|'self'
op|'.'
name|'part_power'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'_ring'
newline|'\n'
nl|'\n'
DECL|member|add_dev
dedent|''
name|'def'
name|'add_dev'
op|'('
name|'self'
op|','
name|'dev'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Add a device to the ring. This device dict should have a minimum of the\n        following keys:\n\n        ======  ===============================================================\n        id      unique integer identifier amongst devices\n        weight  a float of the relative weight of this device as compared to\n                others; this indicates how many partitions the builder will try\n                to assign to this device\n        zone    integer indicating which zone the device is in; a given\n                partition will not be assigned to multiple devices within the\n                same zone ip the ip address of the device\n        port    the tcp port of the device\n        device  the device\'s name on disk (sdb1, for example)\n        meta    general use \'extra\' field; for example: the online date, the\n                hardware description\n        ======  ===============================================================\n\n        .. note::\n            This will not rebalance the ring immediately as you may want to\n            make multiple changes for a single rebalance.\n\n        :param dev: device dict\n        """'
newline|'\n'
name|'if'
name|'dev'
op|'['
string|"'id'"
op|']'
op|'<'
name|'len'
op|'('
name|'self'
op|'.'
name|'devs'
op|')'
name|'and'
name|'self'
op|'.'
name|'devs'
op|'['
name|'dev'
op|'['
string|"'id'"
op|']'
op|']'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Duplicate device id: %d'"
op|'%'
name|'dev'
op|'['
string|"'id'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'while'
name|'dev'
op|'['
string|"'id'"
op|']'
op|'>='
name|'len'
op|'('
name|'self'
op|'.'
name|'devs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'devs'
op|'.'
name|'append'
op|'('
name|'None'
op|')'
newline|'\n'
dedent|''
name|'dev'
op|'['
string|"'weight'"
op|']'
op|'='
name|'float'
op|'('
name|'dev'
op|'['
string|"'weight'"
op|']'
op|')'
newline|'\n'
name|'dev'
op|'['
string|"'parts'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'devs'
op|'['
name|'dev'
op|'['
string|"'id'"
op|']'
op|']'
op|'='
name|'dev'
newline|'\n'
name|'self'
op|'.'
name|'_set_parts_wanted'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devs_changed'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|set_dev_weight
dedent|''
name|'def'
name|'set_dev_weight'
op|'('
name|'self'
op|','
name|'dev_id'
op|','
name|'weight'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Set the weight of a device. This should be called rather than just\n        altering the weight key in the device dict directly, as the builder\n        will need to rebuild some internal state to reflect the change.\n\n        .. note::\n            This will not rebalance the ring immediately as you may want to\n            make multiple changes for a single rebalance.\n\n        :param dev_id: device id\n        :param weight: new weight for device\n        """'
newline|'\n'
name|'self'
op|'.'
name|'devs'
op|'['
name|'dev_id'
op|']'
op|'['
string|"'weight'"
op|']'
op|'='
name|'weight'
newline|'\n'
name|'self'
op|'.'
name|'_set_parts_wanted'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devs_changed'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|remove_dev
dedent|''
name|'def'
name|'remove_dev'
op|'('
name|'self'
op|','
name|'dev_id'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Remove a device from the ring.\n\n        .. note::\n            This will not rebalance the ring immediately as you may want to\n            make multiple changes for a single rebalance.\n\n        :param dev_id: device id\n        """'
newline|'\n'
name|'dev'
op|'='
name|'self'
op|'.'
name|'devs'
op|'['
name|'dev_id'
op|']'
newline|'\n'
name|'dev'
op|'['
string|"'weight'"
op|']'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'_remove_devs'
op|'.'
name|'append'
op|'('
name|'dev'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_set_parts_wanted'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devs_changed'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|rebalance
dedent|''
name|'def'
name|'rebalance'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Rebalance the ring.\n\n        This is the main work function of the builder, as it will assign and\n        reassign partitions to devices in the ring based on weights, distinct\n        zones, recent reassignments, etc.\n\n        The process doesn\'t always perfectly assign partitions (that\'d take a\n        lot more analysis and therefore a lot more time -- I had code that did\n        that before). Because of this, it keeps rebalancing until the device\n        skew (number of partitions a device wants compared to what it has) gets\n        below 1% or doesn\'t change by more than 1% (only happens with ring that\n        can\'t be balanced no matter what -- like with 3 zones of differing\n        weights with replicas set to 3).\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_ring'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_last_part_moves_epoch'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_initial_balance'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devs_changed'
op|'='
name|'False'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'parts'
op|','
name|'self'
op|'.'
name|'get_balance'
op|'('
op|')'
newline|'\n'
dedent|''
name|'retval'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'_update_last_part_moves'
op|'('
op|')'
newline|'\n'
name|'last_balance'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'reassign_parts'
op|'='
name|'self'
op|'.'
name|'_gather_reassign_parts'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_reassign_parts'
op|'('
name|'reassign_parts'
op|')'
newline|'\n'
name|'retval'
op|'+='
name|'len'
op|'('
name|'reassign_parts'
op|')'
newline|'\n'
name|'while'
name|'self'
op|'.'
name|'_remove_devs'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'devs'
op|'['
name|'self'
op|'.'
name|'_remove_devs'
op|'.'
name|'pop'
op|'('
op|')'
op|'['
string|"'id'"
op|']'
op|']'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'balance'
op|'='
name|'self'
op|'.'
name|'get_balance'
op|'('
op|')'
newline|'\n'
name|'if'
name|'balance'
op|'<'
number|'1'
name|'or'
name|'abs'
op|'('
name|'last_balance'
op|'-'
name|'balance'
op|')'
op|'<'
number|'1'
name|'or'
name|'retval'
op|'=='
name|'self'
op|'.'
name|'parts'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'last_balance'
op|'='
name|'balance'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'devs_changed'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'version'
op|'+='
number|'1'
newline|'\n'
name|'return'
name|'retval'
op|','
name|'balance'
newline|'\n'
nl|'\n'
DECL|member|validate
dedent|''
name|'def'
name|'validate'
op|'('
name|'self'
op|','
name|'stats'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Validate the ring.\n\n        This is a safety function to try to catch any bugs in the building\n        process. It ensures partitions have been assigned to distinct zones,\n        aren\'t doubly assigned, etc. It can also optionally check the even\n        distribution of partitions across devices.\n\n        :param stats: if True, check distribution of partitions across devices\n        :returns: if stats is True, a tuple of (device usage, worst stat), else\n                  (None, None)\n        :raises Exception: problem was found with the ring.\n        """'
newline|'\n'
name|'if'
name|'sum'
op|'('
name|'d'
op|'['
string|"'parts'"
op|']'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
op|')'
op|'!='
name|'self'
op|'.'
name|'parts'
op|'*'
name|'self'
op|'.'
name|'replicas'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'All partitions are not double accounted for: %d != %d'"
op|'%'
nl|'\n'
op|'('
name|'sum'
op|'('
name|'d'
op|'['
string|"'parts'"
op|']'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'parts'
op|'*'
name|'self'
op|'.'
name|'replicas'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'stats'
op|':'
newline|'\n'
indent|'            '
name|'dev_usage'
op|'='
name|'array'
op|'('
string|"'I'"
op|','
op|'('
number|'0'
name|'for'
name|'_'
name|'in'
name|'xrange'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'devs'
op|')'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'part'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'parts'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'zones'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'replica'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'dev_id'
op|'='
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replica'
op|']'
op|'['
name|'part'
op|']'
newline|'\n'
name|'if'
name|'stats'
op|':'
newline|'\n'
indent|'                    '
name|'dev_usage'
op|'['
name|'dev_id'
op|']'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'zone'
op|'='
name|'self'
op|'.'
name|'devs'
op|'['
name|'dev_id'
op|']'
op|'['
string|"'zone'"
op|']'
newline|'\n'
name|'if'
name|'zone'
name|'in'
name|'zones'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Partition %d not in %d distinct zones. '"
string|"'Zones were: %s'"
op|'%'
nl|'\n'
op|'('
name|'part'
op|','
name|'self'
op|'.'
name|'replicas'
op|','
nl|'\n'
op|'['
name|'self'
op|'.'
name|'devs'
op|'['
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'r'
op|']'
op|'['
name|'part'
op|']'
op|']'
op|'['
string|"'zone'"
op|']'
nl|'\n'
name|'for'
name|'r'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'zones'
op|'['
name|'zone'
op|']'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'stats'
op|':'
newline|'\n'
indent|'            '
name|'weighted_parts'
op|'='
name|'self'
op|'.'
name|'parts'
op|'*'
name|'self'
op|'.'
name|'replicas'
op|'/'
name|'sum'
op|'('
name|'d'
op|'['
string|"'weight'"
op|']'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
op|')'
newline|'\n'
name|'worst'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'dev'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'dev'
op|'['
string|"'weight'"
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'dev_usage'
op|'['
name|'dev'
op|'['
string|"'id'"
op|']'
op|']'
op|':'
newline|'\n'
indent|'                        '
name|'worst'
op|'='
number|'999.99'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
name|'continue'
newline|'\n'
dedent|''
name|'skew'
op|'='
name|'abs'
op|'('
number|'100.0'
op|'*'
name|'dev_usage'
op|'['
name|'dev'
op|'['
string|"'id'"
op|']'
op|']'
op|'/'
nl|'\n'
op|'('
name|'dev'
op|'['
string|"'weight'"
op|']'
op|'*'
name|'weighted_parts'
op|')'
op|'-'
number|'100.0'
op|')'
newline|'\n'
name|'if'
name|'skew'
op|'>'
name|'worst'
op|':'
newline|'\n'
indent|'                    '
name|'worst'
op|'='
name|'skew'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'dev_usage'
op|','
name|'worst'
newline|'\n'
dedent|''
name|'return'
name|'None'
op|','
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_balance
dedent|''
name|'def'
name|'get_balance'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get the balance of the ring. The balance value is the highest\n        percentage off the desired amount of partitions a given device wants.\n        For instance, if the "worst" device wants (based on its relative weight\n        and its zone\'s relative weight) 123 partitions and it has 124\n        partitions, the balance value would be 0.83 (1 extra / 123 wanted * 100\n        for percentage).\n\n        :returns: balance of the ring\n        """'
newline|'\n'
name|'weighted_parts'
op|'='
name|'self'
op|'.'
name|'parts'
op|'*'
name|'self'
op|'.'
name|'replicas'
op|'/'
name|'sum'
op|'('
name|'d'
op|'['
string|"'weight'"
op|']'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
op|')'
newline|'\n'
name|'balance'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'dev'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'dev'
op|'['
string|"'weight'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'dev'
op|'['
string|"'parts'"
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'balance'
op|'='
number|'999.99'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
name|'continue'
newline|'\n'
dedent|''
name|'dev_balance'
op|'='
name|'abs'
op|'('
number|'100.0'
op|'*'
name|'dev'
op|'['
string|"'parts'"
op|']'
op|'/'
nl|'\n'
op|'('
name|'dev'
op|'['
string|"'weight'"
op|']'
op|'*'
name|'weighted_parts'
op|')'
op|'-'
number|'100.0'
op|')'
newline|'\n'
name|'if'
name|'dev_balance'
op|'>'
name|'balance'
op|':'
newline|'\n'
indent|'                '
name|'balance'
op|'='
name|'dev_balance'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'balance'
newline|'\n'
nl|'\n'
DECL|member|pretend_min_part_hours_passed
dedent|''
name|'def'
name|'pretend_min_part_hours_passed'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Override min_part_hours by marking all partitions as having been moved\n        255 hours ago. This can be used to force a full rebalance on the next\n        call to rebalance.\n        """'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'parts'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_last_part_moves'
op|'['
name|'part'
op|']'
op|'='
number|'0xff'
newline|'\n'
nl|'\n'
DECL|member|_set_parts_wanted
dedent|''
dedent|''
name|'def'
name|'_set_parts_wanted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sets the parts_wanted key for each of the devices to the number of\n        partitions the device wants based on its relative weight. This key is\n        used to sort the devices according to "most wanted" during rebalancing\n        to best distribute partitions.\n        """'
newline|'\n'
name|'weighted_parts'
op|'='
name|'self'
op|'.'
name|'parts'
op|'*'
name|'self'
op|'.'
name|'replicas'
op|'/'
name|'sum'
op|'('
name|'d'
op|'['
string|"'weight'"
op|']'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'dev'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'not'
name|'dev'
op|'['
string|"'weight'"
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|'='
name|'self'
op|'.'
name|'parts'
op|'*'
op|'-'
number|'2'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|'='
name|'int'
op|'('
name|'weighted_parts'
op|'*'
name|'dev'
op|'['
string|"'weight'"
op|']'
op|')'
op|'-'
name|'dev'
op|'['
string|"'parts'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|_initial_balance
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'_initial_balance'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Initial partition assignment is treated separately from rebalancing an\n        existing ring. Initial assignment is performed by ordering all the\n        devices by how many partitions they still want (and kept in order\n        during the process). The partitions are then iterated through,\n        assigning them to the next "most wanted" device, with distinct zone\n        restrictions.\n        """'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'dev'
op|'['
string|"'sort_key'"
op|']'
op|'='
string|"'%08x.%04x'"
op|'%'
op|'('
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|','
name|'randint'
op|'('
number|'0'
op|','
number|'0xffff'
op|')'
op|')'
newline|'\n'
dedent|''
name|'available_devs'
op|'='
name|'sorted'
op|'('
op|'('
name|'d'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
op|')'
op|','
nl|'\n'
name|'key'
op|'='
name|'lambda'
name|'x'
op|':'
name|'x'
op|'['
string|"'sort_key'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_replica2part2dev'
op|'='
op|'['
name|'array'
op|'('
string|"'H'"
op|')'
name|'for'
name|'_'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|']'
newline|'\n'
name|'for'
name|'_'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'parts'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'other_zones'
op|'='
name|'array'
op|'('
string|"'H'"
op|')'
newline|'\n'
name|'for'
name|'replica'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'index'
op|'='
name|'len'
op|'('
name|'available_devs'
op|')'
op|'-'
number|'1'
newline|'\n'
name|'while'
name|'available_devs'
op|'['
name|'index'
op|']'
op|'['
string|"'zone'"
op|']'
name|'in'
name|'other_zones'
op|':'
newline|'\n'
indent|'                    '
name|'index'
op|'-='
number|'1'
newline|'\n'
dedent|''
name|'dev'
op|'='
name|'available_devs'
op|'.'
name|'pop'
op|'('
name|'index'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replica'
op|']'
op|'.'
name|'append'
op|'('
name|'dev'
op|'['
string|"'id'"
op|']'
op|')'
newline|'\n'
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|'-='
number|'1'
newline|'\n'
name|'dev'
op|'['
string|"'parts'"
op|']'
op|'+='
number|'1'
newline|'\n'
name|'dev'
op|'['
string|"'sort_key'"
op|']'
op|'='
string|"'%08x.%04x'"
op|'%'
op|'('
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|','
name|'randint'
op|'('
number|'0'
op|','
number|'0xffff'
op|')'
op|')'
newline|'\n'
name|'index'
op|'='
number|'0'
newline|'\n'
name|'end'
op|'='
name|'len'
op|'('
name|'available_devs'
op|')'
newline|'\n'
name|'while'
name|'index'
op|'<'
name|'end'
op|':'
newline|'\n'
indent|'                    '
name|'mid'
op|'='
op|'('
name|'index'
op|'+'
name|'end'
op|')'
op|'//'
number|'2'
newline|'\n'
name|'if'
name|'dev'
op|'['
string|"'sort_key'"
op|']'
op|'<'
name|'available_devs'
op|'['
name|'mid'
op|']'
op|'['
string|"'sort_key'"
op|']'
op|':'
newline|'\n'
indent|'                        '
name|'end'
op|'='
name|'mid'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'index'
op|'='
name|'mid'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'available_devs'
op|'.'
name|'insert'
op|'('
name|'index'
op|','
name|'dev'
op|')'
newline|'\n'
name|'other_zones'
op|'.'
name|'append'
op|'('
name|'dev'
op|'['
string|"'zone'"
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'_last_part_moves'
op|'='
name|'array'
op|'('
string|"'B'"
op|','
op|'('
number|'0'
name|'for'
name|'_'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'parts'
op|')'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_last_part_moves_epoch'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'dev'
op|'['
string|"'sort_key'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|_update_last_part_moves
dedent|''
dedent|''
name|'def'
name|'_update_last_part_moves'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Updates how many hours ago each partition was moved based on the\n        current time. The builder won\'t move a partition that has been moved\n        more recently than min_part_hours.\n        """'
newline|'\n'
name|'elapsed_hours'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'_last_part_moves_epoch'
op|')'
op|'/'
number|'3600'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'parts'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_last_part_moves'
op|'['
name|'part'
op|']'
op|'='
name|'min'
op|'('
name|'self'
op|'.'
name|'_last_part_moves'
op|'['
name|'part'
op|']'
op|'+'
name|'elapsed_hours'
op|','
number|'0xff'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_last_part_moves_epoch'
op|'='
name|'int'
op|'('
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_gather_reassign_parts
dedent|''
name|'def'
name|'_gather_reassign_parts'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns an array(\'I\') of partitions to be reassigned by gathering them\n        from removed devices and overweight devices.\n        """'
newline|'\n'
name|'reassign_parts'
op|'='
name|'array'
op|'('
string|"'I'"
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_remove_devs'
op|':'
newline|'\n'
indent|'            '
name|'dev_ids'
op|'='
op|'['
name|'d'
op|'['
string|"'id'"
op|']'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'_remove_devs'
name|'if'
name|'d'
op|'['
string|"'parts'"
op|']'
op|']'
newline|'\n'
name|'if'
name|'dev_ids'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'replica'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'part2dev'
op|'='
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replica'
op|']'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'parts'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'part2dev'
op|'['
name|'part'
op|']'
name|'in'
name|'dev_ids'
op|':'
newline|'\n'
indent|'                            '
name|'part2dev'
op|'['
name|'part'
op|']'
op|'='
number|'0xffff'
newline|'\n'
name|'self'
op|'.'
name|'_last_part_moves'
op|'['
name|'part'
op|']'
op|'='
number|'0'
newline|'\n'
name|'reassign_parts'
op|'.'
name|'append'
op|'('
name|'part'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'start'
op|'='
name|'self'
op|'.'
name|'_last_part_gather_start'
op|'/'
number|'4'
op|'+'
name|'randint'
op|'('
number|'0'
op|','
name|'self'
op|'.'
name|'parts'
op|'/'
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_last_part_gather_start'
op|'='
name|'start'
newline|'\n'
name|'for'
name|'replica'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'part2dev'
op|'='
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replica'
op|']'
newline|'\n'
name|'for'
name|'half'
name|'in'
op|'('
name|'xrange'
op|'('
name|'start'
op|','
name|'self'
op|'.'
name|'parts'
op|')'
op|','
name|'xrange'
op|'('
number|'0'
op|','
name|'start'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'part'
name|'in'
name|'half'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'self'
op|'.'
name|'_last_part_moves'
op|'['
name|'part'
op|']'
op|'<'
name|'self'
op|'.'
name|'min_part_hours'
op|':'
newline|'\n'
indent|'                        '
name|'continue'
newline|'\n'
dedent|''
name|'dev'
op|'='
name|'self'
op|'.'
name|'devs'
op|'['
name|'part2dev'
op|'['
name|'part'
op|']'
op|']'
newline|'\n'
name|'if'
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'part2dev'
op|'['
name|'part'
op|']'
op|'='
number|'0xffff'
newline|'\n'
name|'self'
op|'.'
name|'_last_part_moves'
op|'['
name|'part'
op|']'
op|'='
number|'0'
newline|'\n'
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|'+='
number|'1'
newline|'\n'
name|'dev'
op|'['
string|"'parts'"
op|']'
op|'-='
number|'1'
newline|'\n'
name|'reassign_parts'
op|'.'
name|'append'
op|'('
name|'part'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'return'
name|'reassign_parts'
newline|'\n'
nl|'\n'
DECL|member|_reassign_parts
dedent|''
name|'def'
name|'_reassign_parts'
op|'('
name|'self'
op|','
name|'reassign_parts'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        For an existing ring data set, partitions are reassigned similarly to\n        the initial assignment. The devices are ordered by how many partitions\n        they still want and kept in that order throughout the process. The\n        gathered partitions are iterated through, assigning them to devices\n        according to the "most wanted" and distinct zone restrictions.\n        """'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'dev'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'dev'
op|'['
string|"'sort_key'"
op|']'
op|'='
string|"'%08x.%04x'"
op|'%'
op|'('
name|'self'
op|'.'
name|'parts'
op|'+'
nl|'\n'
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|','
name|'randint'
op|'('
number|'0'
op|','
number|'0xffff'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'available_devs'
op|'='
name|'sorted'
op|'('
op|'('
name|'d'
name|'for'
name|'d'
name|'in'
name|'self'
op|'.'
name|'devs'
name|'if'
name|'d'
name|'is'
name|'not'
name|'None'
name|'and'
name|'d'
op|'['
string|"'weight'"
op|']'
op|')'
op|','
nl|'\n'
name|'key'
op|'='
name|'lambda'
name|'x'
op|':'
name|'x'
op|'['
string|"'sort_key'"
op|']'
op|')'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'reassign_parts'
op|':'
newline|'\n'
indent|'            '
name|'other_zones'
op|'='
name|'array'
op|'('
string|"'H'"
op|')'
newline|'\n'
name|'replace'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'replica'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replica'
op|']'
op|'['
name|'part'
op|']'
op|'=='
number|'0xffff'
op|':'
newline|'\n'
indent|'                    '
name|'replace'
op|'='
name|'replica'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'other_zones'
op|'.'
name|'append'
op|'('
name|'self'
op|'.'
name|'devs'
op|'['
nl|'\n'
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replica'
op|']'
op|'['
name|'part'
op|']'
op|']'
op|'['
string|"'zone'"
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'index'
op|'='
name|'len'
op|'('
name|'available_devs'
op|')'
op|'-'
number|'1'
newline|'\n'
name|'while'
name|'available_devs'
op|'['
name|'index'
op|']'
op|'['
string|"'zone'"
op|']'
name|'in'
name|'other_zones'
op|':'
newline|'\n'
indent|'                '
name|'index'
op|'-='
number|'1'
newline|'\n'
dedent|''
name|'dev'
op|'='
name|'available_devs'
op|'.'
name|'pop'
op|'('
name|'index'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_replica2part2dev'
op|'['
name|'replace'
op|']'
op|'['
name|'part'
op|']'
op|'='
name|'dev'
op|'['
string|"'id'"
op|']'
newline|'\n'
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|'-='
number|'1'
newline|'\n'
name|'dev'
op|'['
string|"'parts'"
op|']'
op|'+='
number|'1'
newline|'\n'
name|'dev'
op|'['
string|"'sort_key'"
op|']'
op|'='
string|"'%08x.%04x'"
op|'%'
op|'('
name|'self'
op|'.'
name|'parts'
op|'+'
name|'dev'
op|'['
string|"'parts_wanted'"
op|']'
op|','
nl|'\n'
name|'randint'
op|'('
number|'0'
op|','
number|'0xffff'
op|')'
op|')'
newline|'\n'
name|'index'
op|'='
number|'0'
newline|'\n'
name|'end'
op|'='
name|'len'
op|'('
name|'available_devs'
op|')'
newline|'\n'
name|'while'
name|'index'
op|'<'
name|'end'
op|':'
newline|'\n'
indent|'                '
name|'mid'
op|'='
op|'('
name|'index'
op|'+'
name|'end'
op|')'
op|'//'
number|'2'
newline|'\n'
name|'if'
name|'dev'
op|'['
string|"'sort_key'"
op|']'
op|'<'
name|'available_devs'
op|'['
name|'mid'
op|']'
op|'['
string|"'sort_key'"
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'end'
op|'='
name|'mid'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'index'
op|'='
name|'mid'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'available_devs'
op|'.'
name|'insert'
op|'('
name|'index'
op|','
name|'dev'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'dev'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'dev'
op|'['
string|"'sort_key'"
op|']'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
