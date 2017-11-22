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
This module performs operations related to mac pools.
"""

from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import (
    StorageLocalDiskConfigPolicy)
from ucsmsdk.ucsexception import UcsOperationError


def localdisk_policy_create(handle, name=None,
                            org_dn="org-root",
                            descr=None,
                            flex_flash_raid_reporting_state="disable",
                            flex_flash_state="disable",
                            mode="any-configuration",
                            protect_config="no",
                            **kwargs):

    """
    Creates local disk config policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        flex_flash_raid_reporting_state (string): Used if boot from SD
                                                  ["disable", "enable"]
        flex_flash_state (string): Used if boot from SD
                                   ["disable", "enable"]
        mode (string): RAID
        protect_config (string): Preserve local disk config across
                                 service profile disassociation.
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        StorageLocalDiskConfigPolicy: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        localdisk_policy_create(handle,
                                name="SD_Boot",
                                descr="Boot from SD Cards",
                                flex_flash_raid_reporting_state="enable",
                                flex_flash_state="enable")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("localdisk_policy_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn=obj, name=name,
                                      descr=descr,
    flex_flash_raid_reporting_state=flex_flash_raid_reporting_state,
                                      flex_flash_state=flex_flash_state,
                                      mode=mode,
                                      protect_config=protect_config)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def localdisk_policy_get(handle, name=None,
                         org_dn="org-root",
                         caller="localdisk_policy_get"):

    """
    Gets local disk config policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        StorageLocalDiskConfigPolicy: managed object

    Raises:
        UcsOperationError: if StorageLocalDiskConfigPolicy is not present

    Example:
        localdisk_policy_get(handle,
                             name="SD_Boot",
                             org_dn="org-root")
    """

    dn = org_dn + "/local-disk-config-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "local disk policy {} \
                                does not exist".format(dn))
    return mo


def localdisk_policy_exists(handle, name=None,
                            org_dn="org-root", **kwargs):

    """
    checks if policy exists

    Args:
        handle (UcsHandle)
        name (string): Name of local disk policy
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, StorageLocalDiskConfigPolicy MO/None)

    Raises:
        None

    Example:
        localdisk_policy_exists:(handle,
                                 name="SD_Boot",
                                 org_dn="org-root")
    """

    try:
        mo = localdisk_policy_get(handle=handle, name=name, org_dn=org_dn,
                                  caller="localdisk_policy_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def localdisk_policy_modify(handle, name=None,
                            org_dn="org-root", **kwargs):

    """
    modifies policy

    Args:
        handle (UcsHandle)
        name (string): Name of policy
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        StorageLocalDiskConfigPolicy: managed object

    Raises:
        UcsOperationError: if StorageLocalDiskConfigPolicy is not present

    Example:
        localdisk_policy_modify(handle,
                                name="SD_Boot",
                                descr="prod local disk policy")
    """

    mo = localdisk_policy_get(handle=handle, name=name, org_dn=org_dn,
                              caller="localdisk_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def localdisk_policy_delete(handle, name=None, org_dn="org-root"):

    """
    deletes policy

    Args:
        handle (UcsHandle)
        name (string): Name of policy
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if  is not present

    Example:
        mac_pool_delete(handle,
                        name="test-pool",
                        org_dn="org-root")
    """

    mo = localdisk_policy_get(handle=handle, name=name, org_dn=org_dn,
                              caller="localdisk_policy_delete")
    handle.remove_mo(mo)
    handle.commit()
