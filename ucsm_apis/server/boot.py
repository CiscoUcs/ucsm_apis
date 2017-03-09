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

from ucsmsdk import ucsgenutils
from ucsmsdk.ucsexception import UcsOperationError
from ucsmsdk.ucscoreutils import load_class


def boot_policy_get(handle, name, org_dn="org-root", caller="boot_policy_get"):
    """
    This method fetches boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        org_dn (string): Org DN.
        caller (string): Name of the caller method.

    Returns:
        LsbootPolicy: Managed Object

    Raises:
        UcsOperationError

    Example:
_       boot_policy_get(handle,
                        name="sample_boot",
                        parent_dn="org-root/org-finance",
                        caller="boot_policy_modify")
    """

    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcscOperationError(caller, "BootPolicy '%s' does not exist" % dn)
    return mo


def boot_policy_create(handle, name, org_dn="org-root",
                       reboot_on_update=False, enforce_vnic_name=True,
                       boot_mode="legacy", policy_owner="local",
                       descr=None, **kwargs):
    """
    This method creates boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        org_dn (string): Org DN.
        reboot_on_update (bool): True/False. Default False.
        enforce_vnic_name (bool): True/False. Default True.
        boot_mode (string): "legacy" or "uefi"
        policy_owner (string): "local" or "pending-policy" or  "policy"
        descr (string): Basic description.

    Returns:
        LsbootPolicy: Managed Object

    Raises:
        UcsOperationError

    Example:
        boot_policy_create(handle,
                           name="sample_boot",
                           org_dn="org-root/org-finance",
                           reboot_on_update=True,
                           enforce_vnic_name=True,
                           boot_mode="legacy",
                           descr="sample description")

    """

    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

    obj = handle.query_dn(org_dn)
    if not obj:
        raise UcscOperationError("boot_policy_create", "Org '%s' does not \
                                 exist" % parent_dn)

    reboot_on_update = ("no", "yes")[reboot_on_update]
    enforce_vnic_name = ("no", "yes")[enforce_vnic_name]
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


def boot_policy_modify(handle, name, org_dn="org-root", **kwargs):
    """
    This method modifies boot policy.

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        org_dn (string): Org Dn.

    Returns:
        LsbootPolicy: Managed Object

    Raises:
        UcsOperationError

    Example:
        boot_policy_modify(handle, name="sample_boot",
                           org_dn="org-root/org-test",
                           reboot_on_update=True,
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
    This method removes boot policy.

    Args:
        handle (UcsHandle)
        org_name (string): Name of the organization
        name (string): Name of the boot policy.
        org_dn (string): Org Dn.

    Returns:
        None

    Raises:
        UcsOperationError

    Example:
        boot_policy_remove(handle, name="sample_boot",
                           org_dn="org-root/org-test")
    """

    mo = boot_policy_get(handle=handle, name=name, org_dn=org_dn,
                         caller="boot_policy_remove")
    handle.remove_mo(mo)
    handle.commit()


def boot_policy_exist(handle, name, org_dn="org-root", **kwargs):
    """
    checks if boot policy exist

    Args:
        handle (UcsHandle)
        name (string): Name of the boot policy.
        org_dn (string): Org DN.

    Returns:
        True/False: Boolean

    Example:
        boot_policy_exist(handle, name="sample_boot",
                          org_dn="org-root/org-finance")
    """

    try:
        mo = boot_policy_mo_get(handle=handle,
                                name=name,
                                org_dn=org_dn)
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


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
            order)
    if mo and mo[0].child:
        child_count = len(mo[0].child)
        if child_count >= 2:
            raise UcsOperationError(
    "_local_lun_add",
     "Both instance of Local Lun already added.")
        if mo[0].child[0].type == type:
            raise UcsOperationError("_local_lun_add",
                                    "Instance of Local Lun of type '%s' already added at  order '%s'." % (type, mo[0].order))

        if not lun_name or not type:
            raise UcsOperationError(
                "_local_lun_add",
                "Required parameter 'lun_name' or 'type' missing.")

        LsbootLocalLunImagePath(parent_mo_or_dn=mo[0], lun_name=lun_name,
                                type=type)
        return

    mo = LsbootLocalHddImage(parent_mo_or_dn=parent_mo, order=order)
    if not lun_name and not type:
        return
    if (lun_name and not type) or (not lun_name and type):
        raise UcsOperationError(
            "_local_lun_add",
            "Required parameter 'lun_name' or 'type' missing.")
    LsbootLocalLunImagePath(parent_mo_or_dn=mo,
                            lun_name=lun_name,
                            type=type)


