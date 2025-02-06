"""
Take json output from pipdeptree --json and make it into
a tree rooted at the indicated package.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any, Dict, TypeVar

if TYPE_CHECKING:
    from typing_extensions import Self

_T = TypeVar("_T")


def by_package_key(
    item: Mapping[str, Mapping[str, _T]],
) -> _T:
    return by_key(item['package'])


def by_key(item: Mapping[str, _T]) -> _T:
    return item['key']


def main() -> None:
    (root,) = sys.argv[1:]
    pkgs = Packages.from_defn(json.load(sys.stdin))
    json.dump(pkgs.make_tree(root), sys.stdout)


class Packages(Dict[str, Dict[str, Any]]):
    @classmethod
    def from_defn(cls, items: Iterable[dict[str, Any]]) -> Self:
        return cls(
            (key, next(items))
            for key, items in itertools.groupby(items, by_package_key)
        )

    def make_tree(self, target: str) -> dict[str, Any]:
        if not hasattr(self, 'visited'):
            self.visited: set[str] = set()
        root = self[target].copy()
        if target in self.visited:
            # short-circuit circular dependencies
            del root['dependencies']
            return root
        self.visited.add(target)
        deps_names = map(by_key, root['dependencies'])
        root['dependencies'] = list(map(self.make_tree, deps_names))
        return root


if __name__ == '__main__':
    main()
