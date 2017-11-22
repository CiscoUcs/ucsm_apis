import pytest
from ucsm_apis.server import localdisk
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_localdisk_policy_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_localdisk = mocker.patch('ucsm_apis.server.localdisk.StorageLocalDiskConfigPolicy')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    localdisk.localdisk_policy_create(handle, name="dummypolicy")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_localdisk.assert_called_with(name='dummypolicy',
                                      descr=None,
                                      parent_mo_or_dn='org-root',
                    flex_flash_raid_reporting_state="disable",
                                      flex_flash_state="disable",
                                      mode="any-configuration",
                                      protect_config="no")


def test_localdisk_policy_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(localdisk.UcsOperationError):
        localdisk.localdisk_policy_create(handle, name="dummypolicy",
                                          org_dn="dummy")


def test_localdisk_policy_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/local-disk-config-dummypolicy"

    localdisk.localdisk_policy_get(handle, name="dummypolicy")

    mock_query_dn.assert_called_with(handle, "org-root/local-disk-config-dummypolicy")


def test_localdisk_policy_get_fail_policy_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(localdisk.UcsOperationError):
        localdisk.localdisk_policy_get(handle, name="nopool")


def test_localdisk_policy_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/local-disk-config-dummypolicy"
    mock_check_prop = mocker.patch.object(localdisk.StorageLocalDiskConfigPolicy,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(localdisk, 'localdisk_policy_get',
                                   autospec=True)

    localdisk.localdisk_policy_exists(handle, name="dummypolicy")

    mock_get.assert_called_with(handle=handle, caller='localdisk_policy_exists',
                                name="dummypolicy", org_dn="org-root")


def test_localdisk_policy_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(localdisk, 'localdisk_policy_get',
                                   autospec=True)
    mock_get.side_effect = localdisk.UcsOperationError("query_dn",
                                                      "pool does not exist")

    result = localdisk.localdisk_policy_exists(handle, name="dummypolicy")

    assert result == (False, None)


def test_localdisk_policy_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(localdisk, 'localdisk_policy_get',
                                   autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    localdisk.localdisk_policy_modify(handle, name="dummypolicy",
                                      descr="This is a new policy")

    mock_get.assert_called_with(handle=handle, name="dummypolicy",
                                org_dn="org-root", caller="localdisk_policy_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new policy")


def test_localdisk_policy_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(localdisk, 'localdisk_policy_get',
                                   autospec=True)
    mock_get.side_effect = localdisk.UcsOperationError("query_dn",
                                                      "pool does not exist")

    with pytest.raises(localdisk.UcsOperationError):
        localdisk.localdisk_policy_modify(handle, name="nopolicy",
                                      descr="Policy no aqui")


def test_localdisk_policy_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(localdisk, 'localdisk_policy_get',
                                   autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    localdisk.localdisk_policy_delete(handle, "dummypolicy")

    mock_get.assert_called_with(handle=handle, name="dummypolicy",
                                org_dn="org-root", caller="localdisk_policy_delete")
    assert mock_remove_mo.call_count == 1


def test_localdisk_policy_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(localdisk, 'localdisk_policy_get',
                                   autospec=True)
    mock_get.side_effect = localdisk.UcsOperationError("query_dn",
                                                    "pool does not exist")

    with pytest.raises(localdisk.UcsOperationError):
        localdisk.localdisk_policy_delete(handle, name="dummypolicy")
