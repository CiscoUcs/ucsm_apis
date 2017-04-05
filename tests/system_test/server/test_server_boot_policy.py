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

def setup_module():
    global handle
    handle = custom_setup()
    # handle.set_dump_xml()


def teardown_module():
    custom_teardown(handle)

@raises(UcsOperationError)
def test_001_boot_policy_delete_bpnotexist():
    boot_policy_delete(handle, name=boot_policy_name)


def test_002_boot_policy_exist_bpnotexist():
    (status, mo) = boot_policy_exists(handle, name=boot_policy_name)
    assert not status


def test_003_boot_policy_create_default():
    boot_policy_create(handle, name=boot_policy_name)


def test_004_boot_policy_exist_default():
    (status, mo) = boot_policy_exists(handle, name=boot_policy_name)
    assert status


def test_005_boot_policy_modify_default():
    boot_policy_modify(handle, name=boot_policy_name)


def test_006_boot_policy_modify_descr_empty():
    boot_policy_modify(handle, name=boot_policy_name, descr="")


def test_007_boot_policy_modify_descr_default():
    boot_policy_modify(handle, name=boot_policy_name, descr="default")


def test_008_boot_policy_delete_default():
    boot_policy_delete(handle, name=boot_policy_name)




