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


def boot_policy_dn_get(name, parent_dn="org-root"):
    return parent_dn + "/boot-policy-" + name


def boot_policy_get(handle, name, parent_dn="org-root"):
    dn = boot_policy_dn_get(name, parent_dn)
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcscOperationError("boot_policy_get", "BootPolicy %s does not exist" % dn)
    return mo


def mo_exist(func, primary_kwargs=None, *args, **kwargs):
    try:
        mo = func(*args, **kwargs)
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**primary_kwargs)
    return (mo_exists, mo if mo_exists else None)


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

    mo = boot_policy_get(handle=handle, name=name, parent_dn=parent_dn)
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
    mo = boot_policy_get(handle=handle, name=name, parent_dn=parent_dn)
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

    return mo_exist(func=boot_policy_mo_get, handle=handle, name=name, parent_dn=parent_dn, primary_kwargs=kwargs)


def _lsboot_local_storage_get(boot_policy_mo):
    lsboot_storage =  LsbootStorage(parent_mo_or_dn=boot_policy_mo)
    return LsbootLocalStorage(parent_mo_or_dn=lsboot_storage)


def _local_disk_add(parent_mo, order):
    LsbootDefaultLocalImage(parent_mo_or_dn=parent_mo, order=order)


def _local_lun_add(parent_mo, order):
    LsbootLocalHddImage(parent_mo_or_dn=parent_mo, order=order)


def _local_jbod_add(parent_mo, order, type, slot_number):
    from ucsmsdk.mometa.lsboot.LsbootLocalDiskImage import LsbootLocalDiskImage
    from ucsmsdk.mometa.lsboot.LsbootLocalDiskImagePath import LsbootLocalDiskImagePath

    mo_ = LsbootLocalDiskImage(parent_mo_or_dn=parent_mo, order=order)
    LsbootLocalDiskImagePath(parent_mo_or_dn=mo_, type=type, slot_number=slot_number)


def _local_sdcard_add(parent_mo, order):
    LsbootUsbFlashStorageImage(parent_mo_or_dn=parent_mo, order=order)


def _local_int_usb_add(parent_mo, order):
    LsbootUsbInternalImage(parent_mo_or_dn=parent_mo, order=order)


def _local_ext_usb_add(parent_mo, order):
    LsbootUsbExternalImage(parent_mo_or_dn=parent_mo, order=order)


def _local_embed_lun_add(parent_mo, order):
    LsbootEmbeddedLocalLunImage(parent_mo_or_dn=parent_mo, order=order)


def _local_embed_disk_add(parent_mo, order):
    LsbootEmbeddedLocalDiskImage(parent_mo_or_dn=parent_mo, order=order)


