3.2
===

Add Python 2.6 support for Sphinx extension.

3.1
===

Added Sphinx extension for loading several keys from
their package metadata.

3.0
===

Removed pmxbot uploader.

2.11
====

Moved hosting to Github.

Add support for retaining the active bookmark after
updating to tagged revision for release.

2.10
====

``release`` script no longer invokes register prior to the
upload. Instead, the user should either set the password
in .pypirc (not recommended) or use Setuptools 20.1 and
keyring to store the password securely.

2.9
===

Add ``show`` distutils command for showing attributes of the
distribution.

2.8
===

Add ``packaging.depends.load_dependencies``.

2.7
===

Added ``--register`` option to ``upload-package`` command.

2.4
===

Added ``jaraco.packaging.cheese`` and the ``upload-package`` command from the
YouGov project of the same namesake.

2.3
===

Add 'dist_commands' to config so projects released with
``jaraco.packaging.release`` can specify which dist commands are run.

2.2
===

Added ``depends`` module implementing a ``dependency-tree`` command and
also a distutils Command ``dependency_tree``.
