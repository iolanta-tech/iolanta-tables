from pathlib import Path
from typing import Union, Type

import funcy
import pytest
from dominate.tags import table, thead, tbody, tr, td, th, html_tag
from iolanta.iolanta import Iolanta
from iolanta.namespaces import LOCAL, IOLANTA
from iolanta.parsers.errors import SpaceInProperty


@pytest.mark.parametrize(
    ('file_name', 'expected'),
    [
        (
            'bool.yaml',
            table(
                thead(tr(th('Boolean value'))),
                tbody(
                    tr(td('✔️')),
                    tr(td('❌')),
                    tr(td('✔️')),
                    tr(td('❌')),
                ),
            ),
        ),
        (
            'class.yaml',
            table(
                thead(tr(th(), th('Name'))),
                tbody(tr(td('Badoom'), td('boo')))
            ),
        ),
        ('column-title.yaml', table()),
        ('description-column.yaml', table()),
        ('invalid.yaml', table()),
        ('order.yaml', table()),
        ('self-without-class.yaml', table()),
        ('space in filename.yaml', table(
            thead(tr(th('Description'))),
            tbody(tr(td('foo'))),
        )),
        ('space-in-property.yaml', SpaceInProperty),
        ('url.yaml', table()),
    ],
    ids=[
        'bool', 'class', 'title', 'description', 'invalid', 'order',
        'self', 'space-filename', 'space-property', 'url',
    ]
)
def test_data(
    data_directory: Path,
    file_name: str,
    expected: Union[html_tag, Type[Exception]],
):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            Iolanta().add(
                data_directory / file_name,
            ).render(
                LOCAL.table,
                environments=[IOLANTA.html],
            )

    else:
        assert str(
            rendered := Iolanta().add(
                data_directory / file_name,
            ).render(
                LOCAL.table,
                environments=[IOLANTA.html],
            ),
        ) == str(expected), str(rendered)
