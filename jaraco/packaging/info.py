import subprocess
import re

import six

import setuptools


class Show(setuptools.Command):
    description = "Report attributes of a distribution's metadata"
    user_options = [
        (str('attributes='), str('a'), "space or comma-separated attributes"),
    ]

    def finalize_options(self):
        if isinstance(self.attributes, six.string_types):
            self.attributes = re.split('[, ]', self.attributes)

    def initialize_options(self):
        self.attributes = 'name', 'version'

    def _lookup_attribute(self, attr_name):
        method_name = 'get_' + attr_name
        return getattr(self.distribution, method_name)()

    def run(self):
        values = map(self._lookup_attribute, self.attributes)
        str_values = map(str, values)
        print(subprocess.list2cmdline(str_values))
