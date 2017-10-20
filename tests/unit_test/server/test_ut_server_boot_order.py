import pytest
from mock import Mock, patch
from nose.tools import assert_raises
from nose.tools import assert_equal

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy

from ucsm_apis.server import boot

handle = UcsHandle("10.10.10.10", "username", "password")
boot_policy_dn = "org-root/boot-policy-test"


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_lun_001(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # case1:
    # Add two local_lun without type
    devices = [
                {"device_name": "local_lun",
                "device_order": "1",
                },
                {"device_name": "local_lun",
                "device_order": "2",
                },
    ]

    expected_error_message = "_local_lun_add failed, error: Instance of Local Lun already added at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_lun_002(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # case2:
    # Add first local_lun without type
    # Add next local_lun with type
    devices = [
                {"device_name": "local_lun",
                 "device_order": "1",
                },
                {"device_name": "local_lun",
                 "device_order": "2",
                 "type": "primary",
                 "lun_name": "test_primary"
                },
    ]

    expected_error_message = "_local_lun_add failed, error: Instance of Local Lun already added at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_lun_003(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # case3:
    # Add first local_lun with type
    # Add next local_lun with type
    devices = [
                {"device_name": "local_lun",
                 "device_order": "1",
                 "type": "primary",
                 "lun_name": "primary"
                },
                {"device_name": "local_lun",
                 "device_order": "2",
                },
    ]

    expected_error_message = "_local_lun_add failed, error: Required parameter 'lun_name' or 'type' missing."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_lun_004(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # case4:
    # Add first local_lun with type
    # Add next local_lun with same type
    devices = [
                {"device_name": "local_lun",
                 "device_order": "1",
                 "type": "primary",
                 "lun_name": "primary"
                },
                {"device_name": "local_lun",
                 "device_order": "2",
                 "type": "primary",
                 "lun_name": "primary"
                },
    ]

    expected_error_message = "_local_lun_add failed, error: Instance of Local Lun of type 'primary' already added at  order '1'."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_lun_005(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # case5:
    # Add first local_lun with type
    # Add next local_lun with other type
    # Add one more local_lun
    devices = [
                {"device_name": "local_lun",
                 "device_order": "1",
                 "type": "primary",
                 "lun_name": "primary"
                },
                {"device_name": "local_lun",
                 "device_order": "2",
                 "type": "secondary",
                 "lun_name": "secondary"
                },
                {"device_name": "local_lun",
                 "device_order": "2",
                 "type": "secondary",
                 "lun_name": "secondary"
                },
    ]

    expected_error_message = "_local_lun_add failed, error: Both instance of Local Lun already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_jbod_001(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_jbod_case1
    # Add local_jbod
    # Add one more local_jbod
    devices = [
                {"device_name": "local_jbod",
                 "device_order": "1",
                 "slot_number": "1"
                },
                {"device_name": "local_jbod",
                 "device_order": "2",
                 "slot_number": "1"
                },
    ]

    expected_error_message = "_local_jbod_add failed, error: Instance of Local JBOD already added at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_local_jbod_002(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_jbod_case2
    # Add local_jbod without slot_number
    devices = [
                {"device_name": "local_jbod",
                 "device_order": "1",
                },
    ]

    expected_error_message = "_local_jbod_add() missing 1 required positional argument: 'slot_number'"
    with pytest.raises(TypeError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_embedded_disk_001(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_embedded_disk_case1:
    # Add two local_embedded_disk  without type
    devices = [
                {"device_name": "embedded_disk",
                "device_order": "1",
                },
                {"device_name": "embedded_disk",
                "device_order": "2",
                },
    ]

    expected_error_message = "_local_embedded_disk_add failed, error: Instance of Local Embedded Disk already added at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_embedded_disk_002(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_embedded_disk_case2:
    # Add first local_embedded_disk without type
    # Add next local_embedded_disk with type
    devices = [
                {"device_name": "embedded_disk",
                "device_order": "1",
                },
                {"device_name": "embedded_disk",
                "device_order": "2",
                 "type": "primary",
                 "slot_number": "1"
                },
    ]

    expected_error_message = "_local_embedded_disk_add failed, error: Instance of Local Embedded Disk already added at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_embedded_disk_003(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_embedded_disk_case3:
    # Add first local_embedded_disk with type
    # Add next local_embedded_disk without type
    devices = [
                {"device_name": "embedded_disk",
                "device_order": "1",
                 "type": "primary",
                 "slot_number": "1"
                },
                {"device_name": "embedded_disk",
                "device_order": "2",
                },
    ]

    expected_error_message = "_local_embedded_disk_add failed, error: Required parameter 'slot_number' or 'type' missing."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_embedded_disk_004(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_embedded_disk_case4:
    # Add first local_embedded_disk with type
    # Add next local_embedded_disk with same type
    devices = [
                {"device_name": "embedded_disk",
                "device_order": "1",
                 "type": "primary",
                 "slot_number": "1"
                },
                {"device_name": "embedded_disk",
                "device_order": "2",
                 "type": "primary",
                 "slot_number": "1"
                },
    ]

    expected_error_message = "_local_embedded_disk_add failed, error: Instance of Local Embedded Disk  of type 'primary' already added at  order '1'."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_embedded_disk_005(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # local_embedded_disk_case5:
    # Add first local_embedded_disk with type
    # Add next local_embedded_disk with other type
    # Add one more local_embedded_disk
    devices = [
                {"device_name": "embedded_disk",
                "device_order": "1",
                 "type": "primary",
                 "slot_number": "1"
                },
                {"device_name": "embedded_disk",
                "device_order": "2",
                 "type": "secondary",
                 "slot_number": "1"
                },
                {"device_name": "embedded_disk",
                "device_order": "3",
                 "type": "secondary",
                 "slot_number": "1"
                },
    ]

    expected_error_message = "_local_embedded_disk_add failed, error: Both instance of Local Embedded Disk already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_lan_001(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # lan_case1:
    # Add first lan without vnic_name and with type
    devices = [
                {"device_name": "lan",
                "device_order": "1",
                },
    ]

    expected_error_message = "_lan_device_add() missing 1 required positional argument: 'vnic_name'"
    with pytest.raises(TypeError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_lan_002(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # lan_case2:
    # Add first lan
    # Add second lan
    # Add one more lan
    devices = [
                {"device_name": "lan",
                "device_order": "1",
                 "vnic_name": "primary"
                },
                {"device_name": "lan",
                "device_order": "2",
                 "vnic_name": "secondary"
                },
                {"device_name": "lan",
                "device_order": "3",
                 "vnic_name": "secondary"
                },
    ]

    expected_error_message = "_lan_device_add failed, error: Both instances of Lan Device are already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_iscsi_001(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # iscsi_case1:
    # Add first iscsi without vnic_name and with type
    devices = [
                {"device_name": "iscsi",
                "device_order": "1",
                 "type": "primary",
                },
    ]

    expected_error_message = "_iscsi_device_add() got an unexpected keyword argument 'type'"
    with pytest.raises(TypeError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_iscsi_002(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # iscsi_case2:
    # Add first iscsi without vnic_name and type
    devices = [
                {"device_name": "iscsi",
                "device_order": "1",
                },
    ]

    expected_error_message = "_iscsi_device_add() missing 1 required positional argument: 'vnic_name'"
    with pytest.raises(TypeError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_iscsi_003(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # iscsi_case3:
    # Add first iscsi
    # Add second iscsi
    # Add one more iscsi
    devices = [
                {"device_name": "iscsi",
                "device_order": "1",
                 "vnic_name": "primary"
                },
                {"device_name": "iscsi",
                "device_order": "2",
                 "vnic_name": "secondary"
                },
                {"device_name": "iscsi",
                "device_order": "3",
                 "vnic_name": "secondary"
                },
    ]

    expected_error_message = "_iscsi_device_add failed, error: Both instances of ISCSI Device are already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_001(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # san_case1:
    # Add first san without type
    # Add second san without type
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                },
    ]


    expected_error_message = "_san_device_add failed, error: Instance of San device is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_002(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None


    # san_case4:
    # Add first san without type
    # Add second san with type
    # Add third san without type
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                },
                {"device_name": "san",
                "device_order": "3",
                },
    ]

    expected_error_message = "_san_device_add failed, error: Instance of San device is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_003(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # san_case5:
    # Add first san without type
    # Add second san with type
    # Add third san with "same" type
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                },
                {"device_name": "san",
                "device_order": "3",
                 "vnic_name": "primary",
                 "type": "primary",
                },
    ]

    expected_error_message = "_san_device_add failed, error: Instance of 'primary' san image is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_004(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None


    # san_case9:
    # Add first san without type
    # Add second san with type(with wwn, lun, target_type)
    # Add third san without type
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                 "wwn": "10:00:00:00:00:00:00:00",
                 "lun": "1",
                 "target_type": "primary"
                },
                {"device_name": "san",
                "device_order": "3",
                },
    ]

    expected_error_message = "_san_device_add failed, error: Instance of San device is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_005(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # san_case10:
    # Add first san without type
    # Add second san with type(with wwn, lun, target_type)
    # Add third san with same type
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                 "wwn": "10:00:00:00:00:00:00:00",
                 "lun": "1",
                 "target_type": "primary"
                },
                {"device_name": "san",
                "device_order": "3",
                 "vnic_name": "primary",
                 "type": "primary",
                },
    ]

    expected_error_message = "_san_device_add failed, error: Instance of 'primary' san image is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_006(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # san_case11:
    # Add first san without type
    # Add second san with type(with wwn, lun, target_type)
    # Add third san with same type(with wwn, lun, target_type(same))
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                 "wwn": "10:00:00:00:00:00:00:00",
                 "lun": "1",
                 "target_type": "primary"
                },
                {"device_name": "san",
                "device_order": "3",
                 "vnic_name": "primary",
                 "type": "primary",
                 "wwn": "10:00:00:00:00:00:00:00",
                 "lun": "1",
                 "target_type": "primary"
                },
    ]

    expected_error_message = "_san_device_add failed, error: Instance of SAN target type 'primary' is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_007(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None


    # san_case15:
    # Add first san without type
    # Add second san with type primary
    # Add third san with other type secondary
    # Add fourth san without type
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                },
                {"device_name": "san",
                "device_order": "3",
                 "vnic_name": "secondary",
                 "type": "secondary",
                },
                {"device_name": "san",
                "device_order": "4",
                },
    ]

    expected_error_message = "_san_device_add failed, error: Instance of San device is already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_008(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None


    # san_case16:
    # Add first san without type
    # Add second san with type primary
    # Add third san with other type secondary
    # Add fourth san with type primary
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                },
                {"device_name": "san",
                "device_order": "3",
                 "vnic_name": "secondary",
                 "type": "secondary",
                },
                {"device_name": "san",
                "device_order": "4",
                 "vnic_name": "primary",
                 "type": "primary",
                },
    ]

    expected_error_message = "_san_device_add failed, error: Both instance of SAN Devices are already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_san_009(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None


    # san_case17:
    # Add first san without type
    # Add second san with type primary
    # Add third san with other type secondary
    # Add fourth san with type secondary
    devices = [
                {"device_name": "san",
                "device_order": "1",
                },
                {"device_name": "san",
                "device_order": "2",
                 "vnic_name": "primary",
                 "type": "primary",
                },
                {"device_name": "san",
                "device_order": "3",
                 "vnic_name": "secondary",
                 "type": "secondary",
                },
                {"device_name": "san",
                "device_order": "4",
                 "vnic_name": "secondary",
                 "type": "secondary",
                },
    ]
    expected_error_message = "_san_device_add failed, error: Both instance of SAN Devices are already added."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message



