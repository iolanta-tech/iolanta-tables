from pathlib import Path

import typer
from sh import ErrorReturnCode


def test_description(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as mkdocs_err:
        typer.echo(mkdocs_err.stderr.decode())
        raise AssertionError()
