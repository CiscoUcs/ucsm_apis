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
This module performs operations related to uuid pools.
"""

from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock
from ucsmsdk.ucsexception import UcsOperationError


def uuid_pool_create(handle, org_dn="org-root",
                     name=None,
                     assign="default",
                     descr=None, **kwargs):

    """
    Creates uuid pool

    Args:
        handle (UCSHandle)
        name (string): Name of uuid pool
        org_dn (string): org dn
        assign (string): Assignment order (default or sequential)
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        UuidpoolPool: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        uuid_pool_create(handle,
                         name="uuid_pool",
                         org_dn="org-root",
                         descr="uuid Pool for Servers")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("uuid_pool_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = UuidpoolPool(parent_mo_or_dn=obj, name=name,
                     assignment_order=assign,
                     descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def uuid_pool_get(handle, name=None,
                 org_dn="org-root",
                 caller="uuid_pool_get"):

    """
    Gets uuid pool

    Args:
        handle (UCSHandle)
        name (string): Name of uuid pool
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        UuidpoolPool: managed object

    Raises:
        UcsOperationError: if UuidpoolPool is not present

    Example:
        uuid_pool_get(handle,
                     name="test_pool",
                     org_dn="org-root")
    """

    dn = org_dn + "/uuid-pool-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "UUID Pool {} "
                                "does not exist".format(dn))
    return mo


def uuid_pool_exists(handle, name=None,
                     org_dn="org-root", **kwargs):

    """
    checks if uuid pool exists

    Args:
        handle (UcsHandle)
        name (string): Name of uuid pool
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, UuidpoolPool MO/None)

    Raises:
        None

    Example:
        uuid_pool_exists:(handle,
                          name="uuid_pool",
                          org_dn="org-root",)
    """

    try:
        mo = uuid_pool_get(handle=handle, name=name, org_dn=org_dn,
                           caller="uuid_pool_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def uuid_pool_modify(handle, name=None,
                     org_dn="org-root", **kwargs):

    """
    modifies uuid pool

    Args:
        handle (UcsHandle)
        name (string): Name of uuid pool
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        UuidpoolPool: managed object

    Raises:
        UcsOperationError: if UuidpoolPool is not present

    Example:
        uuid_pool_modify(handle,
                         name="test-pool",
                         descr="prod uuid pool")
    """

    mo = uuid_pool_get(handle=handle, name=name, org_dn=org_dn,
                       caller="uuid_pool_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def uuid_pool_delete(handle, name=None, org_dn="org-root"):

    """
    deletes uuid pool

    Args:
        handle (UcsHandle)
        name (string): Name of uuid pool
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if UuidpoolPool is not present

    Example:
        uuid_pool_delete(handle,
                         name="test-pool",
                         org_dn="org-root")
    """

    mo = uuid_pool_get(handle=handle, name=name, org_dn=org_dn,
                       caller="uuid_pool_delete")
    handle.remove_mo(mo)
    handle.commit()


def uuid_block_create(handle, pool_name=None, org_dn="org-root",
                      start_uuid=None, end_uuid=None,
                      **kwargs):

    """
    Creates block of uuid addresses

    Args:
        handle (UCSHandle)
        pool_name (string): Name of uuid pool block is associated with
        org_dn (string): org dn
        start_uuid (string): Starting mac address
        end_uuid (string): Ending mac address
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        UuidpoolBlock: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        uuid_block_create(handle,
                         pool_name="uuid_pool_a",
                         org_dn="org-root",
                         start_uuid="0000-000000000001",
                         end_uuid="0000-000000000040",)
    """

    obj = handle.query_dn(org_dn)
    dn = org_dn + "/uuid-pool-" + pool_name
    pool = handle.query_dn(dn)
    if not obj:
        raise UcsOperationError("uuid_block_create", "Org {} \
                                 does not exist".format(org_dn))
    elif not pool:
        raise UcsOperationError("uuid_block_create", "uuid pool {} \
                                 does not exist".format(pool_name))

    mo = UuidpoolBlock(parent_mo_or_dn=dn, r_from=start_uuid,
                      to=end_uuid)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def uuid_block_get(handle, pool_name=None, org_dn="org-root",
                   start_uuid=None, end_uuid=None, caller="uuid_block_get"):

    """
    gets uuid block

    Args:
        handle (Ucshandle)
        pool_name (string): Name of uuid pool block is associated with
        org_dn (string): org dn
        start_uuid (string): 1st uuid in the block
        end_uuid (string): last uuid in the block
        caller (string): caller method name

    Returns:
        UuidpoolBlock: managed object

    Raises:
        UcsOperationError: if UuidpoolBlock is not present

    Example:
        uuid_block_get(handle,
                       pool_name="ext-mgmt",
                       org_dn="org-root",
                       start_uuid="0000-000000000001",
                       end_uuid="0000-000000000040")

    """

    dn = (org_dn + "/uuid-pool-" +
          pool_name + "/block-from-" +
          start_uuid + "-to-" + end_uuid)
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "UUID block {} \
                                does not exist".format(dn))
    return mo


def uuid_block_exists(handle, pool_name, org_dn="org-root", start_uuid=None,
                      end_uuid=None, **kwargs):

    """
    checks if uuid block exists

    Args:
        handle (UcsHandle)
        pool_name (string): Name of uuid pool block is associated with
        org_dn (string): org dn
        start_uuid (string): 1st uuid address in the block
        end_uuid (string): last uuid address in the block
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, UuidpoolBlock MO/None)

    Raises:
        None

    Example:
        uuid_block_exists:(handle,
                           pool_name="default",
                           org_dn="org-root",
                           start_uuid="0000-000000000001",
                           end_uuid="0000-000000000040")

    """

    try:
        mo = uuid_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                            start_uuid=start_uuid, end_uuid=end_uuid,
                            caller="uuid_block_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def uuid_block_modify(handle, pool_name, org_dn="org-root",
                      start_uuid=None, end_uuid=None, **kwargs):

    """
    modifies uuid block

    Args:
        handle (UcsHandle)
        pool_name (string): Name of uuid pool block is associated with
        org_dn (string): org dn
        start_uuid (string): 1st uuid address in the block
        end_uuid (string): last uuid address in the block
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        UuidpoolBlock: managed object

    Raises:
        UcsOperationError: if UuidpoolBlock is not present

    Example:
        uuid_block_modify(handle,
                          pool_name="ext-mgmt",
                          org_dn="org-root",
                          start_uuid="0000-000000000001",
                          end_uuid="0000-000000000040",
                          status="modified")
    """

    mo = uuid_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                        start_uuid=start_uuid, end_uuid=end_uuid,
                        caller="uuid_block_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def uuid_block_delete(handle, pool_name=None, org_dn="org-root",
                      start_uuid=None, end_uuid=None):

    """
    deletes uuid block

    Args:
        handle (UcsHandle)
        pool_name (string): Name of uuid pool block is associated with
        org_dn (string): org dn
        start_uuid (string): 1st uuid address in the block
        end_uuid (string): last uuid address in the block

    Returns:
        None

    Raises:
        UcsOperationError: if UuidpoolBlock is not present

    Example:
        uuid_block_delete(handle,
                          pool_name="test_pool",
                          org_dn="org-root",
                          start_uuid="0000-000000000001",
                          end_uuid="0000-000000000040")
    """

    mo = uuid_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                        start_uuid=start_uuid, end_uuid=end_uuid,
                        caller="uuid_block_delete")
    handle.remove_mo(mo)
    handle.commit()
