#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from setuptools import setup, find_packages

import sys
if sys.version_info[0] == 2:
    from io import open

here = os.path.abspath(os.path.dirname(__file__))

__version__ = None
__license__ = None
__author__ = None
exec(open('hc/_meta.py', 'r', encoding='utf-8').read())
author = re.search(r'^(?P<name>[^<]+) <(?P<email>.*)>$', __author__)

# https://packaging.python.org/
setup(
    name='hc',
    version=__version__,
    description='Holiday converter tool',
    long_description=open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8').read(),
    url='https://gitlab.com/ypid/hc',
    author=author.group('name'),
    author_email=author.group('email'),
    # Basically redundant but when not specified `./setup.py --maintainer` will
    # return "UNKNOWN".
    maintainer=author.group('name'),
    maintainer_email=author.group('email'),
    license=__license__,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        # Could be supported but I don’t see a real need for this.
        # Unicode support would need to be worked around for Python 2 support.
        #  'Programming Language :: Python :: 2',
        #  'Programming Language :: Python :: 2.6',
        #  'Programming Language :: Python :: 2.7',
        #
        # Should match the versions listed in .gitlab-ci.yml and .travis.yml
        'Programming Language :: Python :: 3',
        # 3.2 basically works but the code coverage can not be tested on it as it
        # seems: https://travis-ci.org/ypid/hc/jobs/204811167
        # Dropping 3.2 from support matrix.
        #  'Programming Language :: Python :: 3.2',
        # JSON dump contains trailing whitespace in 3.3.
        # Dropping 3.3 from support matrix.
        #  'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Text Processing :: Markup :: HTML',
    ),
    keywords='school holidays schulferien germany',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'ruamel.yaml<0.15',
        'pyaml',
        'requests_cache',
        'xmltodict',
        'pyquery',
        'appdirs',
        'python-dateutil',
    ],
    extras_require={
        'test': [
            'nose',
            'nose2',
            'freezegun',
            'tox',
            'flake8',
            'pylint',
            'coverage',
            'yamllint',
        ],
        #  'docs': [],  # See docs/requirements.txt
    },
    entry_points={
        'console_scripts': [
            'hc = hc.cli:main',
        ],
    },
)
