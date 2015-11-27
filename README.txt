jaraco.packaging
================

Tools for packaging.

dependency_tree
---------------

A distutils command for reporting the dependency tree as resolved
by setuptools. Use after installing a package.

show
----

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
