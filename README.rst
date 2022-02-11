.. image:: https://img.shields.io/pypi/v/jaraco.packaging.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/jaraco.packaging.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/jaraco.packaging

.. image:: https://github.com/jaraco/jaraco.packaging/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.packaging/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://readthedocs.org/projects/jaracopackaging/badge/?version=latest
   :target: https://jaracopackaging.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2022-informational
   :target: https://blog.jaraco.com/skeleton

Tools for packaging.

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

make-tree
=========

A utility for taking output from ``pipdeptree --json`` and producing a tree
rooted at a given package.

Usage::

    pipdeptree --json | python -m jaraco.packaging.make-tree mypkg
