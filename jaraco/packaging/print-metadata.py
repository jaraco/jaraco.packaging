from . import metadata


def main():
    """
    >>> main()
    Metadata-Version: ...
    """
    md = metadata.load('.')
    # cannot print(md) due to python/cpython#119650
    for key, value in md.items():
        print(key, value, sep=': ')


__name__ == '__main__' and main()
