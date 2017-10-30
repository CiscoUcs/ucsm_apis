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

_syslog_dn = "sys/svc-ext/syslog"


def syslog_local_console_enable(handle, severity="emergencies",
                                name=None, descr=None, **kwargs):
    """
    enables system logs on local console

    Args:
        handle (UcsHandle)
        severity (string): level of logging
         valid values are "emergencies","alerts", "critical"
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogConsole: managed object

    Raises:
        UcsOperationError: if CommSyslogConsole is not present

    Example:
        syslog_local_console_enable(handle, severity="alerts")
    """
    from ucsmsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = _syslog_dn + "/console"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_console_enable",
                                "syslog console '%s' does not exist." % dn)

    args = {'admin_state': CommSyslogConsoleConsts.ADMIN_STATE_ENABLED,
            'severity': severity,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_console_disable(handle):
    """
    disables system logs on local console

    Args:
        handle (UcsHandle)

    Returns:
        CommSyslogConsole: managed object

    Raises:
        UcsOperationError: if CommSyslogConsole is not present

    Example:
        syslog_local_console_disable(handle)
    """
    from ucsmsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = _syslog_dn + "/console"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_console_disable",
                                "syslog console does not exist.")

    args = {'admin_state': CommSyslogConsoleConsts.ADMIN_STATE_DISABLED}

    mo.set_prop_multiple(**args)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_console_exists(handle, **kwargs):
    """
    Checks if the syslog local console already exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        syslog_local_console_exists(handle, severity="alerts")
    """
    from ucsmsdk.mometa.comm.CommSyslogConsole import \
        CommSyslogConsoleConsts

    dn = _syslog_dn + "/console"
    mo = handle.query_dn(dn)
    if not mo:
        return False, None

    kwargs['admin_state'] = CommSyslogConsoleConsts.ADMIN_STATE_ENABLED

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def syslog_local_monitor_enable(handle, severity="emergencies",
                                name=None, descr=None, **kwargs):
    """
    enables sytem logs on local monitor

    Args:
        handle (UcsHandle)
        severity (string): level of logging
         valid values are "alerts", "critical", "debugging", "emergencies",
          "errors", "information", "notifications", "warnings"
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommSyslogMonitor: managed object

    Raises:
        UcsOperationError: if CommSyslogMonitor is not present

    Example:
        syslog_local_monitor_enable(handle, severity="alerts")
    """
    from ucsmsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = _syslog_dn + "/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_monitor_enable",
                                "syslog monitor '%s' does not exist." % dn)

    args = {'admin_state': CommSyslogMonitorConsts.ADMIN_STATE_ENABLED,
            'severity': severity,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_monitor_disable(handle):
    """
    disables system logs on local monitor

    Args:
        handle (UcsHandle)

    Returns:
        CommSyslogMonitor: managed object

    Raises:
        UcsOperationError: if CommSyslogMonitor is not present

    Example:
        mo = syslog_local_monitor_disable(handle)
    """
    from ucsmsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = _syslog_dn + "/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_monitor_disable",
                                "syslog monitor does not exist.")

    args = {'admin_state': CommSyslogMonitorConsts.ADMIN_STATE_DISABLED}

    mo.set_prop_multiple(**args)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_monitor_exists(handle, **kwargs):
    """
    Checks if the syslog local monitor already exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        syslog_local_monitor_exists(handle, severity="alerts")
    """
    from ucsmsdk.mometa.comm.CommSyslogMonitor import \
        CommSyslogMonitorConsts

    dn = _syslog_dn + "/monitor"
    mo = handle.query_dn(dn)
    if not mo:
        return False, None

    kwargs['admin_state'] = CommSyslogMonitorConsts.ADMIN_STATE_ENABLED

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def syslog_local_file_enable(handle, severity="emergencies", size=None,
                             name=None, descr=None, **kwargs):
    """
    enables system logs to save messages on local file

    Args:
        handle (UcsHandle)
        severity (string): level of logging
         valid values are "alerts", "critical", "debugging", "emergencies",
          "errors", "information", "notifications", "warnings"
        size (string): size of log file, (in bytes, between 4096-4194304)
        name (string): name of log file
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CommSyslogFile: managed object

    Raises:
        UcsOperationError: if CommSyslogFile is not present

    Example:
        syslog_local_file_enable(handle, severity="alert", size="435675",
                                name="sys_log")
    """
    from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = _syslog_dn + "/file"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_file_enable",
                                "syslog file '%s' does not exist." % dn)

    args = {'admin_state': CommSyslogFileConsts.ADMIN_STATE_ENABLED,
            'severity': severity,
            'size': size,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_file_disable(handle):
    """
    disables system logs to save messages on local file

    Args:
        handle (UcsHandle)

    Returns:
        CommSyslogFile: managed object

    Raises:
        UcsOperationError: if CommSyslogFile is not present

    Example:
        syslog_local_file_disable(handle)
    """
    from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = _syslog_dn + "/file"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_local_file_disable",
                                "syslog file does not exist.")

    args = {'admin_state': CommSyslogFileConsts.ADMIN_STATE_DISABLED}

    mo.set_prop_multiple(**args)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_local_file_exists(handle, **kwargs):
    """
    Checks if the syslog local file already exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        syslog_local_file_exists(handle, severity="alerts")
    """
    from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFileConsts

    dn = _syslog_dn + "/file"
    mo = handle.query_dn(dn)
    if not mo:
        return False, None

    kwargs['admin_state'] = CommSyslogFileConsts.ADMIN_STATE_ENABLED

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def syslog_remote_enable(handle, name, hostname, severity="emergencies",
                         forwarding_facility="local0", **kwargs):
    """
    enables system logs on remote server

    Args:
        handle (UcsHandle)
        name (string): remote server type
         valid values are "primary", "secondary", "tertiary"
        hostname (string) : remote hostname or ip address
        severity (string): Level of logging
         valid values are "alerts", "critical", "debugging", "emergencies",
          "errors", "information", "notifications", "warnings"
        forwarding_facility (string): forwarding mechanism local0 to local7
         valid values are "local0", "local1", "local2", "local3", "local4",
          "local5", "local6", "local7"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogClient: managed object

    Raises:
        UcsOperationError: if CommSyslogClient is not present

    Example:
        syslog_remote_enable(handle, name="primary", hostname="192.168.1.2",
                             severity="alert")
    """
    from ucsmsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = _syslog_dn + "/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_remote_enable",
                                "Remote Destination '%s' does not exist" % dn)

    args = {'admin_state': CommSyslogClientConsts.ADMIN_STATE_ENABLED,
            'hostname': hostname,
            'severity': severity,
            'forwarding_facility': forwarding_facility
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_remote_disable(handle, name):
    """
    disables system logs on remote server

    Args:
        handle (UcsHandle)
        name (string): remote server type
         valid values are "primary", "secondary", "tertiary"

    Returns:
        CommSyslogClient: managed object

    Raises:
        UcsOperationError: if CommSyslogClient is not present

    Example:
        syslog_remote_disable(handle, name="primary")
    """
    from ucsmsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = _syslog_dn + "/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_remote_disable",
                                "Remote Destination '%s' does not exist" % dn)

    args = {'admin_state': CommSyslogClientConsts.ADMIN_STATE_DISABLED}

    mo.set_prop_multiple(**args)
    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_remote_exists(handle, name, **kwargs):
    """
    Checks if the syslog remote already exists

    Args:
        handle (UcsHandle)
        name (string): remote server type
         valid values are "primary", "secondary", "tertiary"
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        syslog_remote_exists(handle, name="primary", hostname="192.168.1.2",
                             severity="alert")
    """
    from ucsmsdk.mometa.comm.CommSyslogClient import \
        CommSyslogClientConsts

    dn = _syslog_dn + "/client-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return False, None

    kwargs['admin_state'] = CommSyslogClientConsts.ADMIN_STATE_ENABLED

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def syslog_source_configure(handle, faults=None, audits=None, events=None,
                            name=None, descr=None, **kwargs):
    """
    configures system logs for local source (faults, audits and events)

    Args:
        handle (UcsHandle)
        faults (string) : for fault logging
         valid values are "disabled", "enabled"
        audits (string): for audit task logging
         valid values are "disabled", "enabled"
        events (string): for event logging
         valid values are "disabled", "enabled"
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CommSyslogSource: managed object

    Raises:
        UcsOperationError: if CommSyslogSource is not present

    Example:
        syslog_source_configure(handle, faults="enabled", audits="disabled",
                                events="disabled")
    """
    dn = _syslog_dn + "/source"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("syslog_source",
                                "local sources '%s' does not exist" % dn)

    args = {'faults': faults,
            'audits': audits,
            'events': events,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def syslog_source_exists(handle, **kwargs):
    """
    Checks if the syslog source already exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        syslog_source_exists(handle, faults="enabled", audits="disabled",
                                events="disabled")
    """
    dn = _syslog_dn + "/source"
    mo = handle.query_dn(dn)
    if not mo:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)
