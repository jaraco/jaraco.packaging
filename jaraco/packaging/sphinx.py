from __future__ import unicode_literals

import os
import sys
import subprocess


if 'check_output' not in dir(subprocess):
    import subprocess32 as subprocess


def setup(app):
    app.add_config_value('package_url', '', '')
    app.connect('builder-inited', load_config_from_setup)


def load_config_from_setup(app):
    """
    Replace values in app.config from package metadata
    """
    # for now, assume project root is one level up
    root = os.path.join(app.confdir, '..')
    setup_script = os.path.join(root, 'setup.py')
    fields = ['--name', '--version', '--url', '--author']
    dist_info_cmd = [sys.executable, setup_script] + fields
    output_bytes = subprocess.check_output(dist_info_cmd, cwd=root)
    outputs = output_bytes.decode('utf-8').strip().split('\n')
    project, version, url, author = outputs
    app.config.project = project
    app.config.version = app.config.release = version
    app.config.package_url = url
    app.config.author = app.config.copyright = author
