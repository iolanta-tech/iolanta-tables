from iolanta.facet import Facet
from iolanta.renderer import render
from more_itertools import first

from iolanta_tables.models import TABLE


class SelfFacet(Facet):
    """Render table:self property."""

    def show(self):
        """Call rendering for the underlying class of the table."""
        if self.environment is None:
            raise ValueError(
                f'Facet {self} was called with no environment specified.',
            )

        rows = self.query(
            query_text='''
            SELECT * WHERE {
                $table table:class ?cls .
            }
            ''',
            table=self.environment,
        )

        try:
            instance_class = first(rows)['cls']

        except ValueError:
            return ''

        return render(
            node=instance_class,
            iolanta=self.iolanta,
            environments=[TABLE.th],
        )
