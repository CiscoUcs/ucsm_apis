import pytest
from ucsm_apis.server import serverpool
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_server_pool_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_server_pool = mocker.patch('ucsm_apis.server.serverpool.ComputePool')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    serverpool.server_pool_create(handle, name="dummypool")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_server_pool.assert_called_with(name='dummypool',
                                        descr=None,
                                        parent_mo_or_dn='org-root')


def test_server_pool_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(serverpool.UcsOperationError):
        serverpool.server_pool_create(handle, name="dummypool",
                                      org_dn="dummy")


def test_server_pool_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/compute-pool-dummypool"

    serverpool.server_pool_get(handle, name="dummypool")

    mock_query_dn.assert_called_with(handle, "org-root/compute-pool-dummypool")


def test_server_pool_get_fail_pool_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(serverpool.UcsOperationError):
        serverpool.server_pool_get(handle, name="nopool")


def test_server_pool_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/compute-pool-dummypool"
    mock_check_prop = mocker.patch.object(serverpool.ComputePool,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)

    serverpool.server_pool_exists(handle, name="dummypool")

    mock_get.assert_called_with(handle=handle, caller='server_pool_exists',
                                name="dummypool", org_dn="org-root")


def test_server_pool_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mock_get.side_effect = serverpool.UcsOperationError("query_dn",
                                                      "pool does not exist")

    result = serverpool.server_pool_exists(handle, name="dummypool")

    assert result == (False, None)


def test_server_pool_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    serverpool.server_pool_modify(handle, name="dummypool",
                                  descr="This is a new pool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="server_pool_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new pool")


def test_server_pool_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mock_get.side_effect = serverpool.UcsOperationError("query_dn",
                                                      "pool does not exist")

    with pytest.raises(serverpool.UcsOperationError):
        serverpool.server_pool_modify(handle, name="nopool",
                                      descr="Pool no aqui")


def test_server_pool_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    serverpool.server_pool_delete(handle, "dummypool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="server_pool_delete")
    assert mock_remove_mo.call_count == 1


def test_server_pool_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mock_get.side_effect = serverpool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(serverpool.UcsOperationError):
        serverpool.server_pool_delete(handle, name="dummypool")


def test_server_add_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_computepool_slot = mocker.patch('ucsm_apis.server.'
                                         'serverpool.ComputePooledSlot')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    serverpool.server_add(handle, pool_name="dummypool",
                          servers=["1/1", "1/2"])

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="server_add")
    assert mo_mock.set_prop_multiple.call_count == 1
    assert mock_computepool_slot.call_count == 2


def test_server_add_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(serverpool, 'server_pool_get',
                                   autospec=True)
    mock_get.side_effect = serverpool.UcsOperationError("query_dn",
                                                    "pool does not exist")
    with pytest.raises(serverpool.UcsOperationError):
        serverpool.server_add(handle, pool_name="dummypool",
                              servers=["1/1", "1/2"])


def test_server_delete_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root/compute-pool-test_pool/blade-1-1"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.'
                               'UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo', autospec=True)

    serverpool.server_delete(handle, pool_name="test_pool",
                             servers=["1/1", "1/2"])

    assert mock_query_dn.call_count == 2
    assert mock_remove_mo.call_count == 2
    assert mock_commit.call_count == 2


def test_server_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(serverpool.UcsOperationError):
        serverpool.server_delete(handle, pool_name="no_aqui",
                                 servers=["1/1", "1/2"])
