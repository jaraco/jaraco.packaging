v8.2.1
======

Rely on PEP 420 for namespace package.

v8.2.0
======

Inject rst_epilog to include ``|project|`` substitution.

v8.1.1
======

Refresh package metadata.

v8.1.0
======

In ``sphinx`` when loading metadata, trap a ValueError to
include the offending value.

v8.0.0
======

Require Python 3.6 or later.

7.0
===

Removed 'cheese' package as it was built for a use-case that is
no longer needed, depends on deprecated functionality in
setuptools, and is causing errors in tests (SSL).

6.2
===

Sphinx plugin now declares support for parallel reads
(optimistically).

6.1
===

Sphinx plugin now exposes ``package_url`` in HTML templates.

6.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

5.2
===

Show command now also honors direct attributes on a
Distribution instance.

5.1.1
=====

#2: In Sphinx module, use universal newlines to avoid
broken results on Windows.

5.1
===

Added ``jaraco.packaging.make-tree`` utility for taking
output from pipdeptree and making a tree of it.

5.0
===

Drop support for Python 2.6.

Re-aligned to use pkg_resources-managed technique for
the jaraco namespace, all package of which must elect one
technique or another.

4.1
===

Use pkgutil for namespace package handling. Experimental
process based on pypa/python-packaging-user-guide#265.

4.0
===

Remove ``release`` module.

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
