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

def time_zone_set(handle, timezone, **kwargs):
    """
    This method sets the timezone of the UCS Central.

    Args:
        handle (UcsHandle)
        timezone (string): time zone e.g. "Asia/Kolkata"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommDateTime: Managed object

    Raises:
        UcsOperationError: If CommDateTime Mo is not found

    Example:
        To Set Time Zone:
            mo = time_zone_set(handle, "Asia/Kolkata")

        To Un-Set Time Zone:
            mo = time_zone_set(handle, "")
    """

    mo = handle.query_dn(_base_dn + "/datetime-svc")
    if not mo:
        raise UcsOperationError("time_zone_set",
                                 "timezone does not exist")

    mo.timezone = timezone
    mo.admin_state = "enabled"
    mo.port = "0"

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def ntp_server_add(handle, name, descr=None, **kwargs):
    """
    Adds NTP server using IP address.

    Args:
        handle (UcsHandle)
        name (string): NTP server IP address or Name
        descr (string): Basic description about NTP server
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommNtpProvider: Managed object

    Example:
        ntp_server_add(handle, name="72.163.128.140", descr="Default NTP")
    """

    from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider

    mo = CommNtpProvider(
        parent_mo_or_dn=_base_dn + "/datetime-svc",
        name=name,
        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ntp_server_get(handle, name, caller="ntp_server_get"):
    """
    Gets ntp server

    Args:
        handle (UcsHandle)
        name (string): NTP server IP address or Name

    Returns:
        CommNtpProvider: Managed object OR None

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
        name (string): NTP server IP address or Name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

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
    Removes the NTP server.

    Args:
        handle (UcsHandle)
        name : NTP server IP address or Name

    Returns:
        None

    Raises:
        UcsOperationError: If CommNtpProvider is not found

    Example:
        ntp_server_remove(handle, "72.163.128.140")
    """

    mo = ntp_server_get(handle, name, caller="ntp_server_remove")
    handle.remove_mo(mo)
    handle.commit()
