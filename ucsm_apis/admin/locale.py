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
This module performs the operation related to dns server management.
"""
from ucsmsdk.ucsexception import UcsOperationError

_base_dn = "sys/user-ext"


def locale_create(handle, name, policy_owner="local", descr=None, **kwargs):
    """
    creates a locale

    Args:
        handle (UcsHandle)
        name (string): locale name
        policy_owner(string): policy owner
         valid values are "local", "pending-policy", "policy"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLocale : managed object

    Raises: None

    Example:
        locale_create(handle, name="test_locale")
    """
    from ucsmsdk.mometa.aaa.AaaLocale import AaaLocale

    mo = AaaLocale(parent_mo_or_dn=_base_dn,
                   name=name,
                   policy_owner=policy_owner,
                   descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def locale_get(handle, name, caller="locale_get"):
    """
    gets the locale

    Args:
        handle (UcsHandle)
        name (string): locale name

    Returns:
        AaaLocale : managed object

    Raises:
        UcsOperationError: if AaaLocale is not present

    Example:
        locale_get(handle, name="test_locale")
    """
    dn = _base_dn + "/locale-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "Locale '%s' does not exist" % dn)
    return mo


def locale_exists(handle, name, **kwargs):
    """
    checks if locale exists

    Args:
        handle (UcsHandle)
        name (string): locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaLocale MO/None)

    Raises:
        None

    Example:
        locale_exists(handle, name="test_locale")
    """
    try:
        mo = locale_get(handle, name, caller="locale_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def locale_modify(handle, name, **kwargs):
    """
    modifies a locale

    Args:
        handle (UcsHandle)
        name (string): locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaLocale : managed object

    Raises:
        UcsOperationError: if AaaLocale is not present

    Example:
        locale_modify(handle, name="test_locale", descr="testing locale")
    """
    mo = locale_get(handle, name, caller="locale_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def locale_delete(handle, name):
    """
    deletes locale

    Args:
        handle (UcsHandle)
        name (string): locale name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaLocale is not present

    Example:
        locale_delete(handle, name="test_locale")
    """
    mo = locale_get(handle, name, caller="locale_delete")
    handle.remove_mo(mo)
    handle.commit()


def locale_org_assign(handle, locale_name, name, org_dn="org-root", descr=None,
                      **kwargs):
    """
    assigns a locale to org

    Args:
        handle (UcsHandle)
        locale_name(string): locale name
        name (string): name for the org assignment
        org_dn (string): org dn
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaOrg : managed object

    Raises:
        UcsOperationError: If AaaLocale or OrgOrg is not present

    Example:
        locale_org_assign(handle, locale_name="test_locale",
                          name="test_org_assign")
    """
    from ucsmsdk.mometa.aaa.AaaOrg import AaaOrg

    locale = locale_get(handle, locale_name, caller="locale_org_assign")

    if not handle.query_dn(org_dn):
        raise UcsOperationError("locale_org_assign",
                                "org '%s' does not exist" % org_dn)

    mo = AaaOrg(parent_mo_or_dn=locale, name=name, org_dn=org_dn, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def locale_org_exists(handle, locale_name, name, **kwargs):
    """
    checks if org is already assigned to org

    Args:
        handle (UcsHandle)
        locale_name(string): locale name
        name (string): name of org assignment
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaOrg MO/None)

    Raises:
        None

    Example:
        locale_org_exists(handle, locale_name="test_locale,
                            name="org_name")
    """
    locale_dn = _base_dn + "/locale-" + locale_name
    dn = locale_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def locale_org_unassign(handle, locale_name, name):
    """
    unassigns a locale from org

    Args:
        handle (UcsHandle)
        locale_name(string): locale name
        name (string): name of org assignment

    Returns:
        None

    Raises:
        UcsOperationError: If AaaOrg is not present

    Example:
        locale_org_unassign(handle, locale_name="test_locale,
                            name="org_name")
    """
    locale_dn = _base_dn + "/locale-" + locale_name
    dn = locale_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError("locale_org_unassign",
                                "org '%s' not assigned to locale" % dn)

    handle.remove_mo(mo)
    handle.commit()
