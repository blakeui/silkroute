#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pandas',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
    'nose'
]

setup(
    name='silkroute',
    version='0.1.0',
    description="Marketplace for Anonymous Transactions",
    long_description=readme + '\n\n' + history,
    author="Debanjum Singh Solanky",
    author_email='debanjum@gmail.com',
    url='https://github.com/debanjum/silkroute',
    packages=[
        'silkroute', 'seller', 'buyer', 'stocker'
    ],
    package_dir={'silkroute':
                 'silkroute'},
    entry_points={
        'console_scripts': [
            'silkroute=silkroute.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='silkroute',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
