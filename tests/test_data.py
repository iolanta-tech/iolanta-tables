from pathlib import Path
from typing import Type, Union

import funcy
import pytest
from dominate.tags import html_tag, table, tbody, td, th, thead, tr
from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA, LOCAL
from iolanta.parsers.errors import SpaceInProperty
from yaml.parser import ParserError


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
                tbody(tr(td('Badoom'), td('boo'))),
            ),
        ),
        (
            'column-title.yaml',
            table(
                thead(tr(th('FOO'))),
                tbody(tr(td('bar'))),
            ),
        ),
        (
            'description-column.yaml',
            table(
                thead(tr(th('Description'))),
                tbody(tr(td('foo'))),
            ),
        ),
        ('invalid.yaml', ParserError),
        (
            'order.yaml',
            table(
                thead(
                    tr(
                        th('Name'),
                        th('Color'),
                        th('Birthday'),
                    ),
                ),
                tbody(
                    tr(td('Ray'), td('Red'), td('2010-01-01')),
                    tr(td('Smoky'), td('Gray'), td('2010-12-10')),
                ),
            ),
        ),
        (
            'self-without-class.yaml',
            table(
                thead(
                    tr(
                        th(''),
                        th('Name'),
                    ),
                ),
                tbody(
                    tr(
                        td('badoom'),
                        td('boo'),
                    ),
                ),
            ),
        ),
        (
            'space in filename.yaml', table(
                thead(tr(th('Description'))),
                tbody(tr(td('foo'))),
            ),
        ),
        ('space-in-property.yaml', SpaceInProperty),

        # FIXME: uncomment this when a newer version of Iolanta is installed
        # ('url.yaml', table()),
    ],
    ids=[
        'bool', 'class', 'title', 'description', 'invalid', 'order',
        'self', 'space-filename', 'space-property',

        # FIXME: uncomment this when a newer version of Iolanta is installed
        # 'url',
    ],
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
