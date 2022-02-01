#!/usr/bin/env python3

import pathlib
import sys

from setuptools import find_packages, setup


MINIMAL_PY_VERSION = (3, 6)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('This app works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_file(rel_path):
    return (pathlib.Path(__file__).parent / rel_path).read_text('utf-8')


def get_version():
    for line in get_file('downloader/__init__.py').splitlines():
        if line.startswith('__version__'):
            return line.split()[2][1:-1]


setup(
    name='social-downloader',
    version=get_version(),
    url='https://github.com/AivGitHub/social_downloader',
    project_urls={
        'Source': 'https://github.com/AivGitHub/social_downloader',
        'Bug Tracker': 'https://github.com/AivGitHub/social_downloader/issues',
    },
    license='MIT',
    author='Ivan Koldakov',
    author_email='coldie322@gmail.com',
    description='Social media downloader',
    long_description=get_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'certifi==2021.10.8',
        'charset-normalizer==2.0.10',
        'idna==3.3',
        'requests==2.27.1',
        'urllib3==1.26.8',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
