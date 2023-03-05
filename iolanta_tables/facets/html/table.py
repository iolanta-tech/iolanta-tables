import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, TypeVar

import funcy
from dominate.tags import table, td, th
from dominate.util import raw
from iolanta.facets.html.base import HTMLFacet
from iolanta.iolanta import Iolanta
from iolanta.models import NotLiteralNode
from iolanta.namespaces import IOLANTA
from rdflib import URIRef

from iolanta_tables.facets.html.errors import (
    TableBodyNotFound,
    TableColumnsNotFound,
)
from iolanta_tables.facets.html.models import Direction, EmptyValues, OrderBy
from iolanta_tables.models import TABLE

Row = Dict[URIRef, Any]   # type: ignore
ColumnValue = TypeVar('ColumnValue')


def construct_headers(
    iolanta: Iolanta,
    table_iri: NotLiteralNode,
    columns: List[URIRef],
) -> Iterable[th]:
    """Construct table headers."""
    return (
        th(
            iolanta.render(
                node=column,
                # FIXME:
                #   title: Use the table:columns blank node as environment here
                environments=[table_iri, TABLE.th, IOLANTA.html],
            ),
        ) for column in columns
    )


def construct_row(
    instance: URIRef,
    iolanta: Iolanta,
    columns: List[URIRef],
) -> Row:
    """Construct a table row."""
    formatted_columns = '({columns})'.format(
        columns=', '.join([
            f'<{column}>' for column in columns
        ]),
    )

    query_text = '''
    SELECT * WHERE {
        $instance ?column ?value .

        OPTIONAL {
            ?value mkdocs:trustLevel ?trust_level .
        }

        FILTER(?column IN %s) .
    } ORDER BY ?column ?trust_level
    ''' % formatted_columns

    cells = iolanta.query(
        query_text=query_text,
        instance=instance,
    )

    cells.append({
        'column': TABLE.self,
        'value': instance,
    })

    # This dictionary comprehension entails an implicit deduplication by
    # `cell['column']`, in which the last duplicate wins. Since we have sorted
    # the elements by `mkdocs:trustLevel` this means we will prefer a higher
    # trust level over a lower one, or over an absence of defined trust level.
    return {
        cell['column']: instance if (
            cell['column'] == TABLE.self
        ) else cell['value']
        for cell in cells
    }


def render_row(
    row: Row,
    columns: List[URIRef],
    iolanta: Iolanta,
) -> Iterable[td]:
    """Compile a sequence of table cells for a row."""
    for column in columns:
        try:
            cell_value = row[column]
        except KeyError:
            yield td()
            continue

        cell_content = str(
            iolanta.render(
                node=cell_value,
                environments=[column, TABLE.td, IOLANTA.html],
            ),
        )
        yield td(raw(cell_content))


def construct_sorter(order_by: List[Tuple[URIRef, bool]]):
    """Construct a sorting procedure for rows in a table."""
    def sorter(row: Row):   # noqa: WPS430
        return [
            row.get(order_field, None)    # FIXME descending?
            for order_field, is_ascending in order_by
        ]

    return sorter


def construct_sorting_key(
    row: Dict[URIRef, ColumnValue],
    order_by: OrderBy,
) -> Tuple[bool, Optional[ColumnValue]]:
    """
    Construct a sorting key for a given column.

    Idea: https://stackoverflow.com/a/18411610/1245471
    """
    column_value = row.get(order_by.column)
    is_none = column_value is None

    return (
        is_none if order_by.empty_values == EmptyValues.LAST else not is_none,
        column_value,
    )


def order_rows(
    rows: List[Row],
    orderings: List[OrderBy],
):
    """Order rows by particular properties."""
    for order_by in reversed(orderings):
        rows = sorted(
            rows,
            key=functools.partial(
                construct_sorting_key,
                order_by=order_by,
            ),
            reverse=(order_by.direction == Direction.DESC),
        )

    return list(rows)


@dataclass
class Table(HTMLFacet):
    """HTML table facet."""

    def retrieve_body_iri(self) -> NotLiteralNode:
        """Retrieve the node of table body."""
        if instance_class := funcy.first(   # noqa: WPS337
            funcy.pluck(
                'class_list',
                self.stored_query('instance_class.sparql', table=self.iri),
            ),
        ):
            return instance_class

        if rows_iri := funcy.first(
            funcy.pluck(
                'rows',
                self.stored_query('table_rows.sparql', table=self.iri),
            ),
        ):
            return rows_iri

        raise TableBodyNotFound(table=self.iri)

    def retrieve_column_list_iri(self) -> NotLiteralNode:
        if column_list := funcy.first(
            funcy.pluck(
                'column_list',
                self.stored_query('columns_list.sparql', table=self.iri),
            ),
        ):
            return column_list

        raise TableColumnsNotFound(table=self.iri)

    def show(self) -> table:
        """Render the table."""
        header = self.render(
            self.retrieve_column_list_iri(),
            environments=[self.iri, TABLE.header],
        )

        body = self.render(
            self.retrieve_body_iri(),
            environments=[self.iri, TABLE.body],
        )

        return table(header, body)
