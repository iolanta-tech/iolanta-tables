from dataclasses import dataclass
from enum import Enum

from rdflib import URIRef


class Direction(str, Enum):
    """Sorting direction."""

    ASC = 'asc'
    DESC = 'desc'


class EmptyValues(str, Enum):
    """Where to put the empty values."""

    FIRST = 'first'
    LAST = 'last'


@dataclass
class OrderBy:
    """Column and its ordering configuration."""

    column: URIRef
    direction: Direction = Direction.ASC
    empty_values: EmptyValues = EmptyValues.FIRST
