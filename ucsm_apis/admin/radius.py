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
from ucsmsdk.ucsexception import UcsOperationError

_radius_dn = "sys/radius-ext"


def radius_provider_create(handle, name, order="lowest-available", key=None,
                           auth_port="1812", timeout="5", retries="1",
                           enc_key=None, descr=None, **kwargs):
    """
    Creates a radius provider

    Args:
        handle (UcsHandle)
        name (string): radius provider name (Hostname/FQDN or IP Address)
        order (string): order
         valid values are "lowest-available" or "0-16"
        key (string): key
        auth_port (string): authorization port
        timeout (string): timeout
        retries (string): retries
        enc_key (string): enc key
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaRadiusProvider: managed object

    Raises:
        None

    Example:
        radius_provider_create(handle, name="test_radius_prov",
                               auth_port="320", timeout="10")
    """
    from ucsmsdk.mometa.aaa.AaaRadiusProvider import AaaRadiusProvider

    mo = AaaRadiusProvider(
        parent_mo_or_dn=_radius_dn,
        name=name,
        order=order,
        key=key,
        auth_port=auth_port,
        timeout=timeout,
        retries=retries,
        enc_key=enc_key,
        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def radius_provider_get(handle, name, caller="radius_provider_get"):
    """
    gets radius provider

    Args:
        handle (UcsHandle)
        name (string): radius provider name
        caller (string): name of the caller function

    Returns:
        AaaRadiusProvider: managed object

    Raises:
        UcsOperationError: if AaaRadiusProvider is not present

    Example:
        radius_provider_get(handle, name="test_radius_provider")
    """
    dn = _radius_dn + "/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Radius Provider '%s' does not exist" % dn)
    return mo


def radius_provider_exists(handle, name, **kwargs):
    """
    checks if radius provider exists

    Args:
        handle (UcsHandle)
        name (string): radius provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaRadiusProvider MO/None)

    Raises:
        None

    Example:
        radius_provider_exists(handle, name="test_radius_provider")
    """
    try:
        mo = radius_provider_get(handle, name, "radius_provider_exists")
    except UcsOperationError:
        return (False, None)

    if 'order' in kwargs and kwargs['order'] == 'lowest-available':
        kwargs.pop('order', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_modify(handle, name, **kwargs):
    """
    modifies a radius provider

    Args:
        handle (UcsHandle)
        name (string): radius provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaRadiusProvider: managed object

    Raises:
        UcsOperationError: if AaaRadiusProvider is not present

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
        handle (UcsHandle)
        name (string): radius provider name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaRadiusProvider is not present

    Example:
        radius_provider_delete(handle, name="test_radius_provider")
    """
    mo = radius_provider_get(handle, name, caller="radius_provider_delete")
    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_create(handle, name, descr=None, **kwargs):
    """
    creates a radius provider group

    Args:
        handle (UcsHandle)
        name (string): radius provider group name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaProviderGroup: managed object

    Raises:
        None

    Example:
        radius_provider_group_create(handle, name="test_prov_grp")
    """
    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn=_radius_dn, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def radius_provider_group_get(handle, name,
                              caller="radius_provider_group_get"):
    """
    gets radius provider group

    Args:
        handle (UcsHandle)
        name (string): radius provider group name

    Returns:
        AaaProviderGroup: managed object

    Raises:
        UcsOperationError: if AaaProviderGroup is not present

    Example:
        radius_provider_group_get(handle, name="test_prov_grp")
    """
    dn = _radius_dn + "/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                            "Radius Provider Group'%s' does not exist" % dn)
    return mo


def radius_provider_group_exists(handle, name, **kwargs):
    """
    checks if radius provider group exists

    Args:
        handle (UcsHandle)
        name (string): radius provider group name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaProviderGroup MO/None)

    Raises:
        None

    Example:
        radius_provider_group_exists(handle, name="test_prov_grp")
    """
    try:
        mo = radius_provider_group_get(handle, name,
                                       caller="radius_provider_group_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_group_delete(handle, name):
    """
    deletes a radius provider group

    Args:
        handle (UcsHandle)
        name (string): radius provider group name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaProviderGroup is not present

    Example:
        radius_provider_group_delete(handle, name="test_prov_grp")
    """
    mo = radius_provider_group_get(handle, name,
                                   caller="radius_provider_group_delete")
    handle.remove_mo(mo)
    handle.commit()


def radius_provider_group_provider_add(handle, group_name, name,
                                       order="lowest-available", descr=None,
                                       **kwargs):
    """
    adds a provider to a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): radius provider group name
        name (string): radius provider name
        order (string): order
         valid values are "lowest-available" or "0-16"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaProviderRef: managed object

    Raises:
        UcsOperationError: if AaaProviderGroup  or AaaProvider is not present

    Example:
        radius_provider_group_provider_add(
          handle, group_name="test_prov_grp", name="test_radius_prov")
    """
    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    radius_provider = radius_provider_get(handle, name,
                                caller="radius_provider_group_provider_add")

    radius_provider_group = radius_provider_group_get(handle, group_name,
                                caller="radius_provider_group_provider_add")

    mo = AaaProviderRef(parent_mo_or_dn=radius_provider_group,
                        name=name,
                        order=order,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def radius_provider_group_provider_get(handle, group_name, name,
                                caller="radius_provider_group_provider_get"):
    """
    gets provider  under a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): radius provider group name
        name (string): radius provider name

    Returns:
        AaaProviderRef: managed object

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        radius_provider_group_provider_get(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """
    provider_group_dn = _radius_dn + "/providergroup-" + group_name
    provider_ref_dn = provider_group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_ref_dn)
    if mo is None:
        raise UcsOperationError(caller,
            "Radius Provider Reference '%s' does not exist" % provider_ref_dn)
    return mo


def radius_provider_group_provider_exists(handle, group_name, name, **kwargs):
    """
    checks if a provider exists under a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): radius provider group name
        name (string): radius provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaProviderRef MO/None)

    Raises:
        None

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

    if 'order' in kwargs and kwargs['order'] == 'lowest-available':
        kwargs.pop('order', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def radius_provider_group_provider_modify(handle, group_name, name, **kwargs):
    """
    modifies a provider to a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): radius provider group name
        name (string): radius provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaProviderRef: managed object

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        radius_provider_group_provider_modify(
          handle, group_name="test_prov_grp", name="test_radius_prov",
          order="2")
    """
    mo = radius_provider_group_provider_get(handle, group_name, name,
                            caller="radius_provider_group_provider_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def radius_provider_group_provider_remove(handle, group_name, name):
    """
    removes a provider from a radius provider group

    Args:
        handle (UcsHandle)
        group_name (string): radius provider group name
        name (string): radius provider name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        radius_provider_group_provider_remove(handle,
                                    group_name="test_radius_provider_group",
                                    name="test_radius_provider")
    """
    mo = radius_provider_group_provider_get(handle, group_name, name,
                                caller="radius_provider_group_provider_remove")
    handle.remove_mo(mo)
    handle.commit()
