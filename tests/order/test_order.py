from pathlib import Path

import typer
from bs4 import BeautifulSoup
from dominate.tags import table, tbody, td, th, thead, tr
from sh import ErrorReturnCode, iolanta


def test_order(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent

    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as err:
        typer.echo(err.stderr.decode())
        # raise AssertionError()

    try:
        typer.echo(
            iolanta.query(
                'SELECT * WHERE { ?class_list a table:ClassList }',
                _cwd=test_directory,
            ),
        )
    except ErrorReturnCode as err:
        typer.echo(err.stderr)

    index = Path(__file__).parent / 'site/index.html'
    soup = BeautifulSoup(index.read_text(), parser='html.parser')

    assert str(soup.table) == table(
        thead(tr(th('Name'), th('Color'), th('Birthday'))),
        tbody(
            tr(td('Ray'), td('Red'), td('2010-01-01')),
            tr(td('Smoky'), td('Gray'), td('2010-12-10')),
        ),
    ).render(indent=''), soup.table
