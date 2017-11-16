import pytest
from ucsm_apis.network import fabricvlan
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_vlan_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "fabric/lan"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_fabric_vlan = mocker.patch('ucsm_apis.network.'
                                    'fabricvlan.FabricVlan')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    fabricvlan.vlan_create(handle, name="test",
                           id="100")

    mock_query_dn.assert_called_with(handle, "fabric/lan")
    mock_fabric_vlan.assert_called_with(parent_mo_or_dn="fabric/lan",
                                        id="100",
                                        name="test",
                                        sharing=None)


def test_vlan_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricvlan.UcsOperationError):
        fabricvlan.vlan_create(handle, name="test",
                               id="100")


def test_vlan_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "fabric/lan/net-test"

    fabricvlan.vlan_get(handle, name="test")

    mock_query_dn.assert_called_with(handle, "fabric/lan/net-test")


def test_vlan_get_fail_vlan_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricvlan.UcsOperationError):
        fabricvlan.vlan_get(handle, name="noaqui")


def test_vlan_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "fabric/lan/net-test"
    mock_check_prop = mocker.patch.object(fabricvlan.FabricVlan,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(fabricvlan, 'vlan_get', autospec=True)

    fabricvlan.vlan_exists(handle, name="test")

    mock_get.assert_called_with(handle=handle, name="test",
                                caller='vlan_exists',
                                org_dn="fabric/lan")


def test_vlan_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricvlan, 'vlan_get', autospec=True)
    mock_get.side_effect = fabricvlan.UcsOperationError("query_dn",
                                                    "vlan does not exist")

    result = fabricvlan.vlan_exists(handle, name="no_aqui")

    assert result == (False, None)


def test_vlan_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricvlan, 'vlan_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    fabricvlan.vlan_modify(handle, name="test",
                           sharing="isolated")

    mock_get.assert_called_with(handle=handle, name="test",
                                org_dn="fabric/lan",
                                caller="vlan_modify")
    mo_mock.set_prop_multiple.assert_called_with(sharing="isolated")


def test_vlan_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(fabricvlan, 'vlan_get', autospec=True)
    mock_get.side_effect = fabricvlan.UcsOperationError("query_dn",
                                                    "vlan does not exist")

    with pytest.raises(fabricvlan.UcsOperationError):
        fabricvlan.vlan_modify(handle, name="noaqui",
                               sharing="isolated")


def test_vlan_delete_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "fabric/lan/net-test"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.'
                               'UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_remove_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.remove_mo',
                               autospec=True)
    mock_remove_mo.return_value = None

    fabricvlan.vlan_delete(handle, name="test")

    mock_query_dn.assert_called_with(handle, "fabric/lan/net-test")
    assert mock_remove_mo.call_count == 1
    assert mock_commit.call_count == 1


def test_vlan_delete_failure_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(fabricvlan.UcsOperationError):
        fabricvlan.vlan_delete(handle, name="noaqui")
