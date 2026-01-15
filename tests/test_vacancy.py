from unittest.mock import patch

import pytest

from src.vacancy import Vacancy


@patch("builtins.input")
def test_init_vacancy_RUB(input_mock, vacancy3):
    input_mock.return_value = "1"
    vacancy = Vacancy(*vacancy3)
    assert vacancy._Vacancy__id == 23
    assert vacancy._Vacancy__name == "Python Developer"
    assert vacancy._Vacancy__link == "<https://hh.ru/vacancy/123456>"
    assert vacancy._Vacancy__salary == {"salary": {"from": 100, "to": None, "currency": "RUB"}}
    assert vacancy._Vacancy__description == "Требования: опыт работы от 3 лет..."


@patch("builtins.input")
def test_init_vacancy_USD(input_mock, vacancy3):
    input_mock.return_value = "2"
    vacancy = Vacancy(*vacancy3)
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "USD"}}


@patch("builtins.input")
def test_init_vacancy_EUR(input_mock, vacancy3):
    input_mock.return_value = "3"
    vacancy = Vacancy(*vacancy3)
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "EUR"}}


@patch("builtins.input")
def test_init_vacancy_two_RUB(input_mock, vacancy4):
    input_mock.return_value = "1"
    vacancy = Vacancy(*vacancy4)
    assert vacancy._Vacancy__salary == {"salary": {"from": 100, "to": 200, "currency": "RUB"}}


@patch("builtins.input")
def test_init_vacancy_two_USD(input_mock, vacancy4):
    input_mock.return_value = "2"
    vacancy = Vacancy(*vacancy4)
    assert vacancy._Vacancy__salary == {"salary": {"from": 100, "to": 200, "currency": "USD"}}


@patch("builtins.input")
def test_init_vacancy_two_EUR(input_mock, vacancy4):
    input_mock.return_value = "3"
    vacancy = Vacancy(*vacancy4)
    assert vacancy._Vacancy__salary == {"salary": {"from": 100, "to": 200, "currency": "EUR"}}


@patch("builtins.input")
def test_init_vacancy_empty_line_RUB(input_mock, vacancy3):
    input_mock.return_value = ""
    vacancy = Vacancy(*vacancy3)
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "RUB"}}


@patch("builtins.input")
def test_init_vacancy_empty_line_two_RUB(input_mock, vacancy4):
    input_mock.return_value = ""
    vacancy = Vacancy(*vacancy4)
    assert vacancy._Vacancy__salary == {"salary": {"from": 100, "to": 200, "currency": "RUB"}}


@patch("builtins.input")
def test_init_vacancy_any_value_RUB(input_mock, vacancy3):
    input_mock.return_value = "один"
    vacancy = Vacancy(*vacancy3)
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "RUB"}}


@patch("builtins.input")
def test_init_vacancy_any_value_two_RUB(input_mock, vacancy4):
    input_mock.return_value = "один"
    vacancy = Vacancy(*vacancy4)
    assert vacancy._Vacancy__salary == {"salary": {"from": 100, "to": 200, "currency": "RUB"}}


def test_init_vacancy_not_salary():
    vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    assert vacancy._Vacancy__salary == {"salary": "Зарплата не указана"}


@patch("builtins.input")
def test_init_vacancy_error_int_salary(input_mock, capsys):
    input_mock.return_value = "100"
    vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", 100)
    captured = capsys.readouterr()
    assert captured.out == "Значение 100 должно иметь тип 'str', а не <class 'int'>\n"
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "RUB"}}


@patch("builtins.input")
def test_init_vacancy_error_value_salary(input_mock, capsys):
    input_mock.return_value = "100"
    vacancy = Vacancy(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100.50"
    )
    captured = capsys.readouterr()
    assert captured.out == (
        "Не корректно указана заработная плата, значение 'salary' должно быть положительным, \n"
        "иметь тип данных 'str' и быть целым числом, или диапазоном чисел c разделителем '-'.\n"
        "Пример ввода: если указано одно значение ЗП '1000' или '1 000'\n "
        "и '1000-2000', '1000 - 2000' или '1 000 - 2 000 если необходимо указать диапазон значений.'\n\n"
    )
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "RUB"}}


def test_lt_le_gt_(vacancy1, vacancy2, vacancy7, vacancy8, vacancy9):
    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert not (vacancy2 < vacancy1)
    assert not (vacancy1 > vacancy2)
    assert not (vacancy1 == vacancy2)

    assert vacancy7 < vacancy8
    assert vacancy8 > vacancy7
    assert not (vacancy8 < vacancy7)
    assert not (vacancy7 > vacancy8)
    assert not (vacancy7 == vacancy8)

    assert vacancy9 < vacancy2
    assert vacancy2 > vacancy9
    assert not (vacancy2 < vacancy9)
    assert not (vacancy9 > vacancy2)
    assert not (vacancy9 == vacancy2)
    assert vacancy2 != vacancy9


@patch("requests.get")
def test_lt_le_gt_true_USD(mock_get, vacancy5, vacancy6):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 100}
    assert not (vacancy5 > vacancy6)
    assert not (vacancy5 < vacancy6)
    assert vacancy5 == vacancy6


def test_lt_error(vacancy1, object_hh1):
    with pytest.raises(TypeError, match="Переданный объект не является объектом класса 'Vacancy'"):
        vacancy1._Vacancy__get_minimum_wage_other(object_hh1)


def test_init_error():
    with pytest.raises(TypeError, match="Значение 123456 должно иметь тип 'str', а не <class 'int'>"):
        Vacancy("Python Developer", 123456, "Требования: опыт работы от 3 лет...")


@patch("builtins.input")
def test_init_range_error(input_mock, capsys):
    input_mock.return_value = "100"
    vacancy = Vacancy(
        "Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "150-100"
    )
    captured = capsys.readouterr()
    assert captured.out == (
        "Не корректно указана заработная плата, сумма начальной границы, оплаты труда,\n "
        "не должно быть больше конечной границы, пример указания корректной ЗП: '1000-2000', \n"
        "'1000 - 2000' или '1 000 - 2 000'\n\n"
    )
    assert vacancy._Vacancy__salary == {"salary": {"from": None, "to": 100, "currency": "RUB"}}


def test_repr(vacancy7):
    assert repr(vacancy7) == "Vacancy"


def test_cast_to_object_list_error_value(capsys):
    assert Vacancy.cast_to_object_list([]) == []
    captured = capsys.readouterr()
    assert captured.out == "Передаваемый список пуст\n"


def test_cast_to_object_list_error_type(inf1, capsys):
    assert Vacancy.cast_to_object_list(inf1) == []
    captured = capsys.readouterr()
    assert captured.out == f"Передаваемый аргумент должно быть списком вакансий а не {type(inf1)}\n"


def test_cast_to_object_list(vacancy_RUB_to):
    Vacancy.cast_to_object_list(vacancy_RUB_to)
