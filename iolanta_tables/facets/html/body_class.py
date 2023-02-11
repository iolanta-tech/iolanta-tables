from typing import Iterable, Union

import funcy
from dominate.tags import html_tag, tbody
from iolanta.models import NotLiteralNode

from iolanta_tables.facets.html.base import TableBody


class BodyClass(TableBody):
    """Table body defined via class of instances."""

    def select_instances(self) -> Iterable[NotLiteralNode]:
        """Instances of the table's class."""
        return funcy.pluck(
            'instance',
            self.stored_query('instances-class.sparql', column_list=self.iri),
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
