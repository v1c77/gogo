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
    install_requires=[
        'futures>=3.2.0',
        'Geohash==1.0',
        'google-api-python-client>=1.7.4',
        'google-auth>=1.5.0',
        'google-auth-httplib2>=0.0.3',
        'grpcio>=1.14.0',
        'grpcio-tools>=1.14.0',
        'ipython==5.7.0',
        'ipython-genutils==0.2.0',
        'protobuf>=3.6.0',
        'pymongo>=3.7.1',
        'six>=1.11.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',  # fixme change when needed.
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.7",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
