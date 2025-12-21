from unittest.mock import patch

import pytest

from src.api_hh import HH
from src.currency_exchange import CurrencyExchange
from src.vacancy import Vacancy


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
