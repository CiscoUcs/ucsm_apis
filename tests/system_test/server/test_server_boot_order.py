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

import datetime
from nose.tools import *
from ..connection.info import custom_setup, custom_teardown
from ucsmsdk.ucshandle import UcsHandle
from ucsm_apis.server.boot import *

handle = None
boot_policy_name =  "test" + datetime.date.today().strftime('%Y%b%d')
boot_policy_dn = "org-root/boot-policy-" + boot_policy_name

def setup_module():
    global handle
    handle = custom_setup()
    boot_policy_create(handle, name=boot_policy_name)
    # handle.set_dump_xml()


def teardown_module():
    boot_policy_delete(handle, name=boot_policy_name)
    custom_teardown(handle)

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
    boot_policy_order_set(handle, boot_policy_dn, devices)

def test_boot_policy_order_exist():
    boot_policy_order_exists(handle, boot_policy_dn, devices, True)
