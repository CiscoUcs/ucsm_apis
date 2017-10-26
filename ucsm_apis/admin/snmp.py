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
This module performs the operation related to snmp server, user and traps.
"""
from ucsmsdk.ucsexception import UcsOperationError

_base_dn = "sys/svc-ext"


def snmp_config_get(handle, caller="snmp_config_get"):
    """
    gets snmp config

    Args:
        handle (UcsHandle)
        caller (string): name of the caller function

    Returns:
        CommSnmp: managed object

    Raises:
        UcsOperationError: if CommSnmp is not present

    Example:
        mo = snmp_config_get(handle)
    """
    dn = _base_dn + "/snmp-svc"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "SNMP Config '%s' does not exist." % dn)
    return mo


def snmp_enable(handle, policy_owner="local", is_set_snmp_secure="no",
                descr="SNMP Service", community=None, sys_contact=None,
                sys_location=None, **kwargs):
    """
    Enables SNMP.

    Args:
        handle (UcsHandle)
        policy_owner (string): policy owner
         valid values are "local", "pending-policy", "policy"
        is_set_snmp_secure (string): valid values are "yes", "no"
        descr (string): description
        community (string): community
        sys_contact (string): system contact
        sys_location (string): system location
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommSnmp: managed object

    Raises:
        UcsOperationError: if CommSnmp is not present

    Example:
        mo = snmp_enable(handle,
                         community="username",
                         sys_contact="user contact",
                         sys_location="user location",
                         descr="SNMP Service")

    """
    from ucsmsdk.mometa.comm.CommSnmp import CommSnmpConsts

    mo = snmp_config_get(handle, caller="snmp_enable")

    args = {'admin_state': CommSnmpConsts.ADMIN_STATE_ENABLED,
            'policy_owner': policy_owner,
            'is_set_snmp_secure': is_set_snmp_secure,
            'descr': descr,
            'community': community,
            'sys_contact': sys_contact,
            'sys_location': sys_location
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_disable(handle):
    """
    disables SNMP

    Args:
        handle (UcsHandle)

    Returns:
        CommSnmp: managed object

    Raises:
        UcsOperationError: if CommSnmp Mo is not present

    Example:
        snmp_disable(handle)
    """
    from ucsmsdk.mometa.comm.CommSnmp import CommSnmpConsts

    mo = snmp_config_get(handle, "snmp_disable")

    args = {'admin_state': CommSnmpConsts.ADMIN_STATE_DISABLED}

    mo.set_prop_multiple(**args)

    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_exists(handle, **kwargs):
    """
    checks if snmp  exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CommSnmp MO/None)

    Raises:
        None

    Example:
        mo = snmp_exists(handle,
                         community="username",
                         sys_contact="user contact",
                         sys_location="user location",
                         descr="SNMP Service")

    """
    from ucsmsdk.mometa.comm.CommSnmp import CommSnmpConsts

    try:
        mo = snmp_config_get(handle, caller="snmp_exists")
    except UcsOperationError:
        return (False, None)

    kwargs['admin_state'] = CommSnmpConsts.ADMIN_STATE_ENABLED

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def snmp_trap_add(handle, hostname, community, port="162", version="v2c",
                  notification_type="traps", v3_privilege="noauth", **kwargs):
    """
    adds snmp trap.

    Args:
        handle (UcsHandle)
        hostname (string): hostname or ip address
        community (string): community or username
        port (string): port number
        version (string): version
         valid values are "v1", "v2c", "v3"
        notification_type (string): notification type
         valid values are "informs", "traps"
         *note: required only for version "v2c" and "v3"
        v3_privilege (string): privilege for version "v3"
         valid value are auth", "noauth", "priv"
         *note: required only for version "v3"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommSnmpTrap: managed object

    Raises:
        None


    Example:
        snmp_trap_add(handle, hostname="10.10.10.10",
                      community="username", port="162",
                      version="v2c",
                      notification_type="informs")
    """
    from ucsmsdk.mometa.comm.CommSnmpTrap import CommSnmpTrap

    if version == 'v1':
        notification_type = 'traps'

    mo = CommSnmpTrap(
        parent_mo_or_dn=_base_dn + "/snmp-svc",
        hostname=hostname,
        community=community,
        port=port,
        version=version,
        notification_type=notification_type,
        v3_privilege=v3_privilege)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def snmp_trap_get(handle, hostname, caller="snmp_trap_get"):
    """
    gets snmp trap

    Args:
        handle (UcsHandle)
        hostname (string): hostname or ip address
        caller (string): name of the caller function

    Returns:
        CommSnmpTrap: managed object

    Raises:
        UcsOperationError: if CommSnmpTrap is not present

    Example:
        snmp_trap_get(handle, hostname="10.10.10.10")
    """
    dn = _base_dn + "/snmp-svc" + "/snmp-trap" + hostname
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "SNMP Trap '%s' does not exist" % dn)
    return mo


def snmp_trap_exists(handle, hostname, **kwargs):
    """
    checks if snmp trap exists

    Args:
        handle (UcsHandle)
        hostname (string): hostname or ip address
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CommSnmpTrap MO/None)

    Raises:
        None

    Example:
        snmp_trap_exists(handle, hostname="10.10.10.10",
                         community="username", port="162",
                         version="v2c",
                         notification_type="informs")
    """
    try:
        mo = snmp_trap_get(handle, hostname, caller="snmp_trap_exists")
    except UcsOperationError:
        return (False, None)

    if 'version' in kwargs and kwargs['version'] == 'v1':
        kwargs['notification_type'] = 'traps'

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def snmp_trap_modify(handle, hostname, **kwargs):
    """
    modifies snmp trap.

    Args:
        handle (UcsHandle)
        hostname (string): hostname or ip address
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        CommSnmpTrap: managed object

    Raises:
        UcsOperationError: if CommSnmpTrap Mo is not present

    Example:
        snmp_trap_modify(handle, hostname="10.10.10.10",
                         community="username", port="162",
                         version="v3",
                         notification_type="traps",
                         v3_privilege="noauth")
    """
    mo = snmp_trap_get(handle, hostname, caller="snmp_trap_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_trap_remove(handle, hostname):
    """
    removes snmp trap.

    Args:
        handle (UcsHandle)
        hostname (string): hostname or ip address

    Returns:
        None

    Raises:
        UcsOperationError: if CommSnmpTrap Mo is not present

    Example:
        snmp_trap_remove(handle, hostname="10.10.10.10")
    """
    mo = snmp_trap_get(handle, hostname, caller="snmp_trap_remove")
    handle.remove_mo(mo)
    handle.commit()


def snmp_user_add(handle, name, pwd, auth="md5", use_aes="no",
                  privpwd=None, descr=None, **kwargs):
    """
    Adds snmp user.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        pwd (string): password, minimum 8 character
        auth (string): auth type
         valid values are "md5", "sha"
        use_aes (string): Use AES-128, valid values are "yes", "no"
        privpwd (string): privacy password
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommSnmpUser: managed object

    Raises:
        None

    Example:
        snmp_user_add(handle, name="snmpuser", descr=None, pwd="password",
                      privpwd="password", auth="sha")
    """
    from ucsmsdk.mometa.comm.CommSnmpUser import CommSnmpUser

    mo = CommSnmpUser(
        parent_mo_or_dn=_base_dn + "/snmp-svc",
        name=name,
        pwd=pwd,
        auth=auth,
        use_aes=use_aes,
        privpwd=privpwd,
        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def snmp_user_get(handle, name, caller="snmp_user_get"):
    """
    gets snmp user.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        caller (string): name of the caller function

    Returns:
        CommSnmpUser: managed object

    Raises:
        UcsOperationError: if CommSnmpUser is not present

    Example:
        snmp_user_get(handle, name="snmpuser")
    """
    dn = _base_dn + "/snmp-svc" + "/snmpv3-user-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "SNMP User '%s' does not exist" % dn)
    return mo


def snmp_user_exists(handle, name, **kwargs):
    """
    checks if snmp user exists.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CommSnmpUser MO/None)

    Raises:
        None

    Example:
        snmp_user_exists(handle, name="snmpuser", descr=None,
                    auth="sha")
    """
    try:
        mo = snmp_user_get(handle, name, caller="snmp_user_exists")
    except UcsOperationError:
        return (False, None)

    if 'pwd' in kwargs:
        kwargs.pop('pwd', None)
    if 'privpwd' in kwargs:
        kwargs.pop('privpwd', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def snmp_user_modify(handle, name, **kwargs):
    """
    modifies snmp user.

    Args:
        handle (UcsHandle)
        name (string): snmp username
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        CommSnmpUser: managed object

    Raises:
        UcsOperationError: if CommSnmpUser is not present

    Example:
        snmp_user_modify(handle, name="snmpuser", descr=None,
                          pwd="password", privpwd="password",
                          auth="md5", use_aes="no")
    """
    mo = snmp_user_get(handle, name, caller="snmp_user_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def snmp_user_remove(handle, name):
    """
    removes snmp user

    Args:
        handle (UcsHandle)
        name (string): snmp username

    Returns:
        None

    Raises:
        UcsOperationError: if CommSnmpUser is not present

    Example:
        snmp_user_remove(handle, name="snmpuser")
    """
    mo = snmp_user_get(handle, name, caller="snmp_user_remove")
    handle.remove_mo(mo)
    handle.commit()
