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
from ucscsdk.ucscexception import UcscOperationError

_base_dn = "sys/user-ext"


def locale_create(handle, name, descr=None, **kwargs):
    """
    creates a locale

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLocale : Managed Object

    Example:
        locale_create(handle, name="test_locale")
    """

    from ucscsdk.mometa.aaa.AaaLocale import AaaLocale

    mo = AaaLocale(parent_mo_or_dn=_base_dn,
                   name=name,
                   descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_get(handle, name, caller="locale_get"):
    """
    Gets the locale

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider

    Returns:
        AaaLocale : Managed Object OR None

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
        handle (UcscHandle)
        name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

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
        handle (UcscHandle)
        name (string): name of locale
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaLocale : Managed Object

    Raises:
        UcscOperationError: If AaaLocale is not present

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
        handle (UcscHandle)
        name (string): locale name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaLocale is not present

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
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name for the assignment
        org_dn (string): Dn string of the org
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaOrg : Managed Object

    Raises:
        UcscOperationError: If AaaLocale is not present

    Example:
        locale_org_assign(handle, locale_name="test_locale",
                          name="test_org_assign")
    """

    from ucscsdk.mometa.aaa.AaaOrg import AaaOrg

    obj = locale_get(handle, locale_name, caller="locale_org_assign")

    if not handle.query_dn(org_dn):
        raise UcscOperationError("locale_org_assign",
                                 "org_dn does not exist")

    mo = AaaOrg(parent_mo_or_dn=obj, name=name, org_dn=org_dn, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_org_unassign(handle, locale_name, name):
    """
    unassigns a locale from org

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name of assignment

    Returns:
        None

    Raises:
        UcscOperationError: If AaaOrg is not present

    Example:
        locale_org_unassign(handle, locale_name="test_locale,
                            name="org_name")
    """

    locale_dn = _base_dn + "/locale-" + locale_name
    dn = locale_dn + "/org-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcscOperationError("locale_org_unassign",
                                 "No Org assigned to Locale")

    handle.remove_mo(mo)
    handle.commit()


def locale_domaingroup_assign(handle, locale_name, name,
                              domaingroup_dn="domaingroup-root", descr=None,
                              **kwargs):
    """
    assigns a locale to domaingroup

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name for the assignment
        domaingroup_dn (string): Dn string of the domaingroup
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaOrg : Managed Object

    Raises:
        UcscOperationError: If AaaLocale is not present

    Example:
        locale_domaingroup_assign(handle, locale_name="test_locale",
                                  name="test_domgrp_asn")
    """

    from ucscsdk.mometa.aaa.AaaDomainGroup import AaaDomainGroup

    obj = locale_get(handle, locale_name, caller="locale_domaingroup_assign")

    if not handle.query_dn(domaingroup_dn):
        raise UcscOperationError("locale_org_assign",
                                 "domaingroup_dn does not exist")

    mo = AaaDomainGroup(parent_mo_or_dn=obj, name=name,
                        domaingroup_dn=domaingroup_dn, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def locale_domaingroup_unassign(handle, locale_name, name):
    """
    unassigns a locale

    Args:
        handle (UcscHandle)
        locale_name(string): locale name
        name (string): name of assignment
        descr (string): descr

    Returns:
        None

    Raises:
        UcscOperationError: If AaaOrg is not present

    Example:
        locale_domaingroup_unassign(handle, locale_name="test_locale,
                                    name="test_domgrp_asn")
    """

    locale_dn = _base_dn + "/locale-" + locale_name
    dn = locale_dn + "/domaingroup-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcscOperationError("locale_domaingroup_unassign",
                                 "No domaingroup assigned to Locale")

    handle.remove_mo(mo)
    handle.commit()
