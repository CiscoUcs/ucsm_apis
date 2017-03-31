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
This module performs the operation related to syslog.
"""
from ucsmsdk.ucsexception import UcsOperationError

_base_dn = "sys/svc-ext/syslog"

def syslog_local_console_enable(handle, severity="emergencies", **kwargs):
    """
    This method enables system logs on local console.

    Args:
        handle (UcsHandle)
        severity (string): Level of logging.
                        ["emergencies","alerts", "critical"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogConsole: Managed Object

    Raises:
        UcsOperationError: If CommSyslogConsole is not present

    Example:
        syslog_local_console_enable(handle, severity="alerts")
    """

    from ucsmsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = _base_dn + "/console"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_console_enable",
                                 "syslog console does not exist.")

    mo.admin_state = CommSyslogConsoleConsts.ADMIN_STATE_ENABLED
    mo.severity = severity

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_console_disable(handle):
    """
    This method disables system logs on local console.

    Args:
        handle (UcsHandle)

    Returns:
        CommSyslogConsole: Managed Object

    Raises:
        UcsOperationError: If CommSyslogConsole is not present

    Example:
        syslog_local_console_enable(handle)
    """

    from ucsmsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = _base_dn + "/console"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_console_disable",
                                 "syslog console does not exist.")

    mo.admin_state = CommSyslogConsoleConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_monitor_enable(handle, severity="emergencies", **kwargs):
    """
    This method enables logs on local monitor.

    Args:
        handle (UcsHandle)
        severity (string): Level of logging.
                        ["alerts", "critical", "debugging", "emergencies",
                        "errors", "information", "notifications", "warnings"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogMonitor: Managed Object

    Raises:
        UcsOperationError: If CommSyslogMonitor is not present

    Example:
        syslog_local_monitor_enable(handle, severity="alert")
    """

    from ucsmsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = _base_dn + "/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_monitor_enable",
                                 "syslog monitor does not exist.")

    mo.admin_state = CommSyslogMonitorConsts.ADMIN_STATE_ENABLED
    mo.severity = severity

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_monitor_disable(handle):
    """
    This method disables logs on local monitor.

    Args:
        handle (UcsHandle)

    Returns:
        CommSyslogMonitor: Managed Object

    Raises:
        UcsOperationError: If CommSyslogMonitor is not present

    Example:
        mo = syslog_local_monitor_disable(handle)
    """

    from ucsmsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = _base_dn + "/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_monitor_disable",
                                 "syslog monitor does not exist.")

    mo.admin_state = CommSyslogMonitorConsts.ADMIN_STATE_DISABLED

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_file_enable(handle, name=None, severity="emergencies",
                             size="40000", **kwargs):
    """
    This method configures System Logs on local file storage.

    Args:
        handle (UcsHandle)
        name (string): Name of Log file.
        severity (string): Level of logging.
                        ["alerts", "critical", "debugging", "emergencies",
                        "errors", "information", "notifications", "warnings"]
        size (string): Maximum allowed size of log file(In KBs).
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogFile: Managed object

    Raises:
        UcsOperationError: If CommSyslogFile is not present

    Example:
        syslog_local_file_enable(handle, severity="alert", size="435675",
                                name="sys_log")
    """

    from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = _base_dn + "/file"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_file_enable",
                                 "syslog file does not exist.")

    mo.admin_state = CommSyslogFileConsts.ADMIN_STATE_ENABLED
    args = {'name': name,
            'severity': severity,
            'size': size
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_file_disable(handle):
    """
    This method disables System Logs on local file storage.

    Args:
        handle (UcsHandle)

    Returns:
        CommSyslogFile: Managed Object

    Raises:
        UcsOperationError: If CommSyslogFile is not present

    Example:
        syslog_local_file_disable(handle)
    """

    from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = _base_dn + "/file"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_file_disable",
                                 "syslog file does not exist.")

    mo.admin_state = CommSyslogFileConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_remote_enable(handle, name, hostname="none",
                         severity="emergencies", forwarding_facility="local0",
                         **kwargs):
    """
    This method enables System Logs on remote server.

    Args:
        handle (UcsHandle)
        name (string): Remote Server ID -
                            "primary" or "secondary" or "tertiary"
        hostname (string) : Remote host IP or Name
        severity (string): Level of logging.
                        ["alerts", "critical", "debugging", "emergencies",
                        "errors", "information", "notifications", "warnings"]
        forwarding_facility (string): Forwarding mechanism local0 to local7.
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogClient Object

    Raises:
        UcsOperationError: If CommSyslogClient is not present

    Example:
        syslog_remote_enable(handle, name="primary", hostname="192.168.1.2",
                    severity="alert")
    """

    from ucsmsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = _base_dn + "/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_remote_enable",
                                 "Remote Destination '%s' does not exist" % dn)
    mo.admin_state = CommSyslogClientConsts.ADMIN_STATE_ENABLED
    args = {'forwarding_facility': forwarding_facility,
            'hostname': hostname,
            'severity': severity
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_remote_disable(handle, name):
    """
    This method enables System Logs on remote server.

    Args:
        handle (UcsHandle)
        name (string): Remote Server ID -
                            "primary" or "secondary" or "tertiary"

    Returns:
        CommSyslogClient: Managed Object

    Raises:
        UcsOperationError: If CommSyslogClient is not present

    Example:
        syslog_remote_disable(handle, name="primary")
    """

    from ucsmsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = _base_dn + "/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_remote_disable",
                                 "Remote Destination '%s' does not exist" % dn)

    mo.admin_state = CommSyslogClientConsts.ADMIN_STATE_DISABLED
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_source(handle, faults=None, audits=None, events=None, **kwargs):
    """
    This method configures Type of System Logs.

    Args:
        handle (UcsHandle)
        faults (string) : for fault logging. ["disabled", "enabled"]
        audits (string): for audit task logging. ["disabled", "enabled"]
        events (string): for event logging. ["disabled", "enabled"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogSource: Managed object

    Raises:
        UcsOperationError: If CommSyslogSource is not present

    Example:
            syslog_source(handle, faults="enabled", audits="disabled",
                    events="disabled")

    """

    dn = _base_dn + "/source"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_source",
                                 "local sources '%s' does not exist" % dn)

    args = {'faults': faults,
            'audits': audits,
            'events': events
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
