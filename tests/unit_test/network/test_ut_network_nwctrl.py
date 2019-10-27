import pytest
from ucsm_apis.network import nwctrl
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_nwctrl_policy_create_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mock_query_dn.return_value = "org-root"
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mock_nwctrl = mocker.patch('ucsm_apis.network.nwctrl.NwctrlDefinition')
    mock_dpsecmac = mocker.patch('ucsm_apis.network.nwctrl.DpsecMac')
    mock_add_mo = mocker.patch('ucsmsdk.ucshandle.UcsHandle.add_mo',
                               autospec=True)
    mock_add_mo.return_value = None
    mo1_mock = mocker.Mock()
    mock_nwctrl.return_value = mo1_mock

    nwctrl.nwctrl_policy_create(handle, name="cdp_enable",
                                cdp="enabled")

    mock_query_dn.assert_called_with(handle, "org-root")
    mock_nwctrl.assert_called_with(name="cdp_enable",
                                   cdp="enabled",
                                   descr=None,
                                   parent_mo_or_dn="org-root",
                                   lldp_receive="disabled",
                                   lldp_transmit="disabled",
                                   mac_register_mode="only-native-vlan",
                                   uplink_fail_action="link-down")
    mock_dpsecmac.assert_called_with(parent_mo_or_dn=mo1_mock, forge="allow")


def test_nwctrl_policy_create_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(nwctrl.UcsOperationError):
        nwctrl.nwctrl_policy_create(handle, name="cdp_enable",
                                    org_dn="dummy")


def test_nwctrl_policy_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/nwctrl-cdp_enable"

    nwctrl.nwctrl_policy_get(handle, name="cdp_enable")

    mock_query_dn.assert_called_with(handle, "org-root/nwctrl-cdp_enable")


def test_nwctrl_policy_get_fail_policy_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(nwctrl.UcsOperationError):
        nwctrl.nwctrl_policy_get(handle, "nopolicy")


def test_nwctrl_policy_exists_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = "org-root/nwctrl-cdp_enable"
    mock_check_prop = mocker.patch.object(nwctrl.NwctrlDefinition,
                                          'check_prop_match', autospec=True)
    mock_check_prop.return_value = True
    mock_get = mocker.patch.object(nwctrl, 'nwctrl_policy_get', autospec=True)

    nwctrl.nwctrl_policy_exists(handle, name="cdp_enable")

    mock_get.assert_called_with(handle=handle, caller='nwctrl_policy_exists',
                                name="cdp_enable", org_dn="org-root")


def test_nwctrl_policy_exists_fail_org_does_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(nwctrl, 'nwctrl_policy_get', autospec=True)
    mock_get.side_effect = nwctrl.UcsOperationError("query_dn",
                                                    "policy does not exist")

    result = nwctrl.nwctrl_policy_exists(handle, name="no_policy")

    assert result == (False, None)


def test_nwctrl_policy_modify_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(nwctrl, 'nwctrl_policy_get', autospec=True)
    mo_mock = mocker.Mock()
    mo_mock.set_prop_multiple.return_value = True
    mock_get.return_value = mo_mock
    mock_set_mo = mocker.patch.object(UcsHandle, 'set_mo', autospec=True)
    mock_set_mo.return_value = None
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    nwctrl.nwctrl_policy_modify(handle, name="cdp_enable",
                                descr="This is a new policy")

    mock_get.assert_called_with(handle=handle, name="cdp_enable",
                                org_dn="org-root",
                                caller="nwctrl_policy_modify")
    mo_mock.set_prop_multiple.assert_called_with(descr="This is a new policy")


def test_nwctrl_policy_modify_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(nwctrl, 'nwctrl_policy_get', autospec=True)
    mock_get.side_effect = nwctrl.UcsOperationError("query_dn",
                                                    "policy does not exist")

    with pytest.raises(nwctrl.UcsOperationError):
        nwctrl.nwctrl_policy_modify(handle, name="nopolicy",
                                    descr="Policy no aqui")


def test_nwctrl_policy_delete_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(nwctrl, 'nwctrl_policy_get', autospec=True)
    mock_remove_mo = mocker.patch.object(UcsHandle, 'remove_mo',
                                         autospec=True)
    mock_commit = mocker.patch.object(UcsHandle, 'commit', autospec=True)
    mock_commit.return_value = None

    nwctrl.nwctrl_policy_delete(handle, "cdp_enable")

    mock_get.assert_called_with(handle=handle, name="cdp_enable",
                                org_dn="org-root",
                                caller="nwctrl_policy_delete")
    assert mock_remove_mo.call_count == 1


def test_nwctrl_policy_delete_failure_pool_nonexistent(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_get = mocker.patch.object(nwctrl, 'nwctrl_policy_get', autospec=True)
    mock_get.side_effect = nwctrl.UcsOperationError("query_dn",
                                                    "policy does not exist")

    with pytest.raises(nwctrl.UcsOperationError):
        nwctrl.nwctrl_policy_delete(handle, "cdp_enable")
