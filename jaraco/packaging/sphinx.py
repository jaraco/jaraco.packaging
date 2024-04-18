"""
This module is a Sphinx plugin. Add ``jaraco.packaging.sphinx``
to conf.py, and the setup hook does the rest.

>>> 'setup' in globals()
True
"""

import os
import warnings
from importlib import metadata
from typing import ClassVar

import docutils.statemachine
import domdf_python_tools.stringlist
import sphinx.util.docutils
from docutils.parsers.rst import directives

from jaraco.context import suppress

from . import metadata as jp_metadata


def setup(app):
    app.add_config_value('package_url', '', '')
    app.connect('config-inited', load_config_from_setup)
    app.connect('config-inited', configure_substitutions)
    app.connect('html-page-context', add_package_url)
    app.add_directive("sidebar-links", SidebarLinksDirective)
    return dict(version=metadata.version('jaraco.packaging'), parallel_read_safe=True)


class SidebarLinksDirective(sphinx.util.docutils.SphinxDirective):
    """
    Directive which adds a toctree to the sidebar containing links to the project home
    and PyPI repo.
    """

    has_content: ClassVar[bool] = True

    option_spec = {
        "pypi": directives.flag,
        "home": directives.flag,
        "caption": directives.unchanged_required,
    }

    def run(self):
        """
        Create the installation node.
        """

        if self.env.docname != self.env.config.master_doc:
            return []

        body = domdf_python_tools.stringlist.StringList([
            ".. toctree::",
            "    :hidden:",
        ])

        with body.with_indent("    ", 1):
            body.append(f":caption: {self.options.get('caption', 'Links')}")
            body.blankline()

            if "home" in self.options:
                body.append(f"Home <{self.env.config.package_url}>")
            if "pypi" in self.options:
                body.append(
                    f"PyPI <https://pypi.org/project/{self.env.config.project}>"
                )

            body.extend(self.content)

        body.blankline()
        body.blankline()

        only_node = sphinx.addnodes.only(expr="html")
        content_node = docutils.nodes.paragraph(rawsource=str(body))
        only_node += content_node
        self.state.nested_parse(
            docutils.statemachine.StringList(body), self.content_offset, content_node
        )

        return [only_node]


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
    warnings.warn(
        "JARACO_PACKAGING_SPHINX_WHEEL is deprecated; "
        "use BUILD_ENVIRONMENT=current instead",
        DeprecationWarning,
    )
    (dist,) = metadata.distributions(path=[wheel])
    return dist.metadata


def load_config_from_setup(app, config):
    """
    Replace values in app.config from package metadata
    """
    # for now, assume project root is one level up
    root = os.path.join(app.confdir, '..')
    meta = _load_metadata_from_wheel() or jp_metadata.load(root)
    config.project = meta['Name']
    config.version = config.release = meta['Version']
    config.package_url = jp_metadata.hunt_down_url(meta)
    config.author = config.copyright = jp_metadata.extract_author(meta)


def configure_substitutions(app, config):
    epilogs = config.rst_epilog, f'.. |project| replace:: {config.project}'
    config.rst_epilog = '\n'.join(filter(None, epilogs))


def add_package_url(app, pagename, templatename, context, doctree):
    context['package_url'] = app.config.package_url
