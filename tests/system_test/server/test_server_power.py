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
from ucsm_apis.server.power import *

handle = None

def setup_module():
    global handle
    handle = custom_setup()
    # handle.set_dump_xml()


def teardown_module():
    custom_teardown(handle)

def test_001_server_power_on_rack():
    server_power_on(handle, rack_id="1")

def test_002_server_power_off_rack():
    server_power_off(handle, rack_id="1")

def test_003_server_power_cycle_immediate():
    server_power_cycle_immediate(handle, rack_id="1")

def test_004_server_power_cycle_wait():
    server_power_cycle_wait(handle, rack_id="1")
