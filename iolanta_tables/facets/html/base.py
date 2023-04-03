from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, List

from iolanta.facets.html.base import HTMLFacet
from iolanta.models import NotLiteralNode

from iolanta_tables.facets.html.models import Direction, EmptyValues, OrderBy
from iolanta_tables.models import TABLE, ColumnTree


@dataclass
class IolantaTablesFacet(HTMLFacet, ABC):
    """Base for mkdocs-iolanta-tables facets."""

    def construct_column_trees(
        self,
        column_list_node: NotLiteralNode,
    ) -> List[ColumnTree]:
        rows = self.stored_query(
            'columns.sparql',
            column_list=column_list_node,
        )

        return [
            ColumnTree(
                column=row['column'],
                children=self.construct_column_trees(
                    column_list_node=nested_column_list,
                ) if (
                    nested_column_list := row.get('nested_column_list')
                ) else [],
            )
            for row in rows
        ]

    def _extract_leaves(self, trees: List[ColumnTree]) -> Iterable[NotLiteralNode]:
        for tree in trees:
            if children := tree.children:
                yield from self._extract_leaves(children)
            else:
                yield tree.column

    def list_columns(
        self,
        column_list: NotLiteralNode,
    ) -> List[NotLiteralNode]:
        """List of column IRIs for a table."""
        trees = self.construct_column_trees(column_list)
        return list(self._extract_leaves(trees))


class TableBody(IolantaTablesFacet):
    """Table body facet."""

    def construct_order_by_clause(self, order_by: List[OrderBy]) -> str:
        if not order_by:
            return ''

        sortables = [
            '',
        ]

    def order_by(self) -> List[OrderBy]:
        """
        List of columns that we order by.

        Idea: http://www.snee.com/bobdc.blog/2014/04/rdf-lists-and-sparql.html
        """
        rows = self.stored_query(
            'order-by.sparql',
            iri=self.iri,
        )

        return [
            OrderBy(
                column=row.get('column') or row['column_spec'],

                direction={
                    None: Direction.ASC,
                    TABLE.asc: Direction.ASC,
                    TABLE.desc: Direction.DESC,
                }[row.get('direction')],

                empty_values={
                    None: EmptyValues.FIRST,
                    TABLE.first: EmptyValues.FIRST,
                    TABLE.last: EmptyValues.LAST,
                }[row.get('empty_values')],
            )
            for row in rows
        ]

    @abstractmethod
    def select_instances(self) -> Iterable[NotLiteralNode]:
        """Instances of the table's class."""
