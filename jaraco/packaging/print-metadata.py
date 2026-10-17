from . import metadata


def main() -> None:
    """
    >>> main()
    author_email: ...
    ...
    name: jaraco.packaging
    ...
    """
    for key, value in sorted(metadata.load('.').items()):
        print(key, value, sep=': ')


if __name__ == '__main__':
    main()
