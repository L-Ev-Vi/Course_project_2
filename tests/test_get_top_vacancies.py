from src.get_top_vacancies import get_top_vacancies


def test_get_top_vacancies(list_salary):
    assert get_top_vacancies(list_salary) == list_salary


def test_get_top_vacancies_top_3(list_salary):
    assert get_top_vacancies(list_salary, 3) == list_salary[:3]


def test_get_top_vacancies_top_6(list_salary):
    assert get_top_vacancies(list_salary, 6) == list_salary


def test_get_top_vacancies_error(list_salary, capsys):
    get_top_vacancies(list_salary, "3")
    coptured = capsys.readouterr()
    assert coptured.out == (
        "Для определения количества топовых вакансий, в качестве второго аргумента, \n"
        "необходимо передать целое число\n"
    )
    assert get_top_vacancies(list_salary, "3") == []
