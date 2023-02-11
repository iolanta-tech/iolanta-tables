from pathlib import Path

import typer
from bs4 import BeautifulSoup
from sh import ErrorReturnCode, iolanta


def test_description(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as mkdocs_err:
        typer.echo(mkdocs_err.stderr.decode())
        raise AssertionError()

    try:
        typer.echo(
            iolanta(
                'query',
                'SELECT * WHERE { GRAPH <docs://index.md> { ?s ?p ?o } }',
                _cwd=test_directory,
            ),
        )
    except ErrorReturnCode as iolanta_err:
        typer.echo(iolanta_err.stderr.decode())
        raise AssertionError()

    index = Path(__file__).parent / 'site/index.html'
    soup = BeautifulSoup(index.read_text(), parser='html.parser')

    assert str(soup.table.td) == '<td>foo</td>'
