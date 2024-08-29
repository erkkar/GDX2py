# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2024-08-20
### Changed
* Require `gamsapi` instead of `gdxcc`, because `gdxcc` is now part of GAMS API and 
not its own package. This change provides support for Python 3.12 without the need 
to install Microsoft Visual Studio Build Tools for Windows.

# Removed
* Support for Python 3.6 and 3.7

## [2.1.1] - 2020-08-20
### Added
* Add index names from symbol domain if defined when converting to a pandas object.

### Fixed
* Representation of `GdxFile` object’s keys view was broken

## [2.1.0] - 2020-07-09
### Added
* Convert a GAMS symbol to pandas object using `to_pandas()` method.
