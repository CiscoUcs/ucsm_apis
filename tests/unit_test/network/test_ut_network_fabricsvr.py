import pytest
from ucsm_apis.network import fabricsvr
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_fabric_svr_enable_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "fabric/server/sw-A"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_fabric_svr = mocker.patch('ucsm_apis.network.'
                                   'fabricsvr.FabricDceSwSrvEp')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    fabricsvr.fabric_svr_enable(handle, fabric="A",
                                slot_id="1", port_id="1")

    mock_query_dn.assert_called_with(handle, "fabric/server/sw-A")
    mock_fabric_svr.assert_called_with(admin_state="enabled", slot_id="1",
                                       port_id="1",
                                       parent_mo_or_dn="fabric/server/sw-A")


def test_fabric_svr_enable_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricsvr.UcsOperationError):
        fabricsvr.fabric_svr_enable(handle, fabric="A",
                                    slot_id="1", port_id="100")


def test_fabric_svr_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "fabric/server/sw-A/slot-1-port-1"

    fabricsvr.fabric_svr_get(handle, fabric="A",
                             slot_id="1", port_id="1")

    mock_query_dn.assert_called_with(handle, "fabric/server/"
                                             "sw-A/slot-1-port-1")


def test_fabric_svr_get_fail_port_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricsvr.UcsOperationError):
        fabricsvr.fabric_svr_get(handle, fabric="A",
                                 slot_id="1", port_id="100")


def test_fabric_svr_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "fabric/server/sw-A/slot-1-port-1"
    mock_check_prop = mocker.patch.object(fabricsvr.FabricDceSwSrvEp,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(fabricsvr, 'fabric_svr_get', autospec=True)

    fabricsvr.fabric_svr_exists(handle, fabric="A",
                                slot_id="1", port_id="1")

    mock_get.assert_called_with(handle=handle, caller='fabric_svr_exists',
                                fabric="A", slot_id="1", port_id="1")


def test_fabric_svr_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricsvr, 'fabric_svr_get', autospec=True)
    mock_get.side_effect = fabricsvr.UcsOperationError("query_dn",
                                                    "port does not exist")

    result = fabricsvr.fabric_svr_exists(handle, fabric="A",
                                         slot_id="1", port_id="100")

    assert result == (False, None)


def test_fabric_svr_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricsvr, 'fabric_svr_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    fabricsvr.fabric_svr_modify(handle, fabric="A",
                          slot_id="1",
                          port_id="2",
                          usr_lbl="test")

    mock_get.assert_called_with(handle=handle, fabric="A",
                                slot_id="1", port_id="2",
                                caller="fabric_svr_modify")
    mo_mock.set_prop_multiple.assert_called_with(usr_lbl="test")


def test_fabric_svr_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricsvr, 'fabric_svr_get', autospec=True)
    mock_get.side_effect = fabricsvr.UcsOperationError("query_dn",
                                                    "port does not exist")

    with pytest.raises(fabricsvr.UcsOperationError):
        fabricsvr.fabric_svr_modify(handle, fabric="A",
                                    slot_id="1", port_id="100",
                                    usr_lbl="no aqui")


def test_fabric_svr_disable_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "fabric/server/sw-A/slot-1-port-1"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.'
                               'UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_remove_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.remove_mo',
                               autospec=True)
    mock_remove_mo.return_value = None

    fabricsvr.fabric_svr_disable(handle, fabric="A",
                                slot_id="1", port_id="1")

    mock_query_dn.assert_called_with(handle, "fabric/server/"
                                             "sw-A/slot-1-port-1")
    assert mock_remove_mo.call_count == 1
    assert mock_commit.call_count == 1


def test_fabric_svr_disable_failure_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricsvr.UcsOperationError):
        fabricsvr.fabric_svr_disable(handle, fabric="A",
                                    slot_id="1", port_id="100")
