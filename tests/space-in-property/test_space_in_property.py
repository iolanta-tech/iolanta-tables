from pathlib import Path

from sh import ErrorReturnCode


def test_space_in_property(mkdocs):
    """Without a table:class, table:self column heading is an empty string."""
    test_directory = Path(__file__).parent
    try:
        mkdocs('build', _cwd=test_directory)
    except ErrorReturnCode as err:
        response = err.stderr.decode()

        assert 'space' in response
