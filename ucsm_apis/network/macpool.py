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

from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock
from ucsmsdk.ucsexception import UcsOperationError


def mac_pool_create(handle, org_dn="org-root",
                    name=None,
                    assign="default",
                    descr=None, **kwargs):

    """
    Creates mac pool

    Args:
        handle (UCSHandle)
        name (string): Name of mac pool
        org_dn (string): org dn
        assign (string): Assignment order (default or sequential)
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        MacpoolPool: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        mac_pool_create(handle,
                        name="server_pool",
                        org_dn="org-root",
                        descr="Mac Pool for Servers")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("mac_pool_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = MacpoolPool(parent_mo_or_dn=obj, name=name,
                     assignment_order=assign,
                     descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def mac_pool_get(handle, name=None,
                 org_dn="org-root",
                 caller="mac_pool_get"):

    """
    Gets mac pool

    Args:
        handle (UCSHandle)
        name (string): Name of mac pool
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        MacpoolPool: managed object

    Raises:
        UcsOperationError: if MacpoolPool is not present

    Example:
        mac_pool_get(handle,
                     name="test_pool",
                     org_dn="org-root")
    """

    dn = org_dn + "/mac-pool-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "Mac Pool {} \
                                does not exist".format(dn))
    return mo


def mac_pool_exists(handle, name=None,
                    org_dn="org-root", **kwargs):

    """
    checks if mac pool exists

    Args:
        handle (UcsHandle)
        name (string): Name of mac pool
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MacpoolPool MO/None)

    Raises:
        None

    Example:
        mac_pool_exists:(handle,
                         name="mac_pool_A",
                         org_dn="org-root",)
    """

    try:
        mo = mac_pool_get(handle=handle, name=name, org_dn=org_dn,
                         caller="mac_pool_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def mac_pool_modify(handle, name=None,
                    org_dn="org-root", **kwargs):

    """
    modifies mac pool

    Args:
        handle (UcsHandle)
        name (string): Name of mac pool
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        MacpoolPool: managed object

    Raises:
        UcsOperationError: if MacpoolPool is not present

    Example:
        mac_pool_modify(handle,
                        name="test-pool",
                        descr="prod mac pool")
    """

    mo = mac_pool_get(handle=handle, name=name, org_dn=org_dn,
                      caller="mac_pool_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def mac_pool_delete(handle, name, org_dn="org-root"):

    """
    deletes mac pool

    Args:
        handle (UcsHandle)
        name (string): Name of mac pool
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if MacpoolPool is not present

    Example:
        mac_pool_delete(handle,
                        name="test-pool",
                        org_dn="org-root")
    """

    mo = mac_pool_get(handle=handle, name=name, org_dn=org_dn,
                      caller="mac_pool_delete")
    handle.remove_mo(mo)
    handle.commit()


def mac_block_create(handle, pool_name=None, org_dn="org-root",
                     start_mac=None, end_mac=None,
                     **kwargs):

    """
    Creates block of mac addresses

    Args:
        handle (UCSHandle)
        pool_name (string): Name of mac pool block is associated with
        org_dn (string): org dn
        start_mac (string): Starting mac address
        end_mac (string): Ending mac address
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        MacpoolBlock: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        mac_block_create(handle,
                         pool_name="mac_pool_a",
                         org_dn="org-root",
                         start_mac="00:25:B5:00:0A:00",
                         end_mac="00:25:B5:00:0A:3F",)
    """

    obj = handle.query_dn(org_dn)
    dn = org_dn + "/mac-pool-" + pool_name
    pool = handle.query_dn(dn)
    if not obj:
        raise UcsOperationError("mac_block_create", "Org {} \
                                 does not exist".format(org_dn))
    elif not pool:
        raise UcsOperationError("mac_block_create", "Mac Pool {} \
                                 does not exist".format(pool_name))

    mo = MacpoolBlock(parent_mo_or_dn=dn, r_from=start_mac,
                      to=end_mac)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def mac_block_get(handle, pool_name=None, org_dn="org-root",
                  start_mac=None, end_mac=None, caller="mac_block_get"):

    """
    gets mac address block

    Args:
        handle (Ucshandle)
        pool_name (string): Name of mac pool block is associated with
        org_dn (string): org dn
        start_mac (string): 1st ip in the block
        end_mac (string): last ip in the block
        caller (string): caller method name

    Returns:
        MacpoolBlock: managed object

    Raises:
        UcsOperationError: if MacpoolBlock is not present

    Example:
        mac_block_get(handle,
                      pool_name="ext-mgmt",
                      org_dn="org-root",
                      start_mac="00:25:B5:00:0A:00",
                      end_mac="00:25:B5:00:0A:3F")

    """

    dn = (org_dn + "/mac-pool-" +
          pool_name + "/block-" +
          start_mac + "-" + end_mac)
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "MAC Block {} \
                                does not exist".format(dn))
    return mo


def mac_block_exists(handle, pool_name, org_dn="org-root", start_mac=None,
                     end_mac=None, **kwargs):

    """
    checks if mac block exists

    Args:
        handle (UcsHandle)
        pool_name (string): Name of mac pool block is associated with
        org_dn (string): org dn
        start_mac (string): 1st mac address in the block
        end_mac (string): last mac address in the block
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MacpoolBlock MO/None)

    Raises:
        None

    Example:
        mac_block_exists:(handle,
                          pool_name="default",
                          org_dn="org-root",
                          start_mac="00:25:B5:00:0A:00",
                          end_mac="00:25:B5:00:0A:3F")

    """

    try:
        mo = mac_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                           start_mac=start_mac, end_mac=end_mac,
                           caller="mac_block_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def mac_block_modify(handle, pool_name, org_dn="org-root",
                     start_mac=None, end_mac=None, **kwargs):

    """
    modifies mac block

    Args:
        handle (UcsHandle)
        pool_name (string): Name of ip pool block is associated with
        org_dn (string): org dn
        start_mac (string): 1st mac address in the block
        end_mac (string): last mac address in the block
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        MacpoolBlock: managed object

    Raises:
        UcsOperationError: if MacpoolBlock is not present

    Example:
        mac_block_modify(handle,
                         pool_name="ext-mgmt",
                         org_dn="org-root",
                         start_mac="00:25:B5:00:0A:00",
                         end_mac="00:25:B5:00:0A:3F",
                         status="modified")
    """

    mo = mac_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                       start_mac=start_mac, end_mac=end_mac,
                       caller="mac_block_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def mac_block_delete(handle, pool_name=None, org_dn="org-root",
                     start_mac=None, end_mac=None):

    """
    deletes mac block

    Args:
        handle (UcsHandle)
        pool_name (string): Name of mac pool block is associated with
        org_dn (string): org dn
        start_mac (string): 1st mac address in the block
        end_mac (string): last mac address in the block

    Returns:
        None

    Raises:
        UcsOperationError: if MacpoolBlock is not present

    Example:
        ip_block_delete(handle,
                     pool_name="ext-mgmt",
                     org_dn="org-root",
                     start_mac="00:25:B5:00:0A:00",
                     end_mac="00:25:B5:00:0A:3F")
    """

    mo = mac_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                       start_mac=start_mac, end_mac=end_mac,
                       caller="mac_block_delete")
    handle.remove_mo(mo)
    handle.commit()
