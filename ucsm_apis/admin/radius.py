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
This module performs the operation related to radius configuration.
"""
from ucscsdk.ucscexception import UcscOperationError

_base_dn = "sys/radius-ext"

def radius_provider_create(handle, name, order="lowest-available", key=None,
                           auth_port="1812", timeout="5", retries="1",
                           enc_key=None, descr=None, **kwargs):
    """
    Creates a radius provider

    Args:
        handle (UcscHandle)
        name (string): name
        order (string): order
        key (string): key
        auth_port (string): auth_port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc_key
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaRadiusProvider: Managed Object

    Example:
        radius_provider_create(handle, name="test_radius_prov",
                               auth_port="320", timeout="10")
    """

    from ucscsdk.mometa.aaa.AaaRadiusProvider import AaaRadiusProvider

    mo = AaaRadiusProvider(
        parent_mo_or_dn=_base_dn,
        name=name,
        order=order,
        key=key,
        auth_port=auth_port,
        timeout=timeout,
        retries=retries,
        enc_key=enc_key,
        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_get(handle, name, caller="radius_provider_get"):
    """
    Gets radius provider

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        AaaRadiusProvider: Managed Object OR None

    Example:
        radius_provider_get(handle, name="test_radius_provider")
    """

    dn = _base_dn + "/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Radius Provider '%s' does not exist" % dn)
    return mo


def radius_provider_exists(handle, name, **kwargs):
    """
    checks if radius provider exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        radius_provider_exists(handle, name="test_radius_provider")
    """
    try:
        mo = radius_provider_get(handle, name, "radius_provider_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_modify(handle, name, **kwargs):
    """
    modifies a radius provider

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaRadiusProvider: Managed Object

    Raises:
        UcscOperationError: If AaaRadiusProvider is not present

    Example:
        radius_provider_modify(handle, name="test_radius_prov", timeout="5")
    """

    mo = radius_provider_get(handle, name, caller="radius_provider_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def radius_provider_delete(handle, name):
    """
    deletes a radius provider

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaRadiusProvider is not present

    Example:
        radius_provider_delete(handle, name="test_radius_provider")
    """

    mo = radius_provider_get(handle, name, caller="radius_provider_delete")
    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_create(handle, name, descr=None, **kwargs):
    """
    Creates a radius provider group

    Args:
        handle (UcscHandle)
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderGroup: Managed Object

    Example:
        radius_provider_group_create(handle, name="test_prov_grp")
    """

    from ucscsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn=_base_dn, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_group_get(handle, name,
                              caller="radius_provider_group_get"):
    """
    Get radius provider group

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        AaaProviderGroup: Managed Object OR None

    Example:
        radius_provider_group_get(handle, name="test_prov_grp")
    """

    dn = _base_dn + "/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Radius Provider Group'%s' does not exist" % dn)
    return mo


def radius_provider_group_exists(handle, name, **kwargs):
    """
    checks if radius provider group exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        radius_provider_group_exists(handle, name="test_prov_grp")
    """
    try:
        mo = radius_provider_group_get(handle, name)
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_group_delete(handle, name):
    """
    deletes a radius provider group

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaProviderGroup is not present

    Example:
        radius_provider_group_delete(handle, name="test_prov_grp")
    """

    mo = radius_provider_group_get(handle, name,
                                   caller="radius_provider_group_delete")
    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_add_provider(handle, group_name, name,
                                       order="lowest-available", descr=None,
                                       **kwargs):
    """
    adds a provider to a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name
        order (string): order
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderRef: Managed Object

    Raises:
        UcscOperationError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_add_provider(
          handle, group_name="test_prov_grp", name="test_radius_prov")
    """

    from ucscsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    provider_group_mo = radius_provider_group_get(handle, group_name,
                                caller="radius_provider_group_add_provider")

    provider_mo = radius_provider_get(handle, name,
                                caller="radius_provider_group_add_provider")

    mo = AaaProviderRef(parent_mo_or_dn=provider_group_mo,
                        name=name,
                        order=order,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def radius_provider_group_provider_get(handle, group_name, name):
    """
    Gets provider  under a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name

    Returns:
        AaaProviderRef: Managed Object OR None

    Raises:
        UcscOperationError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_provider_get(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    provider_group = radius_provider_group_get(handle, group_name,
                                caller="radius_provider_group_provider_get")

    provider_dn = provider_group.dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_dn)
    if mo is None:
        raise UcsOperationError(caller,
                    "Tacacsplus Provider '%s' is not present under group " % (
                    dn, provider_group.dn))
    return mo


def radius_provider_group_provider_exists(handle, group_name, name, **kwargs):
    """
    checks if a provider exists under a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Raises:
        UcscOperationError: If AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_provider_exists(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    try:
        mo = radius_provider_group_provider_get(handle, group_name, name,
                            caller="radius_provider_group_provider_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_group_modify_provider(handle, group_name, name, **kwargs):
    """
    modifies a provider to a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaProviderRef: Managed Object

    Raises:
        UcscOperationError: If AaaProviderRef is not present

    Example:
        radius_provider_group_modify_provider(
          handle, group_name="test_prov_grp", name="test_radius_prov",
          order="2")
    """

    mo = radius_provider_group_provider_get(handle, group_name, name,
                            caller="radius_provider_group_modify_provider")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def radius_provider_group_remove_provider(handle, group_name, name):
    """
    removes a provider from a radius provider group

    Args:
        handle (UcscHandle)
        group_name (string): group_name
        name (string): name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaProviderRef is not present

    Example:
        radius_provider_group_remove_provider(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """

    mo = radius_provider_group_provider_get(handle, group_name, name,
                                caller="radius_provider_group_remove_provider")
    handle.remove_mo(mo)
    handle.commit()
