from typing import Union

from dominate.tags import html_tag, th, thead, tr
from iolanta.namespaces import IOLANTA

from iolanta_tables.facets.html.base import IolantaTablesFacet


class TableHeader(IolantaTablesFacet):
    """
    Table head.

    <thead> tag.
    """

    def show(self) -> Union[str, html_tag]:
        columns = self.list_columns(self.iri)

        cells = [
            th(
                self.render(
                    column,
                    environments=[self.iri, IOLANTA.html],
                ),
            ) for column in columns
        ]

        return thead(tr(*cells))
