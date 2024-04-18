import os
import re

from build import util


def load(
    source_dir: util.StrPath,
    isolated: bool = os.environ.get('BUILD_ENVIRONMENT', 'isolated') == 'isolated',
    **kwargs,
):
    """
    Allow overriding the isolation behavior at the enviroment level.
    """
    return util.project_wheel_metadata(source_dir, isolated, **kwargs)


def hunt_down_url(meta):
    """
    Given project metadata, figure out what the package URL is.
    """
    return meta['Home-page'] or get_best(meta.get_all('Project-URL'))


def get_best(project_urls):
    lookup = dict(url.split(', ') for url in project_urls)
    return lookup.get('Source') or lookup.get('Homepage')


def extract_author(meta):
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

    >>> meta = {'Author-email': '"Jason R. Coombs" <jaraco@contoso.com>', 'Author': None}
    >>> extract_author(meta)
    'Jason R. Coombs'
    >>> meta = {'Author-email': 'Foo Bar <foo@bar.name>, Bing Baz <bing@baz.name>', 'Author': None}
    >>> extract_author(meta)
    'Foo Bar, Bing Baz'
    """
    return meta['Author'] or ', '.join(
        match.group('name')
        for match in re.finditer(
            r'["]?(?P<name>\w[\w\s.]*?)["]?\s+<\w+@[\w.]+>', meta['Author-email']
        )
    )
