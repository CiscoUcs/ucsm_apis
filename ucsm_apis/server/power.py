# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..utils.utils import blade_dn_get
from ..utils.utils import rack_dn_get
from ucsmsdk.ucsexception import UcsOperationError


def server_power_on(handle, chassis_id=None, balde_id=None, rack_id=None):
    pass


def server_power_off(handle, chassis_id=None, balde_id=None, rack_id=None):
    pass


def _server_admin_state_set(
        handle,
        chassis_id=None,
        blade_id=None,
        rack_id=None,
        state=None):
    if chassis_id and blade_id:
        dn = blade_dn_get(chassis_id, blade_id)
    elif rack_id:
        dn = rack_dn_get(rack_id)
    else:
        UcsOperationError(
            "server_admin_state_set: Failed to set power state",
            "Missing mandatory arguments. Specify either of, \
            (chassis_id, blade_id) or rack_id")

    mo = handle.query_dn(dn)
    if mo is None:
        UcsOperationError(
            "_server_admin_state_set",
            "server %s not found" %
            (dn))

    mo.admin_power = state
    handle.set_mo(mo)
    handle.commit()


def server_power_cycle_wait(
        handle,
        chassis_id=None,
        blade_id=None,
        rack_id=None):
    _server_admin_state_set(
        handle=handle,
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id,
        state="cycle-wait")


def server_power_cycle_immediate(
        handle,
        chassis_id=None,
        blade_id=None,
        rack_id=None):
    _server_admin_state_set(
        handle=handle,
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id,
        state="cycle-immediate")
