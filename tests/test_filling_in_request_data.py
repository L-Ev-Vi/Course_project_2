from unittest.mock import patch


@patch("builtins.input")
def test_getting_data(input_mock, req1):
    input_mock.return_value = "10"
    assert req1.getting_data() == ["10", 10, "10", 10, 10]
