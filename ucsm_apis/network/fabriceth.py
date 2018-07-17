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
This module performs operations related to Fabric Ethernet Lan Ports.
"""

from ucsmsdk.mometa.fabric.FabricEthLanEp import FabricEthLanEp
from ucsmsdk.ucsexception import UcsOperationError


def fabric_eth_enable(handle, fabric=None,
                      slot_id=None, port_id=None,
                      **kwargs):

    """
    Enables fabric ethernet lan port

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        FabricEthLanEp: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        fabric_eth_enable(handle,
                           fabric="A",
                           slot_id="1",
                           port_id="2")
    """

    org_dn = "fabric/lan/" + fabric
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("fabric_eth_enable", "Org {} \
                                 does not exist".format(org_dn))

    mo = FabricEthLanEp(parent_mo_or_dn=obj, admin_state="enabled",
                        port_id=port_id, slot_id=slot_id,
                        admin_speed="10gbps")
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def fabric_eth_get(handle, fabric=None,
                   slot_id=None, port_id=None,
                   caller="fabric_eth_get"):

    """
    Gets fabric ethernet lan port

    Args:
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        caller (string): caller method name

    Returns:
        FabricEthLanEp: managed object

    Raises:
        UcsOperationError: if FabricEthLanEp is not present

    Example:
        fabric_eth_get(handle,
                        fabric="A",
                        slot_id="1",
                        port_id="2")
    """

    dn = "fabric/lan/" + fabric + "/phys-slot-" + slot_id + "-port-" + port_id
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "Fabric port {} \
                                does not exist".format(dn))
    return mo


def fabric_eth_exists(handle, fabric=None, slot_id=None,
                   port_id=None, **kwargs):

    """
    checks if fabric ethernel lan port exists

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, FabricEthLanEp MO/None)

    Raises:
        None

    Example:
        fabric_eth_exists:(handle,
                           fabric="A",
                           slot_id="1",
                           port_id="2")
    """

    try:
        mo = fabric_eth_get(handle=handle, fabric=fabric,
                            slot_id=slot_id,
                            port_id=port_id,
                            caller="fabric_eth_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def fabric_eth_modify(handle, fabric=None, slot_id=None,
                      port_id=None, **kwargs):

    """
    modifies ip pool

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        FabricEthLanEp: managed object

    Raises:
        UcsOperationError: if FabricEthLanEp is not present

    Example:
        fabric_eth_modify(handle,
                          fabric="A",
                          slot_id="1",
                          port_id="2")
    """

    mo = fabric_eth_get(handle=handle, fabric=fabric,
                        slot_id=slot_id,
                        port_id=port_id,
                        caller="fabric_eth_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def fabric_eth_disable(handle, fabric=None,
                       slot_id=None, port_id=None,
                       **kwargs):

    """
    Disables fabric ethernet lan port

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        None

    Raises:
        UcsOperationError: if if FabricEthLanEp is not present

    Example:
        fabric_eth_disable(handle,
                          fabric="A",
                          slot_id="1",
                          port_id="2")
    """

    org_dn = "fabric/lan/" + fabric
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("fabric_eth_enable", "Org {} \
                                 does not exist".format(org_dn))

    mo = FabricEthLanEp(parent_mo_or_dn=obj, admin_state="disabled",
                        port_id=port_id, slot_id=slot_id)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo
