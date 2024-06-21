from . import metadata


def main():
    md = metadata.load('.')
    # cannot print(md) due to python/cpython#119650
    for key in md:
        print(key, md[key], sep=': ')


__name__ == '__main__' and main()
