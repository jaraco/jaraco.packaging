"""
This module is a Sphinx plugin. Add ``jaraco.packaging.sphinx``
to conf.py, and the setup hook does the rest.

>>> 'setup' in globals()
True
"""

import os

from build.util import project_wheel_metadata as load_metadata
from jaraco.context import suppress

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore


def setup(app):
    app.add_config_value('package_url', '', '')
    app.connect('builder-inited', load_config_from_setup)
    app.connect('builder-inited', configure_substitutions)
    app.connect('html-page-context', add_package_url)
    return dict(version=metadata.version('jaraco.packaging'), parallel_read_safe=True)


@suppress(KeyError)
def _load_metadata_from_wheel():
    """
    If indicated by an environment variable, expect the metadata
    to be present in a wheel and load it from there, avoiding
    the build process. Ref jaraco/jaraco.packaging#7.

    >>> _load_metadata_from_wheel()
    >>> getfixture('static_wheel')
    >>> meta = _load_metadata_from_wheel()
    >>> meta['Name']
    'sampleproject'
    """
    wheel = os.environ['JARACO_PACKAGING_SPHINX_WHEEL']
    (dist,) = metadata.distributions(path=[wheel])
    return dist.metadata


def load_config_from_setup(app):
    """
    Replace values in app.config from package metadata
    """
    # for now, assume project root is one level up
    root = os.path.join(app.confdir, '..')
    meta = _load_metadata_from_wheel() or load_metadata(root)
    app.config.project = meta['Name']
    app.config.version = app.config.release = meta['Version']
    app.config.package_url = meta['Home-page']
    app.config.author = app.config.copyright = meta['Author']


def configure_substitutions(app):
    epilogs = app.config.rst_epilog, f'.. |project| replace:: {app.config.project}'
    app.config.rst_epilog = '\n'.join(filter(None, epilogs))


def add_package_url(app, pagename, templatename, context, doctree):
    context['package_url'] = app.config.package_url
