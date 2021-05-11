#!/usr/bin/env python
import setuptools

import jsonscribe

setuptools.setup(
    name='json-scribe',
    version=jsonscribe.version,
    description='JSON-based logging for the masses',
    long_description=open('README.rst').read(),
    url='https://github.com/aweber/json-scribe',
    author='AWeber Communications, Inc',
    author_email='api@aweber.com',
    packages=['jsonscribe'],
    install_requires=[],
    extras_require={
        'dev': [
            'coverage==5.5',
            'flake8==3.9.2',
            'Sphinx==4.0.1',
            'readme-renderer==21.0',
            'wheel==0.36.2',
            'yapf==0.22.0',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
