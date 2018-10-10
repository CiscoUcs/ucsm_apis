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
This module performs operations related to network control policies.
"""

from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import BiosVfConsistentDeviceNameControl
from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import BiosVfFrontPanelLockout
from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss
from ucsmsdk.ucsexception import UcsOperationError


def bios_policy_create(handle, name=None,
                       org_dn="org-root",
                       reboot="no",
                       descr=None,
                       cdn_ctrl="platform-default",
                       front_panel_lock="platform-default",
                       post_err_pause="platform-default",
                       quiet_boot="platform-default",
                       res_power_loss="platform-default",
                       **kwargs):

    """
    Creates bios policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        descr (string): description
        reboot (string): Reboot on Update ["no", "yes]
        cdn_ctrl (string): Consistent Device Name Control 
                           ["enabled", "disabled", "platform-default",
                            "platform-recommended"]
        front_panel_lock (string): receive lldp 
                                   ["enabled", "disabled", "platform-default",
                                    "platform-recommended"]
        post_err_pause (string): Post Error Pause
                                 ["enabled", "disabled", "platform-default",
                                  "platform-recommended"]
        quiet_boot (string): Quiet Boot
                             ["enabled", "disabled", "platform-default",
                              "platform-recommended"]
        res_power_loss (string): Resume after AC Power Loss 
                                 ["enabled", "disabled", "platform-default",
                                  "platform-recommended"]
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        BiosVProfile: managed object

    Raises:
        UcsOperationError: if Org_dn is not present

    Example:
        bios_policy_create(handle,
                             name="no_quiet",
                             descr="no quiet boot",
                             quiet_boot="disabled")
    """

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("bios_policy_create", "Org {} \
                                 does not exist".format(org_dn))

    mo = BiosVProfile(parent_mo_or_dn=org_dn, name=name,
                      descr=descr, reboot_on_update=reboot)
    mo_1 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
    mo_2 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
    mo_3 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
    mo_4 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="disabled")
    mo_5 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def bios_policy_get(handle, name=None,
                      org_dn="org-root",
                      caller="bios_policy_get"):

    """
    Gets bios policy

    Args:
        handle (UCSHandle)
        name (string): Name of policy
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        BiosVProfile: managed object

    Raises:
        UcsOperationError: if BiosVProfile is not present

    Example:
        bios_policy_get(handle,
                        name="quiet_boot",
                        org_dn="org-root")
    """

    dn = org_dn + "/bios-prof-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise UcsOperationError(caller, "bios policy {} \
                                does not exist".format(dn))
    return mo


def bios_policy_exists(handle, name=None,
                       org_dn="org-root", **kwargs):

    """
    checks if policy exists

    Args:
        handle (UcsHandle)
        name (string): Name of bios policy
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, BiosVProfile MO/None)

    Raises:
        None

    Example:
        bios_policy_exists:(handle,
                            name="quiet_boot",
                            org_dn="org-root")
    """

    try:
        mo = bios_policy_get(handle=handle, name=name, org_dn=org_dn,
                             caller="bios_policy_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def bios_policy_modify(handle, name=None,
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
        BiosVProfile: managed object

    Raises:
        UcsOperationError: if BiosVProfile is not present

    Example:
        bios_policy_modify(handle,
                           name="quiet_boot",
                           descr="prod bios policy")
    """

    mo = bios_policy_get(handle=handle, name=name, org_dn=org_dn,
                         caller="bios_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def bios_policy_delete(handle, name=None, org_dn="org-root"):

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
        bios_policy_delete(handle,
                           name="quiet_boot",
                           org_dn="org-root")
    """

    mo = bios_policy_get(handle=handle, name=name, org_dn=org_dn,
                           caller="bios_policy_delete")
    handle.remove_mo(mo)
    handle.commit()
