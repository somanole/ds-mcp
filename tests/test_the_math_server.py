from mcp_servers.the_math_server import add_numbers


def test_add_numbers_with_positive_integers():
    assert add_numbers(2, 3) == 5


def test_add_numbers_with_negative_and_zero():
    assert add_numbers(-7, 0) == -7
