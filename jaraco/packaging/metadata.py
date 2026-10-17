from __future__ import annotations

import os
import pathlib
import re
import tempfile
from collections.abc import Iterable
from importlib import metadata as importlib_metadata
from typing import TYPE_CHECKING

import pyproject_hooks
from build import ProjectBuilder
from build.env import DefaultIsolatedEnv

if TYPE_CHECKING:
    from _typeshed import StrPath
    from importlib_metadata import PackageMetadata
    from pyproject_hooks import SubprocessRunner


def _prepared_metadata(builder: ProjectBuilder) -> PackageMetadata:
    """
    Prepare the wheel metadata and load it in-process.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = pathlib.Path(builder.metadata_path(tmpdir))
        metadata = importlib_metadata.PathDistribution(path).metadata
        assert metadata is not None
        return metadata


def load(
    source_dir: StrPath,
    isolated: bool = os.environ.get('BUILD_ENVIRONMENT', 'isolated') == 'isolated',
    *,
    runner: SubprocessRunner = pyproject_hooks.quiet_subprocess_runner,
) -> PackageMetadata:
    """
    Load and return the metadata for the project at ``source_dir``.

    Reimplements the (now deprecated) ``build.util.project_wheel_metadata``
    in-process via build's public ``ProjectBuilder`` API, avoiding the
    subprocess-based ``python -m build --metadata`` replacement and preserving
    the ``PackageMetadata`` return type. Allows overriding the isolation
    behavior at the environment level.
    """
    if not isolated:
        return _prepared_metadata(ProjectBuilder(source_dir, runner=runner))
    with DefaultIsolatedEnv() as env:
        builder = ProjectBuilder.from_isolated_env(env, source_dir, runner=runner)
        env.install(builder.build_system_requires)
        env.install(builder.get_requires_for_build('wheel'))
        return _prepared_metadata(builder)


def hunt_down_url(meta: PackageMetadata) -> str | None:
    """
    Given project metadata, figure out what the package URL is.

    >>> hunt_down_url(load('.'))
    'https://github.com/jaraco/jaraco.packaging'
    """
    return meta.get('Home-page') or get_best(meta.get_all('Project-URL', ()))


def get_best(project_urls: Iterable[str]) -> str | None:
    lookup = dict(url.split(', ') for url in project_urls)
    return lookup.get('Source') or lookup.get('Homepage')


def get_source_url(meta: PackageMetadata) -> str | None:
    """
    Given project metadata, return the Source URL from Project-URL entries.

    >>> get_source_url(load('.'))
    'https://github.com/jaraco/jaraco.packaging'
    >>> import email.message
    >>> get_source_url(email.message.Message()) is None
    True
    """
    lookup = dict(url.split(', ', 1) for url in meta.get_all('Project-URL', ()))
    return lookup.get('Source')


combo_re = r'["]?(?P<name>\w[\w\s.]*?)["]?\s+<(?P<email>\w+@[\w.]+)>'
"""The pattern for matching name and email from *-email fields."""


def extract_author(meta: PackageMetadata) -> str:
    """
    Given project metadata, figure out who the author is.

    The metadata is so irregular, just make some inferences and refine.

    This form comes from a setup.cfg file or setup.py.

    >>> meta = {'Author': 'Jason R. Coombs'}
    >>> extract_author(meta)
    'Jason R. Coombs'
    >>> meta = {'Author': 'Foo Bar, Bing Baz'}
    >>> extract_author(meta)
    'Foo Bar, Bing Baz'

    This form comes from pyproject.toml converted from the above config.

    >>> meta = {'Author-email': '"Jason R. Coombs" <jaraco@contoso.com>'}
    >>> extract_author(meta)
    'Jason R. Coombs'
    >>> meta = {'Author-email': 'Foo Bar <foo@bar.name>, Bing Baz <bing@baz.name>'}
    >>> extract_author(meta)
    'Foo Bar, Bing Baz'
    """
    return meta.get('Author') or ', '.join(
        match.group('name') for match in re.finditer(combo_re, meta['Author-email'])
    )


def extract_email(meta: PackageMetadata) -> str:
    """
    Given project metadata, figure out the author's email.

    The metadata is so irregular, just make some inferences and refine.

    This form comes from a setup.cfg file or setup.py.

    >>> meta = {'Author-email': 'jaraco@contoso.com'}
    >>> extract_email(meta)
    'jaraco@contoso.com'
    >>> meta = {'Author-email': 'foo@bar.name, bing@baz.name'}
    >>> extract_email(meta)
    'foo@bar.name, bing@baz.name'

    This form comes from pyproject.toml converted from the above config.

    >>> meta = {'Author-email': '"Jason R. Coombs" <jaraco@contoso.com>', 'Author': None}
    >>> extract_email(meta)
    'jaraco@contoso.com'
    >>> meta = {'Author-email': 'Foo Bar <foo@bar.name>, Bing Baz <bing@baz.name>', 'Author': None}
    >>> extract_email(meta)
    'foo@bar.name, bing@baz.name'
    """
    if '<' not in meta['Author-email']:
        return meta['Author-email']
    return ', '.join(
        match.group('email') for match in re.finditer(combo_re, meta['Author-email'])
    )
