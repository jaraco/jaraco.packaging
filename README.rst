.. image:: https://img.shields.io/pypi/v/jaraco.packaging.svg
   :target: https://pypi.org/project/jaraco.packaging

.. image:: https://img.shields.io/pypi/pyversions/jaraco.packaging.svg

.. image:: https://github.com/jaraco/jaraco.packaging/actions/workflows/main.yml/badge.svg
   :target: https://github.com/jaraco/jaraco.packaging/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://readthedocs.org/projects/jaracopackaging/badge/?version=latest
   :target: https://jaracopackaging.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2024-informational
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

To enable, include 'jaraco.packaging' in the requirements and add
'jaraco.packaging.sphinx' to the list of extensions in a Sphinx config
file::

    extensions=['jaraco.packaging.sphinx']

The extension by default builds the project in an isolated environment in
order to extract the metadata. To build the documentation offline,
provide an already built wheel by setting the environment variable
``JARACO_PACKAGING_SPHINX_WHEEL`` to the path of the existing wheel.

make-tree
=========

A utility for taking output from ``pipdeptree --json`` and producing a tree
rooted at a given package.

Usage::

    pipdeptree --json | python -m jaraco.packaging.make-tree mypkg
