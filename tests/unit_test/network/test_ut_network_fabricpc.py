import pytest
from ucsm_apis.network import fabricpc
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_fabric_pc_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "fabric/lan/A"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_fabric_pc = mocker.patch('ucsm_apis.network.'
                                  'fabricpc.FabricEthLanPc')
    mock_fabric_pc_port = mocker.patch('ucsm_apis.network.'
                                       'fabricpc.FabricEthLanPcEp')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    fabricpc.fabric_pc_create(handle, fabric="A",
                              pc_id="13", ports=["1/1", "1/2"])

    mock_query_dn.assert_called_with(handle, "fabric/lan/A")
    mock_fabric_pc.assert_called_with(admin_state="enabled", name=None,
                                      parent_mo_or_dn="fabric/lan/A",
                                      port_id="13")
    assert mock_fabric_pc_port.call_count == 2


def test_fabric_pc_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricpc.UcsOperationError):
        fabricpc.fabric_pc_create(handle, fabric="A",
                                  pc_id="13")


def test_fabric_pc_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "fabric/lan/A/pc-13"

    fabricpc.fabric_pc_get(handle, fabric="A",
                           pc_id="13")

    mock_query_dn.assert_called_with(handle, "fabric/lan/A/pc-13")


def test_fabric_pc_get_fail_pc_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricpc.UcsOperationError):
        fabricpc.fabric_pc_get(handle, fabric="A",
                               pc_id="1000")


def test_fabric_pc_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "fabric/lan/A/pc-13"
    mock_check_prop = mocker.patch.object(fabricpc.FabricEthLanPc,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(fabricpc, 'fabric_pc_get', autospec=True)

    fabricpc.fabric_pc_exists(handle, fabric="A",
                              pc_id="13")

    mock_get.assert_called_with(handle=handle, caller='fabric_pc_exists',
                                fabric="A", pc_id="13")


def test_fabric_pc_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricpc, 'fabric_pc_get', autospec=True)
    mock_get.side_effect = fabricpc.UcsOperationError("query_dn",
                                                      "port channel"
                                                      "does not exist")

    result = fabricpc.fabric_pc_exists(handle, fabric="A",
                                       pc_id="1000")

    assert result == (False, None)


def test_fabric_pc_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricpc, 'fabric_pc_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    fabricpc.fabric_pc_modify(handle, fabric="A",
                              pc_id="13",
                              descr="test")

    mock_get.assert_called_with(handle=handle, fabric="A",
                                pc_id="13",
                                caller="fabric_pc_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="test")


def test_fabric_pc_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricpc, 'fabric_pc_get', autospec=True)
    mock_get.side_effect = fabricpc.UcsOperationError("query_dn",
                                                      "port channel"
                                                      "does not exist")

    with pytest.raises(fabricpc.UcsOperationError):
        fabricpc.fabric_pc_modify(handle, fabric="A",
                                  pc_id="1000",
                                  descr="no aqui")


def test_fabric_pc_delete_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "fabric/lan/A"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.'
                               'UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo', autospec=True)

    fabricpc.fabric_pc_delete(handle, fabric="A",
                              pc_id="13")

    mock_query_dn.assert_called_with(handle, "fabric/lan/A/pc-13")
    assert mock_remove_mo.call_count == 1


def test_fabric_pc_delete_failure_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricpc.UcsOperationError):
        fabricpc.fabric_pc_delete(handle, fabric="A",
                                  pc_id="1000")
