#!/usr/bin/env python

from setuptools import setup, find_packages

from gdx2py import __version__

setup(name='GDX2py',
      version=__version__,
      author='Erkka Rinne',
      author_email='erkka.rinne@vtt.fi',
      description='Read and write GAMS Data eXchange (GDX) files using Python',
      install_requires=[
        'gdxcc>=7',
        'numpy>=1.10',
        'pandas>=0.17.1'
      ],
      url='https://github.com/ererkka/GDX2py',
      packages=find_packages(),
)
