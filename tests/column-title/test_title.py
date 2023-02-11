from pathlib import Path

import typer
from bs4 import BeautifulSoup
from sh import ErrorReturnCode


def test_column_title(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as mkdocs_err:
        typer.echo(mkdocs_err.stderr.decode())
        raise AssertionError()

    index = Path(__file__).parent / 'site/index.html'
    soup = BeautifulSoup(index.read_text(), parser='html.parser')

    assert str(soup.table.th) == '<th>FOO</th>'
