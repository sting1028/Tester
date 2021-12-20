#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages
import platform

requirements = ['python-can','pyserial','pyserial-asyncio','smbus2','pyvisa']
if platform.system().lower() == 'linux':
    requirements.append('RPi.GPIO')
setup_requirements = ['pytest-runner']

test_requirements = ['pytest', 'pytest-cov', 'pytest-mock']

setup(
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A data acquisition library.",
    install_requires=requirements,
    include_package_data=True,
    keywords='Acqer',
    name='Acqer',
    packages=find_packages(include=['pi','pi.dcLoad','pi.handler','pi.powerSupply','pi.scope']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='http://github.com/sting1028/Tester.git',
    version='0.0.1',
    zip_safe=False,
)
