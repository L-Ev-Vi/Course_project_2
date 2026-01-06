from unittest.mock import patch

import pytest

from src.api_hh import HH
from src.currency_exchange import CurrencyExchange
from src.filling_in_job_information import FillingInJobInformation
from src.filling_in_request_data import FillingInRequestData
from src.json_saver import JSONSaver
from src.vacancy import Vacancy
from src.xlsx_saver import XLSXSaver


@pytest.fixture
def object_hh1():
    return HH()


@pytest.fixture
@patch("builtins.input")
def vacancy1(input_mock):
    input_mock.return_value = "1"
    vacancy1 = Vacancy(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100"
    )
    return vacancy1


@pytest.fixture
@patch("builtins.input")
def vacancy2(input_mock):
    input_mock.return_value = "1"
    vacancy2 = Vacancy(
        "Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "200"
    )
    return vacancy2


@pytest.fixture
def vacancy3():
    return ["Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100"]


@pytest.fixture
def vacancy4():
    return ["Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100-200"]


@pytest.fixture
def currencyexchange():
    return CurrencyExchange("USD")


@pytest.fixture
@patch("builtins.input")
def vacancy5(input_mock):
    input_mock.return_value = "2"
    vacancy5 = Vacancy(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100"
    )
    return vacancy5


@pytest.fixture
@patch("builtins.input")
def vacancy6(input_mock):
    input_mock.return_value = "2"
    vacancy6 = Vacancy(
        "Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "200"
    )
    return vacancy6


@pytest.fixture
@patch("builtins.input")
def vacancy7(input_mock):
    input_mock.return_value = "1"
    vacancy7 = Vacancy(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100-150"
    )
    return vacancy7


@pytest.fixture
@patch("builtins.input")
def vacancy8(input_mock):
    input_mock.return_value = "1"
    vacancy8 = Vacancy(
        "Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "200-250"
    )
    return vacancy8


@pytest.fixture
def vacancy9():
    vacancy9 = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    return vacancy9


@pytest.fixture
def inf1():
    return FillingInJobInformation()


@pytest.fixture
def req1():
    return FillingInRequestData()


@pytest.fixture
def list_salary():
    return [
        {"salary": {"from": 500, "to": None, "currency": "RUB"}},
        {"salary": {"from": 400, "to": None, "currency": "RUB"}},
        {"salary": {"from": 300, "to": None, "currency": "RUB"}},
        {"salary": {"from": 200, "to": None, "currency": "RUB"}},
        {"salary": {"from": 100, "to": None, "currency": "RUB"}},
    ]


@pytest.fixture
def list_sort():
    return [
        {"salary": {"from": 500, "to": None, "currency": "RUB"}},
        {"salary": {"from": None, "to": 400, "currency": "RUB"}},
        {"salary": {"from": 300, "to": None, "currency": "RUB"}},
        {"salary": {"from": None, "to": 200, "currency": "RUB"}},
        {"salary": {"from": 100, "to": None, "currency": "RUB"}},
        {"salary": "Зарплата не указана"},
    ]


@pytest.fixture
def list_sort_USD_from():
    return [
        {"salary": {"from": 500, "to": None, "currency": "RUB"}},
        {"salary": {"from": None, "to": 400, "currency": "RUB"}},
        {"salary": {"from": 300, "to": None, "currency": "RUB"}},
        {"salary": {"from": None, "to": 200, "currency": "RUB"}},
        {"salary": {"from": 100, "to": None, "currency": "USD"}},
        {"salary": "Зарплата не указана"},
    ]


@pytest.fixture
def list_sort_USD_to():
    return [
        {"salary": {"from": 500, "to": None, "currency": "RUB"}},
        {"salary": {"from": None, "to": 400, "currency": "RUB"}},
        {"salary": {"from": 300, "to": None, "currency": "RUB"}},
        {"salary": {"from": None, "to": 200, "currency": "RUB"}},
        {"salary": {"from": None, "to": 100, "currency": "USD"}},
        {"salary": "Зарплата не указана"},
    ]


@pytest.fixture
def json1():
    return JSONSaver("test")


@pytest.fixture
def vacancy_RUB_to():
    return [
        {
            "id": 1,
            "name": "Java Developer",
            "salary": {"from": None, "to": 150, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]


@pytest.fixture
def vacancy_USD_to():
    return [
        {
            "id": 1,
            "name": "Java Developer",
            "salary": {"from": None, "to": 150, "currency": "USD"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]


@pytest.fixture
def vacancy_RUB_from():
    return [
        {
            "id": 1,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]


@pytest.fixture
def vacancy_USD_from():
    return [
        {
            "id": 1,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "USD"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]


@pytest.fixture
def vacancy_USD_from_to():
    return [
        {
            "id": 1,
            "name": "Java Developer",
            "salary": {"from": 100, "to": 150, "currency": "USD"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]


@pytest.fixture
def vacancy_RUB_from_to():
    return [
        {
            "id": 1,
            "name": "Java Developer",
            "salary": {"from": 100, "to": 150, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]


@pytest.fixture
def xlsx1():
    return XLSXSaver("test")


@pytest.fixture
@patch("builtins.input")
def vacancy10(input_mock):
    input_mock.return_value = "2"
    vacancy10 = Vacancy(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100-150"
    )
    return vacancy10
