from unittest.mock import patch

from src.sort_vacancies import sort_vacancies


def test_sort_vacancies(list_sort):
    assert sort_vacancies(list_sort) == list_sort


def test_sort_vacancies_error(capsys):
    sort_vacancies([])
    captured = capsys.readouterr()
    assert captured.out == "Список вакансий пуст.\n"
    assert sort_vacancies([]) == []


@patch("requests.get")
def test_sort_vacancies_from(mock_get, list_sort_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 100}
    assert sort_vacancies(list_sort_USD_from) == list_sort_USD_from


@patch("requests.get")
def test_sort_vacancies_to(mock_get, list_sort_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 100}
    assert sort_vacancies(list_sort_USD_to) == list_sort_USD_to
