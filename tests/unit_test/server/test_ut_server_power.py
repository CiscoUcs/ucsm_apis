import pytest
from mock import Mock, patch
from nose.tools import assert_raises
from nose.tools import assert_equal
from ucsmsdk.ucshandle import UcsHandle

from ucsm_apis.server import power

handle = UcsHandle("1.1.1.1", "admin", "dummy")


@patch.object(UcsHandle, 'login', autospec=True)
def test_power_on_all_None(mock_login):
    mock_login.return_value = True

    expected_error_message = "server_admin_state_set: Failed to set power "\
        "state failed, error: Missing mandatory arguments. Specify either "\
        "of (chassis_id, blade_id) or rack_id"
    with pytest.raises(power.UcsOperationError) as error:
        power.server_power_on(handle)
    assert error.value.args[0] == expected_error_message


@patch.object(UcsHandle, 'login', autospec=True)
def test_power_on_chassis1_bladeNone(mock_login):
    mock_login.return_value = True

    expected_error_message = "server_admin_state_set: Failed to set power "\
        "state failed, error: Missing mandatory arguments. Specify either "\
        "of (chassis_id, blade_id) or rack_id"
    with pytest.raises(power.UcsOperationError) as error:
        power.server_power_on(handle, chassis_id=1)
    assert error.value.args[0] == expected_error_message


@patch.object(UcsHandle, 'login', autospec=True)
def test_power_on_chassisNone_blade1(mock_login):
    mock_login.return_value = True

    expected_error_message = "server_admin_state_set: Failed to set power "\
        "state failed, error: Missing mandatory arguments. Specify either "\
        "of (chassis_id, blade_id) or rack_id"
    with pytest.raises(power.UcsOperationError) as error:
        power.server_power_on(handle, blade_id=1)
    assert error.value.args[0] == expected_error_message


@patch.object(UcsHandle, 'query_dn')
@patch.object(UcsHandle, 'login', autospec=True)
def test_power_on_chassis1_blade1_notexist(mock_login, mock_query_dn):
    mock_login.return_value = True
    mock_query_dn.return_value = None

    expected_error_message = "server_power_set: Failed to set server power "\
        "failed, error: server sys/chassis-1/blade-1 does not exist"
    with pytest.raises(power.UcsOperationError) as error:
        power.server_power_on(handle, chassis_id=1, blade_id=1)
    assert error.value.args[0] == expected_error_message


@patch.object(UcsHandle, 'query_dn')
@patch.object(UcsHandle, 'login', autospec=True)
def test_power_on_chassis1_blade1_not_assigned_to_dn(
        mock_login, mock_query_dn):
    mock_login.return_value = True

    server_mo = Mock()
    server_mo.assigned_to_dn = None

    mock_query_dn.return_value = server_mo

    expected_error_message = "server_power_set: Failed to set server power "\
        "failed, error: server sys/chassis-1/blade-1 is not associated to a "\
        "service profile"
    with pytest.raises(power.UcsOperationError) as error:
        power.server_power_on(handle, chassis_id=1, blade_id=1)
    assert error.value.args[0] == expected_error_message


@patch.object(UcsHandle, 'commit')
@patch.object(UcsHandle, 'query_dn')
@patch.object(UcsHandle, 'login', autospec=True)
def test_power_on_chassis1_blade1_pass(mock_login, mock_query_dn, mock_commit):
    from ucsmsdk.mometa.compute.ComputeBlade import ComputeBlade
    from ucsmsdk.mometa.ls.LsServer import LsServer

    mock_login.return_value = True

    server_mo = Mock()
    server_mo.assigned_to_dn = "org-root/ls-testsp"

    sp_mo = LsServer("org-root", name="testsp")

    mock_query_dn.side_effect = [server_mo, sp_mo]
    mock_commit.return_value = None

    assert power.server_power_on(handle, chassis_id=1, blade_id=1) is None
