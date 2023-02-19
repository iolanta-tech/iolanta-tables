from pathlib import Path

from dominate.tags import table, tbody, td, th, thead, tr
from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA, LOCAL
from rdflib import URIRef


def test_bool(data_directory: Path):
    """Boolean value as an icon."""
    assert str(
        Iolanta().add(
            data_directory / 'bool.yaml',
        ).render(
            LOCAL['bool-table'],
            environments=[IOLANTA.html],
        ),
    ) == str(
        table(
            thead(
                tr(
                    th('Boolean value'),
                ),
            ),
            tbody(
                tr(td('✔️')),
                tr(td('❌')),
                tr(td('✔️')),
                tr(td('❌')),
            ),
        ),
    )
