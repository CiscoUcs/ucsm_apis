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
This module performs operations related to server pools.
"""

from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot
from ucsmsdk.ucsexception import UcsOperationError


def server_pool_create(handle, org_dn="org-root",
                       name=None,
                       descr=None, **kwargs):

    """
    Creates server pools

    Args:
        handle (UCSHandle)
        name (string): Name of server pool
        org_dn (string): org dn
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        ComputePool: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        server_pool_create(handle,
                           name="server_pool",
                           org_dn="org-root",
                           descr="server pool for Servers")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("server_pool_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = ComputePool(parent_mo_or_dn=obj, name=name,
                     descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def server_pool_get(handle, name=None,
                    org_dn="org-root",
                    caller="server_pool_get"):

    """
    Gets server pool

    Args:
        handle (UCSHandle)
        name (string): Name of server pool
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        ComputePool: managed object

    Raises:
        UcsOperationError: if ComputePool is not present

    Example:
        server_pool_get(handle,
                        name="test_pool",
                        org_dn="org-root")
    """

    dn = org_dn + "/compute-pool-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "Server Pool {} "
                                "does not exist".format(dn))
    return mo


def server_pool_exists(handle, name=None,
                       org_dn="org-root", **kwargs):

    """
    Checks if server pool exists

    Args:
        handle (UcsHandle)
        name (string): Name of server pool
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, ComputePool MO/None)

    Raises:
        None

    Example:
        server_pool_exists:(handle,
                            name="server_pool",
                            org_dn="org-root",)
    """

    try:
        mo = server_pool_get(handle=handle, name=name, org_dn=org_dn,
                             caller="server_pool_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def server_pool_modify(handle, name=None,
                       org_dn="org-root", **kwargs):

    """
    modifies server pool

    Args:
        handle (UcsHandle)
        name (string): Name of server pool
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        ComputePool: managed object

    Raises:
        UcsOperationError: if ComputePool is not present

    Example:
        server_pool_modify(handle,
                         name="test-pool",
                         descr="prod server pool")
    """

    mo = server_pool_get(handle=handle, name=name, org_dn=org_dn,
                         caller="server_pool_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def server_pool_delete(handle, name=None, org_dn="org-root"):

    """
    deletes server pool

    Args:
        handle (UcsHandle)
        name (string): Name of server pool
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if ComputePool is not present

    Example:
        server_pool_delete(handle,
                           name="test-pool",
                           org_dn="org-root")
    """

    mo = server_pool_get(handle=handle, name=name, org_dn=org_dn,
                         caller="server_pool_delete")
    handle.remove_mo(mo)
    handle.commit()


def server_add(handle, pool_name=None, org_dn="org-root",
               servers=None, **kwargs):

    """
    Adds servers to server pool

    Args:
        handle (UCSHandle)
        pool_name (string): Name of server pool
        org_dn (string): org dn
        servers (list): List of servers to add to the pool
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        ComputePool: managed object

    Raises:
        UcsOperationError: if Org_dn or pool is not present

    Example:
        server_add(handle,
                   pool_name="server_pool",
                   org_dn="org-root",
                   servers=["1/1", "1/2"])
    """

    mo = server_pool_get(handle=handle, name=pool_name, org_dn=org_dn,
                         caller="server_add")
    mo.set_prop_multiple(**kwargs)

    server_list = [s.split("/") for s in servers]
    mo_list = []
    for server in server_list:
        mos = ComputePooledSlot(parent_mo_or_dn=mo,
                                chassis_id=server[0],
                                slot_id=server[1])
        mo_list.append(mos)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def server_delete(handle, pool_name=None, org_dn="org-root",
                  servers=None):

    """
    Deletes servers from server pool

    Args:
        handle (UCSHandle)
        pool_name (string): Name of server pool
        org_dn (string): org dn
        servers (list): List of servers to delete from the pool

    Returns:
        None

    Raises:
        UcsOperationError: if Org_dn or pool is not present

    Example:
        server_delete(handle,
                      pool_name="server_pool",
                      org_dn="org-root",
                      servers=["1/1", "1/2"])
    """

    server_list = [s.split("/") for s in servers]
    for server in server_list:
        mo = handle.query_dn(org_dn + "/compute-pool-" +
                             pool_name + "/blade-" +
                             server[0] + "-" + server[1])
        if not mo:
            raise UcsOperationError("server_delete", "Org {} "
                                    "does not exist".format(org_dn))
        handle.remove_mo(mo)
        handle.commit()
