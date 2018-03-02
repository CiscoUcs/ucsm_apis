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
This module performs operations related to Fabric Port Channels.
"""

from ucsmsdk.mometa.fabric.FabricEthLanPc import FabricEthLanPc
from ucsmsdk.mometa.fabric.FabricEthLanPcEp import FabricEthLanPcEp
from ucsmsdk.ucsexception import UcsOperationError


def fabric_pc_create(handle, fabric=None,
                     name=None, pc_id=None,
                     ports=None,
                     **kwargs):

    """
    Creates fabric portchannel

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        name (string): Portchannel name
        pc_id (string): portchannel id number
        ports (list): List of port members in the portchannel
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        FabricEthLanPc: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        fabric_pc_create(handle,
                           fabric="A",
                           name="vpc-nexus-a"
                           pc_id="10",
                           ports=["1/1", "1/2"]
    """

    org_dn = "fabric/lan/" + fabric
    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("fabric_pc_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = FabricEthLanPc(parent_mo_or_dn=obj, admin_state="enabled",
                        name=name, port_id=pc_id,)
    mo.set_prop_multiple(**kwargs)

    port_list = [p.split("/") for p in ports]
    mo_list = []
    for port in port_list:
        mop = FabricEthLanPcEp(parent_mo_or_dn=mo, admin_state="enabled",
                               auto_negotiate="yes",
                               eth_link_profile_name="default",
                               slot_id=port[0], port_id=port[1])
        mo_list.append(mop)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def fabric_pc_get(handle, fabric=None,
                  pc_id=None,
                  caller="fabric_pc_get"):

    """
    Gets fabric port channel

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        pc_id (string): portchannel id number
        caller (string): caller method name

    Returns:
        FabricEthLanPc: managed object

    Raises:
        UcsOperationError: if FabricEthLanPc is not present

    Example:
        fabric_pc_get(handle,
                      fabric="A",
                      pc_id="1")
    """

    dn = "fabric/lan/" + fabric + "/pc-" + pc_id
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "Fabric port {} \
                                does not exist".format(dn))
    return mo


def fabric_pc_exists(handle, fabric=None, pc_id=None,
                     **kwargs):

    """
    checks if fabric port channel exists

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        pc_id (string): portchannel id number
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, FabricEthLanPc MO/None)

    Raises:
        None

    Example:
        fabric_pc_exists:(handle,
                          fabric="A",
                          pc_id="13")
    """

    try:
        mo = fabric_pc_get(handle=handle, fabric=fabric,
                           pc_id=pc_id,
                           caller="fabric_pc_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def fabric_pc_modify(handle, fabric=None,
                     pc_id=None, **kwargs):

    """
    modifies fabric port channel

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        pc_id (string): port channel id number
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        FabricEthLanPc: managed object

    Raises:
        UcsOperationError: if FabricEthLanPc is not present

    Example:
        fabric_pc_modify(handle,
                         fabric="A",
                         pc_id)
    """

    mo = fabric_pc_get(handle=handle, fabric=fabric,
                       pc_id=pc_id,
                       caller="fabric_pc_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def fabric_pc_delete(handle, fabric=None,
                     pc_id=None,
                     **kwargs):

    """
    Deletes fabric port channel

    Args:
        handle (UCSHandle)
        fabric (string): Fabric A or B
        pc_id (string): port channel id number
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        None

    Raises:
        UcsOperationError: if if FabricEthLanPc is not present

    Example:
        fabric_pc_delete(handle,
                         fabric="A",
                         pc_id="13")
    """

    org_dn = "fabric/lan/" + fabric + "/pc-" + pc_id
    mo = handle.query_dn(org_dn)
    if not mo:
        raise UcsOperationError("fabric_pc_delete", "Org {} \
                                 does not exist".format(org_dn))
    handle.remove_mo(mo)
    handle.commit()
