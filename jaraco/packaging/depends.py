"""
This module should only import modules from stdlib and setuptools
"""

from __future__ import print_function

import os
import re
import argparse
import subprocess

import pkg_resources

def tree_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('requirement', help="A setuptools requirement "
        "spec (e.g. 'eggmonster' or 'eggmonster==0.1')")
    parser.add_argument('--python', help="Use a remote environment rather "
        "than the local one.")
    args = parser.parse_args()
    if args.python:
        return check_dependencies_remote(args)
    check_dependencies(args.requirement)

def print_package(requirement, indent):
    r = requirement
    print('  ' * indent + str(r), '[{0}]'.format(
        pkg_resources.get_distribution(r))
        )

def parse_extras(req):
    pattern = re.compile('\[(.*)\]')
    res = pattern.search(unicode(req))
    return res.group(1).split(',') if res else []

def check_dependencies(req, indent=1, history=None):
    """
    Given a setuptools package requirement (e.g. 'gryphon==2.42' or just
    'gryphon'), print a tree of dependencies as they resolve in this
    environment.
    """
    # keep a history to avoid infinite loops
    if history is None: history = set()
    if req in history: return
    history.add(req)
    d = pkg_resources.get_distribution(req)
    extras = parse_extras(req)
    if indent == 1:
        print_package(req, 0)
    for r in d.requires(extras=extras):
        print_package(r, indent)
        check_dependencies(r, indent + 1, history)

def check_dependencies_remote(args):
    """
    Invoke this command on a remote Python.
    """
    cmd = [args.python, '-m', 'depends', args.requirement]
    env = dict(PYTHONPATH=os.path.dirname(__file__))
    return subprocess.check_call(cmd, env=env)

if __name__ == '__main__':
    tree_cmd()