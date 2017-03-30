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
        handle (UcscHandle)
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
    Configures call home

    Args:
        handle (UcscHandle)
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
        SmartcallhomeSource: ManagedObject

    Raises:
        UcsOperationError: If SmartcallhomeSource is not present

    Example:
        from ucsmsdk.mometa.callhome.SmartcallhomeSource import \
            SmartcallhomeSourceConsts

        call_home_config(handle,
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

    # configure call home
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
        handle (UcscHandle)

    Returns:
        CallhomeEp : ManagedObject

    Raises:
        UcsOperationError: If CallhomeEp is not present

    Example:
        call_home_state_disable(handle)
    """

    mo = handle.query_dn(_base_dn)
    if not mo:
        raise UcsOperationError("call_home_disable",
                                 "Call home not available.")

    mo.admin_state = "off"

    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_profile_create(handle, name, format="xml", level="debug",
                             max_size="1000000", alert_groups=None,
                             descr=None, **kwargs):

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
    dn = _base_dn + "/profile-" + name
    if mo is None:
        raise UcsOperationError(caller,
                                "Callhome Profile '%s' does not exist" % dn)
    return mo


def call_home_profile_exist(handle, name, **kwargs):
    try:
        mo = call_home_profile_get(handle, name,
                                   caller="call_home_profile_exist")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def call_home_profile_modify(handle, name, **kwargs):
    mo = call_home_profile_get(handle, name, caller="call_home_profile_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_profile_remove(handle, name):
    mo = call_home_profile_get(handle, name, caller="call_home_profile_remove")
    handle.remove_mo(mo)
    handle.commit()


def call_home_profile_email_add(handle, profile_name, email, **kwargs):
    profile = call_home_profile_get(handle, profile_name,
                                    caller="call_home_profile_email_add")
    mo = CallhomeDest(parent_mo_or_dn=profile, email=email)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo

def call_home_profile_email_get(handle, profile_name, email,
                                caller="call_home_profile_email_get"):
    profile_dn = _base_dn + "/profile-" + profile_name
    dn = profile_dn + "/email-" + email
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Callhome Profile Email '%s' does not exist" % dn)
    return mo


def call_home_profile_email_exist(handle, profile_name, email, **kwargs):
    try:
        mo = call_home_profile_email_get(handle, profile_name, email,
                                    caller="call_home_profile_email_exist")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def call_home_profile_email_remove(handle, profile_name, email):
    mo = call_home_profile_email_get(handle, profile_name, email,
                                caller="call_home_profile_email_remove")
    handle.remove_mo(mo)
    handle.commit()


def call_home_policy_create(handle, cause, admin_state="enabled",
                            name=None, descr=None, **kwargs):
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
    dn = _base_dn + "/policy-" + cause
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Callhome Policy '%s' does not exist" % dn)
    return mo


def call_home_policy_exist(handle, cause, **kwargs):
    try:
        mo = call_home_policy_get(handle, cause,
                                  caller="call_home_policy_exist")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def call_home_policy_modify(handle, cause, **kwargs):
    mo = call_home_policy_get(handle, cause, caller="call_home_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_policy_remove(handle, cause):
    mo = call_home_policy_get(handle, cause, caller="call_home_policy_remove")
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
                                         send_now="no",
                                         **kwargs):
    dn = _base_dn + "periodicsysteminventory"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_system_inventory_configure",
                        "Callhome system inventory '%s' does not exist." % dn)

    mo.admin_state = admin_state
    mo.interval_days = interval_days
    mo.time_of_day_hour = time_of_day_hour
    mo.time_of_day_minute = time_of_day_minute
    mo.maximum_retry_count = maximum_retry_count
    mo.poll_interval_seconds = poll_interval_seconds
    mo.retry_delay_minutes = retry_delay_minutes
    mo.minimum_send_now_interval_seconds = minimum_send_now_interval_seconds
    mo.send_now = send_now

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_system_inventory_send_now(handle):
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
    dn = _base_dn + "anonymousreporting"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_anonymous_reporting_on",
                    "Callhome Anonymous Reporting '%s' does not exist." % dn)

    mo.admin_state="on"
    handle.set_mo(mo)
    handle.commit()
    return mo


def call_home_anonymous_reporting_off(handle, user_acknowledged=True):
    dn = _base_dn + "anonymousreporting"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError("call_home_anonymous_reporting_off",
                    "Callhome Anonymous Reporting '%s' does not exist." % dn)

    mo.admin_state="off"
    handle.set_mo(mo)
    handle.commit()
    return mo

