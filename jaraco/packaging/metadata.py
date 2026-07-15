from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from _typeshed import StrPath

Metadata = dict[str, Any]
"""
Core metadata as the JSON mapping emitted by ``python -m build --metadata``.

Field names are lower-cased with dashes replaced by underscores (e.g.
``Author-email`` becomes ``author_email``) and multi-valued fields such as
``Project-URL`` are collapsed into structured values (``project_urls`` is a
mapping of label to URL). This is a different shape than the
``email.message.Message`` returned by the former ``build.util`` helper.
"""


def load(
    source_dir: StrPath,
    isolated: bool = os.environ.get('BUILD_ENVIRONMENT', 'isolated') == 'isolated',
) -> Metadata:
    """
    Load and return the metadata for the project at ``source_dir``.

    Generates the metadata by invoking ``python -m build --metadata`` in a
    subprocess, per the recommendation that deprecated
    ``build.util.project_wheel_metadata``, and returns the parsed JSON mapping.
    Allows overriding the isolation behavior at the environment level.
    """
    cmd = [sys.executable, '-m', 'build', '--metadata']
    if not isolated:
        cmd.append('--no-isolation')
    cmd.append(os.fspath(source_dir))
    out = subprocess.run(
        cmd, check=True, capture_output=True, text=True, encoding='utf-8'
    ).stdout
    meta: Metadata = json.loads(out)
    return meta


def hunt_down_url(meta: Metadata) -> str | None:
    """
    Given project metadata, figure out what the package URL is.

    >>> hunt_down_url(load('.'))
    'https://github.com/jaraco/jaraco.packaging'
    """
    return meta.get('home_page') or get_best(meta.get('project_urls', {}))


def get_best(project_urls: Mapping[str, str]) -> str | None:
    return project_urls.get('Source') or project_urls.get('Homepage')


def get_source_url(meta: Metadata) -> str | None:
    """
    Given project metadata, return the Source URL from the project URLs.

    >>> get_source_url(load('.'))
    'https://github.com/jaraco/jaraco.packaging'
    >>> get_source_url({}) is None
    True
    """
    project_urls: Mapping[str, str] = meta.get('project_urls', {})
    return project_urls.get('Source')


combo_re = r'["]?(?P<name>\w[\w\s.]*?)["]?\s+<(?P<email>\w+@[\w.]+)>'
"""The pattern for matching name and email from *-email fields."""


def extract_author(meta: Metadata) -> str:
    """
    Given project metadata, figure out who the author is.

    The metadata is so irregular, just make some inferences and refine.

    This form comes from a setup.cfg file or setup.py.

    >>> extract_author({'author': 'Jason R. Coombs'})
    'Jason R. Coombs'
    >>> extract_author({'author': 'Foo Bar, Bing Baz'})
    'Foo Bar, Bing Baz'

    This form comes from pyproject.toml converted from the above config.

    >>> extract_author({'author_email': '"Jason R. Coombs" <jaraco@contoso.com>'})
    'Jason R. Coombs'
    >>> extract_author({'author_email': 'Foo Bar <foo@bar.name>, Bing Baz <bing@baz.name>'})
    'Foo Bar, Bing Baz'
    """
    author: str | None = meta.get('author')
    email: str = meta.get('author_email', '')
    return author or ', '.join(
        match.group('name') for match in re.finditer(combo_re, email)
    )


def extract_email(meta: Metadata) -> str:
    """
    Given project metadata, figure out the author's email.

    The metadata is so irregular, just make some inferences and refine.

    This form comes from a setup.cfg file or setup.py.

    >>> extract_email({'author_email': 'jaraco@contoso.com'})
    'jaraco@contoso.com'
    >>> extract_email({'author_email': 'foo@bar.name, bing@baz.name'})
    'foo@bar.name, bing@baz.name'

    This form comes from pyproject.toml converted from the above config.

    >>> extract_email({'author_email': '"Jason R. Coombs" <jaraco@contoso.com>'})
    'jaraco@contoso.com'
    >>> extract_email({'author_email': 'Foo Bar <foo@bar.name>, Bing Baz <bing@baz.name>'})
    'foo@bar.name, bing@baz.name'
    """
    email: str = meta['author_email']
    if '<' not in email:
        return email
    return ', '.join(match.group('email') for match in re.finditer(combo_re, email))