def _local_jbod_add(parent_mo, order, slot_number):
    from ucsmsdk.mometa.lsboot.LsbootLocalDiskImage import LsbootLocalDiskImage
    from ucsmsdk.mometa.lsboot.LsbootLocalDiskImagePath import LsbootLocalDiskImagePath

    mo = [mo for mo in parent_mo.child
          if mo.get_class_id() == "LsbootLocalDiskImage"]
    if mo:
        raise UcsOperationError(
    "_local_jbod_add",
    "Instance of Local JBOD already added at order '%s'" %
     mo[0].order)

    if not slot_number:
        raise UcsOperationError("_local_jbod_add",
     "Required Parameter 'slot_number' missing")

    mo = LsbootLocalDiskImage(parent_mo_or_dn=parent_mo, order=order)
    LsbootLocalDiskImagePath(
    parent_mo_or_dn=mo,
    type="primary",
     slot_number=slot_number)


def _local_embedded_disk_add(parent_mo, order, slot_number=None, type=None):
    from ucsmsdk.mometa.lsboot.LsbootEmbeddedLocalDiskImage import LsbootEmbeddedLocalDiskImage
    from ucsmsdk.mometa.lsboot.LsbootEmbeddedLocalDiskImagePath import LsbootEmbeddedLocalDiskImagePath

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


