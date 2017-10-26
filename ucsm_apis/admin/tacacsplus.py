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

_tacacs_dn = "sys/tacacs-ext"


def tacacsplus_provider_create(handle, name, order="lowest-available",
                               port="49", timeout="5", retries="1",
                               key=None, enc_key=None, descr=None, **kwargs):
    """
    creates a tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider name
        order (string): order
         valid values are "lowest-available" or "0-16"
        port (string): port
        timeout (string): timeout
        retries (string): retries
        key (string): key
        enc_key (string): enc_key
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaTacacsPlusProvider: managed object

    Raises:
        None

    Example:
        tacacsplus_provider_create(
          handle, name="test_tacac_prov", port="320", timeout="10")
    """
    from ucsmsdk.mometa.aaa.AaaTacacsPlusProvider import \
        AaaTacacsPlusProvider

    mo = AaaTacacsPlusProvider(parent_mo_or_dn=_tacacs_dn,
                               name=name,
                               order=order,
                               port=port,
                               timeout=timeout,
                               retries=retries,
                               key=key,
                               enc_key=enc_key,
                               descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def tacacsplus_provider_get(handle, name, caller="tacacsplus_provider_get"):
    """
    gets tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider name
        caller (string): name of the caller function

    Returns:
        AaaTacacsPlusProvider: managed object

    Raises:
        UcsOperationError: if AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_get(handle, name="test_tacac_prov")
    """
    dn = _tacacs_dn + "/provider-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Tacacsplus Provider '%s' does not exist" % dn)
    return mo


