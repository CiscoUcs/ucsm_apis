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
This module performs operations related to power control policies.
"""

from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy
from ucsmsdk.ucsexception import UcsOperationError


def powerctrl_policy_create(handle, name=None,
                            org_dn="org-root", descr=None,
                            fan_speed="any",
                            prio="no-cap",
                            **kwargs):

    """
    Creates power control policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        fan_speed (string): fan speed ["any", "balanced", "err",
                            "high-power", "low-power", "max-power",
                            "na", "no-update", "not-supported",
                            "performance"]
        descr (string): description
        prio (string): power allocation ["no-cap", "utility"], ["1-10"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        PowerPolicy: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        powerctrl_policy_create(handle,
                                name="no_cap",
                                descr="no power cap")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("powerctrl_policy_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = PowerPolicy(parent_mo_or_dn=org_dn, name=name,
                     descr=descr,
                     fan_speed=fan_speed,
                     prio=prio)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def powerctrl_policy_get(handle, name=None,
                         org_dn="org-root",
                         caller="powerctrl_policy_get"):

    """
    Gets power control policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        PowerPolicy: managed object

    Raises:
        UcsOperationError: if PowerPolicy is not present

    Example:
        powerctrl_policy_get(handle,
                             name="no-power-cap",
                             org_dn="org-root")
    """

    dn = org_dn + "/power-policy-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "power control policy {} \
                                does not exist".format(dn))
    return mo


def powerctrl_policy_exists(handle, name=None,
                            org_dn="org-root", **kwargs):

    """
    checks if policy exists

    Args:
        handle (UcsHandle)
        name (string): Name of power control policy
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, PowerPolicy MO/None)

    Raises:
        None

    Example:
        powerctrl_policy_exists:(handle,
                                 name="no-power-cap",
                                 org_dn="org-root")
    """

    try:
        mo = powerctrl_policy_get(handle=handle, name=name, org_dn=org_dn,
                                  caller="powerctrl_policy_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def powerctrl_policy_modify(handle, name=None,
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
        PowerPolicy: managed object

    Raises:
        UcsOperationError: if PowerPolicy is not present

    Example:
        powerctrl_policy_modify(handle,
                                name="no-power-cap",
                                descr="prod power control policy")
    """

    mo = powerctrl_policy_get(handle=handle, name=name, org_dn=org_dn,
                              caller="powerctrl_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def powerctrl_policy_delete(handle, name=None, org_dn="org-root"):

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
        powerctrl_policy_delete(handle,
                                name="test-pool",
                                org_dn="org-root")
    """

    mo = powerctrl_policy_get(handle=handle, name=name, org_dn=org_dn,
                              caller="powerctrl_policy_delete")
    handle.remove_mo(mo)
    handle.commit()
