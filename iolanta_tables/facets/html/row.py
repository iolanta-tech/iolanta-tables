from dataclasses import dataclass
from typing import Union

import funcy
from dominate.tags import html_tag, td, tr
from iolanta.models import NotLiteralNode
from iolanta.namespaces import IOLANTA

from iolanta_tables.facets.html.base import IolantaTablesFacet
from iolanta_tables.facets.html.errors import TableColumnsNotFound
from iolanta_tables.models import TABLE


@dataclass
class TableRow(IolantaTablesFacet):
    """Table row."""

    def column_list_iri(self) -> NotLiteralNode:
        """Find column definition for this table."""
        return funcy.first(
            funcy.pluck(
                'column_list',
                self.stored_query(
                    'column_list_by_row_list.sparql',
                    environment=self.environment,
                    node=self.iri,
                ),
            ),
        )

    def show(self) -> Union[str, html_tag]:
        """Render <tr> tag."""
        instance_links = self.stored_query('tr.sparql', instance=self.iri)

        row_value_by_column = {
            link['column']: link['value']
            for link in instance_links
        }

        row_value_by_column = {
            **row_value_by_column,
            TABLE.self: self.iri,
        }

        column_list = self.column_list_iri()
        if column_list is None:
            raise TableColumnsNotFound(table=self.iri)

        columns = self.list_columns(
            column_list=column_list,
        )

        maybe_cell_values = [
            row_value_by_column.get(column) for column in columns
        ]

        cells = [
            td(
                self.render(
                    cell_value,
                    environments=[IOLANTA.html],
                ),
            ) if cell_value is not None else td()
            for cell_value in maybe_cell_values
        ]

        return tr(*cells)
