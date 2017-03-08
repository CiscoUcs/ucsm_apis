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


import logging
log = logging.getLogger('ucs')


from ..utils.utils import boot_policy_dn_get
from ..utils.utils import boot_policy_mo_get
from ..utils.utils import mo_exist

from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import \
    LsbootDefaultLocalImage
from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
from ucsmsdk.mometa.lsboot.LsbootUsbFlashStorageImage import \
    LsbootUsbFlashStorageImage
from ucsmsdk.mometa.lsboot.LsbootUsbInternalImage import LsbootUsbInternalImage
from ucsmsdk.mometa.lsboot.LsbootUsbExternalImage import LsbootUsbExternalImage



def boot_policy_create(handle, name, boot_mode="legacy", descr=None, enforce_vnic_name=None, policy_owner=None, reboot_on_update=None,  parent_dn="org-root", **kwargs):
    """
    This method creates boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        boot_mode (string): "legacy" or "uefi"
        descr (string): Basic description.
        enforce_vnic_name (string): "yes" or "no"
        policy_owner (string): "local" or "pending-policy" or  "policy"
        reboot_on_update (string): "yes" or "no"
        parent_dn (string): Org DN.

    Returns:
        LsbootPolicy: Managed Object

    Example:
        boot_policy_create(handle, name="sample_boot",
                            reboot_on_update="yes",
                            boot_mode="legacy",
                            parent_dn="org-root/org-finance",

    """
    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise UcscOperationError("boot_policy_create", "Org %s does not exist" % parent_dn)

    mo = LsbootPolicy(parent_mo_or_dn=obj, name=name, boot_mode=boot_mode, descr=descr, enforce_vnic_name=enforce_vnic_name, policy_owner=policy_owner, reboot_on_update=reboot_on_update)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def boot_policy_modify(handle, name, parent_dn="org-root", **kwargs):
    """
    This method modifies boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        parent_dn (string): Parent of Org.

    Returns:
        LsbootPolicy: Managed Object

    Raises:
        ValueError: If LsbootPolicy is not present

    Example:
        boot_policy_modify(handle, name="sample_boot",
                                reboot_on_update="yes",
                                boot_mode="legacy",
                                parent_dn="org-root/org-test")
    """

    mo = boot_policy_mo_get(handle, parent_dn, name=name)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def boot_policy_delete(handle, name, parent_dn="org-root"):
    """
    This method removes boot policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the boot policy.
        parent_dn (string): Parent of Org

    Returns:
        None

    Raises:
        ValueError: If LsbootPolicy is not present

    Example:
        boot_policy_remove(handle, name="sample_boot",
                            parent_dn="org-root/org-test")
    """

    mo = boot_policy_mo_get(handle, parent_dn, name=name)
    handle.remove_mo(mo)
    handle.commit()


def boot_policy_exist(handle, name, parent_dn="org-root", **kwargs):
    """
    checks if boot policy exist

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        reboot_on_update (string): "yes" or "no"
        enforce_vnic_name (string): "yes" or "no"
        boot_mode (string): "legacy" or "uefi"
        parent_dn (string): Org DN.
        descr (string): Basic description.

    Returns:
        True/False: Boolean

    Example:
        boot_policy_exist(handle,
                        name="sample_boot",
                        reboot_on_update="yes",
                        boot_mode="legacy",
                        parent_dn="org-root/org-finance")
    """

    return mo_exist(func=boot_policy_mo_get, handle=handle, parent_dn=parent_dn, name=name, primary_kwargs=kwargs)


def _add_device(handle, parent_mo, boot_device):
    count = 0
    children = handle.query_children(parent_mo)
    for child in children:
        if hasattr(child, 'order'):
            order = getattr(child, 'order')
            if order not in boot_device:
                log.debug("Deleting boot device from boot policy: %s",
                          child.dn)
                handle.remove_mo(child)
                
    for k in boot_device.keys():
        log.debug("Add boot device: order=%s, %s", k, boot_device[k])
        if boot_device[k] in ["cdrom-local", "cdrom"]:
            _add_cdrom_local(parent_mo, k)
        elif boot_device[k] == "cdrom-cimc":
            _add_cdrom_cimc(parent_mo, k)
        elif boot_device[k] == "cdrom-remote":
            _add_cdrom_remote(parent_mo, k)
        elif boot_device[k] in ["lun", "local-disk", "sd-card", "usb-internal",
                                "usb-external"]:
            if count == 0:
                mo = LsbootStorage(parent_mo_or_dn=parent_mo, order=k)
                mo_1 = LsbootLocalStorage(parent_mo_or_dn=mo)
                count += 1
            if boot_device[k] == "lun":
                _add_local_lun(mo_1, k)
            elif boot_device[k] == "local-disk":
                _add_local_disk(mo_1, k)
            elif boot_device[k] == "sd-card":
                _add_sd_card(mo_1, k)
            elif boot_device[k] == "usb-internal":
                _add_usb_internal(mo_1, k)
            elif boot_device[k] == "usb-external":
                _add_usb_external(mo_1, k)
        elif boot_device[k] in ["floppy", "floppy-local"]:
            _add_floppy_local(parent_mo, k)
        elif boot_device[k] == "floppy-external":
            _add_floppy_remote(parent_mo, k)
        elif boot_device[k] == "virtual-drive":
            _add_virtual_drive(parent_mo, k)
        else:
            log.debug("Option <%s> not recognized." % boot_device[k])


def _add_cdrom_local(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-only-local",
                       order=order)


def _add_cdrom_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-only-remote",
                       order=order)


def _add_cdrom_cimc(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-only-remote-cimc",
                       order=order)


def _add_floppy_local(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                       access="read-write-local",
                       order=order)


def _add_floppy_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-remote",
                       order=order)


def _add_virtual_drive(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-drive",
                       order=order)


def _add_local_disk(parent_mo, order):
    LsbootDefaultLocalImage(parent_mo_or_dn=parent_mo, order=order)


def _add_local_lun(parent_mo, order):
    LsbootLocalHddImage(parent_mo_or_dn=parent_mo, order=order)


def _add_sd_card(parent_mo, order):
    LsbootUsbFlashStorageImage(parent_mo_or_dn=parent_mo, order=order)


def _add_usb_internal(parent_mo, order):
    LsbootUsbInternalImage(parent_mo_or_dn=parent_mo, order=order)


def _add_usb_external(parent_mo, order):
    LsbootUsbExternalImage(parent_mo_or_dn=parent_mo, order=order)
