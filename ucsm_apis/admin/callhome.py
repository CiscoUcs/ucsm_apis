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
This module performs the operation related to callhome.
"""
from ucsmsdk.ucsexception import UcsOperationError

_base_dn = "call-home"


def call_home_enable(handle, alert_throttling_admin_state="on",
                     policy_owner="local",name=None, descr=None, **kwargs):
    """
    Enables call home alert.

    NOTE:
	If enabling call home for the first time then first update contact and
	smtp server.
	- contact information using 'call_home_contact_update'
		call_home_contact_update(handle,
							     contact="ciscoucs",
                                 phone="+911234567890",
                                 email="ciscoucs@cisco.com",
                                 addr="cisco",
							     reply_to="ciscoucs@cisco.com"
                                 )
    - smtp server using 'call_home_smtp_update'.
		call_home_smtp_update(handle, host="1.1.1.1")


    Args:
        handle (UcsHandle)
        alert_throttling_admin_state (string): "on" or "off"
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CallhomeEp : ManagedObject

    Raises:
        UcsOperationError: If CallhomeEp is not present

    Example:
        call_home_enable(handle, alert_throttling_admin_state="on")
    """
    mo = handle.query_dn(_base_dn)
    if not mo:
        raise UcsOperationError("call_home_state_enable",
                                 "Call home not available.")

    mo.admin_state = "on"
    mo.alert_throttling_admin_state = alert_throttling_admin_state
    mo.name = name
    mo.descr = descr

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_contact_update(handle, contact=None, phone=None, email=None,
                        addr=None, customer=None, contract=None, site=None,
                        r_from=None, reply_to=None, urgency=None, **kwargs):
    """
    Updates the contact detail for callhome

    Args:
        handle (UcsHandle)
        contact (string): Contact Name
        phone (string): phone number e.g. +91-1234567890
        email (string): contact email address
        addr (string): contact address
        customer (number): customer id
        contract (number): contract id
        site (number): site id
        r_from (string): from email address
        reply_to (string): to email address
        urgency (string): alert priority
         valid values are "alert", "critical", "debug", "emergency",
         "error", "info", "notice", "warning"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CallhomeSource: ManagedObject

    Raises:
        UcsOperationError: If CallhomeSource is not present

    Example:
        from ucsmsdk.mometa.callhome.CallhomeSource import \
            CallhomeSourceConsts

        call_home_contact_update(handle,
                                 contact="user name",
                                 phone="+91-1234567890",
                                 email="user@cisco.com",
                                 addr="user address",
                                 customer="1111",
                                 contract="2222",
                                 site="3333",
                                 r_from="from@cisco.com",
                                 reply_to="to@cisco.com",
                                 urgency=CallhomeSourceConsts.URGENCY_ALERT,
                                 )
    """
    dn = _base_dn + "/source"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("call_home_config",
                                 "Call home source '%s' not available." % dn)

    args = {'contact': contact,
            'phone': phone,
            'email': email,
            'addr': addr,
            'customer': customer,
            'contract': contract,
            'site': site,
            'r_from': r_from,
            'reply_to': reply_to,
            'urgency': urgency}

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo

def call_home_smtp_update(handle, host=None, port="25", **kwargs):
    """
    Updates the SMTP server for callhome

    Args:
        handle (UcsHandle)
        host (string): ip address of SMTP server
        port (string): port of SMTP server
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        CallhomeSmtp: ManagedObject

    Raises:
        UcsOperationError: If CallhomeSmtp is not present

    Example:
        call_home_smtp_update(handle,
                              host="1.1.1.1",
                              port="25")
    """
    dn = _base_dn + "/smtp"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("call_home_smtp_update",
                            "Call home smtp server '%s' not available." % dn)

    args = {'host': host, 'port': port}

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_disable(handle):
    """
    Disables call home alert.

    Args:
        handle (UcsHandle)

    Returns:
        CallhomeEp : ManagedObject

    Raises:
        UcsOperationError: If CallhomeEp is not present

    Example:
        call_home_disable(handle)
    """
    mo = handle.query_dn(_base_dn)
    if not mo:
        raise UcsOperationError("call_home_disable",
                                 "Call home not available.")

    mo.admin_state = "off"

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_profile_create(handle, name, format="xml", max_size="1000000",
                             level="debug", alert_groups=None,
                             descr=None, **kwargs):
    """
    Creates callhome profile.

    Args:
        handle (UcsHandle)
        name (string): name of callhome profile
        format (string): message format.
         valid values are "fullTxt", "shortTxt", "xml"
        max_size (string): message max size
        level (string): debug level
         valid values are "critical", "debug", "disaster", "fatal",
          "major", "minor", "normal", "notification", "warning"
        alert_groups (string): Alert Groups
         valid values are "ciscoTac", "diagnostic", "environmental"
        descr: Description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CallhomeProfile : ManagedObject

    Raises:
        UcsOperationError: If CallhomeProfile is not present

    Example:
        call_home_profile_create(handle, name="callhomeprofile")
    """
    from ucsmsdk.mometa.callhome.CallhomeProfile import CallhomeProfile

    mo = CallhomeProfile(parent_mo_or_dn=_base_dn,
                         name=name,
                         format=format,
                         level=level,
                         max_size=max_size,
                         alert_groups=alert_groups,
                         descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def call_home_profile_get(handle, name, caller="call_home_profile_get"):
    """
    Gets callhome profile.

    Args:
        handle (UcsHandle)
        name (string): name of callhome profile
        caller (string): name of caller function

    Returns:
        CallhomeProfile : ManagedObject

    Raises:
        UcsOperationError: If CallhomeProfile is not present

    Example:
        call_home_profile_get(handle, name="callhomeprofile")
    """
    dn = _base_dn + "/profile-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Callhome Profile '%s' does not exist" % dn)
    return mo


def call_home_profile_exists(handle, name, **kwargs):
    """
    Checks if the given callhome profile already exists with the same params

    Args:
        handle (UcsHandle)
        name (string): name of callhome profile
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CallhomeProfile MO/None)

    Raises:
        None

    Example:
        call_home_profile_exists(handle, name="callhomeprofile", format="xml")
    """
    try:
        mo = call_home_profile_get(handle, name,
                                   caller="call_home_profile_exist")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def call_home_profile_modify(handle, name, **kwargs):
    """
    Modifies callhome profile.

    Args:
        handle (UcsHandle)
        name (string): name of callhome profile
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        CallhomeProfile : ManagedObject

    Raises:
        UcsOperationError: If CallhomeProfile is not present

    Example:
        call_home_profile_modify(handle, name="callhomeprofile", format="xml")
    """
    mo = call_home_profile_get(handle, name, caller="call_home_profile_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_profile_delete(handle, name):
    """
    Deletes callhome profile.

    Args:
        handle (UcsHandle)
        name (string): name of callhome profile
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        None

    Raises:
        UcsOperationError: If CallhomeProfile is not present

    Example:
        call_home_profile_delete(handle, name="callhomeprofile")
    """
    mo = call_home_profile_get(handle, name, caller="call_home_profile_delete")
    handle.remove_mo(mo)
    handle.commit()


def call_home_profile_email_add(handle, profile_name, email, **kwargs):
    """
    Adds email to callhome profile.

    Args:
        handle (UcsHandle)
        profile_name (string): name of callhome profile
        email (string): receipient email address
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CallhomeDest : ManagedObject

    Raises:
        UcsOperationError: If CallhomeProfile is not present

    Example:
        call_home_profile_email_add(handle, profile_name="callhomeprofile",
                                    email="ciscoucs@cisco.com")
    """
    from ucsmsdk.mometa.callhome.CallhomeDest import CallhomeDest

    profile = call_home_profile_get(handle, profile_name,
                                    caller="call_home_profile_email_add")
    mo = CallhomeDest(parent_mo_or_dn=profile, email=email)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo

def call_home_profile_email_get(handle, profile_name, email,
                                caller="call_home_profile_email_get"):
    """
    Gets receipient email from callhome profile.

    Args:
        handle (UcsHandle)
        profile_name (string): name of callhome profile
        email (string): receipient email address
        caller (string): name of caller function

    Returns:
        CallhomeDest : ManagedObject

    Raises:
        UcsOperationError: If CallhomeDest is not present

    Example:
        call_home_profile_email_get(handle, profile_name="callhomeprofile",
                                    email="ciscoucs@cisco.com")
    """
    profile_dn = _base_dn + "/profile-" + profile_name
    dn = profile_dn + "/email-" + email
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Callhome Profile Email '%s' does not exist" % dn)
    return mo


def call_home_profile_email_exists(handle, profile_name, email, **kwargs):
    """
    Checks if the given receipient email already exists with the same params

    Args:
        handle (UcsHandle)
        profile_name (string): name of callhome profile
        email (string): receipient email address
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CallhomeDest MO/None)

    Raises:
        None

    Example:
        call_home_profile_email_exists(handle, profile_name="callhomeprofile",
                                       email="ciscoucs@cisco.com")
    """
    try:
        mo = call_home_profile_email_get(handle, profile_name, email,
                                    caller="call_home_profile_email_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def call_home_profile_email_remove(handle, profile_name, email):
    """
    Removes receipient email from callhome profile.

    Args:
        handle (UcsHandle)
        profile_name (string): name of callhome profile
        email (string): receipient email address
        caller (string): name of caller function

    Returns:
        None

    Raises:
        UcsOperationError: If CallhomeDest is not present

    Example:
        call_home_profile_email_remove(handle, profile_name="callhomeprofile",
                                       email="ciscoucs@cisco.com")
    """
    mo = call_home_profile_email_get(handle, profile_name, email,
                                caller="call_home_profile_email_remove")
    handle.remove_mo(mo)
    handle.commit()


def call_home_policy_create(handle, cause, admin_state="enabled",
                            name=None, descr=None, **kwargs):
    """
    Creates callhome policy.

    Args:
        handle (UcsHandle)
        cause (string): cause to trigger call home alert
		 valid values are "adaptor-mismatch", "arp-targets-config-error",
		  "association-failed", "backplane-port-problem",
	      "configuration-failure", "configuration-mismatch",
		  "connectivity-problem", "election-failure", "equipment-degraded",
		  "equipment-deprecated", "equipment-disabled",
		  "equipment-inaccessible", "equipment-inoperable",
		  "equipment-missing", "equipment-offline", "equipment-problem",
		  "equipment-removed", "equipment-unacknowledged",
		  "equipment-unhealthy", "fan-removal", "fru-problem",
		  "health-critical", "health-led-amber", "health-led-amber-blinking",
		  "health-major", "identity-unestablishable", "image-unusable",
		  "inventory-failed", "kernel-mem-critical-threshold",
		  "license-graceperiod-expired", "limit-reached", "link-down",
		  "management-services-failure", "management-services-unresponsive",
		  "memory-error", "mgmtif-down", "ndisc-targets-config-error",
		  "near-max-limit", "not-supported", "port-failed", "power-problem",
		  "psu-insufficient", "psu-mixed-mode", "thermal-problem",
		  "unspecified", "version-incompatible", "vif-ids-mismatch",
		  "voltage-problem"
        admin_state (string): admin_state
         valid values are "disabled", "enabled"
        name (string): policy name
        descr: Description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CallhomePolicy : ManagedObject

    Raises:
        None

    Example:
        call_home_policy_create(handle, cause="equipment-removed",
                                "name="callhomepolicy")
    """
    from ucsmsdk.mometa.callhome.CallhomePolicy import CallhomePolicy

    mo = CallhomePolicy(parent_mo_or_dn=_base_dn,
                        cause=cause,
                        admin_state=admin_state,
                        name=name,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def call_home_policy_get(handle, cause, caller="call_home_policy_get"):
    """
    Gets callhome policy.

    Args:
        handle (UcsHandle)
        cause (string): cause to trigger call home alert
        caller (string): name of caller function

    Returns:
        CallhomePolicy : ManagedObject

    Raises:
        UcsOperationError: If CallhomePolicy is not present

    Example:
        call_home_policy_get(handle, cause="equipment-removed")
    """
    dn = _base_dn + "/policy-" + cause
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Callhome Policy '%s' does not exist" % dn)
    return mo


def call_home_policy_exists(handle, cause, **kwargs):
    """
    Checks if the given callhome policy already exists with the same params

    Args:
        handle (UcsHandle)
        cause (string): cause to trigger call home alert
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, CallhomePolicy MO/None)

    Raises:
        None

    Example:
        call_home_policy_exists(handle, cause="equipment-removed")
    """
    try:
        mo = call_home_policy_get(handle, cause,
                                  caller="call_home_policy_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def call_home_policy_modify(handle, cause, **kwargs):
    """
    Modifies the callhome policy

    Args:
        handle (UcsHandle)
        cause (string): cause to trigger call home alert
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        CallhomePolicy : ManagedObject

    Raises:
        UcsOperationError: If CallhomePolicy is not present

    Example:
        call_home_policy_modify(handle, cause="equipment-removed")
    """
    mo = call_home_policy_get(handle, cause, caller="call_home_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_policy_delete(handle, cause):
    """
    Modifies the callhome policy

    Args:
        handle (UcsHandle)
        cause (string): cause to trigger call home alert

    Returns:
        None

    Raises:
        UcsOperationError: If CallhomePolicy is not present

    Example:
        call_home_policy_delete(handle, cause="equipment-removed")
    """
    mo = call_home_policy_get(handle, cause, caller="call_home_policy_delete")
    handle.remove_mo(mo)
    handle.commit()


def call_home_system_inventory_configure(handle,
                                         admin_state="on",
                                         interval_days="30",
                                         time_of_day_hour="0",
                                         time_of_day_minute="0",
                                         maximum_retry_count="1",
                                         poll_interval_seconds="300",
                                         retry_delay_minutes="10",
                                         minimum_send_now_interval_seconds="5",
                                         send_now=False,
                                         **kwargs):
    """
    Configures callhome system inventory

    Args:
        handle (UcsHandle)
        admin_state (string): enable/disable send inventory
         valid values "on" and "off"
        interval_days (string): send interval(days)
        time_of_day_hour (string): Hours of day to send
        time_of_day_minute (string): Minute of hour
        poll_interval_seconds (string): poll interval in seconds
        retry_delay_minutes (string): retry after 'n' minutes
        minimum_send_now_interval_seconds (string): minimum send interval
        send_now (bool): send inventory now, True/False
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        CallhomePeriodicSystemInventory : ManagedObject

    Raises:
        UcsOperationError: If CallhomePeriodicSystemInventory is not present

    Example:
        call_home_system_inventory_configure(handle, admin_state="off")
    """
    dn = _base_dn + "periodicsysteminventory"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_system_inventory_configure",
                        "Callhome system inventory '%s' does not exist." % dn)

    send_now = ("no", "yes")[send_now]

    args = {
        'admin_state': admin_state,
        'interval_days': interval_days,
        'time_of_day_hour': time_of_day_hour,
        'time_of_day_minute': time_of_day_minute,
        'maximum_retry_count': maximum_retry_count,
        'poll_interval_seconds': poll_interval_seconds,
        'retry_delay_minutes': retry_delay_minutes,
        'minimum_send_now_interval_seconds': minimum_send_now_interval_seconds,
        'send_now': send_now
    }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_system_inventory_send_now(handle):
    """
    Sends callhome system inventory now.

    Args:
        handle (UcsHandle)

    Returns:
        CallhomePeriodicSystemInventory : ManagedObject

    Raises:
        UcsOperationError: If CallhomePeriodicSystemInventory is not present

    Example:
        call_home_system_inventory_send_now(handle)
    """
    dn = _base_dn + "periodicsysteminventory"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_system_inventory_configure",
                        "Callhome system inventory '%s' does not exist." % dn)

    mo.send_now = "yes"
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_anonymous_reporting_on(handle, user_acknowledged=True):
    """
    Sets anonymous reporting 'on'

    Args:
        handle (UcsHandle)
        user_acknowledged (bool): True or False

    Returns:
        CallhomeAnonymousReporting : ManagedObject

    Raises:
        UcsOperationError: If CallhomeAnonymousReporting is not present

    Example:
        call_home_anonymous_reporting_on(handle)
    """
    dn = _base_dn + "anonymousreporting"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_anonymous_reporting_on",
                    "Callhome Anonymous Reporting '%s' does not exist." % dn)

    user_acknowledged = ("no", "yes")[user_acknowledged]

    mo.admin_state="on"
    mo.user_acknowledged=user_acknowledged

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_anonymous_reporting_off(handle, user_acknowledged=True):
    """
    Sets anonymous reporting 'off'

    Args:
        handle (UcsHandle)
        user_acknowledged (bool): True or False

    Returns:
        CallhomeAnonymousReporting : ManagedObject

    Raises:
        UcsOperationError: If CallhomeAnonymousReporting is not present

    Example:
        call_home_anonymous_reporting_off(handle)
    """
    dn = _base_dn + "anonymousreporting"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_anonymous_reporting_off",
                    "Callhome Anonymous Reporting '%s' does not exist." % dn)

    user_acknowledged = ("no", "yes")[user_acknowledged]

    mo.admin_state="off"
    mo.user_acknowledged=user_acknowledged

    handle.set_mo(mo)
    handle.commit()
    return mo

