# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('gogo/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


def _get_requirements():
    requirement_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'requirements_2.txt')
    return open(requirement_file).readlines()


setup(
    name='gogo',
    version=version,
    url='http://github.com/v1c77/gogo',
    license='WTFPL',
    author='v1c77',
    author_email='heyuhuade@gmail.com',
    description='grpc dev toolkit',
    include_package_data=True,
    packages=['gogo'],
    zip_safe=False,
    platforms='any',
    install_requires=_get_requirements(),
    classifiers=[
        'Development Status :: 1 - Planning',  # fixme change when needed.
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.7",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
