import os
from unittest.mock import patch

from dotenv import load_dotenv


def test_init_currency_exchange(currencyexchange):
    assert currencyexchange.currency == "USD"


@patch("requests.get")
def test_get_currency_exchange(mock_get, currencyexchange):
    load_dotenv(".env")
    aip_key = os.getenv("EXC_AIP_KEY")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 100}
    assert currencyexchange.get_currency_exchange(10) == 100
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10",
        headers={"apikey": f"{aip_key}"},
        data={},
    )


@patch("requests.get")
def test_get_currency_exchange_error_500(mock_get, currencyexchange, capsys):
    mock_get.return_value.status_code = 500
    currencyexchange.get_currency_exchange(10)
    captured = capsys.readouterr()
    assert captured.out == "Ошибка на стороне сервера при выполнении запроса.\n"
    assert currencyexchange.get_currency_exchange(10) == 0


@patch("requests.get")
def test_get_currency_exchange_error_400(mock_get, currencyexchange, capsys):
    mock_get.return_value.status_code = 400
    currencyexchange.get_currency_exchange(10)
    captured = capsys.readouterr()
    assert captured.out == "Ошибка со стороны пользователя при выполнении запроса.\n"
    assert currencyexchange.get_currency_exchange(10) == 0


@patch("requests.get")
def test_get_currency_exchange_error_not_200(mock_get, currencyexchange, capsys):
    mock_get.return_value.status_code = 300
    currencyexchange.get_currency_exchange(10)
    captured = capsys.readouterr()
    assert captured.out == "Ошибка при выполнении запроса на базовый URL.\n"
    assert currencyexchange.get_currency_exchange(10) == 0
