#!/usr/bin/env python

from setuptools import setup, find_packages

# Get version string
with open('gdx2py/version.py') as f: exec(f.read())

setup(name='GDX2py',
      version=__version__,  # pylint: disable=undefined-variable
      author='Erkka Rinne',
      author_email='erkka.rinne@vtt.fi',
      description='Read and write GAMS Data eXchange (GDX) files using Python',
      python_requires='>=3.6',
      install_requires=[
        'gdxcc>=7',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'pytest-datadir'],
      url='https://github.com/ererkka/GDX2py',
      packages=find_packages(exclude=['tests']),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"
    ],
)
