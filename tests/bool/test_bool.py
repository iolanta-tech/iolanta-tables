from pathlib import Path

import typer
from bs4 import BeautifulSoup
from sh import ErrorReturnCode, iolanta


def test_bool(mkdocs):
    """Boolean value as an icon."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as mkdocs_err:
        typer.echo(mkdocs_err.stderr.decode())
        raise AssertionError()

    assert iolanta(
        'query',
        'SELECT * WHERE { ?s iolanta:datatypeFacet ?o }',
        _cwd=test_directory,
    )

    index = Path(__file__).parent / 'site/index.html'
    soup = BeautifulSoup(index.read_text(), parser='html.parser')

    assert [
        td.string
        for td in soup.table.select('td')
    ] == ['✔️', '❌', '✔️', '❌']