def _san_device_add(parent_mo, order,
                    vnic_name=None, type=None,
                    wwn=None, lun=None, target_type=None):
    from ucsmsdk.mometa.lsboot.LsbootSan import LsbootSan
    from ucsmsdk.mometa.lsboot.LsbootSanCatSanImage import \
        LsbootSanCatSanImage
    from ucsmsdk.mometa.lsboot.LsbootSanCatSanImagePath import \
        LsbootSanCatSanImagePath

    mo = [mo for mo in parent_mo.child if mo.get_class_id() == "LsbootSan"]
    if mo and not mo[0].child:
        if not (vnic_name and type):
            raise UcsOperationError("_san_device_add",
                                    "Instance of San device already added")
        san_image_exist = False
        if vnic_name or type:
            if not (vnic_name and type):
                raise UcsOperationError("Required Parameter 'vnic_name' or "
                                        "'type' missing.")
            san_image = LsbootSanCatSanImage(parent_mo_or_dn=mo[0],
                                             vnic_name=vnic_name,
                                             type=type)

            if wwn or lun or target_type:
                if not (wwn and lun and target_type):
                    raise UcsOperationError("Required Parameter 'wwn' or "
                                            "'lun' or 'target_type' missing.")
                LsbootSanCatSanImagePath(parent_mo_or_dn=san_image,
                                         wwn=wwn, type=target_type, lun=lun)
            return

    elif mo and mo[0].child:
        child_count = len(mo[0].child)
        if child_count >= 2:
            raise UcsOperationError("_san_device_add",
                                    "Both instance of SAN Devices are "
                                    "already added.")

        if mo[0].child[0].type == type:
            sub_child = mo[0].child[0].child
            if sub_child:
                sub_child_count = len(sub_child)
                if sub_child_count >= 2:
                    raise UcsOperationError(
    "_san_device_add",
     "Both instance of SAN target devices are already added.")

                if sub_child[0].type == target_type:
                    raise UcsOperationError(
    "_san_device_add",
    "Instance of SAN target type '%s' is already added." %
     target_type)

                LsbootSanCatSanImagePath(parent_mo_or_dn=mo[0].child[0],
                                         wwn=wwn, type=target_type, lun=lun)
                return

            if wwn or lun or target_type:
                if not (wwn and lun and target_type):
                    raise UcsOperationError("Required Parameter 'wwn' or "
                                            "'lun' or 'target_type' missing.")
                LsbootSanCatSanImagePath(parent_mo_or_dn=mo[0].child[0],
                                         wwn=wwn, type=target_type, lun=lun)
                return
            else:
                raise UcsOperationError("_san_device_add",
                                    "Instance of San of type '%s' already "
                                    "added at order '%s'." % (type, mo[0].order))

        if not vnic_name or not type:
            raise UcsOperationError("_san_device_add",
                                    "Required parameter 'vnic_name' or "
                                    "'type' missing.")

        san_image = LsbootSanCatSanImage(parent_mo_or_dn=mo[0],
                                         vnic_name=vnic_name,
                                         type=type)
        if wwn or lun:
            if not (wwn and lun):
                raise UcsOperationError("Required Parameter 'wwn' or "
                                        "'lun' missing.")
            LsbootSanCatSanImagePath(parent_mo_or_dn=san_image,
                                     wwn=wwn, type=type, lun=lun)
        return

    mo = LsbootSan(parent_mo_or_dn=parent_mo, order=order)
    san_image_exist = False
    if vnic_name or type:
        if not (vnic_name and type):
            raise UcsOperationError("Required Parameter 'vnic_name' or "
                                    "'type' missing.")

        san_image = LsbootSanCatSanImage(parent_mo_or_dn=mo,
                                         vnic_name=vnic_name,
                                         type=type)
        san_image_exist = True

    if not san_image_exist:
        return

    if wwn or lun:
        if not (wwn and lun):
            raise UcsOperationError("Required Parameter 'wwn' or "
                                    "'lun' missing.")
    LsbootSanCatSanImagePath(parent_mo_or_dn=parent_mo,
                             wwn=wwn, type=type, lun=lun)


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


_class_details = {
    "LsbootDefaultLocalImage": {
        "props": None,
        "sub_child": None
    },
    "LsbootLocalHddImage": {
        "props": None,
        "sub_child": "LsbootLocalLunImagePath",
        "sub_child_props": ["lun_name", "type"],
        "is_sub_child_needed": False
    },
    "LsbootLocalLunImagePath": {
        "props": {
            "lun_name": {"mandatory": True, "Default": None},
            "type": {"mandatory": True, "Default": "primary",
                     "valid_set": ["primary", "secondary"]}
        },
        "sub_child": None
    }

}

_local_devices = {
    "local_disk": ["LsbootDefaultLocalImage", None],
    "local_lun": ["LsbootLocalHddImage", _local_lun_add],
    "local_jbod": ["LsbootLocalDiskImage", _local_jbod_add],
    "sdcard": ["LsbootUsbFlashStorageImage", None],
    "internal_usb": ["LsbootUsbInternalImage", None],
    "external_usb": ["LsbootUsbExternalImage", None],
    "embedded_lun": ["LsbootEmbeddedLocalLunImage", None],
    "embedded_disk": ["LsbootEmbeddedLocalDiskImage", _local_embedded_disk_add],
}

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


def _local_device_add(parent_mo, device_name, device_order, **kwargs):

    explicit_method = _local_devices[device_name][1]
    if explicit_method is not None:
        explicit_method(parent_mo=parent_mo,
                        order=device_order,
                        **kwargs)
        return

    class_id = _local_devices[device_name][0]
    # class_info = _class_details(class_id)
    # class_props = class_info['props']
    # if class_props:
    #    for prop in class_props:
    #        if prop not in kwargs:
    #            raise UcsOperationError("TO Be added",
    #                                "Required Property '%s' missing." % prop)
    # if class_info("sub_child_props") and is class_info("")

    class_struct = load_class(class_id)
    class_obj = class_struct(parent_mo_or_dn=parent_mo, order=device_order,
                             **kwargs)


