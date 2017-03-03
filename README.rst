===============================
ucsm_apis
===============================


.. image:: https://img.shields.io/pypi/v/ucsm_apis.svg
        :target: https://pypi.python.org/pypi/ucsm_apis

`ucsm_apis` provide python based API layer for performing actions on Cisco UCS
Managed servers. The APIs are one layer higher than that of ucsmsdk. ucsmsdk
deals with every object individually. The purpose of ucsm_apis is to provide
flows versus CRUD APIs in ucsmsdk.

License
-------
* Free software: Apache Software License 2.0

Install
-------
Pre-requisite

.. code:: python

    sudo pip install ucsmsdk

For github:

.. code:: python

    git clone https://github.com/ciscoucs/ucsm_apis
    cd ucsm_apis
    sudo make install

Uninstall
---------

.. code:: python

    sudo pip uninstall ucsm_apis


History
=======
0.9.0.0
-------
- [03/03/2017] Added server power on,off,powercycle immediate and powercycle wait APIs



