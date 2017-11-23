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
This module performs operations related to network control policies.
"""

from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac
from ucsmsdk.ucsexception import UcsOperationError


def nwctrl_policy_create(handle, name=None,
                         org_dn="org-root",
                         cdp="disabled",
                         descr=None,
                         lldp_receive="disabled",
                         lldp_transmit="disabled",
                         mac_register_mode="only-native-vlan",
                         uplink_fail_action="link-down",
                         forge="allow",
                         **kwargs):

    """
    Creates network control policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        cdp (string): cdp ["enabled", "disabled"]
        descr (string): description
        lldp_receive (string): receive lldp  ["enabled", "disabled"]
        lldp_transmit (string): transmit lldp ["enabled", "disabled"]
        mac_register_mode (string): mac register mode
                                    ["all-host-vlans", "only-native-vlan"]
        uplink_fail_action (string): ["link-down", "warning"]
        forge (string): mac security forged transmits ["allow", "deny"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        NwctrlDefinition: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        nwctrl_policy_create(handle,
                             name="cdp_enable",
                             descr="enable cdp")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("nwctrl_policy_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = NwctrlDefinition(parent_mo_or_dn=org_dn, name=name,
                          cdp=cdp, descr=descr,
                          lldp_receive=lldp_receive,
                          lldp_transmit=lldp_transmit,
                          mac_register_mode=mac_register_mode,
                          uplink_fail_action=uplink_fail_action)
    mo1 = DpsecMac(parent_mo_or_dn=mo, forge=forge)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def nwctrl_policy_get(handle, name=None,
                      org_dn="org-root",
                      caller="nwctrl_policy_get"):

    """
    Gets network control policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        StoragenwctrlConfigPolicy: managed object

    Raises:
        UcsOperationError: if StoragenwctrlConfigPolicy is not present

    Example:
        nwctrl_policy_get(handle,
                          name="SD_Boot",
                          org_dn="org-root")
    """

    dn = org_dn + "/nwctrl-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "network control policy {} \
                                does not exist".format(dn))
    return mo


def nwctrl_policy_exists(handle, name=None,
                         org_dn="org-root", **kwargs):

    """
    checks if policy exists

    Args:
        handle (UcsHandle)
        name (string): Name of network control policy
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, StoragenwctrlConfigPolicy MO/None)

    Raises:
        None

    Example:
        nwctrl_policy_exists:(handle,
                              name="SD_Boot",
                              org_dn="org-root")
    """

    try:
        mo = nwctrl_policy_get(handle=handle, name=name, org_dn=org_dn,
                               caller="nwctrl_policy_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def nwctrl_policy_modify(handle, name=None,
                         org_dn="org-root", **kwargs):

    """
    modifies policy

    Args:
        handle (UcsHandle)
        name (string): Name of policy
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        StoragenwctrlConfigPolicy: managed object

    Raises:
        UcsOperationError: if StoragenwctrlConfigPolicy is not present

    Example:
        nwctrl_policy_modify(handle,
                             name="cdp_enable",
                             descr="prod network control policy")
    """

    mo = nwctrl_policy_get(handle=handle, name=name, org_dn=org_dn,
                           caller="nwctrl_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def nwctrl_policy_delete(handle, name=None, org_dn="org-root"):

    """
    deletes policy

    Args:
        handle (UcsHandle)
        name (string): Name of policy
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if  is not present

    Example:
        nwctrl_policy_delete(handle,
                             name="test-pool",
                             org_dn="org-root")
    """

    mo = nwctrl_policy_get(handle=handle, name=name, org_dn=org_dn,
                           caller="nwctrl_policy_delete")
    handle.remove_mo(mo)
    handle.commit()
