import pytest
from ucsm_apis.server import powerctrl
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_powerctrl_policy_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_powerctrl = mocker.patch('ucsm_apis.server.powerctrl.PowerPolicy')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None

    powerctrl.powerctrl_policy_create(handle, name="no-power-cap")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_powerctrl.assert_called_with(name="no-power-cap",
                                      parent_mo_or_dn="org-root",
                                      descr=None,
                                      fan_speed="any",
                                      prio="no-cap")


def test_powerctrl_policy_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(powerctrl.UcsOperationError):
        powerctrl.powerctrl_policy_create(handle, name="no-power-cap",
                                          org_dn="dummy")


def test_powerctrl_policy_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/power-policy-no-power-cap"

    powerctrl.powerctrl_policy_get(handle, name="no-power-cap")

    mock_query_dn.assert_called_with(handle, "org-root/power-policy-"
                                     "no-power-cap")


def test_powerctrl_policy_get_fail_policy_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(powerctrl.UcsOperationError):
        powerctrl.powerctrl_policy_get(handle, "nopolicy")


def test_powerctrl_policy_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/power-policy-no-power-cap"
    mock_check_prop = mocker.patch.object(powerctrl.PowerPolicy,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(powerctrl, 'powerctrl_policy_get',
                                   autospec=True)

    powerctrl.powerctrl_policy_exists(handle, name="no-power-cap")

    mock_get.assert_called_with(handle=handle,
                                caller='powerctrl_policy_exists',
                                name="no-power-cap", org_dn="org-root")


def test_powerctrl_policy_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(powerctrl, 'powerctrl_policy_get',
                                   autospec=True)
    mock_get.side_effect = powerctrl.UcsOperationError("query_dn",
                                                       "policy does not exist")

    result = powerctrl.powerctrl_policy_exists(handle, name="no_policy")

    assert result == (False, None)


def test_powerctrl_policy_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(powerctrl, 'powerctrl_policy_get',
                                   autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    powerctrl.powerctrl_policy_modify(handle, name="no-power-cap",
                                      descr="This is a new policy")

    mock_get.assert_called_with(handle=handle, name="no-power-cap",
                                org_dn="org-root",
                                caller="powerctrl_policy_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new policy")


def test_powerctrl_policy_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(powerctrl, 'powerctrl_policy_get',
                                   autospec=True)
    mock_get.side_effect = powerctrl.UcsOperationError("query_dn",
                                                       "policy does not exist")

    with pytest.raises(powerctrl.UcsOperationError):
        powerctrl.powerctrl_policy_modify(handle, name="nopolicy",
                                          descr="Policy no aqui")


def test_powerctrl_policy_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(powerctrl, 'powerctrl_policy_get',
                                   autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    powerctrl.powerctrl_policy_delete(handle, "no-power-cap")

    mock_get.assert_called_with(handle=handle, name="no-power-cap",
                                org_dn="org-root",
                                caller="powerctrl_policy_delete")
    assert mock_remove_mo.call_count == 1


def test_powerctrl_policy_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(powerctrl, 'powerctrl_policy_get',
                                   autospec=True)
    mock_get.side_effect = powerctrl.UcsOperationError("query_dn",
                                                       "policy does not exist")

    with pytest.raises(powerctrl.UcsOperationError):
        powerctrl.powerctrl_policy_delete(handle, "no-power-cap")
