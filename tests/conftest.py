import pytest


@pytest.fixture(autouse=True, scope='function')
def new_line_function():
    """Fixture simple makes new line to separate each test logging output."""
    print()
    yield
    print()


@pytest.fixture(params=['forward_interest', 'front_arm', 'reach_wind', 'voice_central', 'write_beautiful'])
def build_name(request) -> str:
    return request.param
