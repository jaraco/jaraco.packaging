v10.2.2
=======

Bugfixes
--------

- Fixed DeprecationWarning in metadata.hunt_down_url.


v10.2.1
=======

Bugfixes
--------

- Fixed issue in rendering non-unique keys in print-metadata.


v10.2.0
=======

Features
--------

- Add script for printing metadata.


v10.1.0
=======

Features
--------

- Add metadata.extract_email helper. Ref jaraco/jaraco.media#2.


v10.0.0
=======

Deprecations and Removals
-------------------------

- Moved metadata helpers to metadata module.


v9.7.1
======

Bugfixes
--------

- In extract_author, expand the logic to support multiple authors in pyproject.toml form.


v9.7.0
======

Features
--------

- Configure Sphinx earlier in 'config-inited', allowing other etxensions to rely on the produced values. (#16)


v9.6.0
======

Features
--------

- Add support for other metadata fields since pyproject.toml shuffles things around. (#17)


v9.5.0
======

Features
--------

- Add ``metadata.load`` for loading metadata from a source dir with support for a BUILD_ENVIRONMENT setting. Set BUILD_ENVIRONMENT=current to bypass isolation when loading metadata. Ref pypa/build#556. (#556)


v9.4.0
======

Features
--------

- Deprecated use of environment variable for isolated builds. The workaround is in the wrong place and should be dealt with upstream. (#11)


v9.3.0
======

Features
--------

- Add sidebar-links directive.
- Require Python 3.8 or later.


v9.2.0
======

#7, #10, #11: Added environment variable to bypass
building metadata for offline builds.

v9.1.2
======

#6: Added minimal test to ``sphinx.packaging``.

v9.1.1
======

Change requirement to ``build[virtualenv]`` as workaround for
`pypa/build#266 <https://github.com/pypa/build/issues/266>`_.

v9.1.0
======

Prefer ``build`` to ``pep517`` for loading package metadata.

v9.0.0
======

Use pep517.meta to load package metadata. Adds support
for packages without setup.py.

Removed info module (and setuptools show command).

Removed depends module. Use other packaging tools instead.

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
