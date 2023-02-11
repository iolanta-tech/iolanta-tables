from pathlib import Path

import typer
from bs4 import BeautifulSoup
from sh import ErrorReturnCode


def test_self_without_class(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as err:
        typer.echo(err.stderr.decode())
        raise AssertionError()

    index = Path(__file__).parent / 'site/index.html'
    soup = BeautifulSoup(index.read_text(), parser='html.parser')

    assert str(soup.table.th) == '<th></th>'
