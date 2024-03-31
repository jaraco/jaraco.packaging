import os

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
