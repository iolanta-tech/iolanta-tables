from typing import Iterable, Union

import funcy
from dominate.tags import html_tag, tbody
from rdflib import URIRef

from iolanta_tables.facets.html.base import TableBody
from iolanta_tables.facets.html.models import Direction


class BodyRows(TableBody):
    """Build table body when it is specified by table:rows property."""

    def select_instances(self) -> Iterable[URIRef]:
        """Select instances, or rows, for the table."""
        order_by = self.order_by()

        bindings_clause = '\n'.join(
            f'OPTIONAL {{ ?instance <{ordering.column}> ?order_by_{index} . }}'
            for index, ordering in enumerate(order_by)
        )

        order_by_particles = [
            f'?order_by_{index}'
            for index, _ordering in enumerate(order_by)
        ]

        order_by_particles = [
            particle if (
                ordering.direction == Direction.ASC
            ) else f'DESC({particle})'
            for particle, ordering in zip(order_by_particles, order_by)
        ]

        order_by_clause = ', '.join(order_by_particles)

        if order_by_clause:
            order_by_clause = f'ORDER BY {order_by_clause}'

        query_text = f'''
            SELECT ?instance WHERE {{
                $iri rdf:rest*/rdf:first ?instance .
                {bindings_clause}
            }} {order_by_clause}
        '''

        return list(
            funcy.pluck(
                'instance',
                self.iolanta.query(
                    query_text,
                    iri=self.iri,
                ),
            ),
        )

    def show(self) -> Union[str, html_tag]:
        """Render as HTML."""
        rendered_rows = [
            self.render(
                instance,
                environments=[self.iri],
            )
            for instance in self.select_instances()
        ]

        return tbody(*rendered_rows)
