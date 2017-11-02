import pytest
from ucsm_apis.equipment import equip_chassis
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_chassis_ack_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "sys"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_chassis = mocker.patch('ucsm_apis.equipment.'
                                'equip_chassis.EquipmentChassis')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    equip_chassis.chassis_ack(handle, id="1")

    mock_query_dn.assert_called_with(handle, "sys")
    mock_chassis.assert_called_with(admin_state="acknowledged", id="1",
                                    parent_mo_or_dn="sys")


def test_chassis_ack_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(equip_chassis.UcsOperationError):
        equip_chassis.chassis_ack(handle, id="1")


def test_chassis_reack_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "sys"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_chassis = mocker.patch('ucsm_apis.equipment.'
                                'equip_chassis.EquipmentChassis')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    equip_chassis.chassis_reack(handle, id="1")

    mock_query_dn.assert_called_with(handle, "sys")
    mock_chassis.assert_called_with(admin_state="re-acknowledged", id="1",
                                    parent_mo_or_dn="sys")


def test_chassis_reack_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(equip_chassis.UcsOperationError):
        equip_chassis.chassis_reack(handle, id="1")


def test_chassis_decomm_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "sys"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_chassis = mocker.patch('ucsm_apis.equipment.'
                                'equip_chassis.EquipmentChassis')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    equip_chassis.chassis_decomm(handle, id="1")

    mock_query_dn.assert_called_with(handle, "sys")
    mock_chassis.assert_called_with(admin_state="decommission", id="1",
                                    parent_mo_or_dn="sys")


def test_chassis_decomm_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(equip_chassis.UcsOperationError):
        equip_chassis.chassis_decomm(handle, id="1")


def test_chassis_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "sys/chassis-1"

    equip_chassis.chassis_get(handle, id="1")

    mock_query_dn.assert_called_with(handle, "sys/chassis-1")


def test_chassis_get_fail_chassis_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(equip_chassis.UcsOperationError):
        equip_chassis.chassis_get(handle, id="100")


def test_chassis_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "sys/chassis-1"
    mock_check_prop = mocker.patch.object(equip_chassis.EquipmentChassis,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(equip_chassis, 'chassis_get', autospec=True)

    equip_chassis.chassis_exists(handle, id="1")

    mock_get.assert_called_with(handle=handle, caller='chassis_exists',
                                id="1")


def test_chassis_exists_fail_chassis_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(equip_chassis, 'chassis_get', autospec=True)
    mock_get.side_effect = equip_chassis.UcsOperationError("query_dn",
                                                           "chassis does"
                                                           "not exist")

    result = equip_chassis.chassis_exists(handle, id="1")

    assert result == (False, None)


def test_chassis_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(equip_chassis, 'chassis_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    equip_chassis.chassis_modify(handle, id="1",
                                 usr_lbl="test")

    mock_get.assert_called_with(handle=handle, id="1",
                                caller="chassis_modify")
    mo_mock.set_prop_multiple.assert_called_with(usr_lbl="test")


def test_chassis_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(equip_chassis, 'chassis_get', autospec=True)
    mock_get.side_effect = equip_chassis.UcsOperationError("query_dn",
                                                           "chassis does"
                                                           "not exist")

    with pytest.raises(equip_chassis.UcsOperationError):
        equip_chassis.chassis_modify(handle, id="1",
                                     usr_lbl="no aqui")


def test_chassis_remove_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "sys"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_chassis = mocker.patch('ucsm_apis.equipment.'
                                'equip_chassis.EquipmentChassis')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    equip_chassis.chassis_remove(handle, id="1")

    mock_query_dn.assert_called_with(handle, "sys")
    mock_chassis.assert_called_with(admin_state="remove", id="1",
                                    parent_mo_or_dn="sys")


def test_chassis_remove_failure_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(equip_chassis.UcsOperationError):
        equip_chassis.chassis_remove(handle, id="1")
