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
This module performs the operation related to ldap.
"""
from ucsmsdk.ucsexception import UcsOperationError

_ldap_dn = "sys/ldap-ext"


def ldap_configure(handle, timeout="30", attribute="CiscoAvPair",
                   filter="cn=$userid", retries="1", policy_owner="local",
                   basedn=None, descr=None, **kwargs):
    """
    Configures the ldap

    Args:
        handle (UcsHandle)
        timeout (string): timeout
        attribute (string): attribute
        filter (string): filter
        retries (string): retries
        policy_owner (string): policy owner
         valid values are "local", "pending-policy", "policy"
        basedn (string): basedn
        descr (string): description

    Returns:
        AaaLdapEp : managed object

    Example:
        ldap_configure(handle, timeout="40")
    """
    mo = handle.query_dn(dn=_ldap_dn)
    args = {
        "timeout": timeout,
        "attribute": attribute,
        "filter": filter,
        "retries": retries,
        "policy_owner": policy_owner,
        "basedn": basedn,
        "descr": descr
    }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_exists(handle, **kwargs):
    """
    checks if ldap configuration exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaLdapEp MO/None)

    Raises:
        None

    Example:
        ldap_exists(handle, timeout="40")
    """
    mo = handle.query_dn(dn=_ldap_dn)
    if mo is None:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_create(handle, name, order="lowest-available", rootdn=None,
                         basedn="", port="389", enable_ssl="no", filter=None,
                         attribute=None, key=None, timeout="30",
                         vendor="OpenLdap", retries="1",
                         descr=None, **kwargs):
    """
    creates a ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider (Hostname/FQDN or IP Address)
        order (string): "lowest-available" or 0-16
        rootdn (string): rootdn
        basedn (string): basedn
        port (string): port
        enable_ssl (string): enable ssl, valid valies are "yes", "no"
        filter (string): filter
        attribute (string): attribute
        key (string): key
        timeout (string): timeout
        vendor (string): vendor
         valid values are "MS-AD", "OpenLdap"
        retries (string): retries
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLdapProvider : managed object

    Raises:
        None

    Example:
        ldap_provider_create(handle, name="test_ldap_prov", port="320",
                             order="3")
    """
    from ucsmsdk.mometa.aaa.AaaLdapProvider import AaaLdapProvider

    mo = AaaLdapProvider(parent_mo_or_dn=_ldap_dn,
                         name=name,
                         order=order,
                         rootdn=rootdn,
                         basedn=basedn,
                         port=port,
                         enable_ssl=enable_ssl,
                         filter=filter,
                         attribute=attribute,
                         key=key,
                         timeout=timeout,
                         vendor=vendor,
                         retries=retries,
                         descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_provider_get(handle, name, caller="ldap_provider_get"):
    """
    Gets the ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        caller (string): name of the caller function

    Returns:
        AaaLdapProvider : managed object

    Raises:
        UcsOperationError: if AaaLdapProvider is not present

    Example:
        ldap_provider_get(handle, name="test_ldap_provider")
    """
    dn = _ldap_dn + "/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Ldap Provider '%s' does not exist" % dn)
    return mo


def ldap_provider_exists(handle, name, **kwargs):
    """
    checks if ldap provider exists

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaLdapProvider MO/None)

    Raises:
        None

    Example:
        ldap_provider_exists(handle, name="test_ldap_provider")
    """
    try:
        mo = ldap_provider_get(handle, name, caller="ldap_provider_exists")
    except UcsOperationError:
        return (False, None)

    if 'order' in kwargs and kwargs['order'] == 'lowest-available':
        kwargs.pop('order', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_modify(handle, name, **kwargs):
    """
    modifies a ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaLdapProvider : Managed Object

    Raises:
        UcsOperationError: if AaaLdapProvider is not present

    Example:
        ldap_provider_modify(handle, name="test_ldap_prov", enable_ssl="yes")
    """
    mo = ldap_provider_get(handle, name, "ldap_provider_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_provider_delete(handle, name):
    """
    deletes a ldap provider

    Args:
        handle (UcsHandle)
        name (string): name of ldap provider

    Returns:
        None

    Raises:
        UcsOperationError: if AaaLdapProvider is not present

    Example:
        ldap_provider_delete(handle, name="test_ldap_prov")
    """
    mo = ldap_provider_get(handle, name, "ldap_provider_delete")
    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_rules_configure(handle, ldap_provider_name,
                                        authorization="enable",
                                        traversal="recursive",
                                        target_attr="memberOf",
                                        use_primary_group="no",
                                        name=None,
                                        descr=None,
                                        **kwargs):
    """
    configures group rules of a ldap provider

    Args:
        handle (UcsHandle)
        ldap_provider_name (string): name of ldap provider
        authorization (string): group authorization
         valid values are "disable", "enable"
        traversal (string): group recursion
         valid values are "non-recursive", "recursive"
        target_attr (string): target atribute
        use_primary_group (string): valid values are "yes", "no"
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLdapGroupRule : managed object

    Raises:
        UcsOperationError: if AaaLdapProvider is not present

    Example:
        ldap_provider_group_rules_configure( handle,
                                        ldap_provider_name="test_ldap_prov",
                                        authorization="enable")
    """
    from ucsmsdk.mometa.aaa.AaaLdapGroupRule import AaaLdapGroupRule

    obj = ldap_provider_get(handle, ldap_provider_name,
                            "ldap_provider_group_rules_configure")

    mo = AaaLdapGroupRule(parent_mo_or_dn=obj,
                          authorization=authorization,
                          traversal=traversal,
                          target_attr=target_attr,
                          use_primary_group=use_primary_group,
                          name=name,
                          descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_provider_group_rules_exists(handle, ldap_provider_name, **kwargs):
    """
    checks if group rules for ldap provider exists

    Args:
        handle (UcsHandle)
        ldap_provider_name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaLdapGroupRule MO/None)

    Raises:
        None

    Example:
        ldap_provider_group_rules_exists(handle,
                                    ldap_provider_name="test_ldap_provider",
                                    authorization="enable")
    """
    provider_dn = _ldap_dn + "/provider-" + ldap_provider_name
    dn = provider_dn + "/ldapgroup-rule"
    mo = handle.query_dn(dn)
    if mo is None:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_create(handle, name, descr=None, **kwargs):
    """
    creates ldap group map

    Args:
        handle (UcsHandle)
        name (string): ldap group name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLdapGroup : managed object

    Example:
        ldap_group_create(handle, name="test_ldap_grp_map")
    """
    from ucsmsdk.mometa.aaa.AaaLdapGroup import AaaLdapGroup

    mo = AaaLdapGroup(parent_mo_or_dn=_ldap_dn, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_group_get(handle, name, caller="ldap_group_get"):
    """
    Gets ldap group map

    Args:
        handle (UcsHandle)
        name (string): ldap group name
        caller (string): name of the caller function

    Returns:
        AaaLdapGroup : managed object

    Raises:
        UcsOperationError: if AaaLdapGroup is not present

    Example:
        ldap_group_get(handle, name="test_ldap_group")
    """
    dn = _ldap_dn + "/ldapgroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Ldap Group Map '%s' does not exist." % dn)
    return mo


def ldap_group_exists(handle, name, **kwargs):
    """
    checks if ldap group map exists

    Args:
        handle (UcsHandle)
        name (string): ldap group map name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaLdapGroup MO/None)

    Example:
        ldap_group_exists(handle, name="test_ldap_group")
    """
    try:
        mo = ldap_group_get(handle, name, "ldap_group_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_delete(handle, name):
    """
    deletes ldap group map

    Args:
        handle (UcsHandle)
        name (string): ldap group map name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaLdapGroup is not present

    Example:
        ldap_group_delete(handle, name="test_ldap_grp_map")
    """
    mo = ldap_group_get(handle, name, "ldap_group_delete")
    handle.remove_mo(mo)
    handle.commit()


def ldap_group_role_add(handle, ldap_group_name, name, descr=None,
                        **kwargs):
    """
    add role to ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  role name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserRole : managed object

    Raises:
        UcsOperationError: if AaaLdapGroup or AaaRole is not present

    Example:
        ldap_group_role_add(
          handle, ldap_group_name="test_ldap_grp_map", name="storage")
    """
    from ucsmsdk.mometa.aaa.AaaUserRole import AaaUserRole
    from ..admin.role import role_get

    role = role_get(handle, name=name)

    ldap_group = ldap_group_get(handle, name=ldap_group_name,
                                caller="ldap_group_role_add")

    mo = AaaUserRole(parent_mo_or_dn=ldap_group, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_group_role_get(handle, ldap_group_name, name,
                        caller="ldap_group_role_get"):
    """
    Gets the role  for the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  role name
        caller (string): name of the caller function

    Returns:
        AaaUserRole : managed object

    Raise:
        UcsOperationError: if AaaUserRole is not present

    Example:
        ldap_group_role_get(handle,
                            ldap_group_name="test_ldap_grp_map",
                            name="test_role")
    """
    dn = _ldap_dn + "/ldapgroup-" + ldap_group_name + "/role-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Ldap group map role '%s' does not exist" % dn)
    return mo


def ldap_group_role_exists(handle, ldap_group_name, name, **kwargs):
    """
    checks if role exists for the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaUserRole MO/None)

    Raises:
        None

    Example:
        ldap_group_role_exists(handle,
                                   ldap_group_name="test_ldap_grp_map",
                                   name="test_role")
    """
    try:
        mo = ldap_group_role_get(handle, ldap_group_name, name,
                                 caller="ldap_group_role_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_role_remove(handle, ldap_group_name, name):
    """
    removes role from the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  role name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaUserRole is not present

    Example:
        ldap_group_role_remove(handle,
                               ldap_group_name="test_ldap_grp_map",
                               name="test_role")
    """
    mo = ldap_group_role_get(handle, ldap_group_name, name,
                             caller="ldap_group_role_remove")
    handle.remove_mo(mo)
    handle.commit()


def ldap_group_locale_add(handle, ldap_group_name, name, descr=None,
                          **kwargs):
    """
    adds locale to ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  locale name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserLocale : managed object

    Raises:
        UcsOperationError: if AaaLdapGroup or AaaLocale is not present

    Example:
        ldap_group_locale_add(
          handle, ldap_group_name="test_ldap_grp_map", name="locale1")
    """
    from ucsmsdk.mometa.aaa.AaaUserLocale import AaaUserLocale
    from ..admin.locale import locale_get

    locale = locale_get(handle, name, caller="ldap_group_locale_add")

    ldap_group = ldap_group_get(handle, name=ldap_group_name,
                         caller="ldap_group_locale_add")

    mo = AaaUserLocale(parent_mo_or_dn=ldap_group, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_group_locale_get(handle, ldap_group_name, name,
                          caller="ldap_group_locale_get"):
    """
    Gets the locale for the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  locale name
        caller (string): name of the caller function

    Returns:
        AaaUserLocale : managed object

    Raises:
        UcsOperationError: if AaaUserLocale is not present

    Example:
        ldap_group_locale_get(handle,
                              ldap_group_name="test_ldap_grp_map",
                              name="locale1")
    """
    dn = _ldap_dn + "/ldapgroup-" + ldap_group_name + "/locale-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Ldap Group Map Locale '%s' does not exist" % dn)
    return mo


def ldap_group_locale_exists(handle, ldap_group_name, name, **kwargs):
    """
    checks if locale exists for the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaUserLocale MO/None)

    Raises:
        None

    Example:
        ldap_group_locale_exists(handle,
                                 ldap_group_name="test_ldap_grp_map",
                                 name="locale1")
    """
    try:
        mo = ldap_group_locale_get(handle, ldap_group_name, name,
                                   caller="ldap_group_locale_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_locale_remove(handle, ldap_group_name, name):
    """
    removes locale from the respective ldap group map

    Args:
        handle (UcsHandle)
        ldap_group_name (string): name of ldap group
        name (string):  locale name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaUserLocale is not present

    Example:
        ldap_group_locale_remove(handle,
                                 ldap_group_name="test_ldap_grp_map",
                                 name="locale1")
    """

    mo = ldap_group_locale_get(handle, ldap_group_name, name,
                               caller="ldap_group_locale_remove")
    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_create(handle, name, descr=None, **kwargs):
    """
    creates ldap provider group

    Args:
        handle (UcsHandle)
        name (string): ldap provider group name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderGroup : managed object

    Raises:
        None

    Example:
        ldap_provider_group_create(handle, name="test_ldap_group")
    """
    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn=_ldap_dn,
                          name=name,
                          descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_provider_group_get(handle, name, caller="ldap_provider_group_get"):
    """
    Gets ldap provider group

    Args:
        handle (UcsHandle)
        name (string): ldap provider group name
        caller (string): name of the caller function

    Returns:
        AaaProviderGroup : managed object

    Raises:
        UcsOperationError: if AaaProviderGroup is not present

    Example:
        ldap_provider_group_get(handle, name="test_ldap_group")
    """
    dn = _ldap_dn + "/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Ldap Provider Group '%s' does not exist" % dn)
    return mo


def ldap_provider_group_exists(handle, name, **kwargs):
    """
    checks if ldap provider group exists

    Args:
        handle (UcsHandle)
        name (string): ldap provider group name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaProviderGroup MO/None)

    Raises:
        None

    Example:
        ldap_provider_group_exists(handle, name="test_ldap_group")
    """
    try:
        mo = ldap_provider_group_get(handle, name,
                                     caller="ldap_provider_group_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_group_delete(handle, name):
    """
    deletes ldap provider group

    Args:
        handle (UcsHandle)
        name (string): ldap provider group name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaProviderGroup is not present

    Example:
        ldap_provider_group_delete(handle, name="test_ldap_group")
    """
    mo = ldap_provider_group_get(handle, name,
                                 caller="ldap_provider_group_delete")
    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_provider_add(handle, group_name, name,
                                     order="lowest-available",
                                     descr=None, **kwargs):
    """
    adds provider to ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): ldap provider name
        order (string): order
         valid values are "lowest-available" or "0-16"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaProviderRef : managed object

    Raises:
        UcsOperationError: if AaaProviderGroup or AaaProvider is not present

    Example:
        ldap_provider_group_provider_add(handle,
                                        group_name="test_ldap_provider_group",
                                        name="test_ldap_provider",
                                        order="1")
    """
    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    ldap_provider = ldap_provider_get(handle, name=name,
                                    caller="ldap_provider_group_provider_add")

    ldap_provider_group = ldap_provider_group_get(handle, name=group_name,
                                    caller="ldap_provider_group_provider_add")

    mo = AaaProviderRef(parent_mo_or_dn=ldap_provider_group,
                        name=name,
                        order=order,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def ldap_provider_group_provider_get(handle, group_name, name,
                                    caller="ldap_provider_group_provider_get"):
    """
    Gets provider for ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): ldap provider name
        caller (string): name of the caller function

    Returns:
        AaaProviderRef : managed object

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        ldap_provider_group_provider_get(handle,
                                         group_name="test_ldap_provider_group",
                                         name="test_provider")
    """
    provider_group_dn = _ldap_dn + "/providergroup-" + group_name
    provider_ref_dn = provider_group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_ref_dn)
    if mo is None:
        raise UcsOperationError(caller,
            "Ldap Provider Reference '%s' does not exist" % provider_ref_dn)
    return mo


def ldap_provider_group_provider_exists(handle, group_name, name, **kwargs):
    """
    checks if provider added ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): ldap provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaProviderRef MO/None)

    Raises:
        None

    Example:
        ldap_provider_group_provider_exists(handle,
                group_name="test_ldap_provider_group", name="test_provider")
    """
    try:
        mo = ldap_provider_group_provider_get(handle, group_name, name,
                                caller="ldap_provider_group_provider_exists")
    except UcsOperationError:
        return (False, None)

    if 'order' in kwargs and kwargs['order'] == 'lowest-available':
        kwargs.pop('order', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_group_provider_modify(handle, group_name, name, **kwargs):
    """
    modify provider of ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): ldap provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaProviderRef : managed object

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        ldap_provider_group_provider_modify(handle,
                                         group_name="test_ldap_provider_group",
                                         name="test_provider",
                                         order="1")
    """
    mo = ldap_provider_group_provider_get(handle, group_name, name,
                                caller="ldap_provider_group_provider_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_provider_group_provider_remove(handle, group_name, name):
    """
    removes provider from ldap provider group

    Args:
        handle (UcsHandle)
        group_name (string): ldap provider group name
        name (string): ldap provider name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        ldap_provider_group_provider_remove(handle,
                                         group_name="test_ldap_provider_group",
                                         name="test_provider")
    """
    mo = ldap_provider_group_provider_get(handle, group_name, name,
                                caller="ldap_provider_group_provider_remove")

    handle.remove_mo(mo)
    handle.commit()
