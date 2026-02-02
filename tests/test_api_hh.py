from unittest.mock import patch


def test_init_object(object_hh1):
    assert object_hh1._HH__url == "https://api.hh.ru/vacancies"
    assert object_hh1._HH__params == {
        "page": 0,
        "per_page": 0,
        "text": "",
        "area": 1,
        "period": 1,
        "search_field": "name",
    }
    assert object_hh1._HH__headers == {"User-Agent": "HH-User-Agent"}
    assert object_hh1._HH__vacancies == []


@patch("requests.get")
def test_get_vacancies(mock_get, object_hh1):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "id": "128762270",
                "name": "Python разработчик (Middle+/Senior)",
                "salary": {"from": None, "to": 410000, "currency": "RUB"},
                "alternate_url": "https://hh.ru/vacancy/128762270",
                "relations": [],
                "snippet": {"requirement": "Опыт коммерческой разработки"},
            },
            {
                "id": "128762270",
                "name": "Python разработчик (Middle+/Senior)",
                "salary": None,
                "alternate_url": "https://hh.ru/vacancy/128762270",
                "relations": [],
                "snippet": {"requirement": "Опыт коммерческой разработки"},
            },
        ],
        "found": 32,
        "pages": 1,
        "page": 1,
        "per_page": 50,
        "clusters": None,
        "arguments": None,
        "fixes": None,
        "suggests": None,
        "alternate_url": "https://hh.ru/search/vacancy?area=1&enable_snippets=true&items_on_page=50&page=1&search_"
        "field=name&search_period=1&text=Python",
    }
    assert object_hh1.get_vacancies("python") == [
        {
            "id": "128762270",
            "name": "Python разработчик (Middle+/Senior)",
            "salary": {"from": None, "to": 410000, "currency": "RUB"},
            "url": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
        {
            "id": "128762270",
            "name": "Python разработчик (Middle+/Senior)",
            "salary": None,
            "url": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        }
    ]
    mock_get.assert_called()


def test_get_vacancies_error(object_hh1, capsys):
    object_hh1.get_vacancies(123456)
    captured = capsys.readouterr()
    assert captured.out == "Для поиска вакансий необходимо указать ключевое слово или фразу\n"
    assert object_hh1.get_vacancies(123456) == []


@patch("requests.get")
def test_connecting_to_api_error_500(mock_get, object_hh1, capsys):
    mock_get.return_value.status_code = 500
    object_hh1.get_vacancies("python")
    captured = capsys.readouterr()
    assert captured.out == "Ошибка на стороне сервера при выполнении запроса.\n"
    assert object_hh1.get_vacancies("python") == []


@patch("requests.get")
def test_connecting_to_api_error_200(mock_get, object_hh1, capsys):
    mock_get.return_value.status_code = 300
    object_hh1.get_vacancies("python")
    captured = capsys.readouterr()
    assert captured.out == "Ошибка при выполнении запроса на базовый URL.\n"
    assert object_hh1.get_vacancies("python") == []


@patch("requests.get")
def test_connecting_to_api_error_400(mock_get, object_hh1, capsys):
    mock_get.return_value.status_code = 400
    object_hh1.get_vacancies("python")
    captured = capsys.readouterr()
    assert captured.out == "Ошибка со стороны пользователя при выполнении запроса.\n"
    assert object_hh1.get_vacancies("python") == []


@patch("requests.get")
def test_get_vacancies_(mock_get, object_hh1):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "id": "128762270",
                "name": "Python разработчик (Middle+/Senior)",
                "salary": {"from": None, "to": 410000, "currency": "RUR"},
                "alternate_url": "https://hh.ru/vacancy/128762270",
                "relations": [],
                "snippet": {"requirement": "Опыт коммерческой разработки"},
            }
        ],
        "found": 32,
        "pages": 1,
        "page": 0,
        "per_page": 50,
        "clusters": None,
        "arguments": None,
        "fixes": None,
        "suggests": None,
        "alternate_url": "https://hh.ru/search/vacancy?area=1&enable_snippets=true&items_on_page=50&page=1&search_"
        "field=name&search_period=1&text=Python",
    }
    assert object_hh1.get_vacancies("python") == [
        {
            "id": "128762270",
            "name": "Python разработчик (Middle+/Senior)",
            "salary": {"from": None, "to": 410000, "currency": "RUB"},
            "url": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        }
    ]
    mock_get.assert_called()
