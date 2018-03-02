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


def user_create(handle, name, pwd=None, clear_pwd_history="no",
                pwd_life_time="no-password-expire", account_status="active",
                expires="no", expiration="never",
                enc_pwd_set="no", enc_pwd=None,
                first_name=None, last_name=None,
                phone=None, email=None, descr=None,
                **kwargs):
    """
    creates user

    Args:
        handle (UcsHandle)
        name (string): user name
        pwd (string): password
        clear_pwd_history (string): clear password history, "yes" or "no"
        pwd_life_time (string): password life time
         valid values are "no-password-expire" or "0-3650" days
        account_status (string): account status
         valid values are "active", "inactive"
        expires (string): expires, valid values are "yes", "no"
        expiration (string): expiration
        enc_pwd_set (string): valid values are "yes", "no"
        enc_pwd (string): encrypted password
        first_name (string): first name
        last_name (string): last name
        phone (string): phone
        email (string): email
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaUser: managed object

    Raises:
        None

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

    mo = AaaUser(parent_mo_or_dn=_base_dn,
                 name=name,
                 pwd=pwd,
                 clear_pwd_history=clear_pwd_history,
                 pwd_life_time=pwd_life_time,
                 account_status=account_status,
                 expires=expires,
                 expiration=expiration,
                 enc_pwd_set=enc_pwd_set,
                 enc_pwd=enc_pwd,
                 first_name=first_name,
                 last_name=last_name,
                 phone=phone,
                 email=email,
                 descr=descr
                 )

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def user_get(handle, name, caller="user_get"):
    """
    gets user

    Args:
        handle (UcsHandle)
        name (string): user name

    Returns:
        AaaUser: managed object

    Raises:
        UcsOperationError: if AaaUser is not present

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
        name (string): user name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaUser MO/None)

    Raises:
        None

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
        name (string): user name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaUser: managed object

    Raises:
        UcsOperationError: if AaaUser is not present

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
        name (string): user name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaUser is not present

    Example:
        user_delete(handle, name="test")

    """
    mo = user_get(handle, name, "user_delete")
    handle.remove_mo(mo)
    handle.commit()


def _user_role_add(handle, user_mo, name, descr=None, **kwargs):
    """
    adds single role to an user
    """
    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole

    mo = AaaUserRole(parent_mo_or_dn=user_mo, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    return mo


def user_role_add(handle, user_name, name, descr=None, **kwargs):
    """
    adds role to an user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): single role or a comma separated string
                       of multiple roles
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaUserRole: managed object

    Raises:
        UcsOperationError: if AaaUser is not present

    Example:
        user_role_add(handle, user_name="test", name="admin")
    """

    user = user_get(handle, user_name, "user_role_add")

    roles = [role.strip() for role in name.split(',')]
    roles_mo = []
    for role in roles:
        role_mo = _user_role_add(handle, user_mo=user, name=role,
                                 descr=descr, **kwargs)
        roles_mo.append(role_mo)

    handle.commit()
    return roles_mo


def user_role_get(handle, user_name, name, caller="user_role_get"):
    """
    gets role of the user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename

    Returns:
        AaaUserRole: managed object

    Raises:
        UcsOperationError: if AaaUserRole is not present

    Example:
        user_role_get(handle, user_name="test", name="admin")
    """
    user_dn = _base_dn + "/user-" + user_name
    dn = user_dn + "/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "User role '%s' does not exist" % dn)
    return mo


def _user_role_exists(handle, user_name, name, **kwargs):
    try:
        mo = user_role_get(handle, user_name, name, "user_role_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def user_role_exists(handle, user_name, name, **kwargs):
    """
    check if role is already added to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): single role or a comma separated string
                       of multiple roles
        **kwargs: key-value pair of managed object(MO) property and value,
                  Use 'print(ucscoreutils.
                  get_meta_info(<classid>).
                  config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaUserRole MO/None)

    Raises:
        None

    Example:
        user_role_exists(handle, user_name="test", name="admin")
    """
    roles = [role.strip() for role in name.split(',')]
    roles_mo = []
    for role in roles:
        status, mo = _user_role_exists(handle, user_name, role, **kwargs)
        if status is False:
            return False, None
        roles_mo.append(mo)

    return True, roles_mo


def user_role_modify(handle, user_name, name, **kwargs):
    """
    modifies user role

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): rolename
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaUserRole: managed object

    Raises:
        UcsOperationError: if AaaUserRole is not present

    Example:
        user_role_modify(handle, user_name="test", name="admin")
    """
    mo = user_role_get(handle, user_name, name, "user_role_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def user_role_remove(handle, user_name, name):
    """
    remove role from user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): single role or a comma separated
                       string of multiple roles

    Returns:
        None

    Raises:
        UcsOperationError: if AaaUserRole is not present

    Example:
        user_role_remove(handle, user_name="test", name="admin")
    """
    roles = [role.strip() for role in name.split(',')]
    for role in roles:
        mo = user_role_get(handle, user_name, role, "user_role_remove")
        handle.remove_mo(mo)
    handle.commit()


def user_locale_add(handle, user_name, name, descr=None, **kwargs):
    """
    adds locale to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserLocale: managed object

    Raises:
        UcsOperationError: if AaaUser is not present

    Example:
        user_locale_add(handle, user_name="test", name="testlocale")
    """
    from ucsmsdk.mometa.aaa.AaaUserLocale import AaaUserLocale

    user = user_get(handle, user_name, caller="user_locale_add")

    mo = AaaUserLocale(parent_mo_or_dn=user, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def user_locale_get(handle, user_name, name, caller="user_locale_get"):
    """
    gets locale for the user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        AaaUserLocale: managed object

    Raises:
        UcsOperationError: if AaaUserLocale is not present

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
    checks if locale already added to user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaUserLocale MO/None)

    Raises:
        None

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