def _vmedia_device_add(parent_mo, device_name, device_order, **kwargs):
    class_id = "LsbootVirtualMedia"
    class_struct = load_class(class_id)
    class_obj = class_struct(parent_mo_or_dn=parent_mo,
                             access=_vmedia_devices[device_name],
                             order=device_order, **kwargs)


def _efi_shell_device_add():
    pass


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
        device_props = {key: value for key, value in device.iteritems()
                        if key not in ["device_name", "device_order"]}
        print "device_props:", device_props
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
            _efi_shell_device_add()
        else:
            raise UcsOpeartionError("_device_add", " Invalid Device <%s>" % device_name)


def _boot_policy_order_clear(handle, boot_policy):

    mo_list = handle.query_children(in_mo=boot_policy)
    if mo_list is None:
        return
    for mo in mo_list:
        handle.remove_mo(mo)

    if boot_policy.reboot_on_update in ucsgenutils.AFFIRMATIVE_LIST:
        boot_policy.reboot_on_update = False
        handle.set_mo(boot_policy)
        handle.commit()
        boot_policy.reboot_on_update = True
        handle.set_mo(boot_policy)
    handle.commit()


def boot_policy_order_set(handle, boot_policy_dn, devices):
    # check if devices is not empty
    if not devices:
        raise UcsOperationError("boot_policy_order_set", "No device present.")

    boot_policy = handle.query_dn(boot_policy_dn)
    if not boot_policy:
        raise UcsOpeationError("boot_policy_order_set", "BootPollicy '%s' does not exist." % boot_policy_dn)

    # Removes all the devices from the boot order
    _boot_policy_order_clear(handle, boot_policy)

    # Add devices and configure boot order
    _device_add(handle, boot_policy, devices)
    handle.set_mo(boot_policy)
    handle.commit()


# def _local_device_mo_to_dict(mo_list):
#     mo_dict = {}
#     for mo in mo_list:
#         mo_dict[mo.get_class_id()] = mo
#     return mo_dict
#
#
# def _vmedia_device_mo_to_dict(mo_list):
#     mo_dict = {}
#     for mo in mo_list:
#         mo_dict[mo.access] = mo
#     return mo_dict
#
#
# def _device_dict_prepare(mo):
#
#     local_devices_mo = None
#     vmedia_devices_mo = None
#     lan_mo = None
#     san_mo = None
#     iscsi_mo = None
#     efi_mo = None
#     device_mo_dict = {}
#     for mo in mo.child:
#         class_id = mo.get_class_id()
#         if class_id == "LsbootStorage":
#             local_devices_mo = mo.child[0].child
#             device_mo_dict.update(_local_device_mo_to_dict(local_devices_mo))
#         elif class_id == "LsbootVirtualMedia":
#             vmedia_devices_mo = mo.child
#             device_mo_dict.update(_local_device_mo_to_dict(_vmedia_devices_mo))
#         elif class_id == "LsbootLan":
#             device_mo_dict["lan"] = mo
#         elif class_id == "LsbootSan":
#             device_mo_dict["san"] = mo
#         elif class_id == "LsbootIScsi":
#             device_mo_dict["iscsi"] = mo
#         else:
#             print ("Unknown_device %s" % class_id)
#
#     return device_mo_dict
#
#
# def _device_dict_compare(exist_mo, expected_mo):
#     pass
#
#
# def boot_policy_order_exist(handle, boot_policy, devices):
#     response = handle.query_dn(dn=boot_policy.dn, hierarchy=True,
#                                need_response=True)
#     mo = response.out_configs.child[0]
#     if not mo:
#         return False
#
#     ucsm_state = device_dict_prepare(mo)
#
#     _device_add(handle, boot_policy, devices)
#     expected_state = device_dict_prepare(boot_policy)
#
#     for key in ucsm_state:
#         if key not in expected_state:
#             return False
