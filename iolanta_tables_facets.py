from pathlib import Path

import funcy
from dominate.tags import code, table, td, tr
from dominate.util import raw
from iolanta.facet import Facet
from iolanta.namespaces import LOCAL

CODE_TEMPLATE = """
```{language} title="{title}"
{code}
```

{annotations}
"""


class SideBySide(Facet):
    """YAML code and its rendering."""

    def show(self):
        """Render Side by Side for HTML."""
        rows = self.query(
            'SELECT * WHERE { GRAPH ?page { $iri ?p ?o } }',
            iri=self.iri,
        )

        page = funcy.first(rows)['page']

        return table(
            tr(
                td(
                    self.render(
                        page,
                        environments=[LOCAL.term('code')],
                    ),
                ),
                td(
                    '⇒',
                    style='font-size: 200%; vertical-align: middle',
                ),
                td(
                    code(
                        '{{ render(\'%s\') }}' % str(self.iri).replace(
                            'local:',
                            '',
                        ),
                    ),
                    self.render(self.iri),
                ),
            ),
            data_facet='side-by-side',
        )


class Code(Facet):
    """Print contents of a file in a code fence."""

    def show(self):
        """Render code as HTML."""
        relative_path = str(self.iri).replace('docs://', '')
        path = Path.cwd() / 'docs' / relative_path
        return raw(
            CODE_TEMPLATE.format(
                language='yaml',
                code=path.read_text(),
                title=relative_path,
                annotations='',
            ),
        )
