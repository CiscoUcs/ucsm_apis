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
This module performs the operation related to key management.
"""
from ucsmsdk.ucsexception import UcsOperationError

_keyring_base_dn = "sys/pki-ext"
_tp_base_dn = "sys/pki-ext"

def key_ring_create(handle, name, modulus="mod2048", regen="no",
                    policy_owner="local", tp=None, cert=None, descr=None,
                    **kwargs):
    """
    Creates a key ring

    Args:
        handle (ucshandle)
        name (string): name
        descr (string): description
        tp (string): tp
        cert (string): certificate
        regen (string): regen, "false", "no", "true", "yes"
        modulus (string): modulus, valid values are
            "mod2048", "mod2560", "mod3072", "mod3584", "mod4096", "modinvalid"
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        PkiKeyRing: managed object

    Example:
        key_ring = key_ring_create(handle, name="mykeyring", regen="yes")
    """

    from ucsmsdk.mometa.pki.PkiKeyRing import PkiKeyRing

    mo = PkiKeyRing(parent_mo_or_dn=_keyring_base_dn,
                    name=name,
                    modulus=modulus,
                    regen=regen,
                    policy_owner=policy_owner,
                    tp=tp,
                    cert=cert,
                    descr=descr)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def key_ring_get(handle, name, caller="key_ring_get"):
    """
    Gets the key ring

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        PkiKeyRing: managed object OR None

    Example:
        key_ring = key_ring_get(handle, name="mykeyring")
    """

    dn = _keyring_base_dn + "/keyring-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Ldap Provider '%s' does not exist" % dn)
    return mo


def key_ring_exists(handle, name, **kwargs):
    """
    Checks if a key ring exists

    Args:
        handle (UcsHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        key_ring = key_ring_exists(handle, name="mykeyring")
    """
    try:
        mo = key_ring_get(handle, name, caller="key_ring_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def key_ring_modify(handle, name, **kwargs):
    """
    Modifies a key ring

    Args:
        handle (UcsHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        PkiKeyRing : Managed object

    Raises:
        UcsOperationError: if PkiKeyRing is not present

    Example:
        key_ring = key_ring_modify(handle, name="test_kr", regen="no")
    """

    mo = key_ring_get(handle, name, caller="key_ring_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def key_ring_delete(handle, name):
    """
    Deletes a key ring

    Args:
        handle (UcsHandle)
        name (string): name

    Returns:
        none

    Raises:
        UcsOperationError: if pkikeyring mo is not present

    Example:
        key_ring_delete(handle, name="mykeyring")
    """

    mo = key_ring_get(handle, name, caller="key_ring_delete")
    handle.remove_mo(mo)
    handle.commit()


def certificate_request_add(handle, name,
                            ip="0.0.0.0", ip_a="0.0.0.0", ip_b="0.0.0.0",
                            ipv6="::", ipv6_a="::", ipv6_b="::", dns=None,
                            locality=None, state=None, country=None,
                            org_name=None, org_unit_name=None, subj_name=None,
                            email=None, pwd=None, **kwargs):
    """
    Adds a certificate request to keyring

    Args:
        handle (UcsHandle)
        name (string): KeyRing name
        ip (string): ipv4
        ip_a (string):
        ip_b (string):
        ipv6 (string):
        ipv6_a (string):
        ipv6_b (string):
        dns (string): dns
        locality (string): locality owner
        state (string): state
        country (string): country
        org_name (string): org_name
        org_unit_name (string): org_unit_name
        subj_name (string): subj_name
        email (string): email
        pwd (string): pwd
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        PkiCertReq: Managed object

    Raises:
        UcsOperationError: If PkiKeyRing is not present

    Example:
        certificate_request_add(handle, name="test_kr", dns="10.10.10.100",
                                country="IN")
    """

    from ucsmsdk.mometa.pki.PkiCertReq import PkiCertReq

    obj = key_ring_get(handle, name, caller="certificate_request_add")
    mo = PkiCertReq(parent_mo_or_dn=obj,
                    dns=dns,
                    ip=ip,
                    ip_a=ip_a,
                    ip_b=ip_b,
                    ipv6=ipv6,
                    ipv6_a=ipv6_a,
                    ipv6_b=ipv6_b,
                    locality=locality,
                    state=state,
                    country=country,
                    org_name=org_name,
                    org_unit_name=org_unit_name,
                    subj_name=subj_name,
                    email=email,
                    pwd=pwd
                    )

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def certificate_request_get(handle, name, caller="certificate_request_get"):
    """
    Checks if a certificate request exists

    Args:
        handle (UcsHandle)
        name (string): KeyRing name

    Returns:
        PkiCertReq: Managed object OR None

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_get(handle, key_ring="keyring")
    """

    dn = _keyring_base_dn + "/keyring-" + name + "/certreq"
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Certificate Request '%s' does not exist" % dn)
    return mo


def certificate_request_exists(handle, name, **kwargs):
    """
    Checks if a certificate request exists

    Args:
        handle (UcsHandle)
        name (string): KeyRing name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_exists(handle, key_ring="keyring")
    """
    try:
        mo = certificate_request_get(handle, name,
                                     caller="certificate_request_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


'''
Note: certificate_request_modify is not possible
'''


def certificate_request_remove(handle, name):
    """
    Removes a certificate request from keyring

    Args:
        handle (UcsHandle)
        name (string): KeyRing name

    Returns:
        None

    Raises:
        UcsOperationError: If PkiCertReq is not present

    Example:
        key_ring = key_ring_create(handle, name="mykeyring")

        certificate_request_remove(handle, key_ring=key_ring)

    """

    mo = certificate_request_get(handle, name,
                                 caller="certificate_request_remove")
    handle.remove_mo(mo)
    handle.commit()


def trusted_point_create(handle, name, policy_owner="local",
                         descr=None, cert_chain=None, **kwargs):
    """
    Creates a trusted point

    Args:
        handle (ucshandle)
        name (string): name
        descr (string): description
        cert_chain (string): chain of certificate
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        PkiTP: managed object

    Example:
        trusted_point = trusted_point_create(handle, name="mytrustedpoint")
    """

    from ucsmsdk.mometa.pki.PkiTP import PkiTP

    mo = PkiTP(parent_mo_or_dn=_tp_base_dn,
               name=name,
               policy_owner=policy_owner,
               descr=descr,
               cert_chain=cert_chain)

    mo.set_prop_multiple(**kwargs)
    handle.add_mo(mo, True)
    handle.commit()
    return mo


def trusted_point_get(handle, name, caller="trusted_point_get"):
    """
    Checks if a trusted point exists

    Args:
        handle (ucshandle)
        name (string): name

    Returns:
        PkiTP: managed object OR None

    Example:
        key_ring = trusted_point_get(handle, name="mytrustedpoint")
    """

    dn = _tp_base_dn + "/tp-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise UcsOperationError(caller,
                                "Trusted Point '%s' does not exist" % dn)
    return mo

def trusted_point_exists(handle, name, **kwargs):
    """
    Checks if a trusted point exists

    Args:
        handle (ucshandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        key_ring = trusted_point_exists(handle, name="mytrustedpoint")
    """
    try:
        mo = trusted_point_get(handle, name, caller="trusted_point_exists")
    except UcsOperationError:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def trusted_point_modify(handle, name, **kwargs):
    """
    Modifies a trusted point

    Args:
        handle (ucshandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucscoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        PkiTP object

    Raises:
        UcsOperationError: if PkiTP not present

    Example:
        trusted_point = trusted_point_modify(handle, name="test_tp",
                                             descr="testing tp")
    """

    mo = trusted_point_get(handle, name, caller="trusted_point_modify")
    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def trusted_point_delete(handle, name):
    """
    Deletes a truted point

    Args:
        handle (ucshandle)
        name (string): name

    Returns:
        None

    Raises:
        UcsOperationError: if PkiTP mo is not present

    Example:
        trusted_point_delete(handle, name="mytrustedpoint")
    """

    mo = trusted_point_get(handle, name, caller="trusted_point_delete")
    handle.remove_mo(mo)
    handle.commit()
