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

from ucsmsdk.mometa.fabric.FabricDceSwSrvEp import FabricDceSwSrvEp
from ucsmsdk.ucsexception import UcsOperationError


def fabric_svr_enable(handle, fabric=None,
                      slot_id=None, port_id=None,
                      **kwargs):

    """
    Enables fabric server port

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        FabricDceSwSrvEp: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        fabric_eth_enable(handle,
                           fabric="A",
                           slot_id="1",
                           port_id="2")
    """

    org_dn = "fabric/server/sw-" + fabric
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("fabric_svr_enable", "Org {} \
                                 does not exist".format(org_dn))

    mo = FabricDceSwSrvEp(parent_mo_or_dn=obj, admin_state="enabled",
                        port_id=port_id, slot_id=slot_id)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def fabric_svr_get(handle, fabric=None,
                   slot_id=None, port_id=None,
                   caller="fabric_svr_get"):

    """
    Gets fabric ethernet server port

    Args:
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        caller (string): caller method name

    Returns:
        FabricDceSwSrvEp: managed object

    Raises:
        UcsOperationError: if FabricDceSwSrvEp is not present

    Example:
        fabric_svr_get(handle,
                        fabric="A",
                        slot_id="1",
                        port_id="2")
    """

    dn = "fabric/server/sw-" + fabric + "/slot-" + slot_id + "-port-" + port_id
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "Fabric port {} \
                                does not exist".format(dn))
    return mo


def fabric_svr_exists(handle, fabric=None, slot_id=None,
                   port_id=None, **kwargs):

    """
    checks if fabric server port exists

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, FabricDceSwSrvEp MO/None)

    Raises:
        None

    Example:
        fabric_svr_exists:(handle,
                           fabric="A",
                           slot_id="1",
                           port_id="2")
    """

    try:
        mo = fabric_svr_get(handle=handle, fabric=fabric,
                            slot_id=slot_id,
                            port_id=port_id,
                            caller="fabric_svr_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def fabric_svr_modify(handle, fabric=None, slot_id=None,
                      port_id=None, **kwargs):

    """
    modifies fabric server port

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        slot_id (string): Fabric slot number
        port_id (string): port number
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        FabricDceSwSrvEp: managed object

    Raises:
        UcsOperationError: if FabricDceSwSrvEp is not present

    Example:
        fabric_svr_modify(handle,
                          fabric="A",
                          slot_id="1",
                          port_id="2")
    """

    mo = fabric_svr_get(handle=handle, fabric=fabric,
                        slot_id=slot_id,
                        port_id=port_id,
                        caller="fabric_svr_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def fabric_svr_disable(handle, fabric=None,
                       slot_id=None, port_id=None,
                       **kwargs):

    """
    Disables fabric server port

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
        UcsOperationError: if if FabricDceSwSrvEp is not present

    Example:
        fabric_svr_disable(handle,
                          fabric="A",
                          slot_id="1",
                          port_id="2")
    """

    dn = "fabric/server/sw-" + fabric + "/slot-" + slot_id + "-port-" + port_id
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("fabric_svr_disable", "Org {} \
                                 does not exist".format(dn))

    handle.remove_mo(mo)
    handle.commit()
    return mo
