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
from ucsmsdk.ucsexception import UcsOperationError

_base_dn = "sys/svc-ext"


def timezone_set(handle, timezone, policy_owner="local",
                 admin_state="enabled", port="0", descr=None, **kwargs):
    """
    sets the timezone of the UCSM

    Args:
        handle (UcsHandle)
        timezone (string): time zone e.g. "Asia/Kolkata"
        policy_owner (string): policy owner
         valid values are "local", "pending-policy", "policy"
        admin_state (string): admin state
         valid values are "disabled", "enabled"
        port (string): port
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommDateTime: managed object

    Raises:
        UcsOperationError: if CommDateTime is not present

    Example:
        To Set Time Zone:
            mo = timezone_set(handle, "Asia/Kolkata")

        To Un-Set Time Zone:
            mo = timezone_set(handle, "")
    """
    mo = handle.query_dn(_base_dn + "/datetime-svc")
    if not mo:
        raise UcsOperationError("timezone_set",
                                "timezone does not exist")

    args = {'timezone': timezone,
            'policy_owner': policy_owner,
            'admin_state': admin_state,
            'port': port,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def timezone_exists(handle, **kwargs):
    """
    checks if timezone exists.

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CommDateTime MO/None)

    Raises:
        None

    Example:
        timezone_exists(handle, timezone="Asia/Kolkata")
    """
    mo = handle.query_dn(_base_dn + "/datetime-svc")
    if not mo:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ntp_server_add(handle, name, descr=None, **kwargs):
    """
    adds ntp server

    Args:
        handle (UcsHandle)
        name (string): ntp server ip address or hostname
        descr (string): ntp server description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommNtpProvider: managed object

    Raises:
        None

    Example:
        ntp_server_add(handle, name="72.163.128.140", descr="Default NTP")
    """
    from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider

    dn = _base_dn + "/datetime-svc"
    mo = CommNtpProvider(parent_mo_or_dn=dn,
                         name=name,
                         descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ntp_server_get(handle, name, caller="ntp_server_get"):
    """
    gets ntp server

    Args:
        handle (UcsHandle)
        name (string): ntp server ip address or hostname
        caller (string): name of the caller function

    Returns:
        CommNtpProvider: managed object

    Raises:
        UcsOperationError: if CommNtpProvider is not present

    Example:
        ntp_server_get(handle, "72.163.128.140")
    """
    dn = _base_dn + "/datetime-svc" + "/ntp-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "NTP Server '%s' does not exist" % dn)
    return mo


def ntp_server_exists(handle, name, **kwargs):
    """
    checks if ntp server exists.

    Args:
        handle (UcsHandle)
        name (string): ntp server ip address or hostname
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CommNtpProvider MO/None)

    Raises:
        None

    Example:
        ntp_server_exists(handle, "72.163.128.140", descr="Default NTP")
    """
    try:
        mo = ntp_server_get(handle, name)
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ntp_server_remove(handle, name):
    """
    removes the NTP server.

    Args:
        handle (UcsHandle)
        name (string): ntp server ip address or hostname

    Returns:
        None

    Raises:
        UcsOperationError: if CommNtpProvider is not present

    Example:
        ntp_server_remove(handle, "72.163.128.140")
    """
    mo = ntp_server_get(handle, name, caller="ntp_server_remove")
    handle.remove_mo(mo)
    handle.commit()
