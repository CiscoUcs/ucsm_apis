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
This module performs the operation related to user.
"""
from ucsmsdk.ucsexception import UcsOperationError
_base_dn = "fabric/lan"


def vlan_create(handle, name, id, sharing=None, mcast_policy_name=None, policy_owner=None,
                default_net=None, compression_type=None, **kwargs):
    """
        creates vlan
        Args:
            handle (UcsHandle)
            name (string): VLAN name
            sharing (string): sharing, valid values "community", "isolated", "none", "primary"
            mcast_policy_name (string):
            policy_owner (string): "local", "pending-policy", "policy"
            default_net (string): "false", "no", "true", "yes"
            compression_type (string): "excluded", "included"
            **kwargs: Any additional key-value pair of managed object(MO)'s
                      property and value, which are not part of regular args.
                      This should be used for future version compatibility.
        Returns:
            FabricVlan: managed object
        Raises:
            None
        Example:
            vlan_create(handle, name="test", id=2, sharing="none", mcast_policy_name="", policy_owner="local",
                        default_net="no", compression_type="included")
        """
    from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
    vlan = FabricVlan(parent_mo_or_dn=_base_dn, name=name, sharing=sharing, id=id,
                      mcast_policy_name=mcast_policy_name,
                      policy_owner=policy_owner, default_net=default_net, compression_type=compression_type)

    vlan.set_prop_multiple(**kwargs)
    handle.add_mo(vlan, modify_present=True)
    handle.commit()
    return vlan

def vlan_get(handle, name, caller="vlan_get"):
    """
    gets user

    Args:
        handle (UcsHandle)
        name (string): vlan name

    Returns:
        FabricVlan: managed object

    Raises:
        UcsOperationError: if FabricVlan is not present

    Example:
        vlan_get(handle, name="test")
    """
    dn = _base_dn + "/net-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "VLAN '%s' does not exist" % dn)
    return mo

def vlan_delete(handle, name):
    """
    deletes vlan

    Args:
        handle (UcsHandle)
        name (string): vlan name

    Returns:
        None

    Raises:
        UcsOperationError: if FabricVlan is not present

    Example:
        user_delete(handle, name="test")

    """
    mo = vlan_get(handle, name, "vlan_delete")
    handle.remove_mo(mo)
    handle.commit()

def vlan_modify(handle, name, **kwargs):
    """
    modifies vlan

    Args:
        handle (UcsHandle)
        name (string): vlan name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        FabricVlan: managed object

    Raises:
        UcsOperationError: if AaaUser is not present

    Example:
        vlan_modify(handle, name="test", id=2, sharing="none", mcast_policy_name="", policy_owner="local",
                        default_net="no", compression_type="included")
    """
    mo = vlan_get(handle, name, "vlan_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo
