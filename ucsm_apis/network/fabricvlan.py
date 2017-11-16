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

from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.ucsexception import UcsOperationError


def vlan_create(handle, org_dn="fabric/lan",
                name=None, id=None,
                sharing=None, **kwargs):

    """
    Creates vlans

    Args:
        handle (UCSHandle)
        org_dn (string): org dn
        name (string): vlan name
        id (string): vlan id number
        sharing(string): sharing type ["community",
                                       "isolated",
                                       "none",
                                       "primary"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        FabricVlan: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        vlan_create(handle,
                    name="vmotion",
                    id="400")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("vlan_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = FabricVlan(parent_mo_or_dn=obj, id=id,
                    name=name, sharing=sharing)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def vlan_get(handle, name=None, org_dn="fabric/lan",
             caller="vlan_get"):

    """
    Gets vlan

    Args:
        handle (UCSHandle)
        org_dn (string): org dn
        name (string): vlan name
        caller (string): caller method name

    Returns:
        FabricVlan: managed object

    Raises:
        UcsOperationError: if FabricVlan is not present

    Example:
        vlan_get(handle,
                 name="test")
    """

    dn = org_dn + "/net-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "vlan {} "
                                "does not exist".format(dn))
    return mo


def vlan_exists(handle, name=None, org_dn="fabric/lan",
                **kwargs):

    """
    checks if vlan exists

    Args:
        handle (UCSHandle)
        org_dn (string): org dn
        name (string): vlan name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, FabricVlan MO/None)

    Raises:
        None

    Example:
        vlan_exists:(handle,
                     name="test")
    """

    try:
        mo = vlan_get(handle=handle, name=name,
                      org_dn=org_dn, caller="vlan_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def vlan_modify(handle, name=None,
                org_dn="fabric/lan", **kwargs):

    """
    modifies vlan

    Args:
        handle (UCSHandle)
        org_dn (string): org dn
        name (string): vlan name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        FabricVlan: managed object

    Raises:
        UcsOperationError: if FabricVlan is not present

    Example:
        vlan_modify(handle,
                    name="test",
                    sharing="community")
    """

    mo = vlan_get(handle=handle, name=name,
                  org_dn=org_dn, caller="vlan_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def vlan_delete(handle, name=None,
                org_dn="fabric/lan", **kwargs):

    """
    Deletes vlan

    Args:
        handle (UCSHandle)
        org_dn (string): org dn
        name (string): vlan name
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        None

    Raises:
        UcsOperationError: if if FabricVlan is not present

    Example:
        vlan_delete(handle,
                    name="test")
    """

    dn = org_dn + "/net-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("vlan_delete", "vlan {} "
                                "does not exist".format(dn))

    handle.remove_mo(mo)
    handle.commit()
