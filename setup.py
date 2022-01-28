#!/usr/bin/env python3

import pathlib
import pkg_resources
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


def get_requirements():
    return get_file('requirements.txt').splitlines()


setup(
    name='social-downloader',
    version=get_version(),
    url='https://github.com/AivGitHub/social_downloader',
    project_urls={
        'Source': 'https://github.com/AivGitHub/social_downloader',
        'Bug Tracker': 'https://github.com/AivGitHub/social_downloader/issues',
    },
    license='MIT',
    #TODO:
    # author='',
    # author_email='',
    description='Social media downloader',
    long_description=get_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    package_data={
        '': ['../requirements.txt'],
    }
)
