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
This module performs the operation related to boot.
"""
from ucsmsdk import ucsgenutils
from ucsmsdk.ucsexception import UcsOperationError
from ucsmsdk.ucscoreutils import load_class


def boot_policy_create(handle, name, org_dn="org-root",
                       reboot_on_update="no", enforce_vnic_name="yes",
                       boot_mode="legacy", policy_owner="local",
                       descr=None, **kwargs):
    """
    creates boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn
        reboot_on_update (string): valid values are "yes", "no"
        enforce_vnic_name (string): valid values are "yes", "no"
        boot_mode (string): "legacy" or "uefi"
        policy_owner (string): "local" or "pending-policy" or  "policy"
        descr (string): Basic description.
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        LsbootPolicy: managed object

    Raises:
        UcsOperationError: if OrgOrg is not present

    Example:
        boot_policy_create(handle,
                           name="sample_boot",
                           org_dn="org-root/org-finance",
                           reboot_on_update="yes",
                           enforce_vnic_name="yes",
                           boot_mode="legacy",
                           descr="sample description")
    """
    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcsOperationError("boot_policy_create", "Org '%s' does not \
                                 exist" % org_dn)

    mo = LsbootPolicy(parent_mo_or_dn=obj, name=name,
                      reboot_on_update=reboot_on_update,
                      enforce_vnic_name=enforce_vnic_name,
                      boot_mode=boot_mode,
                      policy_owner=policy_owner,
                      descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def boot_policy_get(handle, name, org_dn="org-root", caller="boot_policy_get"):
    """
    gets boot policy.

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn
        caller (string): caller method name

    Returns:
        LsbootPolicy: managed object

    Raises:
        UcsOperationError: if LsbootPolicy is not present

    Example:
