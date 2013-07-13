#!/usr/bin/env python

"""
Script to fully automate the release process. Requires Python 2.6+
with sphinx installed and the 'hg' command on the path.
"""

from __future__ import print_function, absolute_import

import subprocess
import shutil
import os
import sys
import getpass
import collections
import re
import importlib
import imp

import requests

try:
    input = raw_input
except NameError:
    pass

try:
    dot = sys.path.pop(0)
    import keyring
    sys.path.insert(0, dot)
except Exception:
    pass

# each package may provide this module to override default behavior
try:
    import release
except ImportError:
    release = imp.new_module('release')

defaults = dict(
    package_index='https://pypi.python.org/pypi',
    files_with_versions=['setup.py'],
)
"Default release definition"

def set_versions():
    prompt = "Release as version [%(version)s]> " % vars(release)
    version = input(prompt) or release.version
    if version != release.version:
        release.version = bump_versions(version)

def infer_next_version(version):
    """
    Infer a next version from the current version by incrementing the last
    number or appending a number.

    >>> infer_next_version('1.0')
    '1.1'

    >>> infer_next_version('1.0b')
    '1.0b1'

    >>> infer_next_version('1.0.10')
    '1.0.10'

    >>> infer_next_version('1')
    '2'

    >>> infer_next_version('')
    '1'
    """
    def incr(match):
        ver = int(match.group(0) or '0')
        return str(ver + 1)
    return re.sub('\d*$', incr, version)

def get_repo_name():
    """
    Get the repo name from the hgrc default path.
    """
    default = subprocess.check_output('hg paths default').strip().decode('utf-8')
    parts = default.split('/')
    if parts[-1] == '':
        parts.pop()
    return '/'.join(parts[-2:])

def get_mercurial_creds(system='https://bitbucket.org', username=None):
    """
    Return named tuple of username,password in much the same way that
    Mercurial would (from the keyring).
    """
    # todo: consider getting this from .hgrc
    username = username or getpass.getuser()
    keyring_username = '@@'.join((username, system))
    system = 'Mercurial'
    password = (
        keyring.get_password(system, keyring_username)
        if 'keyring' in globals()
        else None
    )
    if not password:
        password = getpass.getpass()
    Credential = collections.namedtuple('Credential', 'username password')
    return Credential(username, password)

def add_milestone_and_version(version):
    base = 'https://api.bitbucket.org'
    for type in 'milestones', 'versions':
        url = (base + '/1.0/repositories/{repo}/issues/{type}'
            .format(repo = get_repo_name(), type=type))
        resp = requests.post(url=url,
            data='name='+version, auth=get_mercurial_creds())
        resp.raise_for_status()

def bump_versions(target_ver):
    for filename in release.files_with_versions:
        bump_version(filename, target_ver)
    subprocess.check_call(['hg', 'ci', '-m',
        'Bumped to {target_ver} in preparation for next '
        'release.'.format(**vars())])
    return target_ver

def bump_version(filename, target_ver):
    orig_ver = release.version
    with open(filename, 'rb') as f:
        lines = [
            line.replace(orig_ver.encode('ascii'), target_ver.encode('ascii'))
            for line in f
        ]
    with open(filename, 'wb') as f:
        f.writelines(lines)

def load_defaults():
    for key in defaults:
        vars(release).setdefault(key, defaults[key])
    if not 'version' in vars(release):
        release.version = load_version_from_setup()

def load_version_from_setup():
    setup = importlib.import_module('setup')
    return setup.setup_params['version']

def do_release():
    load_defaults()

    assert all(map(os.path.exists, release.files_with_versions)), (
        "Expected file(s) missing")

    assert has_sphinx(), "You must have Sphinx installed to release"

    set_versions()

    res = input('Have you read through the SCM changelog and '
        'confirmed the changelog is current for releasing {version}? '
        .format(**vars(release)))
    if not res.lower().startswith('y'):
        print("Please do that")
        raise SystemExit(1)

    if 'test_info' in vars(release):
        print(release.test_info)
    res = input('Have you or has someone verified that the tests '
        'pass on this revision? ')
    if not res.lower().startswith('y'):
        print("Please do that")
        raise SystemExit(2)

    subprocess.check_call(['hg', 'tag', release.version])

    subprocess.check_call(['hg', 'update', release.version])

    getattr(release, 'before_upload', lambda: None)()

    upload_to_pypi()
    upload_ez_setup()

    # update to the tip for the next operation
    subprocess.check_call(['hg', 'update'])

    # we just tagged the current version, bump for the next release.
    next_ver = bump_versions(infer_next_version(release.version))

    # push the changes
    subprocess.check_call(['hg', 'push'])

    add_milestone_and_version(next_ver)

def upload_to_pypi():
    has_docs = build_docs()
    if os.path.isdir('./dist'):
        shutil.rmtree('./dist')
    cmd = [
        sys.executable, 'setup.py', '-q',
        'egg_info', '-RD', '-b', '',
        'sdist',
        'register', '-r', release.package_index,
        'upload', '-r', release.package_index,
    ]
    if has_docs:
        cmd.extend([
            'upload_docs', '-r', release.package_index
        ])
    env = os.environ.copy()
    env["SETUPTOOLS_INSTALL_WINDOWS_SPECIFIC_FILES"] = "1"
    subprocess.check_call(cmd, env=env)

def upload_ez_setup():
    """
    TODO: upload ez_setup.py to a permalinked location. Currently, this
    location is https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py .
    In the long term, it should be on PyPI.
    """

def has_sphinx():
    try:
        devnull = open(os.path.devnull, 'wb')
        subprocess.Popen(['sphinx-build', '--version'], stdout=devnull,
            stderr=subprocess.STDOUT).wait()
    except Exception:
        return False
    return True

def build_docs():
    if not os.path.isdir('docs'):
        return
    if os.path.isdir('docs/build'):
        shutil.rmtree('docs/build')
    cmd = [
        'sphinx-build',
        '-b', 'html',
        '-d', 'build/doctrees',
        '.',
        'build/html',
    ]
    subprocess.check_call(cmd, cwd='docs')
    return True

if __name__ == '__main__':
    do_release()