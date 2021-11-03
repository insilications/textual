from __future__ import annotations


import rich.repr

from typing import Iterable, Iterator, TYPE_CHECKING


from .match import match
from .parse import parse_selectors

if TYPE_CHECKING:
    from ..dom import DOMNode


@rich.repr.auto(angular=True)
class DOMQuery:
    def __init__(
        self,
        node: DOMNode | None = None,
        selector: str | None = None,
        nodes: Iterable[DOMNode] | None = None,
    ) -> None:

        self._nodes: list[DOMNode]
        if nodes is not None:
            self._nodes = list(nodes)
        elif node is not None:
            self._nodes = list(node.walk_children())
        else:
            self._nodes = []

        if selector is not None:
            selector_set = parse_selectors(selector)
            self._nodes = [_node for _node in self._nodes if match(selector_set, _node)]

    def __iter__(self) -> Iterator[DOMNode]:
        return iter(self._nodes)

    def __rich_repr__(self) -> rich.repr.Result:
        yield self._nodes

    def filter(self, selector: str) -> DOMQuery:
        selector_set = parse_selectors(selector)
        query = DOMQuery()
        query._nodes = [_node for _node in self._nodes if match(selector_set, _node)]
        return query