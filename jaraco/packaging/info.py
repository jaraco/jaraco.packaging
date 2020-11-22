import subprocess
import re

import setuptools


class Show(setuptools.Command):
    """
    >>> import sys, functools
    >>> show_cmd = [sys.executable, "setup.py", "show"]
    >>> run = functools.partial(
    ...     subprocess.check_output, universal_newlines=True)
    >>> print(run(show_cmd + ['-a', 'name']), end='')
    running show
    jaraco.packaging
    >>> print(run(show_cmd + ['-a', 'install_requires']), end='')
    running show
    ['setuptools']
    """

    description = "Report attributes of a distribution's metadata"
    user_options = [
        (str('attributes='), str('a'), "space or comma-separated attributes")
    ]

    def finalize_options(self):
        if isinstance(self.attributes, str):
            self.attributes = re.split('[, ]', self.attributes)

    def initialize_options(self):
        self.attributes = 'name', 'version'

    def _lookup_attribute(self, attr_name):
        return self._by_getter(attr_name) or self._by_attr(attr_name)

    def _by_attr(self, attr_name):
        return getattr(self.distribution, attr_name)

    def _by_getter(self, attr_name):
        method_name = 'get_' + attr_name
        try:
            method = getattr(self.distribution, method_name)
        except AttributeError:
            return
        return method()

    def run(self):
        values = map(self._lookup_attribute, self.attributes)
        str_values = map(str, values)
        print(subprocess.list2cmdline(str_values))
