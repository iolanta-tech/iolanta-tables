from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def data_directory() -> Path:
    return Path(__file__).parent / 'data'
