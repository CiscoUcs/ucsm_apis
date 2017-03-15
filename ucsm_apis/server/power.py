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
from ucsmsdk.mometa.ls.LsPower import LsPowerConsts
from ucsmsdk.mometa.ls.LsPower import LsPower


def _server_dn_get(chassis_id=None, blade_id=None, rack_id=None):
    if chassis_id and blade_id:
        dn = blade_dn_get(chassis_id, blade_id)
    elif rack_id:
        dn = rack_dn_get(rack_id)
    else:
        raise UcsOperationError(
            "server_admin_state_set: Failed to set power state",
            "Missing mandatory arguments. Specify either of "\
            "(chassis_id, blade_id) or rack_id")
    return dn


def _service_profile_power_set(
        handle,
        chassis_id=None,
        blade_id=None,
        rack_id=None,
        state=None):
    dn = _server_dn_get(
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id)
    blade_mo = handle.query_dn(dn)
    if blade_mo is None:
        raise UcsOperationError(
            "server_power_set: Failed to set server power",
            "server %s does not exist" % (dn))

    if blade_mo.assigned_to_dn is None:
        raise UcsOperationError(
            "server_power_set: Failed to set server power",
            "server %s is not associated to a service profile" % (dn))

    sp_mo = handle.query_dn(blade_mo.assigned_to_dn)
    LsPower(
        parent_mo_or_dn=sp_mo,
        state=state)
    handle.set_mo(sp_mo)
    handle.commit()


def server_power_on(handle, chassis_id=None, blade_id=None, rack_id=None):
    """
    Power-On the server.

    Args:
        handle (UcscHandle)
        chassis_id (int): chassis id
        blade_id (int): blade id
        rack_id (int): rack id

    Returns:
        None

    Raises:
        UcsOperationError

    Example:
        server_power_on(handle, chassis_id=1, blade_id=2)
        server_power_on(handle, rack_id=1)
    """
    _service_profile_power_set(
        handle=handle,
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id,
        state=LsPowerConsts.STATE_UP)


def server_power_off(handle, chassis_id=None, blade_id=None, rack_id=None):
    """
    Power-Off the server.

    Args:
        handle (UcscHandle)
        chassis_id (int): chassis id
        blade_id (int): blade id
        rack_id (int): rack id

    Returns:
        None

    Raises:
        UcsOperationError

    Example:
        server_power_off(handle, chassis_id=1, blade_id=2)
        server_power_off(handle, rack_id=1)
    """

    _service_profile_power_set(
        handle=handle,
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id,
        state=LsPowerConsts.STATE_DOWN)


def _server_admin_power_set(
        handle,
        chassis_id=None,
        blade_id=None,
        rack_id=None,
        state=None):
    dn = _server_dn_get(
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id)
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(
            "_server_admin_power_set",
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
    """
    Triggers a graceful OS shutdown and powercycle operation on the specified server.

    Args:
        handle (UcscHandle)
        chassis_id (int): chassis id
        blade_id (int): blade id
        rack_id (int): rack id

    Returns:
        None

    Raises:
        UcsOperationError

    Example:
        server_power_cycle_wait(handle, chassis_id=1, blade_id=2)
        server_power_cycle_wait(handle, rack_id=1)
    """

    _server_admin_power_set(
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
    """
    Triggers an immediate powercycle operation on the specified server.

    Args:
        handle (UcscHandle)
        chassis_id (int): chassis id
        blade_id (int): blade id
        rack_id (int): rack id

    Returns:
        None

    Raises:
        UcsOperationError

    Example:
        server_power_cycle_immediate(handle, chassis_id=1, blade_id=2)
        server_power_cycle_immediate(handle, rack_id=1)
    """

    _server_admin_power_set(
        handle=handle,
        chassis_id=chassis_id,
        blade_id=blade_id,
        rack_id=rack_id,
        state="cycle-immediate")
