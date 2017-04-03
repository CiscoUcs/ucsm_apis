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
from ucsm_apis.admin.auth import *

handle = None
domain_name =  "test" + datetime.date.today().strftime('%Y%b%d')

def setup_module():
    global handle
    handle = custom_setup()
    # handle.set_dump_xml()


def teardown_module():
    custom_teardown(handle)

@raises(UcsOperationError)
def test_001_auth_domain_delete_domainnotexist():
    auth_domain_delete(handle, name=domain_name)


def test_002_auth_domain_exists_domainnotexist():
    (status, mo) = auth_domain_exists(handle, name=domain_name)
    assert not status


def test_003_auth_domain_create_default():
    auth_domain_create(handle, name=domain_name)


def test_004_auth_domain_exist_default():
    (status, mo) = auth_domain_exists(handle, name=domain_name)
    assert status


def test_005_auth_domain_modify_default():
    auth_domain_modify(handle, name=domain_name)


def test_006_auth_domain_modify_descr_empty():
    auth_domain_modify(handle, name=domain_name, descr="")


def test_007_auth_domain_modify_descr_default():
    auth_domain_modify(handle, name=domain_name, descr="default")


def test_008_auth_domain_realm_configure_default():
    auth_domain_realm_configure(handle, domain_name)


def test_009_auth_domain_delete_default():
    auth_domain_delete(handle, name=domain_name)


def test_010_native_auth_configure_default():
    native_auth_configure(handle)


def test_011_native_auth_default():
    native_auth_default(handle)


def test_012_native_auth_console():
    native_auth_console(handle)


