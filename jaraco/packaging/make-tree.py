"""
Take json output from pipdeptree --json and make it into
a tree rooted at the indicated package.
"""

import itertools
import json
import sys


def by_package_key(item):
    return by_key(item['package'])


def by_key(item):
    return item['key']


def main():
    (root,) = sys.argv[1:]
    pkgs = Packages.from_defn(json.load(sys.stdin))
    json.dump(pkgs.make_tree(root), sys.stdout)


class Packages(dict):
    @classmethod
    def from_defn(cls, items):
        return cls(
            (key, next(items))
            for key, items in itertools.groupby(items, by_package_key)
        )

    def make_tree(self, target):
        vars(self).setdefault('visited', set())
        root = self[target].copy()
        if target in self.visited:
            # short-circuit circular dependencies
            del root['dependencies']
            return root
        self.visited.add(target)
        deps_names = map(by_key, root['dependencies'])
        root['dependencies'] = list(map(self.make_tree, deps_names))
        return root


__name__ == '__main__' and main()
