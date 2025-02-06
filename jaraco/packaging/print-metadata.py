from typing import TYPE_CHECKING, cast

from . import metadata

if TYPE_CHECKING:
    from importlib_metadata._adapters import Message


def main() -> None:
    """
    >>> main()
    Metadata-Version: ...
    """
    # cast: Default PathDistribution.metadata is a Message
    md = cast("Message", metadata.load('.'))
    # cannot print(md) due to python/cpython#119650
    for key, value in md.items():
        print(key, value, sep=': ')


if __name__ == '__main__':
    main()
