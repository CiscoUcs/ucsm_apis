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
This module performs the operation related to role.
"""
from ucsmsdk.ucsexception import UcsOperationError

_user_dn = "sys/user-ext"


def role_create(handle, name, priv="read-only", policy_owner="local",
                descr=None, **kwargs):
    """
    creates a role

    Args:
        handle (UcsHandle)
        name (string): role name
        priv (comma separated string): role privilege
         valid values are "aaa", "admin", "ext-lan-config", "ext-lan-policy",
          "ext-lan-qos", "ext-lan-security", "ext-san-config",
          "ext-san-policy", "ext-san-qos", "ext-san-security", "fault",
          "ls-compute", "ls-config", "ls-config-policy", "ls-ext-access",
          "ls-network", "ls-network-policy", "ls-qos", "ls-qos-policy",
          "ls-security", "ls-security-policy", "ls-server", "ls-server-oper",
          "ls-server-policy", "ls-storage", "ls-storage-policy", "operations",
          "org-management", "pn-equipment", "pn-maintenance", "pn-policy",
          "pn-security", "pod-config", "pod-policy", "pod-qos", "pod-security",
          "power-mgmt", "read-only"
        policy_owner: policy owner
         valid values are "local", "pending-policy", "policy"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaRole: managed object

    Raises:
        None

    Example:
        role_create(handle, name="test_role", priv="admin")
    """
    from ucsmsdk.mometa.aaa.AaaRole import AaaRole

    mo = AaaRole(parent_mo_or_dn=_user_dn,
                 name=name,
                 priv=priv,
                 policy_owner=policy_owner,
                 descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def role_get(handle, name, caller="role_get"):
    """
    gets a role

    Args:
        handle (UcsHandle)
        name (string): role name
        caller (string): name of the caller function

    Returns:
        AaaRole: managed object

    Raises:
        UcsOperationError: if AaaRole is not present

    Example:
        role_get(handle, name="test_role")
    """
    dn = _user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "Role '%s' does not exist" % dn)
    return mo


def role_exists(handle, name, **kwargs):
    """
    checks if a role exists

    Args:
        handle (UcsHandle)
        name (string): role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaRole MO/None)

    Raises:
        None

    Example:
        role_exists(handle, name="test_role", priv="read-only")
    """
    try:
        mo = role_get(handle, name, "role_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def role_modify(handle, name, **kwargs):
    """
    modifies role

    Args:
        handle (UcsHandle)
        name (string): role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaRole: managed object

    Raises:
        UcsOperationError: if AaaRole is not present

    Example:
        role_modify(handle, name="test_role", priv="read-only")
    """
    mo = role_get(handle, name, "role_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def role_delete(handle, name):
    """
    deletes role

    Args:
        handle (UcsHandle)
        name (string): role name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaRole is not present

    Example:
        role_delete(handle, name="test_role")
    """
    mo = role_get(handle, name, caller="role_delete")
    handle.remove_mo(mo)
    handle.commit()
