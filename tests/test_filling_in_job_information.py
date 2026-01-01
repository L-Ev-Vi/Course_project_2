from unittest.mock import patch


@patch("builtins.input")
def test_getting_data(input_mock, inf1):
    input_mock.return_value = "Параметр"
    assert inf1.getting_data() == ["Параметр", "Параметр", "Параметр", "Параметр"]
