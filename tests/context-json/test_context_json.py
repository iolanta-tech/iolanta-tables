from pathlib import Path

import typer
from sh import ErrorReturnCode, iolanta


def test_context_json(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as err:
        typer.echo(err.stderr.decode())
        raise AssertionError()

    url = 'https://mkdocs.iolanta.tech/github/url'

    response = iolanta(
        'query',
        'SELECT * WHERE { local:test <%s> ?url }' % url,
        _cwd=test_directory,
    )
    assert 'iolanta-tech' in response