def _vmedia_cd_dvd_local(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-only-local", order=order)


def _vmedia_cd_dvd_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-only-remote", order=order)


def _vmedia_floppy_local(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-local", order=order)


def _vmedia_floppy_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-remote", order=order)


def _vmedia_vd_remote(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-drive", order=order)


def _vmedia_cimc_cd_dvd(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-only-remote-cimc", order=order)


def _vmedia_cimc_mounted_hdd(parent_mo, order):
    LsbootVirtualMedia(parent_mo_or_dn=parent_mo, access="read-write-remote-cimc", order=order)


_local_devices = {"local_disk": _local_disk_add,
                  "local_lun": _local_lun_add,
                  "local_jbod": _local_jbod_add,
                  "sd_card": _local_sdcard_add,
                  "internal_usb": _local_int_usb_add,
                  "external_usb": _local_ext_usb_add,
                  "embedded_local_lun": _local_embed_lun_add,
                  "embedded_local_disk": _local_embed_disk_add
                  }


_vmedia_devices = {"cd_dvd_local": _vmedia_cd_dvd_local,
                   "cd_dvd_remote": _vmedia_cd_dvd_remote,
                   "floppy_local": _vmedia_floppy_local,
                   "floppy_remote": _vmedia_floppy_remote,
                   "virtual_drive_remote": _vmedia_vd_remote,
                   "cimc_mounted_cd_dvd": _vmedia_cimc_cd_dvd,
                   "cimc_mounted_hdd": _vmedia_cimc_mounted_hdd}


def _local_device_add(lsboot_local_storage, device_name, order, **kwargs):
    _local_devices[device_name](parent_mo=lsboot_local_storage, order=order, **kwargs)


def _vmedia_device_add(parent_mo, device_name, order):
    _vmedia_devices[device_name](parent_mo=parent_mo, order=order)


def _lan_device_add(parent_mo, order, vnic_name, type="primary", **kwargs):
	from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
	from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath

	mo_ = LsbootLan(parent_mo_or_dn=parent_mo, order=order, prot="pxe")
	LsbootLanImagePath(parent_mo_or_dn=mo_, vnic_name=vnic_name, type=type)


def _san_image_path_add(parent_mo, wwn, type, lun):
    from ucsmsdk.mometa.lsboot.LsbootSanCatSanImagePath import LsbootSanCatSanImagePath

    LsbootSanCatSanImagePath(parent_mo_or_dn=parent_mo, wwn=wwn, type=type, lun=lun)


def _san_device_add(parent_mo, order, vnic_name, type="primary", add_image_path=False, wwn=None, lun=None):
    from ucsmsdk.mometa.lsboot.LsbootSan import LsbootSan
    from ucsmsdk.mometa.lsboot.LsbootSanCatSanImage import LsbootSanCatSanImage

    mo_ = LsbootSan(parent_mo_or_dn=parent_mo, order=order)
    san_image = LsbootSanCatSanImage(parent_mo_or_dn=mo_, vnic_name=vnic_name, type=type)

    if not add_image_path:
		return

    _san_image_path_add(parent_mo=san_image, wwn=wwn, type=type, lun=lun)


def _iscsi_device_add(parent_mo, order, vnic_name, type="primary"):
	from ucsmsdk.mometa.lsboot.LsbootIScsi import LsbootIScsi
	from ucsmsdk.mometa.lsboot.LsbootIScsiImagePath import LsbootIScsiImagePath

	mo_ = LsbootIScsi(parent_mo_or_dn=parent_mo, order=order)
	LsbootIScsiImagePath(parent_mo_or_dn=mo_, i_scsi_vnic_name=vnic_name, type=type)


def _efi_shell_device_add():
	pass


def _device_add(handle, boot_policy, devices):
    is_first_local_device = True
    for device in devices:
        device_name = device["device_name"]
        device_order = str(device["device_order"])
        device_props = device["device_props"]

        if device_name in _local_devices:
            if is_first_local_device:
                lsboot_storage =  LsbootStorage(parent_mo_or_dn=boot_policy)
                lsboot_local_storage = LsbootLocalStorage(parent_mo_or_dn=lsboot_storage)
                # handle.add_mo(lsboot_storage, True)
                is_first_local_device = False
            _local_device_add(lsboot_local_storage, device_name, device_order, **device_props)
        elif device_name in _vmedia_devices:
            _vmedia_device_add(boot_policy, device_name, device_order)
        elif device_name == "lan":
            _lan_device_add(boot_policy, device_order, **device_props)
        elif device_name == "san":
            _san_device_add(boot_policy, device_order, **device_props)
        elif device_name == "iscsi":
            _iscsi_device_add(boot_policy, device_order, **device_props)
        elif device_name == "efi":
            _efi_shell_device_add()
        else:
            raise ValueError("Invalid Device <%s>" % device_name)


def _device_remove_all(handle, boot_policy):
    from ucsmsdk import ucsgenutils

    mo_list = handle.query_children(in_mo=boot_policy)
    if mo_list is None:
        return
    for mo in mo_list:
        handle.remove_mo(mo)
		# mo.status = "deleted"
		# boot_policy._child.append(mo)

    if boot_policy.reboot_on_update in ucsgenutils.AFFIRMATIVE_LIST:
		boot_policy.reboot_on_update = False
		handle.set_mo(boot_policy)
		handle.commit()
		boot_policy.reboot_on_update = True
		handle.set_mo(boot_policy)
    handle.commit()


def boot_policy_order_set(handle, boot_policy, devices):
    _device_remove_all(handle, boot_policy)

    _device_add(handle, boot_policy, devices)
    handle.set_mo(boot_policy)
    handle.commit()




