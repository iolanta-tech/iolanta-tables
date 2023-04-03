from dataclasses import dataclass, field
from functools import cached_property
from typing import List, Optional

import funcy
from iolanta.models import NotLiteralNode
from rdflib import Namespace

# FIXME:
#   title: Make it a DefinedNamespace to be developer friendly.
#   description: Perhaps rdflib knows how to generate these.
TABLE = Namespace('https://iolanta.tech/tables/')


@dataclass
class ColumnTree:
    """Tree of table columns."""

    column: NotLiteralNode
    children: List['ColumnTree'] = field(default_factory=list)

    @cached_property
    def depth(self) -> int:
        return funcy.inc(
            max(
                child.depth
                for child
                in self.children
            ) if self.children else 0,
        )

    @cached_property
    def colspan(self) -> Optional[int]:
        if children := self.children:
            return sum(child.colspan or 1 for child in children)

    def calculate_rowspan(self, row_id: int) -> Optional[int]:
        row_span = row_id - self.depth + 2

        if row_span > 1:
            return row_span
