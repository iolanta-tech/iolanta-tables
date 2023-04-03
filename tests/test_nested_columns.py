import pytest
from dominate.tags import table, tbody, td, th, thead, tr


@pytest.mark.parametrize(
    ['data'],
    [[{
        '$id': 'table',
        'table:columns': [
            {
                '$id': 'normal-column',
            }, {
                '$id': 'super-column',
                'table:columns': [
                    'foo',
                    'bar',
                    'baz',
                ],
            },
        ],
        'table:rows': [{
            'normal-column': '?',
            'foo': 'A',
            'bar': 'B',
            'baz': 'C',
        }],
    }]],
)
def test_nested_columns(rendered_html, data):
    assert str(rendered_html) == str(
        table(
            thead(
                tr(
                    th('Normal column', rowspan=2),
                    th('Super column', colspan=3),
                ),
                tr(
                    th('Foo'),
                    th('Bar'),
                    th('Baz'),
                ),
            ),
            tbody(
                tr(
                    td('?'),
                    td('A'),
                    td('B'),
                    td('C'),
                ),
            ),
        ),
    )
