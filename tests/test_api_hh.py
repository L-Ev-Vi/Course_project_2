from unittest.mock import patch


def test_init_object(object_hh1):
    assert object_hh1._HH__url == "https://api.hh.ru/vacancies"
    assert object_hh1._HH__params == {"page": 0, "per_page": 0, "text": "", "area": 1, "period": 1,
                                      "search_field": "name"}
    assert object_hh1._HH__headers == {"User-Agent": "HH-User-Agent"}
    assert object_hh1._HH__vacancies == []


@patch("requests.get")
def test_get_vacancies(mock_get, object_hh1):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"pages": 0, "items":
        [{'id': '128721230', 'premium': False,
          'name': 'Стажёр / Junior Backend-разработчик (Python / Go)',
          'department': None, 'has_test': True,
          'response_letter_required': True,
          'area': {'id': '1', 'name': 'Москва',
                   'url': 'https://api.hh.ru/areas/1'}, 'salary': None,
          'salary_range': None}]}
    assert object_hh1.get_vacancies("python") == [{'id': '128721230', 'premium': False,
                                                   'name': 'Стажёр / Junior Backend-разработчик (Python / Go)',
                                                   'department': None, 'has_test': True,
                                                   'response_letter_required': True,
                                                   'area': {'id': '1', 'name': 'Москва',
                                                            'url': 'https://api.hh.ru/areas/1'}, 'salary': None,
                                                   'salary_range': None}]
    mock_get.assert_called_once_with(url=object_hh1._HH__url,
                                     params={"page": 0, "per_page": 50, "text": "python", "area": 1, "period": 1,
                                             "search_field": "name"})


def test_get_vacancies_error(object_hh1, capsys):
    object_hh1.get_vacancies(123456)
    captured = capsys.readouterr()
    assert captured.out == "Для поиска вакансий необходимо указать ключевое слово или фразу\n"
    assert object_hh1.get_vacancies(123456) == []


@patch("requests.get")
def test_connecting_to_api_error_500(mock_get, object_hh1, capsys):
    mock_get.return_value.status_code = 500
    object_hh1._HH__connecting_to_api()
    captured = capsys.readouterr()
    assert captured.out == "Ошибка на стороне сервера при выполнении запроса.\n"
    assert object_hh1.get_vacancies("python") == []


@patch("requests.get")
def test_connecting_to_api_error_200(mock_get, object_hh1, capsys):
    mock_get.return_value.status_code = 300
    object_hh1._HH__connecting_to_api()
    captured = capsys.readouterr()
    assert captured.out == "Ошибка при выполнении запроса на базовый URL.\n"
    assert object_hh1.get_vacancies("python") == []


@patch("requests.get")
def test_connecting_to_api_error_400(mock_get, object_hh1, capsys):
    mock_get.return_value.status_code = 400
    object_hh1._HH__connecting_to_api()
    captured = capsys.readouterr()
    assert captured.out == "Ошибка со стороны пользователя при выполнении запроса.\n"
    assert object_hh1.get_vacancies("python") == []
