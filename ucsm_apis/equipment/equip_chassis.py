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

"""
This module performs operations related to chassis equipment.
"""

from ucsmsdk.mometa.equipment.EquipmentChassis import EquipmentChassis
from ucsmsdk.ucsexception import UcsOperationError


def chassis_ack(handle, id=None, **kwargs):

    """
    Acknowledges chassis

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        EquipmentChassis: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        chassis_ack(handle, id="1")
    """

    org_dn = "sys"
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("chassis_ack", "Org {} \
                                 does not exist".format(org_dn))

    mo = EquipmentChassis(parent_mo_or_dn=obj, admin_state="acknowledged",
                          id=id)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def chassis_reack(handle, id=None, **kwargs):

    """
    Re-acknowledges chassis

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        EquipmentChassis: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        chassis_reack(handle, id="1")
    """

    org_dn = "sys"
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("chassis_ack", "Org {} \
                                 does not exist".format(org_dn))

    mo = EquipmentChassis(parent_mo_or_dn=obj, admin_state="re-acknowledged",
                          id=id)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def chassis_decomm(handle, id=None, **kwargs):

    """
    Decommission chassis so it can be removed or acknowledged.

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        EquipmentChassis: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        chassis_decomm(handle, id="1")
    """

    org_dn = "sys"
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("chassis_decomm", "Org {} \
                                 does not exist".format(org_dn))

    mo = EquipmentChassis(parent_mo_or_dn=obj, admin_state="decommission",
                          id=id)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def chassis_get(handle, id=None,
                caller="chassis_get"):

    """
    Gets chassis

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        caller (string): caller method name

    Returns:
        EquipmentChassis: managed object

    Raises:
        UcsOperationError: if EquipmentChassis is not present

    Example:
        fabric_svr_get(handle,
                       id="1")
    """

    dn = "sys/chassis-" + id
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "Chassis {} \
                                does not exist".format(dn))
    return mo


def chassis_exists(handle, id=None, **kwargs):

    """
    checks if chassis exists

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, EquipmentChassis MO/None)

    Raises:
        None

    Example:
        chassis_exists:(handle,
                        id="1")
    """

    try:
        mo = chassis_get(handle=handle, id=id,
                         caller="chassis_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def chassis_modify(handle, id=None, **kwargs):

    """
    modifies chassis

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        EquipmentChassis: managed object

    Raises:
        UcsOperationError: if EquipmentChassis is not present

    Example:
        chassis_modify(handle,
                          fabric="A",
                          id="1",
                          usr_lbl="Prod")
    """

    mo = chassis_get(handle=handle, id=id,
                     caller="chassis_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def chassis_remove(handle, id=None, **kwargs):

    """
    Removes chassis

    Args:
        handle (UCSHandle)
        id (string): Chassis ID
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        EquipmentChassis: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        chassis_remove(handle, id="1")
    """

    org_dn = "sys"
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("chassis_remove", "Org {} \
                                 does not exist".format(org_dn))

    mo = EquipmentChassis(parent_mo_or_dn=obj, admin_state="remove",
                          id=id)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo
