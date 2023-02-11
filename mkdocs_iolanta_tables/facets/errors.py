from dataclasses import dataclass

from documented import DocumentedError
from iolanta.models import NotLiteralNode


@dataclass
class TableBodyNotFound(DocumentedError):
    """
    Table body not found.

    Table IRI: {self.table}

    This table does not have a `table:rows` or `table:class` property, so we do
    not know what to render as this table's rows
    """

    table: NotLiteralNode


@dataclass
class TableColumnsNotFound(DocumentedError):
    """
    Table columns not found.

    Table IRI: {self.table}

    This table does not have a `table:columns` property, so we do not know how
    to render its columns.
    """

    table: NotLiteralNode
