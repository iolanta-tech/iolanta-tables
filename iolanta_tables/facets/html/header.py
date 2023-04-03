from typing import Union

import funcy
from dominate.tags import html_tag, th, thead, tr
from iolanta.namespaces import IOLANTA

from iolanta_tables.facets.html.base import IolantaTablesFacet
from iolanta_tables.models import TABLE


class TableHeader(IolantaTablesFacet):
    """
    Table head.

    <thead> tag.
    """

    def show(self) -> Union[str, html_tag]:
        column_trees = self.construct_column_trees(self.iri)
        max_depth = max(column.depth for column in column_trees)

        row = column_trees
        table_rows = []
        for row_id in reversed(range(max_depth)):
            table_rows.append(
                tr(
                    th(
                        self.render(
                            tree.column,
                            environments=[self.iri, TABLE.th, IOLANTA.html],
                        ),
                        colspan=tree.colspan,
                        rowspan=tree.calculate_rowspan(row_id=row_id),
                    )
                    for tree in row
                ),
            )
            row = [
                child
                for tree in row
                for child in tree.children
            ]

        return thead(*table_rows)
