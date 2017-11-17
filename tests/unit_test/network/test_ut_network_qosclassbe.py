import pytest
from ucsm_apis.network import qosclassbe
from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle("10.10.10.10", "username", "password")


def test_qosclassbe_modify_success(mocker):
    mock_login = mocker.patch('ucsmsdk.ucshandle.UcsHandle.login',
                              autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch('ucsmsdk.ucshandle.UcsHandle.query_dn',
                                 autospec=True)
    mo_mock = mocker.Mock()
    mock_query_dn.return_value = mo_mock
    mock_commit = mocker.patch('ucsmsdk.ucshandle.UcsHandle.commit',
                               autospec=True)
    mock_commit.return_value = None
    mo = qosclassbe.qosclassbe_modify(handle, mtu="9216", weight="5")

    mock_query_dn.assert_called_with(handle, "fabric/lan/classes"
                                    "/class-best-effort")
    assert mo.mtu == "9216"
    assert mo.weight == "5"


def test_qosclassbe_modify_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(qosclassbe.UcsOperationError):
        qosclassbe.qosclassbe_modify(handle, mtu="9216", weight="5")


def test_qosclassbe_get_success(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mo_mock = mocker.Mock()
    mock_query_dn.return_value = mo_mock

    qosclassbe.qosclassbe_get(handle)

    mock_query_dn.assert_called_with(handle, "fabric/lan/"
                                     "classes/class-best-effort")


def test_qosclassbe_get_fail_org_not_exist(mocker):
    mock_login = mocker.patch.object(UcsHandle, 'login', autospec=True)
    mock_login.return_value = True
    mock_query_dn = mocker.patch.object(UcsHandle, 'query_dn',
                                        autospec=True)
    mock_query_dn.return_value = None

    with pytest.raises(qosclassbe.UcsOperationError):
        qosclassbe.qosclassbe_get(handle)
