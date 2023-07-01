import pytest


@pytest.fixture(autouse=True, scope='function')
def new_line_function():
    """Fixture simple makes new line to separate each test logging output."""
    print()
    yield
    print()


# XXX
# # NOTE
# # Custom pytest invocation for `profile`
# #
# if __name__ == '__main__':
#     sys.exit(pytest.main(['-xvs']))
