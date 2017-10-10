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
This module performs operations related to ip pools.
"""


from ucsmsdk import ucsgenutils
from ucsmsdk.ucsexception import UcsOperationError
from ucsmsdk.ucscoreutils import load_class

def ip_block_create(handle, pool_name, org_dn="org-root",
                    start_ip=None, end_ip=None, sm=None, gw=None, prim_dns=None,
                    sec_dns=None, **kwargs):
    """
    Creates ip block

    Args:
        handle (UCSHandle)
        pool_name (string): Name of ip pool block is associated with
        org_dn (string): org dn
        start_ip (string): 1st ip in the block
        end_ip (string): last ip in the block
        sm (string): subnet mask
        gw (string): default gateway
        prim_dns (string): primary dns
        sec_dns (string): secondary dns
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    
    Returns:
        Ippoolblock: managed object
    
    Raises:
        UcsOperationError: if Org_dn is not present
    
    Example:
        ip_block_create:(handle,
                         pool_name="ext-mgmt",
                         org_dn="org-root",
                         start_ip="192.168.128.10",
                         end_ip="192.168.128.20",
                         sm="255.255.255.0",
                         gw="192.168.128.1")
    """

    from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock

    obj = handle.query_dn(org_dn)
    dn = org_dn + "/ip-pool-" + pool_name
    pool = handle.query_dn(dn)
    if not obj:
        raise UcsOperationError("ip_block_create", "Org {} \
                                 does not exist".format(org_dn))
    elif not pool:
        raise UcsOperationError("ip_block_create","IP Pool {} \
                                 does not exist".format(pool_name))
    
    mo = IppoolBlock(parent_mo_or_dn=dn, def_gw=gw, r_from=start_ip,
                     to=end_ip, subnet=sm)
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo

def ip_block_get(handle, pool_name, org_dn="org-root",
                 start_ip=None, end_ip=None, caller="ip_block_get"):
    """
    gets ip block

    Args:
        handle (Ucshandle)
        pool_name (string): Name of ip pool block is associated with
        org_dn (string): org dn
        start_ip (string): 1st ip in the block
        end_ip (string): last ip in the block
        caller (string): caller method name

    Returns:
        IppoolBlock: managed object
    
    Raises:
        UcsOperationError: if Ippoolblock is not present
    
    Example:
        ip_block_get(handle,
                     pool_name="ext-mgmt",
                     org_dn="org-root",
                     start_ip="192.168.128.10",
                     end_ip="192.168.128.20")

    """
    
    dn = org_dn + "/ip-pool-" + pool_name + "/block-" + start_ip + "-" + end_ip
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "IP Block {} \
                                does not exist".format(dn))
    return mo

def ip_block_exists(handle, pool_name, org_dn="org-root", start_ip=None,
                    end_ip=None, **kwargs):
    """
    checks if ip block exists

    Args:
        handle (UcsHandle)
        pool_name (string): Name of ip pool block is associated with
        org_dn (string): org dn
        start_ip (string): 1st ip in the block
        end_ip (string): last ip in the block
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    
    Returns:
        (True/False, IppoolBlock MO/None)
    
    Raises:
        None
    
    Example:
        ip_block_exists:(handle,
                         pool_name="ext-mgmt", 
                         org_dn="org-root",
                         start_ip="192.168.128.10",
                         end_ip="192.168.128.20")

    """

    dn = org_dn + "/ip-pool-" + pool_name
    try:
        mo = ip_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                          start_ip=start_ip, end_ip=end_ip, caller="ip_block_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)

def ip_block_modify(handle, pool_name, org_dn="org-root",
                    start_ip=None, end_ip=None, **kwargs):
    """
    modifies ip block

    Args:
        handle (UcsHandle)
        pool_name (string): Name of ip pool block is associated with
        org_dn (string): org dn
        start_ip (string): 1st ip in the block
        end_ip (string): last ip in the block
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class
    
    Returns:
        IppoolBlock: managed object
    
    Raises:
        UcsOperationError: if Ippoolblock is not present
    
    Example:
        ip_block_modify(handle,
                     pool_name="ext-mgmt",
                     org_dn="org-root",
                     start_ip="192.168.128.10",
                     end_ip="192.168.128.20",
                     prim_dns="8.8.8.8")
    """

    mo = ip_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                      start_ip=start_ip, end_ip=end_ip,
                      caller="ip_block_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo

def ip_block_delete(handle, pool_name=None, org_dn="org-root", start_ip=None, end_ip=None):

    """
    deletes ip block

    Args:
        handle (UcsHandle)
        pool_name (string): Name of ip pool block is associated with
        org_dn (string): org dn
        start_ip (string): 1st ip in the block
        end_ip (string): last ip in the block
    
    Returns:
        None
    
    Raises:
        UcsOperationError: if Ippoolblock is not present
    
    Example:
        ip_block_delete(handle,
                     pool_name="ext-mgmt",
                     org_dn="org-root",
                     start_ip="192.168.128.10",
                     end_ip="192.168.128.20")
    """

    mo = ip_block_get(handle=handle, pool_name=pool_name, org_dn=org_dn,
                      start_ip=start_ip, end_ip=end_ip,
                      caller="ip_block_delete")
    handle.remove_mo(mo)
    handle.commit()