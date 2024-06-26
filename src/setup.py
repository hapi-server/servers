from setuptools import setup, find_packages

import json
version = json.load(open('hapimeta/version.json'))['version']
setup(
  name='hapimeta',
  version=version,
  description='A package for getting metadata from HAPI servers.',
  author='Bob Weigel, Jeremy Faden',
  author_email='rweigel@gmu.edu',
  packages=find_packages(),
  install_requires=[]
)