.. image:: https://img.shields.io/pypi/v/jaraco.packaging.svg
   :target: https://pypi.org/project/jaraco.packaging

.. image:: https://img.shields.io/pypi/pyversions/jaraco.packaging.svg

.. image:: https://img.shields.io/pypi/dm/jaraco.packaging.svg

.. image:: https://img.shields.io/travis/jaraco/jaraco.packaging/master.svg
   :target: http://travis-ci.org/jaraco/jaraco.packaging

Tools for packaging.

License
=======

License is indicated in the project metadata (typically one or more
of the Trove classifiers). For more details, see `this explanation
<https://github.com/jaraco/skeleton/issues/1>`_.

dependency_tree
===============

A distutils command for reporting the dependency tree as resolved
by setuptools. Use after installing a package.

show
====

A distutils command for reporting the attributes of a distribution,
such as the version or author name. Here are some examples against
this package::

    $ python -q setup.py show
    jaraco.packaging 2.8.2.dev1+nfaae9fb96b36.d20151127
    $ python -q setup.py show --attributes version
    2.8.2.dev1+nfaae9fb96b36.d20151127
    $ python -q setup.py show --attributes author,author_email
    "Jason R. Coombs" jaraco@jaraco.com
    $ python setup.py -q show --attributes classifiers
    "['Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3']"
    $ python setup.py -q show --attributes "description url"
    "tools to supplement packaging Python releases" https://bitbucket.org/jaraco/jaraco.packaging

Note that passing -q suppresses the "running show" message.

Attributes may be specified as comma-separated or space-separated keys.
Results are printed using ``subprocess.list2cmdline`` so may be parsed using
``shlex.split``. By default, 'name' and 'version' are printed.

sphinx
======

This package provides a Sphinx extension that will inject into the config
the following values from the project's package metadata (as presented by
distutils):

 - project (from name)
 - author
 - copyright (same as author)
 - version
 - release (same as version)
 - package_url (from url)

To enable, include 'jaraco.packaging' in your requirements and add
'jaraco.packaging.sphinx' to your list of extensions in your config file::

    extensions=['jaraco.packaging.sphinx']
