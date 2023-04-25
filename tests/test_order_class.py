from pathlib import Path

from dominate.tags import table, tbody, td, th, thead, tr
from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA, LOCAL


def test_order_class(data_directory: Path):
    rendered, stack = Iolanta().add(
        data_directory / 'order-class.yaml',
    ).render(
        LOCAL.table,
        environments=[IOLANTA.html],
    )

    expected = table(
        thead(
            tr(
                th('Year'),
            ),
        ),
        tbody(
            tr(td('2000')),
            tr(td('2010')),
        ),
    )

    assert str(
        rendered,
    ) == str(expected), str(rendered)
