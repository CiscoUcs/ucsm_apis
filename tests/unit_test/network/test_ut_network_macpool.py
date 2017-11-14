import pytest
from ucsm_apis.network import macpool
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_mac_pool_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_mac_pool = mocker.patch('ucsm_apis.network.macpool.MacpoolPool')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    macpool.mac_pool_create(handle, name="dummypool")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_mac_pool.assert_called_with(name='dummypool',
                                     assignment_order="default",
                                     descr=None,
                                     parent_mo_or_dn='org-root')


def test_mac_pool_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_pool_create(handle, name="dummypool",
                                org_dn="dummy")


def test_mac_pool_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/mac-pool-dummypool"

    macpool.mac_pool_get(handle, name="dummypool")

    mock_query_dn.assert_called_with(handle, "org-root/mac-pool-dummypool")


def test_mac_pool_get_fail_pool_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_pool_get(handle, "nopool")


def test_mac_pool_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/mac-pool-dummypool"
    mock_check_prop = mocker.patch.object(macpool.MacpoolPool,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_pool_get', autospec=True)

    macpool.mac_pool_exists(handle, name="dummypool")

    mock_get.assert_called_with(handle=handle, caller='mac_pool_exists',
                                name="dummypool", org_dn="org-root")


def test_mac_pool_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_pool_get', autospec=True)
    mock_get.side_effect = macpool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    result = macpool.mac_pool_exists(handle, name="dummypool")

    assert result == (False, None)


def test_mac_pool_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_pool_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    macpool.mac_pool_modify(handle, name="dummypool",
                            descr="This is a new pool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="mac_pool_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new pool")


def test_mac_pool_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_pool_get', autospec=True)
    mock_get.side_effect = macpool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_pool_modify(handle, name="nopool", descr="Pool no aqui")


def test_mac_pool_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_pool_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    macpool.mac_pool_delete(handle, "dummypool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="mac_pool_delete")
    assert mock_remove_mo.call_count == 1


def test_mac_pool_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_pool_get', autospec=True)
    mock_get.side_effect = macpool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_pool_delete(handle, "dummypool")


def test_mac_block_create_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/mac-pool-dummypool"
    mock_mac_pool_block = mocker.patch.object(macpool, 'MacpoolBlock',
                                             autospec=True)
    mock_add_mo = mocker.patch.object(UcsHandle, 'add_mo', autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)

    macpool.mac_block_create(handle, pool_name="dummypool",
                             start_mac="00:25:B5:00:0A:00",
                             end_mac="00:25:B5:00:0A:3F")

    assert mock_query_dn.call_count == 2
    mock_mac_pool_block.assert_called_with(parent_mo_or_dn="org-root/"
                                           "mac-pool-dummypool",
                                           r_from="00:25:B5:00:0A:00",
                                           to="00:25:B5:00:0A:3F")
    mock_add_mo.assert_called()
    mock_commit.assert_called()


def test_mac_block_create_fail_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_block_create(handle, pool_name="dummypool",
                                 start_mac="00:25:B5:00:0A:00",
                                 end_mac="00:25:B5:00:0A:3F")


def test_mac_block_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)

    macpool.mac_block_get(handle, pool_name="dummypool",
                          start_mac="00:25:B5:00:0A:00",
                          end_mac="00:25:B5:00:0A:3F")

    mock_query_dn.assert_called_with(handle,
                                     "org-root/"
                                     "mac-pool-dummypool/"
                                     "block-00:25:B5:00:0A"
                                     ":00-00:25:B5:00:0A:3F")


def test_mac_block_get_fail_block_non_existent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_block_get(handle, pool_name="dummypool",
                              start_mac="00:25:B5:00:0A:00",
                              end_mac="00:25:B5:00:0A:3F")


def test_mac_block_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = "org-root/mac-pool-dummypool"
    managed_object_mock = mocker.Mock()
    managed_object_mock.check_prop_match.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_block_get', autospec=True)
    mock_get.return_value = managed_object_mock

    result = macpool.mac_block_exists(handle, pool_name="dummypool",
                                      start_mac="00:25:B5:00:0A:00",
                                      end_mac="00:25:B5:00:0A:3F")

    mock_get.assert_called_with(handle=handle, caller='mac_block_exists',
                                pool_name="dummypool", org_dn="org-root",
                                start_mac="00:25:B5:00:0A:00",
                                end_mac="00:25:B5:00:0A:3F")
    managed_object_mock.check_prop_match.assert_called()
    assert result == (True, managed_object_mock)


def test_mac_block_exists_fail(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_block_get', autospec=True)
    mock_get.side_effect = macpool.UcsOperationError("query_dn",
                                                    "block does not exist")

    result = macpool.mac_block_exists(handle, pool_name="dummypool",
                                      start_mac="00:25:B5:00:0A:00",
                                      end_mac="00:25:B5:00:0A:3F")

    assert result == (False, None)


def test_mac_block_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_block_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    macpool.mac_block_modify(handle,
                             pool_name="dummypool",
                             org_dn="org-root",
                             start_mac="00:25:B5:00:0A:00",
                             end_mac="00:25:B5:00:0A:3F",
                             status="modified")

    mock_get.assert_called_with(handle=handle, pool_name="dummypool",
                                org_dn="org-root",
                                caller="mac_block_modify",
                                start_mac="00:25:B5:00:0A:00",
                                end_mac="00:25:B5:00:0A:3F")
    mo_mock.set_prop_multiple.assert_called_with(status="modified")


def test_mac_block_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_block_get', autospec=True)
    mock_get.side_effect = macpool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_block_modify(handle,
                             pool_name="nopool",
                             org_dn="org-root",
                             start_mac="00:25:B5:00:0A:00",
                             end_mac="00:25:B5:00:0A:3F",
                             status="modified")


def test_mac_block_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_block_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo', autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    macpool.mac_block_delete(handle, pool_name="dummypool",
                             start_mac="00:25:B5:00:0A:00",
                             end_mac="00:25:B5:00:0A:3F")

    mock_get.assert_called_with(handle=handle, pool_name="dummypool",
                                org_dn="org-root",
                                start_mac="00:25:B5:00:0A:00",
                                end_mac="00:25:B5:00:0A:3F",
                                caller="mac_block_delete")
    assert mock_remove_mo.call_count == 1


def test_mac_blcok_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(macpool, 'mac_block_get', autospec=True)
    mock_get.side_effect = macpool.UcsOperationError("query_dn",
                                                    "block does not exist")

    with pytest.raises(macpool.UcsOperationError):
        macpool.mac_block_delete(handle, pool_name="dummypool",
                                 start_mac="00:25:B5:00:0A:00",
                                 end_mac="00:25:B5:00:0A:00")
