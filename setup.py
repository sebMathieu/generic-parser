# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='generic-parser',
    version='1.0.2',
    description='Generic text parser from a JSON structure using regex or separator.',
    long_description=readme,
    author='Sebastien Mathieu',
    author_email='smathieu@live.be',
    url='https://github.com/sebMathieu/generic-parser',
    license=license,
    install_requires=['docopt'],
    packages=find_packages(exclude=('tests', 'doc'))
)

