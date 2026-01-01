import json
import os
from unittest.mock import patch

from src.vacancy import Vacancy


def test_init_json_saver(json1):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "test.json")
    assert json1._JSONSaver__name_file == "test"
    assert json1._JSONSaver__path_file == path
    os.remove("data/test.json")


def test_add_vacancy(json1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    assert not os.path.getsize("data/test.json")
    json1.add_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    os.remove("data/test.json")


def test_add_vacancy_overflow_error(json1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    json1.add_vacancy(vacancy)
    captured = capsys.readouterr()
    assert captured.out == f"В файл не сохраняются дубликаты вакансий, {str(vacancy)} уже содержится в файле.\n"
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    os.remove("data/test.json")


def test_add_vacancy_type_error(json1, inf1, capsys):
    json1.add_vacancy(inf1)
    captured = capsys.readouterr()
    assert captured.out == f"Добавляемый объект реализован от {type(inf1)}, а не от класса Vacancy(Вакансия)!\n"
    os.remove("data/test.json")


def test_get_job_information(json1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information() == [
        {
            "id": 3,
            "name": "Java Developer",
            "salary": "Зарплата не указана",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


def test_get_job_information_keyword(json1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information("Java") == [
        {
            "id": 4,
            "name": "Java Developer",
            "salary": "Зарплата не указана",
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range_min(json1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information("Java", 100) == []
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range(json1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information("Java", 100, 200) == []
    os.remove("data/test.json")


@patch("builtins.input")
def test_get_job_information_keyword_salary(input_mock, json1):
    input_mock.return_value = "1"
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "150")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information("Java", 100) == [
        {
            "id": 7,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


@patch("builtins.input")
def test_get_job_information_keyword_salary_range_max(input_mock, json1):
    input_mock.return_value = "1"
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "150")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information("Java", salary_range_max=200) == [
        {
            "id": 8,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


@patch("builtins.input")
def test_get_job_information_salary_range_max(input_mock, json1):
    input_mock.return_value = "1"
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "150")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information(salary_range_max=200) == [
        {
            "id": 9,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


@patch("builtins.input")
def test_get_job_information_salary_range_min(input_mock, json1):
    input_mock.return_value = "1"
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "150")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information(salary_range_min=100) == [
        {
            "id": 10,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


@patch("builtins.input")
def test_get_job_information_salary_range(input_mock, json1):
    input_mock.return_value = "1"
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "150")
    json1.add_vacancy(vacancy)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == [
        {
            "id": 11,
            "name": "Java Developer",
            "salary": {"from": 150, "to": None, "currency": "RUB"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


def test_get_job_information_error_keyword(json1, capsys):
    json1.get_job_information(100)
    captured = capsys.readouterr()
    assert captured.out == (
        "Ключевое слово для поиска должно иметь тип 'str'. \n"
        "Если не указывать ключевое слово, \n"
        "то по умолчанию результатом будет содержимое всего файла.\n"
    )
    assert json1.get_job_information(100) == []
    os.remove("data/test.json")


def test_get_job_information_error_salary_range_min(json1, capsys):
    json1.get_job_information(salary_range_min="100")
    captured = capsys.readouterr()
    assert captured.out == (
        "Не обязательный параметр обозначающий минимальную заработную плату, \n"
        "должен быть целым числом и иметь тип 'int'.\n"
    )
    assert json1.get_job_information(salary_range_min="100") == []
    os.remove("data/test.json")


def test_get_job_information_error_salary_range_max(json1, capsys):
    json1.get_job_information(salary_range_max="100")
    captured = capsys.readouterr()
    assert captured.out == (
        "Не обязательный параметр обозначающий максимальную заработную плату, \n"
        "должен быть целым числом и иметь тип 'int'.\n"
    )
    assert json1.get_job_information(salary_range_max="100") == []
    os.remove("data/test.json")


def test_get_job_information_error_salary_range_max_0(json1, capsys):
    json1.get_job_information(salary_range_max=-1)
    captured = capsys.readouterr()
    assert captured.out == "Сумма заработной платы не может быть отрицательной.\n"
    assert json1.get_job_information(salary_range_max=-1) == []
    os.remove("data/test.json")


def test_get_job_information_error_salary_range_min_0(json1, capsys):
    json1.get_job_information(salary_range_min=-1)
    captured = capsys.readouterr()
    assert captured.out == "Сумма заработной платы не может быть отрицательной.\n"
    assert json1.get_job_information(salary_range_min=-1) == []
    os.remove("data/test.json")


def test_get_job_information_error_salary_range(json1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    json1.get_job_information(salary_range_min=200, salary_range_max=100)
    captured = capsys.readouterr()
    assert captured.out == (
        "Не корректно указанны суммы обозначающие границы оплаты труда, \n"
        "значение минимальной оплаты не может быть больше "
        "значения максимальной оплаты.\n"
    )
    assert json1.get_job_information(salary_range_min=200, salary_range_max=100) == []
    os.remove("data/test.json")


def test_get_job_information_keyword_error_salary_range(json1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    json1.get_job_information("Java", salary_range_min=200, salary_range_max=100)
    captured = capsys.readouterr()
    assert captured.out == (
        "Не корректно указанны суммы обозначающие границы оплаты труда, \n"
        "значение минимальной оплаты не может быть больше "
        "значения максимальной оплаты.\n"
    )
    assert json1.get_job_information(salary_range_min=200, salary_range_max=100) == []
    os.remove("data/test.json")


def test_delete_vacancy(json1):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    json1.delete_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 0
    os.remove("data/test.json")


def test_delete_vacancy_error_type(json1, inf1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    json1.delete_vacancy(inf1)
    captured = capsys.readouterr()
    assert captured.out == (
        f"Не возможно выполнить удаление, " f"объект реализован от {type(inf1)}, а не от класса Vacancy(Вакансия)!\n"
    )
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    os.remove("data/test.json")


def test_delete_vacancy_error_filenotfound(json1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    json1.delete_vacancy(vacancy)
    json1.delete_vacancy(vacancy)
    captured = capsys.readouterr()
    assert captured.out == "Не возможно выполнить удаление объекта из пустого файла\n"
    json1.add_vacancy(vacancy)
    os.remove("data/test.json")


def test_delete_content(json1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    vacancy2 = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 2 лет...")
    json1.add_vacancy(vacancy)
    json1.add_vacancy(vacancy2)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 2
    json1.delete_content()
    captured = capsys.readouterr()
    assert captured.out == "Выполнена очистка файла!\n"
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 0


def test_delete_content_error_(json1, capsys):
    vacancy = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    json1.add_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    json1.delete_vacancy(vacancy)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 0
    json1.delete_content()
    captured = capsys.readouterr()
    assert captured.out == "Не возможно выполнить удаление объекта из пустого файла!\n"


@patch("requests.get")
def test_get_job_information_range_max(mock_get, json1, vacancy6):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    json1.add_vacancy(vacancy6)
    assert json1.get_job_information(salary_range_max=200) == [
        {
            "id": 20,
            "name": "Java Developer",
            "salary": {"from": None, "to": 200, "currency": "USD"},
            "url": "<https://hh.ru/vacancy/123456>",
            "description": "Требования: опыт работы от 3 лет...",
        }
    ]
    os.remove("data/test.json")


def test_get_job_information_salary_range_max_to(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_max=200) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_salary_range_max_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_max=200) == vacancy_USD_from
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_range_min(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100) == vacancy_USD_to
    os.remove("data/test.json")


def test_get_job_information_salary_range_min_to(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_salary_range_min_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100) == vacancy_USD_from
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_range_USD(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_USD_to
    os.remove("data/test.json")


def test_get_job_information_salary_range_to(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_salary_range_USD_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_USD_from
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_range_USD_to(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_USD_to
    os.remove("data/test.json")


def test_get_job_information_salary_range_RUB_to(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_salary_range_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_USD_from
    os.remove("data/test.json")


def test_get_job_information_salary_range_from_to_RUB(json1, vacancy_RUB_from_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_from_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_RUB_from_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_salary_range_from_to_USD(mock_get, json1, vacancy_USD_from_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information(salary_range_min=100, salary_range_max=200) == vacancy_USD_from_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_range_max(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_max=200) == vacancy_USD_to
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range_max_to(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_max=200) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_salary_range_max_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_max=200) == vacancy_USD_from
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_range_min(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100) == vacancy_USD_to
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range_min_to(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_salary_range_min_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100) == vacancy_USD_from
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_range_USD_to(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_USD_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_salary_range_USD_from(mock_get, json1, vacancy_USD_from):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_USD_from
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_range_USD(mock_get, json1, vacancy_USD_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_USD_to
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range_RUB(json1, vacancy_RUB_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_RUB_to
    os.remove("data/test.json")


@patch("requests.get")
def test_get_job_information_keyword_salary_range_from_to_USD(mock_get, json1, vacancy_USD_from_to):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 200}
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_USD_from_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_USD_from_to
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range_RUB_from(json1, vacancy_RUB_from):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_from, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_RUB_from
    os.remove("data/test.json")


def test_get_job_information_keyword_salary_range_from_to_RUB(json1, vacancy_RUB_from_to):
    with open("data/test.json", "a", encoding="utf-8") as f:
        json.dump(vacancy_RUB_from_to, f, ensure_ascii=False, indent=4)
    assert json1.get_job_information("Java", salary_range_min=100, salary_range_max=200) == vacancy_RUB_from_to
    os.remove("data/test.json")


def test_delete_vacancy_error_value(json1, vacancy7, vacancy8, capsys):
    json1.add_vacancy(vacancy7)
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    json1.delete_vacancy(vacancy8)
    captured = capsys.readouterr()
    assert captured.out == f"Не возможно выполнить удаление, в файле отсутствует вакансия, {str(vacancy8)}\n"
    with open("data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    os.remove("data/test.json")
