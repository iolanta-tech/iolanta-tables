from pathlib import Path

import pytest
from iolanta.iolanta import Iolanta
from iolanta.namespaces import IOLANTA, LOCAL


@pytest.fixture(scope='session')
def data_directory() -> Path:
    return Path(__file__).parent / 'data'


@pytest.fixture()
def rendered_html_and_stack(data):
    return Iolanta().add(data).render(
        LOCAL.table,
        environments=[IOLANTA.html],
    )


@pytest.fixture()
def rendered_html(rendered_html_and_stack):
    html, _stack = rendered_html_and_stack
    return html
