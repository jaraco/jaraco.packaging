import os
import sys
import subprocess

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
    setup_script = os.path.join(root, 'setup.py')
    fields = ['--name', '--version', '--url', '--author']
    dist_info_cmd = [sys.executable, setup_script] + fields
    output = subprocess.check_output(dist_info_cmd, cwd=root, universal_newlines=True)
    outputs = output.strip().split('\n')
    try:
        project, version, url, author = outputs
    except ValueError:
        raise ValueError("Unexpected metadata output", output)
    app.config.project = project
    app.config.version = app.config.release = version
    app.config.package_url = url
    app.config.author = app.config.copyright = author


def configure_substitutions(app):
    epilogs = app.config.rst_epilog, f'.. |project| replace:: {app.config.project}'
    app.config.rst_epilog = '\n'.join(filter(None, epilogs))


def add_package_url(app, pagename, templatename, context, doctree):
    context['package_url'] = app.config.package_url
