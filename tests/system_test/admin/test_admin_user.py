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
from ucsm_apis.admin.user import *

handle = None
user_name =  "test" + datetime.date.today().strftime('%Y%b%d')

def setup_module():
    global handle
    handle = custom_setup()
    # handle.set_dump_xml()


def teardown_module():
    custom_teardown(handle)


def test_user_create():
    user_create(handle, name=user_name, pwd="password")

