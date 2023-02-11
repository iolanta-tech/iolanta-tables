from pathlib import Path

import pytest
import typer
from bs4 import BeautifulSoup
from dominate.tags import a, table, tbody, td, th, thead, tr
from sh import ErrorReturnCode


@pytest.fixture()
def expected_table():
    return table(
        thead(
            tr(th('Link')),
        ),
        tbody(
            tr(td(a('boo', href='https://boo.com'))),
        ),
    ).render(
        indent='',
    )


def test_url(mkdocs, expected_table):
    """Boolean value as an icon."""
    test_directory = Path(__file__).parent
    try:
        typer.echo(
            mkdocs('build', _cwd=test_directory),
        )
    except ErrorReturnCode as mkdocs_err:
        typer.echo(mkdocs_err.stderr.decode())
        raise AssertionError()

    index = Path(__file__).parent / 'site/index.html'
    soup = BeautifulSoup(index.read_text(), parser='html.parser')

    assert str(soup.table) == str(expected_table), soup.table
