import os
import subprocess
import pep517.meta

try:
    import importlib.metadata as imp_meta
except ImportError:
    import importlib_metadata as imp_meta  # type: ignore


if 'check_output' not in dir(subprocess):
    import subprocess32 as subprocess  # type: ignore


def setup(app):
    app.add_config_value('package_url', '', '')
    app.connect('builder-inited', load_config_from_setup)
    app.connect('builder-inited', configure_substitutions)
    app.connect('html-page-context', add_package_url)
    return dict(version=imp_meta.version('jaraco.packaging'), parallel_read_safe=True)


def load_config_from_setup(app):
    """
    Replace values in app.config from package metadata
    """
    # for now, assume project root is one level up
    root = os.path.join(app.confdir, '..')
    meta = pep517.meta.load(root).metadata
    app.config.project = meta['Name']
    app.config.version = app.config.release = meta['Version']
    app.config.package_url = meta['Home-page']
    app.config.author = app.config.copyright = meta['Author']


def configure_substitutions(app):
    epilogs = app.config.rst_epilog, f'.. |project| replace:: {app.config.project}'
    app.config.rst_epilog = '\n'.join(filter(None, epilogs))


def add_package_url(app, pagename, templatename, context, doctree):
    context['package_url'] = app.config.package_url