def user_locale_modify(handle, user_name, name, **kwargs):
    """
    modifies locale of user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaUserLocale: managed object

    Raises:
        UcsOperationError: if AaaUserLocale is not present

    Example:
        user_locale_modify(handle, user_name="test", name="testlocale")
    """
    mo = user_locale_get(handle, user_name, name, caller="user_locale_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()


def user_locale_remove(handle, user_name, name):
    """
    removes locale from user

    Args:
        handle (UcsHandle)
        user_name (string): username
        name (string): locale name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaUserLocale is not present

    Example:
        user_locale_remove(handle, user_name="test", name="testlocale")
    """
    mo = user_locale_get(handle, user_name, name, caller="user_locale_remove")
    handle.remove_mo(mo)
    handle.commit()


def password_strength_check_enable(handle, policy_owner="local", descr=None,
                            **kwargs):
    """
    Check password strength for locally authenticated user

    Args:
        handle (UcsHandle)
        policy_owner (string): policy owner
         valid values are "local", "pending-policy", "policy"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaUserEp: managed object

    Raises:
        None

    Example:
        password_strength_check_enable(handle)
    """
    mo = handle.query_dn(_base_dn)

    args = {'pwd_strength_check': "yes",
            'policy_owner': policy_owner,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.set_mo(mo)
    handle.commit()
    return mo


def password_strength_check_exists(handle, **kwargs):
    """
    checks if password strength is checked

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaUserEp MO/None)

    Raises:
        None

    Example:
        password_strength_check_exists(handle)
    """
    mo = handle.query_dn(_base_dn)
    if mo is None:
        return False, None

    kwargs['pwd_strength_check'] = 'yes'
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def password_strength_check_disable(handle):
    """
    un-checks password strength for locally authenticated user

    Args:
        handle (UcsHandle)

    Returns:
        AaaUserEp: managed object

    Raises:
        None

    Example:
        password_strength_check_disable(handle)
    """
    mo = handle.query_dn(_base_dn)

    args = {'pwd_strength_check': "no"}

    mo.set_prop_multiple(**args)
    handle.set_mo(mo)
    handle.commit()
    return mo


def password_profile_modify(handle,
                            min_passphrase_len="8",
                            policy_owner="local",
                            change_during_interval="disable",
                            change_interval=None,
                            no_change_interval=None,
                            history_count=None,
                            change_count=None,
                            expiration_warn_time=None,
                            descr=None,
                            **kwargs):
    """
    modifies password profile of locally authenticated user

    Args:
        handle (UcsHandle)
        min_passphrase_len (string): min passphrase length
        policy_owner (string): policy_owner
         valid values are "local", "pending-policy", "policy"
        change_interval (string): change interval in hours, "1-745"
         Specifies the maximum number of hours over which the
         number of password changes specified in the change_count
         field are enforced.
        no_change_interval (string): no change interval in hours, "1-745"
         Specifies the minimum number of hours that a
         locally authenticated user must wait before changing
         a newly created password.
        change_during_interval (string): change during interval
         valid values are "disable", "enable"
         Restricts the number of password changes a locally
         authenticated user can make within a given number of
         hours.
        change_count (string): change count, "0-10"
         Specifies the maximum number of times a locally
         authenticated user can change his or her password during
         the change_interval
        history_count (string): history password count, "0-15"
         Specifies the number of unique passwords that a locally
         authenticated user must create before that user can reuse
         a previously used password
        expiration_warn_time(string): expiration warning time
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaPwdProfile: managed object

    Raises:
        UcsOperationError: if AaaPwdProfile is not present

    Example:
        password_profile_modify(handle, change_count="2")
    """
    dn = _base_dn + "/pwd-profile"
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("password_profile_modify",
                                "password profile does not exist.")

    args = {'min_passphrase_len': min_passphrase_len,
            'policy_owner': policy_owner,
            'change_interval': change_interval,
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


def password_profile_exists(handle, **kwargs):
    """
    checks if password profile exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaPwdProfile MO/None)

    Raises:
        None

    Example:
        password_profile_exists(handle, change_count="2")
    """
    dn = _base_dn + "/pwd-profile"
    mo = handle.query_dn(dn)
    if mo is None:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)
