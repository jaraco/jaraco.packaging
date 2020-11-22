"""
This module should only import modules from stdlib and setuptools
"""

import os
import re
import argparse
import subprocess

import setuptools
import pkg_resources

text_type = getattr(__builtins__, 'unicode', str)

req_help = "A setuptools requirement spec (e.g. 'eggmonster' or " "'eggmonster==0.1')"
python_help = "Use a remote environment rather than the local one."


def tree_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('requirement', help=req_help)
    parser.add_argument('--python', help=python_help)
    args = parser.parse_args()
    if args.python:
        return check_dependencies_remote(args)
    check_dependencies(args.requirement)


def print_package(requirement, indent):
    r = requirement
    print('  ' * indent + str(r), '[{0}]'.format(pkg_resources.get_distribution(r)))


def parse_extras(req):
    pattern = re.compile(r'\[(.*)\]')
    res = pattern.search(text_type(req))
    return res.group(1).split(',') if res else []


def check_dependencies(req, indent=1, history=None):
    """
    Given a setuptools package requirement (e.g. 'gryphon==2.42' or just
    'gryphon'), print a tree of dependencies as they resolve in this
    environment.
    """
    # keep a history to avoid infinite loops
    if history is None:
        history = set()
    if req in history:
        return
    history.add(req)
    d = pkg_resources.get_distribution(req)
    extras = parse_extras(req)
    if indent == 1:
        print_package(req, 0)
    for r in d.requires(extras=extras):
        print_package(r, indent)
        check_dependencies(r, indent + 1, history)


def load_dependencies(req, history=None):
    """
    Load the dependency tree as a Python object tree,
    suitable for JSON serialization.

    >>> deps = load_dependencies('jaraco.packaging')
    >>> import json
    >>> doc = json.dumps(deps)
    """
    if history is None:
        history = set()
    dist = pkg_resources.get_distribution(req)
    spec = dict(requirement=str(req), resolved=str(dist))
    if req not in history:
        # traverse into children
        history.add(req)
        extras = parse_extras(req)
        depends = [
            load_dependencies(dep, history=history)
            for dep in dist.requires(extras=extras)
        ]
        if depends:
            spec.update(depends=depends)
    return spec


class DependencyTree(setuptools.Command):
    description = "Report a tree of resolved dependencies"
    user_options = [
        (str('requirement='), str('r'), req_help),
        (str('python='), str('p'), python_help),
    ]

    def finalize_options(self):
        pass

    def initialize_options(self):
        self.requirement = self.distribution.get_name()
        self.python = None

    def run(self):
        if self.python:
            return check_dependencies_remote(self)
        check_dependencies(self.requirement)


def check_dependencies_remote(args):
    """
    Invoke this command on a remote Python.
    """
    cmd = [args.python, '-m', 'depends', args.requirement]
    env = dict(PYTHONPATH=os.path.dirname(__file__))
    return subprocess.check_call(cmd, env=env)


if __name__ == '__main__':
    tree_cmd()
