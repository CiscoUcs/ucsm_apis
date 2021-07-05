import pytest
from ucsm_apis.server import uuidpool
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_uuid_pool_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_uuid_pool = mocker.patch('ucsm_apis.server.uuidpool.UuidpoolPool')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    uuidpool.uuid_pool_create(handle, name="dummypool")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_uuid_pool.assert_called_with(name='dummypool',
                                      assignment_order="default",
                                      descr=None,
                                      parent_mo_or_dn='org-root')


def test_uuid_pool_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_pool_create(handle, name="dummypool",
                                  org_dn="dummy")


def test_uuid_pool_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/uuid-pool-dummypool"

    uuidpool.uuid_pool_get(handle, name="dummypool")

    mock_query_dn.assert_called_with(handle, "org-root/uuid-pool-dummypool")


def test_uuid_pool_get_fail_pool_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_pool_get(handle, "nopool")


def test_uuid_pool_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/uuid-pool-dummypool"
    mock_check_prop = mocker.patch.object(uuidpool.UuidpoolPool,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_pool_get', autospec=True)

    uuidpool.uuid_pool_exists(handle, name="dummypool")

    mock_get.assert_called_with(handle=handle, caller='uuid_pool_exists',
                                name="dummypool", org_dn="org-root")


def test_uuid_pool_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_pool_get', autospec=True)
    mock_get.side_effect = uuidpool.UcsOperationError("query_dn",
                                                      "pool does not exist")

    result = uuidpool.uuid_pool_exists(handle, name="dummypool")

    assert result == (False, None)


def test_uuid_pool_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_pool_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    uuidpool.uuid_pool_modify(handle, name="dummypool",
                              descr="This is a new pool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="uuid_pool_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new pool")


def test_uuid_pool_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_pool_get', autospec=True)
    mock_get.side_effect = uuidpool.UcsOperationError("query_dn",
                                                      "pool does not exist")

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_pool_modify(handle, name="nopool", descr="Pool no aqui")


def test_uuid_pool_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_pool_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    uuidpool.uuid_pool_delete(handle, "dummypool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="uuid_pool_delete")
    assert mock_remove_mo.call_count == 1


def test_uuid_pool_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_pool_get', autospec=True)
    mock_get.side_effect = uuidpool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_pool_delete(handle, name="dummypool")


def test_uuid_block_create_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/uuid-pool-dummypool"
    mock_uuid_pool_block = mocker.patch.object(uuidpool, 'UuidpoolBlock',
                                             autospec=True)
    mock_add_mo = mocker.patch.object(UcsHandle, 'add_mo', autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)

    uuidpool.uuid_block_create(handle, pool_name="dummypool",
                               start_uuid="0000-000000000001",
                               end_uuid="0000-000000000040")

    assert mock_query_dn.call_count == 2
    mock_uuid_pool_block.assert_called_with(parent_mo_or_dn="org-root/"
                                            "uuid-pool-dummypool",
                                            r_from="0000-000000000001",
                                            to="0000-000000000040")
    mock_add_mo.assert_called()
    mock_commit.assert_called()


def test_uuid_block_create_fail_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_block_create(handle, pool_name="dummypool",
                                   start_uuid="0000-000000000001",
                                   end_uuid="0000-000000000040")


def test_uuid_block_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)

    uuidpool.uuid_block_get(handle, pool_name="dummypool",
                            start_uuid="0000-000000000001",
                            end_uuid="0000-000000000040")

    mock_query_dn.assert_called_with(handle,
                                     "org-root/"
                                     "uuid-pool-dummypool/"
                                     "block-from-"
                                     "0000-000000000001"
                                     "-to-0000-000000000040")


def test_uuid_block_get_fail_block_non_existent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_block_get(handle, pool_name="dummypool",
                                start_uuid="0000-000000000001",
                                end_uuid="0000-000000000040")


def test_uuid_block_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = "org-root/uuid-pool-dummypool"
    managed_object_mock = mocker.Mock()
    managed_object_mock.check_prop_match.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_block_get', autospec=True)
    mock_get.return_value = managed_object_mock

    result = uuidpool.uuid_block_exists(handle, pool_name="dummypool",
                                        start_uuid="0000-000000000001",
                                        end_uuid="0000-000000000040")

    mock_get.assert_called_with(handle=handle, caller='uuid_block_exists',
                                pool_name="dummypool", org_dn="org-root",
                                start_uuid="0000-000000000001",
                                end_uuid="0000-000000000040")
    managed_object_mock.check_prop_match.assert_called()
    assert result == (True, managed_object_mock)


def test_uuid_block_exists_fail(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_block_get', autospec=True)
    mock_get.side_effect = uuidpool.UcsOperationError("query_dn",
                                                      "block does not exist")

    result = uuidpool.uuid_block_exists(handle, pool_name="dummypool",
                                        start_uuid="0000-000000000001",
                                        end_uuid="0000-000000000040")

    assert result == (False, None)


def test_uuid_block_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_block_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    uuidpool.uuid_block_modify(handle,
                               pool_name="dummypool",
                               org_dn="org-root",
                               start_uuid="0000-000000000001",
                               end_uuid="0000-000000000040",
                               status="modified")

    mock_get.assert_called_with(handle=handle, pool_name="dummypool",
                                org_dn="org-root",
                                caller="uuid_block_modify",
                                start_uuid="0000-000000000001",
                                end_uuid="0000-000000000040")
    mo_mock.set_prop_multiple.assert_called_with(status="modified")


def test_uuid_block_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_block_get', autospec=True)
    mock_get.side_effect = uuidpool.UcsOperationError("query_dn",
                                                      "pool does not exist")

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_block_modify(handle,
                                   pool_name="nopool",
                                   org_dn="org-root",
                                   start_uuid="0000-000000000001",
                                   end_uuid="0000-000000000040",
                                   status="modified")


def test_uuid_block_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_block_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo', autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    uuidpool.uuid_block_delete(handle, pool_name="dummypool",
                               start_uuid="0000-000000000001",
                               end_uuid="0000-000000000040")

    mock_get.assert_called_with(handle=handle, pool_name="dummypool",
                                org_dn="org-root",
                                start_uuid="0000-000000000001",
                                end_uuid="0000-000000000040",
                                caller="uuid_block_delete")
    assert mock_remove_mo.call_count == 1


def test_mac_blcok_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(uuidpool, 'uuid_block_get', autospec=True)
    mock_get.side_effect = uuidpool.UcsOperationError("query_dn",
                                                      "block does not exist")

    with pytest.raises(uuidpool.UcsOperationError):
        uuidpool.uuid_block_delete(handle, pool_name="dummypool",
                                   start_uuid="0000-000000000001",
                                   end_uuid="0000-000000000060")
