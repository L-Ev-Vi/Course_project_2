import os
from unittest.mock import patch

import pandas as pd

from src.vacancy import Vacancy


def test_init_xlsx_saver(xlsx1):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "test.xlsx")
    assert xlsx1._XLSXSaver__name_file == "test"
    assert xlsx1._XLSXSaver__path_file == path
    os.remove("data/test.xlsx")


def test_add_vacancy(xlsx1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    assert not os.path.getsize("data/test.xlsx")
    xlsx1.add_vacancy(vacancy)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    os.remove("data/test.xlsx")


def test_add_vacancy_overflow_error(xlsx1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    xlsx1.add_vacancy(vacancy)
    xlsx1.add_vacancy(vacancy)
    captured = capsys.readouterr()
    assert captured.out == f"В файл не сохраняются дубликаты вакансий, {str(vacancy)} уже содержится в файле.\n"
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    os.remove("data/test.xlsx")


def test_add_vacancy_type_error(xlsx1, inf1, capsys):
    xlsx1.add_vacancy(inf1)
    captured = capsys.readouterr()
    assert captured.out == f"Добавляемый объект реализован от {type(inf1)}, а не от класса Vacancy(Вакансия)!\n"
    os.remove("data/test.xlsx")


def test_get_job_information(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information() == [
        {
            "id": 49,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_keyword(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information("Python") == [
        {
            "id": 50,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_keyword_salary_range_min(xlsx1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    xlsx1.add_vacancy(vacancy)
    assert xlsx1.get_job_information("Java", 100) == []
    os.remove("data/test.xlsx")


def test_get_job_information_keyword_salary_range(xlsx1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    xlsx1.add_vacancy(vacancy)
    assert xlsx1.get_job_information("Java", 100, 200) == []
    os.remove("data/test.xlsx")


def test_get_job_information_keyword_salary(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information("Python", 100) == [
        {
            "id": 53,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_keyword_salary_range_max(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information("Python", salary_range_max=200) == [
        {
            "id": 54,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_salary_range_max(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information(salary_range_max=200) == [
        {
            "id": 55,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_salary_range_min(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information(salary_range_min=100) == [
        {
            "id": 56,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_salary_range(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    assert xlsx1.get_job_information(salary_range_min=100, salary_range_max=200) == [
        {
            "id": 57,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "RUB",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_get_job_information_error_keyword(xlsx1, capsys):
    xlsx1.get_job_information(100)
    captured = capsys.readouterr()
    assert captured.out == (
        "Ключевое слово для поиска должно иметь тип 'str'. \n"
        "Если не указывать ключевое слово, \n"
        "то по умолчанию результатом будет содержимое всего файла.\n"
    )
    assert xlsx1.get_job_information(100) == []
    os.remove("data/test.xlsx")


def test_get_job_information_error_salary_range_min(xlsx1, capsys):
    xlsx1.get_job_information(salary_range_min="100")
    captured = capsys.readouterr()
    assert captured.out == (
        "Не обязательный параметр обозначающий минимальную заработную плату, \n"
        "должен быть целым числом и иметь тип 'int'.\n"
    )
    assert xlsx1.get_job_information(salary_range_min="100") == []
    os.remove("data/test.xlsx")


def test_get_job_information_error_salary_range_max(xlsx1, capsys):
    xlsx1.get_job_information(salary_range_max="100")
    captured = capsys.readouterr()
    assert captured.out == (
        "Не обязательный параметр обозначающий максимальную заработную плату, \n"
        "должен быть целым числом и иметь тип 'int'.\n"
    )
    assert xlsx1.get_job_information(salary_range_max="100") == []
    os.remove("data/test.xlsx")


def test_get_job_information_error_salary_range_max_0(xlsx1, capsys):
    xlsx1.get_job_information(salary_range_max=-1)
    captured = capsys.readouterr()
    assert captured.out == "Сумма заработной платы не может быть отрицательной.\n"
    assert xlsx1.get_job_information(salary_range_max=-1) == []
    os.remove("data/test.xlsx")


def test_get_job_information_error_salary_range_min_0(xlsx1, capsys):
    xlsx1.get_job_information(salary_range_min=-1)
    captured = capsys.readouterr()
    assert captured.out == "Сумма заработной платы не может быть отрицательной.\n"
    assert xlsx1.get_job_information(salary_range_min=-1) == []
    os.remove("data/test.xlsx")


def test_get_job_information_error_salary_range(xlsx1, vacancy7, capsys):
    xlsx1.add_vacancy(vacancy7)
    xlsx1.get_job_information(salary_range_min=200, salary_range_max=100)
    captured = capsys.readouterr()
    assert captured.out == (
        "Не корректно указанны суммы обозначающие границы оплаты труда, \n"
        "значение минимальной оплаты не может быть больше "
        "значения максимальной оплаты.\n"
    )
    assert xlsx1.get_job_information(salary_range_min=200, salary_range_max=100) == []
    os.remove("data/test.xlsx")


def test_delete_vacancy(xlsx1, vacancy7):
    xlsx1.add_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    xlsx1.delete_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 0
    os.remove("data/test.xlsx")


def test_delete_vacancy_error_type(xlsx1, inf1, vacancy7, capsys):
    xlsx1.add_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    xlsx1.delete_vacancy(inf1)
    captured = capsys.readouterr()
    assert captured.out == (
        f"Не возможно выполнить удаление, " f"объект реализован от {type(inf1)}, а не от класса Vacancy(Вакансия)!\n"
    )
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    os.remove("data/test.xlsx")


def test_delete_vacancy_error_filenotfound(xlsx1, vacancy7, capsys):
    xlsx1.add_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    xlsx1.delete_vacancy(vacancy7)
    xlsx1.delete_vacancy(vacancy7)
    captured = capsys.readouterr()
    assert captured.out == "Не возможно выполнить удаление объекта из пустого файла\n"
    os.remove("data/test.xlsx")


def test_delete_content(xlsx1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    vacancy2 = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 2 лет...")
    xlsx1.add_vacancy(vacancy)
    xlsx1.add_vacancy(vacancy2)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 2
    xlsx1.delete_content()
    captured = capsys.readouterr()
    assert captured.out == "Выполнена очистка файла!\n"
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 0


def test_delete_content_error_(xlsx1, vacancy7, capsys):
    xlsx1.add_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    xlsx1.delete_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 0
    xlsx1.delete_content()
    captured = capsys.readouterr()
    assert captured.out == "Не возможно выполнить удаление объекта из пустого файла!\n"


@patch("requests.get")
def test_get_job_information_range_max(mock_get, xlsx1, vacancy10):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    xlsx1.add_vacancy(vacancy10)
    assert xlsx1.get_job_information(salary_range_max=200) == [
        {
            "id": 65,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "USD",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


@patch("requests.get")
def test_get_job_information_range_min(mock_get, xlsx1, vacancy10):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 100}
    xlsx1.add_vacancy(vacancy10)
    assert xlsx1.get_job_information(salary_range_min=100) == [
        {
            "id": 66,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "USD",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


@patch("requests.get")
def test_get_job_information_range_min_max(mock_get, xlsx1, vacancy10):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    xlsx1.add_vacancy(vacancy10)
    assert xlsx1.get_job_information(salary_range_min=100, salary_range_max=200) == [
        {
            "id": 67,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "USD",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


@patch("requests.get")
def test_get_job_information_keyword_range_min_max(mock_get, xlsx1, vacancy10):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    xlsx1.add_vacancy(vacancy10)
    assert xlsx1.get_job_information("Python", salary_range_min=100, salary_range_max=200) == [
        {
            "id": 68,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "USD",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


@patch("requests.get")
def test_get_job_information_keyword_range_min(mock_get, xlsx1, vacancy10):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    xlsx1.add_vacancy(vacancy10)
    assert xlsx1.get_job_information("Python", salary_range_min=100) == [
        {
            "id": 69,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "USD",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


@patch("requests.get")
def test_get_job_information_keyword_range_max(mock_get, xlsx1, vacancy10):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    xlsx1.add_vacancy(vacancy10)
    assert xlsx1.get_job_information("Python", salary_range_max=200) == [
        {
            "id": 70,
            "name": "Python Developer",
            "from": 100,
            "to": 150,
            "currency": "USD",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.xlsx")


def test_delete_vacancy_error_value(xlsx1, vacancy7, vacancy8, capsys):
    xlsx1.add_vacancy(vacancy7)
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    xlsx1.delete_vacancy(vacancy8)
    captured = capsys.readouterr()
    assert captured.out == f"Не возможно выполнить удаление, в файле отсутствует вакансия, {str(vacancy8)}\n"
    data = pd.read_excel("data/test.xlsx").to_dict(orient="records")
    assert len(data) == 1
    os.remove("data/test.xlsx")