@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_special_case_01(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # special_case1:
    # Add first local_disk
    # Add another local_device
    devices = [
                {"device_name": "local_disk",
                "device_order": "1",
                },
                {"device_name": "sdcard",
                "device_order": "2",
                },
    ]

    expected_error_message = "_device_add failed, error: local_disk cannot be added with other local devices."
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_special_case_02(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None


    # special_case2:
    # Add first cd_dvd
    # Add another cd_dvd_local
    devices = [
                {"device_name": "cd_dvd",
                "device_order": "1",
                },
                {"device_name": "cd_dvd_local",
                "device_order": "2",
                },
    ]

    expected_error_message = "_device_add failed, error: 'cd_dvd' or 'cd_dvd_local, cd_dvd_remote'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message



@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_special_case_03(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # special_case3:
    # Add first floppy
    # Add another floppy_local
    devices = [
                {"device_name": "floppy",
                "device_order": "1",
                },
                {"device_name": "floppy_local",
                "device_order": "2",
                },
    ]

    expected_error_message = "_device_add failed, error: 'floppy' or 'floppy_local, floppy_remote'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_special_case_04(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # special_case4:
    # Add sdcard
    # Add sdcard
    devices = [
                {"device_name": "sdcard",
                "device_order": "1",
                },
                {"device_name": "sdcard",
                "device_order": "2",
                },
    ]

    expected_error_message = "_local_device_add failed, error: Device 'sdcard' already exist at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message


@patch('ucsm_apis.server.boot._boot_policy_order_clear', autospec=True)
@patch.object(UcsHandle, 'query_dn', autospec=True)
@patch.object(UcsHandle, 'login', autospec=True)
def test_boot_special_case_05(mock_login, mock_query_dn, mock_order_clear):
    mock_login.return_value = True
    bp = LsbootPolicy("org-root", name="test")
    mock_query_dn.return_value = bp
    mock_order_clear.return_value = None

    # special_case4:
    # Add virtual_drive
    # Add virtual_drive
    devices = [
                {"device_name": "virtual_drive",
                "device_order": "1",
                },
                {"device_name": "virtual_drive",
                "device_order": "2",
                },
    ]

    expected_error_message = "_vmedia_device_add failed, error: Device 'virtual_drive' already exist at order '1'"
    with pytest.raises(boot.UcsOperationError) as error:
         boot.boot_policy_order_set(handle, boot_policy_dn, devices)
    assert error.value.args[0] == expected_error_message