def tacacsplus_provider_exists(handle, name, **kwargs):
    """
    checks if a tacacsplus provider exists

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaTacacsPlusProvider MO/None)

    Raises:
        None

    Example:
        tacacsplus_provider_exists(handle, name="test_tacac_prov", port="320")
    """
    try:
        mo = tacacsplus_provider_get(handle, name,
                                     caller="tacacsplus_provider_exists")
    except UcsOperationError:
        return (False, None)

    if 'order' in kwargs and kwargs['order'] == 'lowest-available':
        kwargs.pop('order', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def tacacsplus_provider_modify(handle, name, **kwargs):
    """
    modifies a tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaTacacsPlusProvider: managed object

    Raises:
        UcsOperationError: if AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_modify(handle, "test_tacac_prov", timeout="5")
    """
    mo = tacacsplus_provider_get(handle, name,
                                 caller="tacacsplus_provider_modify")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def tacacsplus_provider_delete(handle, name):
    """
    deletes a tacacsplus provider

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaTacacsPlusProvider is not present

    Example:
        tacacsplus_provider_delete(handle, name="test_tacac_prov")
    """
    mo = tacacsplus_provider_get(handle, name,
                                 caller="tacacsplus_provider_delete")
    handle.remove_mo(mo)
    handle.commit()


def tacacsplus_provider_group_create(handle, name, descr=None, **kwargs):
    """
    creates a tacacsplus provider group

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider group name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaProviderGroup: managed object

    Raises:
        None

    Example:
        tacacsplus_provider_group_create(handle, name="test_prov_grp")
    """
    from ucsmsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn=_tacacs_dn, name=name, descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def tacacsplus_provider_group_get(handle, name,
                                  caller="tacacsplus_provider_group_get"):
    """
    gets tacacsplus provider group

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider group name
        caller (string): name of the caller function

    Returns:
        AaaProviderGroup: managed object

    Raises:
        UcsOperationError: if AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_get(handle, name="test_prov_grp")
    """
    dn = _tacacs_dn + "/providergroup-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                        "Tacacsplus  Provider Group '%s' does not exist" % dn)
    return mo


def tacacsplus_provider_group_exists(handle, name, **kwargs):
    """
    checks if a tacacsplus provider group exists

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider group name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, AaaProviderGroup MO/None)

    Raises:
        None

    Example:
        tacacsplus_provider_group_exists(handle, name="test_prov_grp")
    """
    try:
        mo = tacacsplus_provider_group_get(handle, name,
                                    caller="tacacsplus_provider_group_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def tacacsplus_provider_group_delete(handle, name):
    """
    deletes a tacacsplus provider group

    Args:
        handle (UcsHandle)
        name (string): tacacsplus provider group name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaProviderGroup is not present

    Example:
        tacacsplus_provider_group_delete(handle, name="test_prov_grp")
    """
    mo = tacacsplus_provider_group_get(handle, name,
                                    caller="tacacsplus_provider_group_delete")
    handle.remove_mo(mo)
    handle.commit()


def tacacsplus_provider_group_provider_add(handle, group_name, name,
                                           order="lowest-available",
                                           descr=None, **kwargs):
    """
    adds a tacacsplus provider to a tacacsplus provider group

    Args:
        handle (UcsHandle)
        group_name (string): tacacsplus provider group name
        name (string): tacacsplus provider name
        order (string): order
         valid values are "lowest-available" or "0-16"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaProviderRef: managed object

    Raises:
        UcsOperationError: if AaaProviderGroup Or AaaProvider is not present

    Example:
        tacacsplus_provider_group_provider_add(handle,
                                               group_name="test_prov_grp",
                                               name="test_tacac_prov")
    """
    from ucsmsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    tacacsplus_provider = tacacsplus_provider_get(handle, name,
                            caller="tacacsplus_provider_group_provider_add")

    tacacsplus_provider_group = tacacsplus_provider_group_get(handle,
                group_name, caller="tacacsplus_provider_group_provider_add")

    mo = AaaProviderRef(parent_mo_or_dn=tacacsplus_provider_group,
                        name=name,
                        order=order,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def tacacsplus_provider_group_provider_get(handle, group_name, name,
                            caller="tacacsplus_provider_group_provider_get"):
    """
    checks if a tacacsplus provider added to a tacacsplus provider group

    Args:
        handle (UcsHandle)
        group_name (string): tacacsplus provider group name
        name (string): tacacsplus provider name
        caller (string): name of the caller function

    Returns:
        AaaProviderRef: managed object

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_provider_get(handle,
                                    group_name="test_prov_grp",
                                    name="test_tacac_prov")
    """
    provider_group_dn = _tacacs_dn + "/providergroup-" + group_name
    provider_ref_dn = provider_group_dn + "/provider-ref-" + name
    mo = handle.query_dn(provider_ref_dn)
    if mo is None:
        raise UcsOperationError(caller,
        "Tacacsplus Provider Reference '%s' does not exist" % provider_ref_dn)
    return mo


def tacacsplus_provider_group_provider_exists(handle, group_name, name,
                                              **kwargs):
    """
    checks if a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): tacacsplus provider group name
        name (string): tacacsplus provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False,  AaaProviderRef MO/None)

    Raises:
        None

    Example:
        tacacsplus_provider_group_provider_exists(handle,
                                                  group_name="test_prov_grp",
                                                  name="test_tacac_prov")
    """
    try:
        mo = tacacsplus_provider_group_provider_get(handle, group_name, name,
                        caller="tacacsplus_provider_group_provider_exists")
    except UcsOperationError:
        return (False, None)

    if 'order' in kwargs and kwargs['order'] == 'lowest-available':
        kwargs.pop('order', None)

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def tacacsplus_provider_group_provider_modify(handle, group_name, name,
                                              **kwargs):
    """
    modifies a tacacsplus provider added to a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): tacacsplus provider group name
        name (string): tacacsplus provider name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaProviderRef: managed object

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_provider_modify(
          handle, group_name="test_prov_grp", name="test_tacac_prov",
          order="2")
    """
    mo = tacacsplus_provider_group_provider_get(handle, group_name, name,
                        caller="tacacsplus_provider_group_provider_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def tacacsplus_provider_group_provider_remove(handle, group_name, name):
    """
    removes a tacacsplus provider from a tacacsplus provider  group

    Args:
        handle (UcsHandle)
        group_name (string): tacacsplus provider group name
        name (string): tacacsplus provider name

    Returns:
        None

    Raises:
        UcsOperationError: if AaaProviderRef is not present

    Example:
        tacacsplus_provider_group_provider_remove(handle,
                                                  group_name="test_prov_grp",
                                                  name="test_tacac_prov")
    """
    mo = tacacsplus_provider_group_provider_get(handle, group_name, name,
                        caller="tacacsplus_provider_group_provider_remove")
    handle.remove_mo(mo)
    handle.commit()
