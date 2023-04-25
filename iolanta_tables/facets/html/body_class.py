from typing import Iterable, Union

import funcy
from dominate.tags import html_tag, tbody
from iolanta.models import NotLiteralNode

from iolanta_tables.facets.html.base import TableBody


class BodyClass(TableBody):
    """Table body defined via class of instances."""

    def select_instances(self) -> Iterable[NotLiteralNode]:
        """Instances of the table's class."""
        order_by = self.order_by()

        bindings_clause = self._construct_bindings_clause(order_by=order_by)
        order_by_clause = self._construct_order_by_clause(order_by=order_by)

        query_text = f"""
            SELECT ?instance WHERE {{
                $iri rdf:first ?class .
                ?instance a ?class .

                {bindings_clause}
            }} {order_by_clause}
        """

        return list(
            funcy.pluck(
                'instance',
                self.query(
                    query_text,
                    iri=self.iri,
                ),
            ),
        )

    def show(self) -> Union[str, html_tag]:
        """Render as HTML."""
        instances = self.select_instances()

        rendered_rows = [
            self.render(
                instance,
                environments=[self.iri],
            )
            for instance in instances
        ]

        return tbody(*rendered_rows)
