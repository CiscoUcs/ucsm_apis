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
from ucsm_apis.admin.callhome import *

handle = None
user_name =  "test" + datetime.date.today().strftime('%Y%b%d')

def setup_module():
    global handle
    handle = custom_setup()
    # handle.set_dump_xml()

def teardown_module():
    custom_teardown(handle)

# testcases
# ---------
def test_001_call_home_contact_update():
    call_home_contact_update(handle)

def test_002_call_home_contact_update():
    call_home_contact_update(handle, contact="ciscoucs")

def test_003_call_home_contact_update():
    call_home_contact_update(handle,
                     phone="+911234567890",
                     email="ciscoucs@cisco.com",
                     addr="cisco",
                     )

def test_004_call_home_contact_update():
    call_home_contact_update(handle,
                             reply_to="ciscoucs@cisco.com")

def test_005_call_home_smtp_update():
    call_home_smtp_update(handle, host="1.1.1.1")

def test_call_home_enable():
    call_home_enable(handle)

def test_call_home_disable():
    call_home_disable(handle)
