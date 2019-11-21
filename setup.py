#!/usr/bin/env python

from setuptools import setup, find_packages

# Get version string
with open('gdx2py/version.py') as f:
    exec(f.read())

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name='GDX2py',
    version=__version__,  # pylint: disable=undefined-variable
    author='Erkka Rinne',
    author_email='erkka.rinne@vtt.fi',
    description='Read and write GAMS Data eXchange (GDX) files using Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=['gdxcc>=7'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-datadir', 'pandas'],
    url='https://github.com/ererkka/GDX2py',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
    ],
    license="MIT",
)
