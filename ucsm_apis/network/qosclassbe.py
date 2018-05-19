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
This module performs operations related to Fabric Ethernet Lan Ports.
"""

from ucsmsdk.ucsexception import UcsOperationError


def qosclassbe_modify(handle, org_dn="fabric/lan/classes/class-best-effort",
                      mtu="normal", weight="5", **kwargs):

    """
    Modifies Best Effort QOS Class

    Args:
        handle (UCSHandle)
        org_dn (string): org_dn
        mtu (string): mtu value ["fc", "normal"], ["1500-9216"]
        weight (string): qos channel weight ["1-10"], ["best-effort", "none"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        QosclassEthBE: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        qosclassbe_modify(handle,
                          mtu="9216")
    """

    mo = handle.query_dn(org_dn)
    if not mo:
        raise UcsOperationError("qosclass_modify", "Org {} "
                                "does not exist".format(org_dn))

    mo.mtu = mtu
    mo.weight = weight
    # handle.add_mo(mo, modify_present=True)
    handle.set_mo(mo)
    handle.commit()
    return mo


def qosclassbe_get(handle, org_dn="fabric/lan/classes/"
                   "class-best-effort",
                   **kwargs):

    """
    Gets Best Effort QOS Class

    Args:
        handle (UCSHandle)
        org_dn (string): org_dn
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        QosclassEthBE: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        qosclassbe_get(handle)
    """

    mo = handle.query_dn(org_dn)
    if not mo:
        raise UcsOperationError("qosclass_modify", "Org {} "
                                "does not exist".format(org_dn))

    return mo