_       boot_policy_get(handle,
                        name="sample_boot",
                        org_dn="org-root/org-finance",
                        caller="boot_policy_modify")
    """
    dn = org_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "BootPolicy '%s' does not exist" % dn)
    return mo


def boot_policy_exists(handle, name, org_dn="org-root", **kwargs):
    """
    checks if boot policy exist

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, LsbootPolicy MO/None)

    Raises:
        None

    Example:
        boot_policy_exists(handle, name="sample_boot",
                          org_dn="org-root/org-finance")
    """
    try:
        mo = boot_policy_get(handle=handle, name=name, org_dn=org_dn,
                             caller="boot_policy_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def boot_policy_modify(handle, name, org_dn="org-root", **kwargs):
    """
    modifies boot policy.

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        LsbootPolicy: managed object

    Raises:
        UcsOperationError: if LsbootPolicy is not present

    Example:
        boot_policy_modify(handle, name="sample_boot",
                           org_dn="org-root/org-test",
                           reboot_on_update="yes",
                           boot_mode="legacy")
    """
    mo = boot_policy_get(handle=handle, name=name, org_dn=org_dn,
                         caller="boot_policy_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def boot_policy_delete(handle, name, org_dn="org-root"):
    """
    deletes boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if LsbootPolicy is not present

    Example:
        boot_policy_delete(handle, name="sample_boot",
                           org_dn="org-root/org-test")
    """
    mo = boot_policy_get(handle=handle, name=name, org_dn=org_dn,
                         caller="boot_policy_delete")
    handle.remove_mo(mo)
    handle.commit()


def _boot_security_configure(handle, name, org_dn, secure_boot, **kwargs):
    from ucsmsdk.mometa.lsboot.LsbootBootSecurity import LsbootBootSecurity

    boot_policy = boot_policy_get(handle, name, org_dn,
                                  caller="boot_security_enable")
    if boot_policy.boot_mode != "uefi":
        raise UcsOperationError("boot_security_enable",
            "boot mode should be equal to 'uefi' to configure boot security")

    mo = LsbootBootSecurity(parent_mo_or_dn=boot_policy)

    args = {
            'secure_boot': secure_boot
           }

    mo.set_prop_multiple(**args)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(boot_policy, modify_present=True)
    handle.commit()
    return mo


def boot_security_enable(handle, name, org_dn="org-root", **kwargs):
    """
    enables boot security of boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn

    Returns:
        LsbootBootSecurity: managed object

    Raises:
        UcsOperationError: if LsbootPolicy is not present or
                           LsbootPolicy 'boot_mode' != 'uefi'

    Example:
        boot_security_enable(handle, name="sample_boot",
                             org_dn="org-root/org-test")
    """
    return _boot_security_configure(handle, name, org_dn, secure_boot="yes",
                                    **kwargs)


def boot_security_exists(handle, name, org_dn="org-root", **kwargs):
    """
    checks if boot security enabled for a boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, LsbootBootSecurity MO/None)

    Raises:
        None

    Example:
        boot_security_exists(handle, name="sample_boot",
                          org_dn="org-root/org-finance")
    """
    dn = org_dn + "/boot-policy-" + name + "/boot-security"
    mo = handle.query_dn(dn)
    if mo is None:
        return False, None

    kwargs['secure_boot'] = "yes"
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def boot_security_disable(handle, name, org_dn="org-root"):
    """
    disables boot security of boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn

    Returns:
        LsbootPolicy: managed object

    Raises:
        UcsOperationError: if LsbootPolicy is not present or
                           LsbootPolicy 'boot_mode' != 'uefi'

    Example:
        boot_security_disable(handle, name="sample_boot",
                             org_dn="org-root/org-test")
    """
    return _boot_security_configure(handle, name, org_dn, secure_boot="no")


def _local_lun_add(parent_mo, order, lun_name=None, type=None):
    from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
    from ucsmsdk.mometa.lsboot.LsbootLocalLunImagePath import \
        LsbootLocalLunImagePath

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == "LsbootLocalHddImage"]
    if mo and not mo[0].child:
        raise UcsOperationError(
            "_local_lun_add",
            "Instance of Local Lun already added at order '%s'" %
            mo[0].order)
    if mo and mo[0].child:
        child_count = len(mo[0].child)
        if child_count >= 2:
            raise UcsOperationError(
                "_local_lun_add",
                "Both instance of Local Lun already added.")
        if mo[0].child[0].type == type:
            raise UcsOperationError("_local_lun_add",
                                    "Instance of Local Lun of type '%s' "
                                    "already added at  order '%s'." %
                                   (type, mo[0].order))

        if not lun_name or not type:
            raise UcsOperationError("_local_lun_add",
                                    "Required parameter 'lun_name' "
                                    "or 'type' missing.")

        LsbootLocalLunImagePath(parent_mo_or_dn=mo[0], lun_name=lun_name,
                                type=type)
        return

    mo = LsbootLocalHddImage(parent_mo_or_dn=parent_mo, order=order)
    if not lun_name and not type:
        return
    if (lun_name and not type) or (not lun_name and type):
        raise UcsOperationError("_local_lun_add",
                                "Required parameter 'lun_name' \
                                or 'type' missing.")
    LsbootLocalLunImagePath(parent_mo_or_dn=mo,
                            lun_name=lun_name,
                            type=type)


def _local_jbod_add(parent_mo, order, slot_number):
    from ucsmsdk.mometa.lsboot.LsbootLocalDiskImage import \
        LsbootLocalDiskImage
    from ucsmsdk.mometa.lsboot.LsbootLocalDiskImagePath import \
        LsbootLocalDiskImagePath

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == "LsbootLocalDiskImage"]
    if mo:
        raise UcsOperationError("_local_jbod_add",
                                "Instance of Local JBOD already "
                                "added at order '%s'" % mo[0].order)

    if not slot_number:
        raise UcsOperationError("_local_jbod_add",
                                "Required Parameter 'slot_number' missing")

    mo = LsbootLocalDiskImage(parent_mo_or_dn=parent_mo, order=order)
    LsbootLocalDiskImagePath(
        parent_mo_or_dn=mo,
        type="primary",
        slot_number=slot_number)


def _local_embedded_disk_add(parent_mo, order, slot_number=None, type=None):
    from ucsmsdk.mometa.lsboot.LsbootEmbeddedLocalDiskImage import \
        LsbootEmbeddedLocalDiskImage
    from ucsmsdk.mometa.lsboot.LsbootEmbeddedLocalDiskImagePath import \
        LsbootEmbeddedLocalDiskImagePath

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == "LsbootEmbeddedLocalDiskImage"]
    if mo and not mo[0].child:
        raise UcsOperationError("_local_embedded_disk_add",
                                "Instance of Local Embedded Disk already "
                                "added at order '%s'" % mo[0].order)
    if mo and mo[0].child:
        child_count = len(mo[0].child)
        if child_count >= 2:
            raise UcsOperationError("_local_embedded_disk_add",
                                    "Both instance of Local Embedded Disk "
                                    "already added.")
        if mo[0].child[0].type == type:
            raise UcsOperationError("_local_embedded_disk_add",
                                    "Instance of Local Embedded Disk  of "
                                    "type '%s' already added at  order '%s'."
                                    % (type, mo[0].order))

        if not slot_number or not type:
            raise UcsOperationError("_local_embedded_disk_add",
                                    "Required parameter 'slot_number' or "
                                    "'type' missing.")

        LsbootEmbeddedLocalDiskImagePath(parent_mo_or_dn=mo[0],
                                         slot_number=slot_number,
                                         type=type)
        return

    mo = LsbootEmbeddedLocalDiskImage(parent_mo_or_dn=parent_mo, order=order)
    if not slot_number and not type:
        return
    if (slot_number and not type) or (not slot_number and type):
        raise UcsOperationError("_local_embedded_disk_add",
                                "Required parameter 'slot_number' or 'type'"
                                " missing.")
    LsbootEmbeddedLocalDiskImagePath(parent_mo_or_dn=mo,
                                     slot_number=slot_number,
                                     type=type)


def _lan_device_add(parent_mo, order, vnic_name):
    from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
    from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == "LsbootLan"]

    if mo and mo[0].child:
        child_count = len(mo[0].child)
        if child_count >= 2:
            raise UcsOperationError("_lan_device_add",
                                    "Both instances of Lan Device are "
                                    "already added.")

        if not vnic_name:
            raise UcsOperationError("_local_device_add",
                                    "Required parameter 'vnic_name' missing.")

        LsbootLanImagePath(
            parent_mo_or_dn=mo[0],
            vnic_name=vnic_name,
            type="secondary")
        return

    if not vnic_name:
        raise UcsOperationError("Required Parameter 'vnic_name' missing.")

    mo_ = LsbootLan(parent_mo_or_dn=parent_mo, order=order, prot="pxe")
    LsbootLanImagePath(
        parent_mo_or_dn=mo_,
        vnic_name=vnic_name,
        type="primary")


def _children_get(parent_mo, class_id):
    return [mo for mo in parent_mo.child if mo.get_class_id() == class_id]


def _san_add(parent_mo, order):
    from ucsmsdk.mometa.lsboot.LsbootSan import LsbootSan
    return LsbootSan(parent_mo_or_dn=parent_mo, order=order)


def _san_image_add(parent_mo, type, vnic_name):
    from ucsmsdk.mometa.lsboot.LsbootSanCatSanImage import \
        LsbootSanCatSanImage
    if not (vnic_name and type):
        raise UcsOperationError("Required Parameter 'vnic_name' or "
                                "'type' missing.")
    return LsbootSanCatSanImage(parent_mo_or_dn=parent_mo,
                                vnic_name=vnic_name,
                                type=type)


def _san_boot_target_add(parent_mo, target_type, wwn, lun):
    from ucsmsdk.mometa.lsboot.LsbootSanCatSanImagePath import \
        LsbootSanCatSanImagePath
    if target_type or wwn or lun:
        if not (wwn and lun and target_type):
            raise UcsOperationError("Required Parameter 'wwn' or "
                                    "'lun' or 'target_type' missing.")
        return LsbootSanCatSanImagePath(parent_mo_or_dn=parent_mo,
                                        type=target_type,
                                        wwn=wwn,
                                        lun=lun)
    return None


def _san_boot_target_add_validate(parent_mo, target_type, wwn, lun):

    if not(target_type or wwn or lun):
        raise UcsOperationError(
            "_san_device_add",
            "Instance of '%s' san image is already added." %
            parent_mo.type)

    san_boot_targets = parent_mo.child
    san_boot_targets_count = len(san_boot_targets)

    # case3.2.1) if no boot targets added yet, add boot target
    if san_boot_targets_count == 0:
        _san_boot_target_add(parent_mo=parent_mo,
                             target_type=target_type,
                             wwn=wwn,
                             lun=lun)

    # case3.2.2) if both boot targets already added, raise error
    elif san_boot_targets_count >= 2:
        raise UcsOperationError(
            "_san_device_add",
            "Both instance of SAN target devices are already added.")

    # case3.2.3) if only single boot target is added yet
    else:
        existing_boot_target = san_boot_targets[0]

        # case3.2.3.1) if existing boot target_type == i/p target_type
        # raise error
        if existing_boot_target.type == target_type:
            raise UcsOperationError(
                "_san_device_add",
                "Instance of SAN target type '%s' is already added." %
                target_type)

        # case3.2.3.2) if existing boot target_type != i/p target_type
        # add boot target of input target_type
        _san_boot_target_add(parent_mo=parent_mo,
                             target_type=target_type,
                             wwn=wwn,
                             lun=lun)


def _san_device_add(parent_mo, order,
                    vnic_name=None, type=None,
                    wwn=None, lun=None, target_type=None):

    # mo = [mo for mo in parent_mo.child if mo.get_class_id() == "LsbootSan"]
    # Get LsbootSan
    sans = _children_get(parent_mo, "LsbootSan")

    # if lsbootSan not added yet, add it and it's respective child
    if not sans:
        # Add LsbootSan
        san = _san_add(parent_mo=parent_mo, order=order)

        san_image = None
        if vnic_name or type:
            san_image = _san_image_add(parent_mo=san,
                                       type=type,
                                       vnic_name=vnic_name)
        if san_image:
            _san_boot_target_add(parent_mo=san_image,
                                 target_type=target_type,
                                 wwn=wwn,
                                 lun=lun)
        return

    # elif lsbootSan is already added, check for san_images
    san = sans[0]
    san_images = san.child
    san_images_count = len(san_images)

    # case1)  if not (vnic and type) - raise error
    if not (vnic_name and type):
        raise UcsOperationError("_san_device_add",
                                "Instance of San device is already added.")

    # case2) if no san images, add san_image
    if san_images_count == 0:
        san_image = _san_image_add(parent_mo=san,
                                   type=type,
                                   vnic_name=vnic_name)
        _san_boot_target_add(parent_mo=san_image,
                             target_type=target_type,
                             wwn=wwn,
                             lun=lun)
        return

    # case3) if only one san images is already added
    if san_images_count == 1:
        existing_san_image = san_images[0]

        # case3.1) if existing_san_image.type != input_type,
        # add the san image of input type
        if existing_san_image.type != type:
            san_image = _san_image_add(parent_mo=san,
                                       type=type,
                                       vnic_name=vnic_name)
            _san_boot_target_add(parent_mo=san_image,
                                 target_type=target_type,
                                 wwn=wwn,
                                 lun=lun)
            return

        # case3.2) if existing_san_image.type == input_type,
        # check for boot target
        _san_boot_target_add_validate(parent_mo=existing_san_image,
                                      target_type=target_type,
                                      wwn=wwn,
                                      lun=lun)
        return

    # case4) if both san images already added, check for boot target
    if not (target_type and wwn and lun):
        raise UcsOperationError(
            "_san_device_add",
            "Both instance of SAN Devices are already added.")
    if type is None:
        raise UcsOperationError(
            "_san_device_add",
            "Specify 'type' under which boot target to be added.")

    san_image_to_check = [san_image for san_image in san_images
                          if san_image.type == target_type][0]

    _san_boot_target_add_validate(parent_mo=san_image_to_check,
                                  target_type=target_type,
                                  wwn=wwn,
                                  lun=lun)


def _iscsi_device_add(parent_mo, order, vnic_name):
    from ucsmsdk.mometa.lsboot.LsbootIScsi import LsbootIScsi
    from ucsmsdk.mometa.lsboot.LsbootIScsiImagePath import LsbootIScsiImagePath

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == "LsbootIScsi"]

    if mo and mo[0].child:
        child_count = len(mo[0].child)
        if child_count >= 2:
            raise UcsOperationError("_iscsi_device_add",
                                    "Both instances of ISCSI Device are "
                                    "already added.")

        if not vnic_name:
            raise UcsOperationError("_iscsi_device_add",
                                    "Required parameter 'vnic_name' missing.")
        LsbootIScsiImagePath(parent_mo_or_dn=mo[0],
                             i_scsi_vnic_name=vnic_name, type="secondary")
        return

    if not vnic_name:
        raise UcsOperationError("_iscsi_device_add",
                                "Required parameter 'vnic_name' missing.")

    mo_ = LsbootIScsi(parent_mo_or_dn=parent_mo, order=order)
    LsbootIScsiImagePath(parent_mo_or_dn=mo_,
                         i_scsi_vnic_name=vnic_name, type="primary")


_local_devices = {
    "local_disk": ["LsbootDefaultLocalImage", None],
    "local_lun": ["LsbootLocalHddImage", _local_lun_add],
    "local_jbod": ["LsbootLocalDiskImage", _local_jbod_add],
    "sdcard": ["LsbootUsbFlashStorageImage", None],
    "internal_usb": ["LsbootUsbInternalImage", None],
    "external_usb": ["LsbootUsbExternalImage", None],
    "embedded_lun": ["LsbootEmbeddedLocalLunImage", None],
    "embedded_disk": ["LsbootEmbeddedLocalDiskImage",
                      _local_embedded_disk_add],
}

_local_device_invert = dict(
    zip([value[0] for value in _local_devices.values()],
        _local_devices.keys()))

_vmedia_devices = {
    "cd_dvd": "read-only",
    "cd_dvd_local": "read-only-local",
    "cd_dvd_remote": "read-only-remote",
    "floppy": "read-write",
    "floppy_local": "read-write-local",
    "floppy_remote": "read-write-remote",
    "virtual_drive": "read-write-drive",
    "cd_dvd_cimc": "read-only-remote-cimc",
    "hdd_cimc": "read-write-remote-cimc"
}

_vmedia_device_invert = dict(
    zip(_vmedia_devices.values(), _vmedia_devices.keys()))


def _local_device_add(parent_mo, device_name, device_order, **kwargs):

    explicit_method = _local_devices[device_name][1]
    if explicit_method is not None:
        explicit_method(parent_mo=parent_mo,
                        order=device_order,
                        **kwargs)
        return

    class_id = _local_devices[device_name][0]
    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == class_id]

    if mo:
        raise UcsOperationError(
            "_local_device_add", "Device '%s' already exist at order '%s'" %
            (device_name, mo[0].order))

    class_struct = load_class(class_id)
    class_obj = class_struct(parent_mo_or_dn=parent_mo, order=device_order,
                             **kwargs)


def _vmedia_device_add(parent_mo, device_name, device_order, **kwargs):
    class_id = "LsbootVirtualMedia"
    access = _vmedia_devices[device_name]

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == class_id and mo.access == access]
    if mo:
        raise UcsOperationError(
            "_vmedia_device_add", "Device '%s' already exist at order '%s'" %
            (device_name, mo[0].order))

    class_struct = load_class(class_id)
    class_obj = class_struct(parent_mo_or_dn=parent_mo,
                             access=access,
                             order=device_order, **kwargs)


def _efi_device_add(parent_mo, device_order, **kwargs):
    class_id = "LsbootEFIShell"

    mo = [mo for mo in parent_mo.child if mo.get_class_id() == class_id]
    if mo:
        raise UcsOperationError(
            "__efi_device_add", "Device '%s' already exist at order '%s'" %
            (device_name, mo[0].order))

    class_struct = load_class(class_id)
    class_obj = class_struct(parent_mo_or_dn=parent_mo,
                             order=device_order, **kwargs)


def _validate_device_combination(devices):
    local_outer_level = False
    local_inner_level = False

    cd_dvd = False
    cd_dvd_rest = False

    floppy = False
    floppy_rest = False

    for device in devices:
        device_name = device["device_name"]

        if device_name == "local_disk":
            local_outer_level = True
        elif device_name in _local_devices:
            local_inner_level = True
        elif device_name == "cd_dvd":
            cd_dvd = True
        elif device_name in ["cd_dvd_local", "cd_dvd_remote"]:
            cd_dvd_rest = True
        elif device_name == "floppy":
            floppy = True
        elif device_name in ["floppy_local", "floppy_remote"]:
            floppy_rest = True

    if local_outer_level and local_inner_level:
        raise UcsOperationError(
            "_device_add",
            "local_disk cannot be added with other local devices.")
    elif cd_dvd and cd_dvd_rest:
        raise UcsOperationError("_device_add",
                                "'cd_dvd' or 'cd_dvd_local, cd_dvd_remote'")
    elif floppy and floppy_rest:
        raise UcsOperationError("_device_add",
                                "'floppy' or 'floppy_local, floppy_remote'")


def _device_add(handle, boot_policy, devices):
    from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
    from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage

    _validate_device_combination(devices)

    ls_boot_storage_exist = False
    for device in devices:
        device_name = device["device_name"]
        device_order = str(device["device_order"])
        device_props = {key: value for key, value in device.items()
                        if key not in ["device_name", "device_order"]}
        if device_name in _local_devices:
            if not ls_boot_storage_exist:
                lsboot_storage = LsbootStorage(parent_mo_or_dn=boot_policy)
                lsboot_local_storage = LsbootLocalStorage(
                    parent_mo_or_dn=lsboot_storage)
                ls_boot_storage_exist = True
            _local_device_add(lsboot_local_storage, device_name,
                              device_order, **device_props)
        elif device_name in _vmedia_devices:
            _vmedia_device_add(boot_policy, device_name, device_order)
        elif device_name == "lan":
            _lan_device_add(boot_policy, device_order, **device_props)
        elif device_name == "san":
            _san_device_add(boot_policy, device_order, **device_props)
        elif device_name == "iscsi":
            _iscsi_device_add(boot_policy, device_order, **device_props)
        elif device_name == "efi":
            _efi_device_add(boot_policy, device_order, **device_props)
        else:
            raise UcsOperationError(
                "_device_add",
                " Invalid Device <%s>" %
                device_name)


def _boot_policy_order_clear(handle, boot_policy):

    mo_list = handle.query_children(in_mo=boot_policy)
    if mo_list is None:
        return
    for mo in mo_list:
        if mo.get_class_id() == "LsbootBootSecurity":
            continue
        handle.remove_mo(mo)

    if boot_policy.reboot_on_update in ucsgenutils.AFFIRMATIVE_LIST:
        boot_policy.reboot_on_update = "no"
        handle.set_mo(boot_policy)
        handle.commit()
        boot_policy.reboot_on_update = "yes"
        handle.set_mo(boot_policy)
    handle.commit()


def _extract_device_from_bp_child(bp_child):
    bp_devices = {}

    for ch_ in bp_child:
        class_id = ch_.get_class_id()
        if class_id == "LsbootBootSecurity":
            continue
        elif class_id == "LsbootSan":
            bp_devices["san"] = ch_
        elif class_id == "LsbootLan":
            bp_devices["lan"] = ch_
        elif class_id == "LsbootVirtualMedia":
            access = ch_.access
            device = _vmedia_device_invert[access]
            bp_devices[device] = ch_
        elif class_id == "LsbootStorage":
            local_storage = ch_.child[0]
            for local_ch_ in local_storage.child:
                local_class_id = local_ch_.get_class_id()
                device = _local_device_invert[local_class_id]
                bp_devices[device] = local_ch_
        elif class_id == "LsbootIScsi":
            bp_devices["iscsi"] = ch_
        elif class_id == "LsbootEFIShell":
            bp_devices["efi"] = ch_
        else:
            raise UcsOperationError("_compare_boot_policy", "Unknown Device.")

    return bp_devices


def _device_compare(existing_device, device_name, **kwargs):
    if not existing_device.check_prop_match(**kwargs):
        raise UcsOperationError(
            "_compare_boot_policy",
            "Properties mismatch for device '%s'" %
            device_name)


def _child_pri_sec_filter(child_list):
    if child_list[0].type == "primary":
        child_primary = child_list[0]
        child_secondary = child_list[1]
    else:
        child_primary = child_list[1]
        child_secondary = child_list[0]

    return child_primary, child_secondary


def _compare_local_lun(existing_lun, expected_lun):
    _device_compare(existing_lun, 'local_lun', order=expected_lun.order)

    existing_child = existing_lun.child
    expected_child = expected_lun.child
    if len(existing_child) != len(expected_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch for 'local_lun'.")
    if len(existing_child) == 0:
        return
    if len(existing_child) == 1:
        _device_compare(existing_child[0],
                        'local_lun',
                        type=expected_child[0].type,
                        lun_name=expected_child[0].lun_name)
    elif len(existing_child) == 2:
        existing_child_primary, existing_child_secondary =\
            _child_pri_sec_filter(existing_child)

        expected_child_primary, expected_child_secondary =\
            _child_pri_sec_filter(expected_child)

        _device_compare(existing_child_primary,
                        'local_lun',
                        type=expected_child_primary.type,
                        lun_name=expected_child_primary.lun_name)
        _device_compare(existing_child_secondary,
                        'local_lun',
                        type=expected_child_secondary.type,
                        lun_name=expected_child_secondary.lun_name)


def _compare_local_jbod(existing_jbod, expected_jbod):
    _device_compare(existing_jbod, 'local_jbod', order=expected_jbod.order)

    existing_child = existing_jbod.child
    expected_child = expected_jbod.child
    if len(existing_child) != len(expected_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch for 'local_jbod'.")
    if len(existing_child) == 0:
        return
    if len(existing_child) == 1:
        _device_compare(existing_child[0],
                        'local_jbod',
                        slot_number=expected_child[0].slot_number)


def _compare_embedded_disk(existing_disk, expected_disk):
    _device_compare(existing_disk,
                    'embedded_disk',
                    order=expected_disk.order)

    existing_child = existing_disk.child
    expected_child = expected_disk.child
    if len(existing_child) != len(expected_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch for 'embedded_disk'.")
    if len(existing_child) == 0:
        return
    if len(existing_child) == 1:
        _device_compare(existing_child[0],
                        'embedded_disk',
                        type=expected_disk.type,
                        slot_number=expected_disk.slot_number)
    if len(existing_child) == 2:
        existing_child_primary, existing_child_secondary =\
            _child_pri_sec_filter(existing_child)

        expected_child_primary, expected_child_secondary =\
            _child_pri_sec_filter(expected_child)

        _device_compare(existing_child_primary,
                        'embedded_disk',
                        type=expected_child_primary.type,
                        slot_number=expected_child_primary.slot_number)
        _device_compare(existing_child_secondary,
                        'embedded_disk',
                        type=expected_child_secondary.type,
                        slot_number=expected_child_secondary.slot_number)


def _compare_lan(existing_lan, expected_lan):
    _device_compare(existing_lan,
                    'lan',
                    order=expected_lan.order)

    existing_child = existing_lan.child
    expected_child = expected_lan.child
    if len(existing_child) != len(expected_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch for 'lan'.")
    if len(existing_child) == 0:
        return
    if len(existing_child) == 1:
        _device_compare(existing_child[0],
                        'lan',
                        type=expected_lan.type,
                        vnic_name=expected_lan.vnic_name)
    if len(existing_child) == 2:
        existing_child_primary, existing_child_secondary =\
            _child_pri_sec_filter(existing_child)

        expected_child_primary, expected_child_secondary =\
            _child_pri_sec_filter(expected_child)

        _device_compare(existing_child_primary,
                        'lan',
                        type=expected_child_primary.type,
                        vnic_name=expected_child_primary.vnic_name)
        _device_compare(existing_child_secondary,
                        'lan',
                        type=expected_child_secondary.type,
                        vnic_name=expected_child_secondary.vnic_name)


def _compare_san_sub_child(existing_sub_child, expected_sub_child,
                           expected_san):

    if len(existing_sub_child) != len(expected_sub_child):
        raise UcsOperationError("_compare_boot_policy",
                                "sub child count mismatch for 'san'.")

    if len(existing_sub_child) == 0:
        return
    if len(existing_sub_child) == 1:
        _device_compare(existing_sub_child[0],
                        'san',
                        type=expected_san.type,
                        wwn=expected_sub_child.wwn,
                        lun=expected_sub_child.lun)
    if len(existing_sub_child) == 2:
        existing_sub_child_primary, existing_sub_child_secondary =\
            _child_pri_sec_filter(existing_sub_child)

        expected_sub_child_primary, expected_sub_child_secondary =\
            _child_pri_sec_filter(expected_sub_child)

        _device_compare(existing_sub_child_primary,
                        'san',
                        type=expected_sub_child_primary.type,
                        wwn=expected_sub_child_primary.wwn,
                        lun=expected_sub_child_primary.lun
                        )
        _device_compare(existing_sub_child_secondary,
                        'san',
                        type=expected_sub_child_secondary.type,
                        wwn=expected_sub_child_secondary.wwn,
                        lun=expected_sub_child_secondary.lun)


def _compare_san(existing_san, expected_san):
    _device_compare(existing_san,
                    'san',
                    order=expected_san.order)

    existing_child = existing_san.child
    expected_child = expected_san.child
    if len(existing_child) != len(expected_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch for 'san'.")
    if len(existing_child) == 0:
        return
    if len(existing_child) == 1:
        _device_compare(existing_child[0],
                        'san',
                        type=expected_san.type,
                        vnic_name=expected_san.vnic_name)

        existing_sub_child = existing_child.child
        expected_sub_child = expected_child.child

        _compare_san_sub_child(existing_sub_child, expected_sub_child)

    if len(existing_child) == 2:
        existing_child_primary, existing_child_secondary =\
            _child_pri_sec_filter(existing_child)

        expected_child_primary, expected_child_secondary =\
            _child_pri_sec_filter(expected_child)

        _device_compare(existing_child_primary,
                        'san',
                        type=expected_child_primary.type,
                        vnic_name=expected_child_primary.vnic_name)
        # compare sub_child under primary child
        _compare_san_sub_child(existing_child_primary.child,
                               expected_child_primary.child)

        _device_compare(existing_child_secondary,
                        'san',
                        type=expected_child_secondary.type,
                        vnic_name=expected_child_secondary.vnic_name)
        # compare sub_child under secondary child
        _compare_san_sub_child(existing_child_secondary.child,
                               expected_child_secondary.child)


def _compare_iscsi(existing_iscsi, expected_iscsi):
    _device_compare(existing_iscsi,
                    'iscsi',
                    order=expected_iscsi.order)

    existing_child = existing_iscsi.child
    expected_child = expected_iscsi.child

    if len(existing_child) != len(expected_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch for 'iscsi'.")
    if len(existing_child) == 0:
        return
    if len(existing_child) == 1:
        _device_compare(existing_child[0],
                        'iscsi',
                        type=expected_child[0].type,
                        i_scsi_vnic_name=expected_child[0].i_scsi_vnic_name)
    if len(existing_child) == 2:
        existing_child_primary, existing_child_secondary =\
            _child_pri_sec_filter(existing_child)

        expected_child_primary, expected_child_secondary =\
            _child_pri_sec_filter(expected_child)

        _device_compare(
            existing_child_primary,
            'iscsi',
            type=expected_child_primary.type,
            i_scsi_vnic_name=expected_child_primary.i_scsi_vnic_name)
        _device_compare(
            existing_child_secondary,
            'iscsi',
            type=expected_child_secondary.type,
            i_scsi_vnic_name=expected_child_secondary.i_scsi_vnic_name)


def _compare_efi(existing_efi, expected_efi):
    _device_compare(existing_efi, 'efi', order=expected_efi.order)


def _compare_boot_policy(existing_boot_policy, expected_boot_policy):
    # check child count
    existing_bp_child = existing_boot_policy.child
    expected_bp_child = expected_boot_policy.child

    existing_bp_child = [ch for ch in existing_bp_child
                         if ch.get_class_id() != "LsbootBootSecurity"]

    if len(existing_bp_child) != len(expected_bp_child):
        raise UcsOperationError("_compare_boot_policy",
                                "Child count mismatch.")

    existing_bp_devices = _extract_device_from_bp_child(existing_bp_child)
    expected_bp_devices = _extract_device_from_bp_child(expected_bp_child)

    for device_name in existing_bp_devices:
        if device_name not in expected_bp_devices:
            raise UcsOperationError("_compare_boot_policy",
                                    "Device does not already exist.")

        existing_bp_device = existing_bp_devices[device_name]
        expected_bp_device = expected_bp_devices[device_name]

        if device_name in _vmedia_devices:
            if not existing_bp_device.check_prop_match(
                    order=expected_bp_device.order):
                raise UcsOperationError(
                    "_compare_boot_policy",
                    "Order mismatch for device '%s'." %
                    device_name)
        elif device_name in _local_devices:
            if _local_devices[device_name][1] is None:
                if not existing_bp_device.check_prop_match(
                        order=expected_bp_device.order):
                    raise UcsOperationError(
                        "_compare_boot_policy",
                        "Order mismatch for device '%s'." %
                        device_name)
            elif device_name == "local_lun":
                _compare_local_lun(existing_bp_device,
                                   expected_bp_device)
            elif device_name == "local_jbod":
                _compare_local_jbod(existing_bp_device,
                                    expected_bp_device)
            elif device_name == "embedded_disk":
                _compare_embedded_disk(existing_bp_device,
                                       expected_bp_device)
        elif device_name == "lan":
            _compare_lan(existing_bp_device,
                         expected_bp_device)
        elif device_name == "san":
            _compare_san(existing_bp_device,
                         expected_bp_device)
        elif device_name == "iscsi":
            _compare_iscsi(existing_bp_device,
                           expected_bp_device)
        elif device_name == "efi":
            _compare_efi(existing_bp_device,
                         expected_bp_device)


def boot_policy_order_set(handle, name, devices, org_dn="org-root"):
    """
    sets boot order for a given boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        devices (list of dict):
         [
            {
             "device_name": device_name,
             "device_order" "1-16",
             },
            {
             "device_name": device_name,
             "device_order" "1-16",
             "property_name": "property_value",
            },
            {
             "device_name": device_name,
             "device_order" "1-16",
             "property_name": "property_value",
             "property_name": "property_value",
             "property_name": "property_value",
            },
         ]

         device_name (string): device name
          valid values are "local_lun",  "local_jbod",  "sdcard",
           "internal_usb",  "external_usb",  "embedded_lun",
           "embedded_disk",  "cd_dvd_local",  "cd_dvd_remote",
           "floppy_local",  "floppy_remote",  "virtual_drive",
           "cd_dvd_cimc",  "hdd_cimc",  "lan",  "san",  "iscsi"
         device_order (string): boot order for a device, "0-16"

         *note - mandatory keys are 'device_name' and 'device_order'
                 other key depends on the device.
        org_dn (string): org dn

    Returns:
        None

    Raises:
        UcsOperationError: if LsbootPolicy is not present

    Example:
        devices = [
                    {"device_name": "local_lun",
                     "device_order": "1",
                     "type": "primary",
                     "lun_name": "primary"
                    },
                    {"device_name": "local_lun",
                     "device_order": "1",
                     "type": "secondary",
                     "lun_name": "secondary"
                    },
                    {"device_name": "local_jbod",
                     "device_order": "2",
                     "slot_number": "1"
                    },
                    {"device_name": "sdcard",
                     "device_order": "3",
                    },
                    {"device_name": "internal_usb",
                     "device_order": "4",
                    },
                    {"device_name": "external_usb",
                     "device_order": "5",
                    },
                    {"device_name": "embedded_lun",
                     "device_order": "6",
                    },
                    {"device_name": "embedded_disk",
                     "device_order": "7",
                     "type": "primary",
                     "slot_number": "1"
                    },
                    {"device_name": "embedded_disk",
                     "device_order": "7",
                     "type": "secondary",
                     "slot_number": "1"
                    },
                    {"device_name": "cd_dvd_local",
                     "device_order": "8",
                    },
                    {"device_name": "cd_dvd_remote",
                     "device_order": "9",
                    },
                    {"device_name": "floppy_local",
                     "device_order": "10",
                    },
                    {"device_name": "floppy_remote",
                     "device_order": "11",
                    },
                    {"device_name": "virtual_drive",
                     "device_order": "12",
                    },
                    {"device_name": "cd_dvd_cimc",
                     "device_order": "13",
                    },
                    {"device_name": "hdd_cimc",
                     "device_order": "14",
                    },
                    {"device_name": "lan",
                     "device_order": "15",
                     "vnic_name": "vnic_primary"
                    },
                    {"device_name": "lan",
                     "device_order": "15",
                     "vnic_name": "vnic_secondary"
                    },
                    {"device_name": "san",
                     "device_order": "16",
                     "vnic_name": "vnic_primary",
                     "type": "primary",
                     "target_type": "primary",
                     "lun": "1",
                     "wwn": "10:00:00:00:00:00:00:00"
                    },
                    {"device_name": "san",
                     "device_order": "16",
                     "vnic_name": "vnic_primary",
                     "type": "primary",
                     "target_type": "secondary",
                     "lun": "1",
                     "wwn": "10:00:00:00:00:00:00:00"
                    },
                    {"device_name": "san",
                     "device_order": "16",
                     "vnic_name": "vnic_secondary",
                     "type": "secondary",
                     "target_type": "primary",
                     "lun": "1",
                     "wwn": "10:00:00:00:00:00:00:00"
                    },
                    {"device_name": "san",
                     "device_order": "16",
                     "vnic_name": "vnic_secondary",
                     "type": "secondary",
                     "target_type": "secondary",
                     "lun": "1",
                     "wwn": "10:00:00:00:00:00:00:00"
                    },
                    # {"device_name": "iscsi",
                    #  "device_order": "17",
                    #  "vnic_name": "vnic_primary"
                    # },
                    # {"device_name": "iscsi",
                    #  "device_order": "17",
                    #  "vnic_name": "vnic_secondary"
                    # },
        ]

        def test_boot_policy_order_set():
            boot_policy_order_set(handle, name="sample_boot", devices=devices)

    """
    # check if devices is not empty
    if not devices:
        raise UcsOperationError("boot_policy_order_set", "No device present.")

    boot_policy = boot_policy_get(handle=handle, name=name, org_dn=org_dn,
                                  caller="boot_policy_order_set")

    # Removes all the devices from the boot order
    _boot_policy_order_clear(handle, boot_policy)

    # Add devices and configure boot order
    _device_add(handle, boot_policy, devices)
    handle.set_mo(boot_policy)
    handle.commit()


def boot_policy_order_exists(handle, name, devices, org_dn="org-root",
                             debug=False):
    """
    checks if a given boot order exists for a given boot policy

    Args:
        handle (UcsHandle)
        name (string): boot policy name
        org_dn (string): org dn
        devices (list of dict):
         [
            {
             "device_name": device_name,
             "device_order" "1-16",
             },
            {
             "device_name": device_name,
             "device_order" "1-16",
             "property_name": "property_value",
            },
            {
             "device_name": device_name,
             "device_order" "1-16",
             "property_name": "property_value",
             "property_name": "property_value",
             "property_name": "property_value",
            },
         ]

         device_name (string): device name
          valid values are "local_lun",  "local_jbod",  "sdcard",
           "internal_usb",  "external_usb",  "embedded_lun",
           "embedded_disk",  "cd_dvd_local",  "cd_dvd_remote",
           "floppy_local",  "floppy_remote",  "virtual_drive",
           "cd_dvd_cimc",  "hdd_cimc",  "lan",  "san",  "iscsi"
         device_order (string): boot order for a device, "0-16"

         *note - mandatory keys are 'device_name' and 'device_order'
                 other key depends on the device.
        debug (bool): True/False, if True, incase of error print stacktrace

    Returns:
        (True/False, LsbootPolicy MO/None)

    Raises:
        UcsOperationError:

    Example:
        boot_policy_order_exists(handle, name="sample_boot", devices=devices)
    """
    # create the boot_policy_order_tree
    try:
        # check if devices is not empty
        if not devices:
            raise UcsOperationError(
                "boot_policy_order_exists",
                "No device present.")

        boot_policy = boot_policy_get(handle=handle, name=name, org_dn=org_dn,
                                      caller="boot_policy_order_exists")

        # Add devices and configure boot order
        _device_add(handle, boot_policy, devices)
    except Exception as err:
        return False, None

    expected_boot_policy = boot_policy

    try:
        response = handle.query_dn(dn=boot_policy.dn,
                                   hierarchy=True,
                                   need_response=True)
        existing_boot_policy = response.out_configs.child[0]
    except Exception as err:
        if debug:
            import traceback
            print(str(traceback.print_exc()))
        return False, None

    try:
        _compare_boot_policy(existing_boot_policy, expected_boot_policy)
    except Exception as err:
        return False, None

    return True, boot_policy
