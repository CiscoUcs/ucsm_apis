# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module performs the operation related to Authentication management.
"""
from ucsmsdk.ucsexception import UcsOperationError

_auth_realm_dn = "sys/auth-realm"


def auth_domain_get(handle, name, caller="auth_domain_get"):
    """
    Gets the auth domain

    Args:
        handle (UcsHandle)
        name (string): name of auth domain

    Returns:
        AaaDomain Managed Object OR None

    Example:
        auth_domain_get(handle, name="ciscoucs")
    """

    dn = _auth_realm_dn + "/domain-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller, "Auth Domain '%s' does not exist" % dn)
    return mo


def auth_domain_create(handle, name, refresh_period="600",
                       session_timeout="7200", descr=None, **kwargs):
    """
    Adds a auth domain

    Args:
        handle (UcsHandle)
        name (string): name of auth domain
        refresh_period: refresh period in seconds. Default 600.
        session_timeout: timeout in seconds. Default 7200.
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaDomain : Managed Object

    Example:
        auth_domain_create(handle, name="ciscoucs")
    """
    from ucsmsdk.mometa.aaa.AaaDomain import AaaDomain

    mo = AaaDomain(parent_mo_or_dn=_auth_realm_dn,
                   name=name,
                   refresh_period=refresh_period,
                   session_timeout=session_timeout,
                   descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def auth_domain_exists(handle, name, **kwargs):
    """
    checks if auth domain exists

    Args:
        handle (UcsHandle)
        name (string): name of auth domain
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        auth_domain_exists(handle, name="ciscoucs")
    """
    try:
        mo = auth_domain_get(handle, name, caller="auth_domain_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def auth_domain_modify(handle, name, **kwargs):
    """
    Modifies a domain

    Args:
        handle (UcsHandle)
        name (string): name of domain
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaDomain : Managed Object

    Raises:
        UcsOperationError: If AaaDomain is not present

    Example:
        auth_domain_modify(handle, name="test_auth_dom",
                           session_timeout="1000")
    """

    mo = auth_domain_get(handle, name, caller="auth_domain_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def auth_domain_delete(handle, name):
    """
    deletes a auth domain.

    Args:
        handle (UcsHandle)
        name (string): auth domain name

    Returns:
        None

    Raises:
        UcsOperationError: If AaaDomain is not present

    Example:
        auth_domain_delete(handle, name="test_auth_dom")
    """

    mo = auth_domain_get(handle, name, caller="auth_domain_delete")
    handle.remove_mo(mo)
    handle.commit()


def auth_domain_realm_configure(handle, domain_name, realm="local",
                                use2_factor="no", provider_group="",
                                name=None, descr=None,
                                **kwargs):
    """
    configure realm of a auth domain.

    Args:
        handle (UcsHandle)
        domain_name (string): auth domain name
        realm (string): realm ["ldap", "local", "none", "radius", "tacacs"]
                        Use "none" to disable auth
        use2_factor(string): Two Factor Authentication ["yes", "no"]
        provider_group (string): provider group name
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaDomainAuth : Managed Object

    Raises:
        UcsOperationError: If AaaDomain is not present

    Example:
        auth_domain_realm_configure(handle, domain_name="ciscoucs",
                                    realm="ldap")
    """
    from ucsmsdk.mometa.aaa.AaaDomainAuth import AaaDomainAuth

    obj = auth_domain_get(handle, domain_name,
                          caller="auth_domain_realm_configure")

    if realm in ("none", "local"):
        provider_group = ""
    if realm in ("none", "local", "ldap"):
        use2_factor = "no"

    mo = AaaDomainAuth(parent_mo_or_dn=obj,
                       realm=realm,
                       use2_factor=use2_factor,
                       provider_group=provider_group,
                       name=name,
                       descr=descr)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def auth_domain_realm_exists(handle, domain_name, **kwargs):
    """
    checks if auth domain realm exists

    Args:
        handle (UcsHandle)
        domain_name (string): name of auth domain
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        auth_domain_realm_exists(handle, domain_name="ciscoucs", realm="ldap")
    """
    domain_dn = _auth_realm_dn + "/domain-" + domain_name
    dn = domain_dn + "/domain-auth"
    mo = handle.query_dn(dn)
    if mo is None:
        return False, None

    realm = kwargs['realm']
    if realm in ("none", "local"):
        kwargs['provider_group'] = ""
    if realm in ("none", "local", "ldap"):
        kwargs['use2_factor'] = "no"

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def native_auth_configure(handle, def_role_policy=None,
                          def_login=None, con_login=None,
                          descr=None, **kwargs):
    """
    configure native authentication.

    Args:
        handle (UcsHandle)
        def_role_policy (string): role policy for remote users
         valid values are "assign-default-role", "no-login"
        def_login (string): default authentication realm
         valid values are "ldap", "local", "none", "radius", "tacacs"
        con_login (string): console authentication realm
         valid values are "ldap", "local", "none", "radius", "tacacs"
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.

    Returns:
        AaaAuthRealm : Managed Object

    Raises:
        UcsOperationError: If AaaAuthRealm is not present

    Example:
        native_auth_configure(handle, def_role_policy="assign-default-role",
                              con_login="local")
    """
    from ucsmsdk.mometa.aaa.AaaAuthRealm import AaaAuthRealm

    mo = AaaAuthRealm(parent_mo_or_dn="sys")

    args = {'def_role_policy': def_role_policy,
            'def_login': def_login,
            'con_login': con_login,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def native_auth_exists(handle, **kwargs):
    """
    checks if native auth exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        native_auth_exists(handle, def_role_policy="assign-default-role")
    """
    from ucsmsdk.mometa.aaa.AaaAuthRealm import AaaAuthRealm

    mo = AaaAuthRealm(parent_mo_or_dn="sys")
    mo = handle.query_dn(mo.dn)
    if mo is None:
        return False, None

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def native_auth_default_configure(handle, realm="local", refresh_period="600",
                                  session_timeout="7200", provider_group="",
                                  use2_factor="no", name=None, descr=None,
                                  **kwargs):
    """
    configure default native authentication.

    Args:
        handle (UcsHandle)
        realm (string): realm ["ldap", "local", "none", "radius", "tacacs"]
                        Use "none" to disable auth
        refresh_period (string): web session refresh period (in seconds)
        session_timeout (string): web session timeout (in seconds)
        provider_group (string): providergroup
        use2_factor (string): two factor authentication ["yes", "no"]
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaDefaultAuth : Managed Object

    Raises:
        UcsOperationError: If AaaDefaultAuth is not present

    Example:
        native_auth_default_configure(handle, realm="radius")
    """
    from ucsmsdk.mometa.aaa.AaaDefaultAuth import AaaDefaultAuth

    mo = AaaDefaultAuth(parent_mo_or_dn=_auth_realm_dn)

    if realm in ("none", "local"):
        provider_group = ""
    if realm in ("none", "local", "ldap"):
        use2_factor = "no"

    args = {'realm': realm,
            'refresh_period': refresh_period,
            'session_timeout': session_timeout,
            'provider_group': provider_group,
            'use2_factor': use2_factor,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def native_auth_default_exists(handle, **kwargs):
    """
    checks if native auth console exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        native_auth_default_exists(handle, realm="radius")
    """
    from ucsmsdk.mometa.aaa.AaaDefaultAuth import AaaDefaultAuth

    mo = AaaDefaultAuth(parent_mo_or_dn=_auth_realm_dn)
    mo = handle.query_dn(mo.dn)
    if mo is None:
        return False, None

    realm = kwargs['realm']
    if realm in ("none", "local"):
        kwargs['provider_group'] = ""
    if realm in ("none", "local", "ldap"):
        kwargs['use2_factor'] = "no"

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def native_auth_console_configure(handle, realm="local", provider_group="",
                                  use2_factor="no", name=None, descr=None,
                                  **kwargs):
    """
    configure console native authentication.

    Args:
        handle (UcsHandle)
        realm (string): realm ["ldap", "local", "none", "radius", "tacacs"]
                        Use "none" to disable auth
        provider_group (string): provider group name
        use2_factor (string): two factor authentication ["yes", "no"]
        name (string): name
        descr (string): description
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaConsoleAuth : Managed Object

    Raises:
        UcsOperationError: If AaaConsoleAuth is not present

    Example:
        native_auth_console_configure(handle, realm="local")
    """
    from ucsmsdk.mometa.aaa.AaaConsoleAuth import AaaConsoleAuth

    mo = AaaConsoleAuth(parent_mo_or_dn=_auth_realm_dn)

    if realm in ("none", "local"):
        provider_group = ""
    if realm in ("none", "local", "ldap"):
        use2_factor = "no"

    args = {'realm': realm,
            'provider_group': provider_group,
            'use2_factor': use2_factor,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def native_auth_console_exists(handle, **kwargs):
    """
    checks if native auth console exists

    Args:
        handle (UcsHandle)
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        native_auth_console_exists(handle, realm="local")
    """
    from ucsmsdk.mometa.aaa.AaaConsoleAuth import AaaConsoleAuth

    mo = AaaConsoleAuth(parent_mo_or_dn=_auth_realm_dn)
    mo = handle.query_dn(mo.dn)
    if mo is None:
        return False, None

    realm = kwargs['realm']
    if realm in ("none", "local"):
        kwargs['provider_group'] = ""
    if realm in ("none", "local", "ldap"):
        kwargs['use2_factor'] = "no"

    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)
