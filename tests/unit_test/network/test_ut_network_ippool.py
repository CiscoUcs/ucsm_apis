import pytest
from ucsm_apis.network import ippool
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_ip_pool_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_ip_pool = mocker.patch('ucsm_apis.network.ippool.IppoolPool')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    ippool.ip_pool_create(handle, "dummypool")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_ip_pool.assert_called_with(descr=None, name='dummypool',
                                    parent_mo_or_dn='org-root')


def test_ip_pool_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_pool_create(handle, "dummypool", org_dn="dummy")


def test_ip_pool_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/ip-pool-dummypool"

    ippool.ip_pool_get(handle, "dummypool")

    mock_query_dn.assert_called_with(handle, "org-root/ip-pool-dummypool")


def test_ip_pool_get_fail_pool_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_pool_get(handle, "nopool")


def test_ip_pool_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/ip-pool-dummypool"
    mock_check_prop = mocker.patch.object(ippool.IppoolPool,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_pool_get', autospec=True)

    ippool.ip_pool_exists(handle, "dummypool")

    mock_get.assert_called_with(handle=handle, caller='ip_pool_exists',
                                name="dummypool", org_dn="org-root")


def test_ip_pool_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_pool_get', autospec=True)
    mock_get.side_effect = ippool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    result = ippool.ip_pool_exists(handle, "dummypool")

    assert result == (False, None)


def test_ip_pool_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_pool_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    ippool.ip_pool_modify(handle, "dummypool", descr="This is a new pool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="ip_pool_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new pool")


def test_ip_pool_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_pool_get', autospec=True)
    mock_get.side_effect = ippool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_pool_modify(handle, "nopool", descr="Pool no aqui")


def test_ip_pool_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_pool_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    ippool.ip_pool_delete(handle, "dummypool")

    mock_get.assert_called_with(handle=handle, name="dummypool",
                                org_dn="org-root", caller="ip_pool_delete")
    assert mock_remove_mo.call_count == 1


def test_ip_pool_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_pool_get', autospec=True)
    mock_get.side_effect = ippool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_pool_delete(handle, "dummypool")


def test_ip_block_create_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/ip-pool-dummypool"
    mock_ip_pool_block = mocker.patch.object(ippool, 'IppoolBlock',
                                             autospec=True)
    mock_add_mo = mocker.patch.object(UcsHandle, 'add_mo', autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)

    ippool.ip_block_create(handle, "dummypool", start_ip="192.168.10.50",
                           end_ip="192.168.10.60",
                           sm="255.255.255.0", gw="192.168.10.1")

    assert mock_query_dn.call_count == 2
    mock_ip_pool_block.assert_called_with(parent_mo_or_dn="org-root/"
                                          "ip-pool-dummypool",
                                          def_gw="192.168.10.1",
                                          r_from="192.168.10.50",
                                          to="192.168.10.60",
                                          subnet="255.255.255.0")
    mock_add_mo.assert_called()
    mock_commit.assert_called()


def test_ip_block_create_fail_org_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_block_create(handle, "dummypool", org_dn="dummyorg",
                               start_ip="192.168.10.50",
                               end_ip="192.168.10.60",
                               sm="255.255.255.0", gw="192.168.10.1")


def test_ip_block_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)

    ippool.ip_block_get(handle, "dummypool", start_ip="192.168.10.50",
                        end_ip="192.168.10.60")

    mock_query_dn.assert_called_with(handle,
                                     "org-root/"
                                     "ip-pool-dummypool/"
                                     "block-192.168.10.50-192.168.10.60")


def test_ip_block_get_fail_block_non_existent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_block_get(handle, "dummypool", start_ip="192.168.10.50",
                            end_ip="192.168.10.60")


def test_ip_block_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn', autospec=True)
    mock_query_dn.return_value = "org-root/ip-pool-dummypool"
    managed_object_mock = mocker.Mock()
    managed_object_mock.check_prop_match.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_block_get', autospec=True)
    mock_get.return_value = managed_object_mock

    result = ippool.ip_block_exists(handle, "dummypool",
                                    start_ip="192.168.10.50",
                                    end_ip="192.168.10.60")

    mock_get.assert_called_with(handle=handle, caller='ip_block_exists',
                                pool_name="dummypool", org_dn="org-root",
                                start_ip="192.168.10.50",
                                end_ip="192.168.10.60")
    managed_object_mock.check_prop_match.assert_called()
    assert result == (True, managed_object_mock)


def test_ip_block_exists_fail(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_block_get', autospec=True)
    mock_get.side_effect = ippool.UcsOperationError("query_dn",
                                                    "block does not exist")

    result = ippool.ip_block_exists(handle, "dummypool",
                                    start_ip="192.168.10.50",
                                    end_ip="192.168.10.60")

    assert result == (False, None)


def test_ip_block_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_block_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    ippool.ip_block_modify(handle, "dummypool",
                           start_ip="192.168.10.50", end_ip="192.168.10.60",
                           prim_dns="8.8.8.8")

    mock_get.assert_called_with(handle=handle, pool_name="dummypool",
                                org_dn="org-root",
                                caller="ip_block_modify",
                                start_ip="192.168.10.50",
                                end_ip="192.168.10.60")
    mo_mock.set_prop_multiple.assert_called_with(prim_dns="8.8.8.8")


def test_ip_block_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_block_get', autospec=True)
    mock_get.side_effect = ippool.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_block_modify(handle, "nopool", start_ip="192.168.10.50",
                               end_ip="192.168.10.60",
                               prim_dns="8.8.8.8")


def test_ip_block_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_block_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo', autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    ippool.ip_block_delete(handle, "dummypool", start_ip="192.168.10.50",
                           end_ip="192.168.10.60")

    mock_get.assert_called_with(handle=handle, pool_name="dummypool",
                                org_dn="org-root",
                                caller="ip_block_delete",
                                start_ip="192.168.10.50",
                                end_ip="192.168.10.60")
    assert mock_remove_mo.call_count == 1


def test_ip_blcok_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(ippool, 'ip_block_get', autospec=True)
    mock_get.side_effect = ippool.UcsOperationError("query_dn",
                                                    "block does not exist")

    with pytest.raises(ippool.UcsOperationError):
        ippool.ip_block_delete(handle, "dummypool",
                               start_ip="192.168.10.50",
                               end_ip="192.168.10.60")
