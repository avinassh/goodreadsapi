#!/usr/bin/env python

from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (ImportError, IOError):
    long_description = open('README.md').read()

version = '0.1'

setup(
    name='goodreadsapi',
    version=version,
    author='Avinash Sajjanshetty',
    author_email='hi@avi.im',
    py_modules=['goodreadsapi'],
    url='https://github.com/avinassh/goodreadsapi/',
    license='MIT',
    description='Simple wrapper for Goodreads API',
    long_description=long_description,
    install_requires=[
        'py-bing-search==0.2.6',
        'requests==2.12.3',
        'xmltodict==0.10.2'
    ],
    classifiers=[
        'Development Status :: 6 - Mature',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
