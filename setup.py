#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'ucsmsdk'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ucsm_apis',
    version='0.9.0.0',
    description="API bindings for UCSM python SDK",
    long_description=readme + '\n\n' + history,
    author="Cisco Ucs",
    author_email='ucs-python@cisco.com',
    url='https://github.com/ciscoucs/ucsm_apis',
    packages=[
        'ucsm_apis',
    ],
    package_dir={'ucsm_apis':
                 'ucsm_apis'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='ucsm_apis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=[
        'nose',
        'mock',
        'pytest',
        'pytest-mock',
        'pytest-runner'
        ],
    test_suite='tests',
)
