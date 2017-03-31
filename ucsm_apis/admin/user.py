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
This module performs the operation related to user.
"""
from ucsmsdk.ucsexception import UcsOperationError

_base_dn = "sys/user-ext"


def user_create(handle, name, pwd, clear_pwd_history=False,
                pwd_life_time="no-password-expire", account_status="active",
                expires=False, expiration="never",
                enc_pwd_set=False, enc_pwd=None,
                first_name=None, last_name=None,
                phone=None, email=None, descr=None,
                **kwargs):


    """
    Creates user

    Args:
        handle (UcsHandle)
        name (string): name
        first_name (string): first_name
        last_name (string): last_name
        descr (string): descr
        clear_pwd_history (string): clear_pwd_history
        phone (string): phone
        email (string): email
        pwd (string): pwd
        expires (string): expires
        pwd_life_time (string): pwd_life_time
        expiration (string): expiration
        enc_pwd (string): enc_pwd
        account_status (string): account_status
        role (string): role
        role_descr (string): role_descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUser: Managed Object

    Example:
        user_create(handle, name="test", first_name="firstname",
                  last_name="lastname", descr=None, clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  pwd="p@ssw0rd", expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd=None,
                  account_status="active")
    """

    from ucsmsdk.mometa.aaa.AaaUser import AaaUser

    clear_pwd_history = ("no", "yes")[clear_pwd_history]
    expires = ("no", "yes")[expires]
    enc_pwd_set = ("no", "yes")[enc_pwd_set]

    mo = AaaUser(parent_mo_or_dn=_base_dn,
                 name=name,
                 first_name=first_name,
                 last_name=last_name,
                 descr=descr,
                 clear_pwd_history=clear_pwd_history,
                 phone=phone,
                 email=email,
                 pwd=pwd,
                 expires=expires,
                 pwd_life_time=pwd_life_time,
                 expiration=expiration,
                 enc_pwd=enc_pwd,
                 enc_pwd_set=enc_pwd_set,
                 account_status=account_status)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_get(handle, name, caller="user_get"):
    """
    Gets user

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        AaaUser: Managed Object OR None

    Example:
        user_get(handle, name="test")
    """

    dn = _base_dn + "/user-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "User '%s' does not exist" % dn)
    return mo


def user_exists(handle, name, **kwargs):
    """
    checks if user exists

    Args:
        handle (UcsHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        user_exists(handle, name="test", first_name="firstname",
                  last_name="lastname", descr=None, clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd=None,
                  account_status="active")
    """
    try:
        mo = user_get(handle, name, caller="user_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_modify(handle, name, **kwargs):
    """
    modifies user

    Args:
        handle (UcsHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaUser: Managed Object

    Raises:
        UcsOperationError: If AaaUser is not present

    Example:
        user_modify(handle, name="test", first_name="firstname",
                  last_name="lastname", descr=None, clear_pwd_history="no",
                  phone="+91-1234567890", email="test@cisco.com",
                  expires="yes",
                  pwd_life_time="no-password-expire",
                  expiration="2016-01-13T00:00:00", enc_pwd=None,
                  account_status="active")
    """

    mo = user_get(handle, name, "user_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def user_delete(handle, name):
    """
    deletes user

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        None

    Raises:
        UcsOperationError: If AaaUser is not present

    Example:
        user_delete(handle, name="test")

    """

    mo = user_get(handle, name, "user_delete")
    handle.remove_mo(mo)
    handle.commit()


def user_role_add(handle, user_name, name, descr=None, **kwargs):
    """
    Adds role to an user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserRole: Managed object

    Raises:
        UcsOperationError: If AaaUser is not present

    Example:
        user_role_add(handle, user_name="test", name="admin")
    """
    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole

    user = user_get(handle, user_name, "user_role_add")

    mo = AaaUserRole(parent_mo_or_dn=user, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_role_get(handle, user_name, name, caller="user_role_get"):
    """
    Gets role for the user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        AaaUserRole: Managed object OR None

    Example:
        user_role_get(handle, user_name="test", name="admin")
    """

    user_dn = _base_dn + "/user-" + user_name
    dn = user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "User role '%s' does not exist" % dn)
    return mo


def user_role_exists(handle, user_name, name, **kwargs):
    """
    check if role is already added to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        user_role_exists(handle, user_name="test", name="admin")
    """
    try:
        mo = user_role_get(handle, user_name, name, "user_role_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_role_remove(handle, user_name, name):
    """
    Remove role from user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        None

    Raises:
        UcsOperationError: If AaaUserRole is not present

    Example:
        user_role_remove(handle, user_name="test", name="admin")
    """

    mo = user_role_get(handle, user_name, name, "user_role_remove")
    handle.remove_mo(mo)
    handle.commit()


def user_locale_add(handle, user_name, name, descr=None, **kwargs):
    """
    Adds locale to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserLocale: Managed Object

    Raises:
        UcsOperationError: If AaaUser is not present

    Example:
        user_locale_add(handle, user_name="test", name="testlocale")
    """

    from ucsmsdk.mometa.aaa.AaaUserLocale import AaaUserLocale

    user = user_get(handle, user_name, caller="user_locale_add")

    mo = AaaUserLocale(parent_mo_or_dn=user, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def user_locale_get(handle, user_name, name, caller="user_locale_get"):
    """
    Gets locale for the user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        AaaUserLocale: Managed Object OR None

    Example:
        user_locale_get(handle, user_name="test", name="testlocale")
    """
    user_dn = _base_dn + "/user-" + user_name
    dn = user_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "User locale '%s' does not exist" % dn)
    return mo


def user_locale_exists(handle, user_name, name, **kwargs):
    """
    check if locale already added to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        user_locale_exists(handle, user_name="test", name="testlocale")
    """
    try:
        mo = user_locale_get(handle, user_name, name,
                             caller="user_locale_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_locale_remove(handle, user_name, name):
    """
    Remove locale from user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        None

    Raises:
        UcsOperationError: If AaaUserLocale is not present

    Example:
        user_locale_remove(handle, user_name="test", name="testlocale")
    """

    mo = user_locale_get(handle, user_name, name, caller="user_locale_remove")
    handle.remove_mo(mo)
    handle.commit()


def password_strength_check(handle, descr=None, **kwargs):
    """
    Check password strength for locally authenticated user

    Args:
        handle (UcsHandle)
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserEp: Managed Object

    Example:
        password_strength_check(handle)
    """

    mo = handle.query_dn(_base_dn + "/pwd-profile")
    mo.pwd_strength_check = "yes"
    mo.descr = descr

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def password_strength_uncheck(handle):
    """
    check or un-check password strength for locally authenticated user

    Args:
        handle (UcsHandle)

    Returns:
        AaaUserEp: Managed Object

    Example:
        password_strength_uncheck(handle)
    """

    mo = handle.query_dn(_base_dn + "/pwd-profile")
    mo.pwd_strength_check = "no"
    handle.set_mo(mo)
    handle.commit()
    return mo


def password_profile_modify(handle, change_interval=None,
                            no_change_interval=None,
                            change_during_interval=None, change_count=None,
                            history_count=None, expiration_warn_time=None,
                            descr=None, **kwargs):
    """
    Modify password profile of locally authenticated user

    Args:
        handle (UcsHandle)
        change_interval (string): change interval
        no_change_interval (string): no change interval
        change_during_interval (string): ["disable", "enable"]
        change_count (string): change count
        history_count (string): history count
        expiration_warn_time(string): expiration warn time
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaPwdProfile: Managed Object

    Raises:
        UcsOperationError: If AaaPwdProfile is not present

    Example:
        password_profile_modify(handle, change_count="2")
    """

    dn = _base_dn + "/pwd-profile"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("password_profile_modify",
                                 "password profile does not exist.")

    args = {'change_interval': change_interval,
            'no_change_interval': no_change_interval,
            'change_during_interval': change_during_interval,
            'change_count': change_count,
            'history_count': history_count,
            'expiration_warn_time': expiration_warn_time,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo
