"""
This module is a Sphinx plugin. Add ``jaraco.packaging.sphinx``
to conf.py, and the setup hook does the rest.

>>> 'setup' in globals()
True
"""

import os
import subprocess
from email import message_from_string as load_metadata_from_wheel
from zipfile import ZipFile

from build.util import project_wheel_metadata as load_metadata_from_source
from jaraco.context import suppress

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore


if 'check_output' not in dir(subprocess):
    import subprocess32 as subprocess  # type: ignore


def setup(app):
    app.add_config_value('package_url', '', '')
    app.connect('builder-inited', load_config_from_setup)
    app.connect('builder-inited', configure_substitutions)
    app.connect('html-page-context', add_package_url)
    return dict(version=metadata.version('jaraco.packaging'), parallel_read_safe=True)


@suppress(KeyError)
def _load_metadata_from_wheel():
    """
    If indicated by an environment variable, expect the metadat
    to be present in a wheel and load it from there, avoiding
    the build process. Ref jaraco/jaraco.packaging#7.
    """
    with ZipFile(os.environ['JARACO_PACKAGING_SPHINX_WHEEL']) as wheel:
        meta = None
        for name in wheel.namelist():
            if '.dist-info' in name and name.endswith("METADATA"):
                return load_metadata_from_wheel(wheel.read(name).decode())
        if meta is None:
            raise RuntimeError(
                "The environment variable JARACO_PACKAGING_SPHINX_WHEEL "
                "points to a file not containing metadata."
            )


def load_config_from_setup(app):
    """
    Replace values in app.config from package metadata
    """
    # for now, assume project root is one level up
    root = os.path.join(app.confdir, '..')
    meta = _load_metadata_from_wheel() or load_metadata_from_source(root)
    app.config.project = meta['Name']
    app.config.version = app.config.release = meta['Version']
    app.config.package_url = meta['Home-page']
    app.config.author = app.config.copyright = meta['Author']


def configure_substitutions(app):
    epilogs = app.config.rst_epilog, f'.. |project| replace:: {app.config.project}'
    app.config.rst_epilog = '\n'.join(filter(None, epilogs))


def add_package_url(app, pagename, templatename, context, doctree):
    context['package_url'] = app.config.package_url
