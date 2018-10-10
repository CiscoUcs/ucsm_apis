import pytest
from ucsm_apis.server import bios
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_bios_policy_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_bios = mocker.patch('ucsm_apis.server.bios.BiosVProfile')
    mock_cdn = mocker.patch('ucsm_apis.server.bios.BiosVfConsistentDeviceNameControl')
    mock_fpl = mocker.patch('ucsm_apis.server.bios.BiosVfFrontPanelLockout')
    mock_pep = mocker.patch('ucsm_apis.server.bios.BiosVfPOSTErrorPause')
    mock_quiet = mocker.patch('ucsm_apis.server.bios.BiosVfQuietBoot')
    mock_res = mocker.patch('ucsm_apis.server.bios.BiosVfResumeOnACPowerLoss')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None
    mo1_mock = mocker.Mock()
    mock_bios.return_value = mo1_mock

    bios.bios_policy_create(handle, name="no_reboot")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_bios.assert_called_with(name="no_reboot",
                                 parent_mo_or_dn="org-root",
                                 descr=None,
                                 reboot_on_update="no")
    mock_cdn.assert_called_with(parent_mo_or_dn=mo1_mock,
                                vp_cdn_control="platform-default")
    mock_fpl.assert_called_with(parent_mo_or_dn=mo1_mock,
                                vp_front_panel_lockout="platform-default")
    mock_pep.assert_called_with(parent_mo_or_dn=mo1_mock,
                                vp_post_error_pause="platform-default")
    mock_quiet.assert_called_with(parent_mo_or_dn=mo1_mock,
                                  vp_quiet_boot="disabled")
    mock_res.assert_called_with(parent_mo_or_dn=mo1_mock,
                                vp_resume_on_ac_power_loss="platform-default")



def test_bios_policy_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(bios.UcsOperationError):
        bios.bios_policy_create(handle, name="quiet_boot",
                                        org_dn="dummy")


def test_bios_policy_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/bios-prof-quiet_boot"

    bios.bios_policy_get(handle, name="quiet_boot")

    mock_query_dn.assert_called_with(handle, "org-root/bios-prof-"
                                     "quiet_boot")


def test_bios_policy_get_fail_policy_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(bios.UcsOperationError):
        bios.bios_policy_get(handle, "nopolicy")


def test_bios_policy_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/bios-prof-quiet_boot"
    mock_check_prop = mocker.patch.object(bios.BiosVProfile,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(bios, 'bios_policy_get',
                                   autospec=True)

    bios.bios_policy_exists(handle, name="quiet_boot")

    mock_get.assert_called_with(handle=handle,
                                caller='bios_policy_exists',
                                name="quiet_boot", org_dn="org-root")


def test_bios_policy_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(bios, 'bios_policy_get',
                                   autospec=True)
    mock_get.side_effect = bios.UcsOperationError("query_dn",
                                                       "policy does not exist")

    result = bios.bios_policy_exists(handle, name="no_policy")

    assert result == (False, None)


def test_bios_policy_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(bios, 'bios_policy_get',
                                   autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    bios.bios_policy_modify(handle, name="quiet_boot",
                                      descr="This is a new policy")

    mock_get.assert_called_with(handle=handle, name="quiet_boot",
                                org_dn="org-root",
                                caller="bios_policy_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new policy")


def test_bios_policy_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(bios, 'bios_policy_get',
                                   autospec=True)
    mock_get.side_effect = bios.UcsOperationError("query_dn",
                                                  "policy does not exist")

    with pytest.raises(bios.UcsOperationError):
        bios.bios_policy_modify(handle, name="nopolicy",
                                descr="Policy no aqui")


def test_bios_policy_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(bios, 'bios_policy_get',
                                   autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    bios.bios_policy_delete(handle, "quiet_boot")

    mock_get.assert_called_with(handle=handle, name="quiet_boot",
                                org_dn="org-root",
                                caller="bios_policy_delete")
    assert mock_remove_mo.call_count == 1


def test_bios_policy_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(bios, 'bios_policy_get',
                                   autospec=True)
    mock_get.side_effect = bios.UcsOperationError("query_dn",
                                                  "policy does not exist")

    with pytest.raises(bios.UcsOperationError):
        bios.bios_policy_delete(handle, "quiet_boot")
