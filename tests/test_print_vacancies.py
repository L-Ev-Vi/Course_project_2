from src.print_vacancies import print_vacancies


def test_print_vacancies(list_salary, capsys):
    print_vacancies(list_salary)
    captured = capsys.readouterr()
    assert captured.out == (
        "{'salary': {'from': 500, 'to': None, 'currency': 'RUB'}}\n"
        "{'salary': {'from': 400, 'to': None, 'currency': 'RUB'}}\n"
        "{'salary': {'from': 300, 'to': None, 'currency': 'RUB'}}\n"
        "{'salary': {'from': 200, 'to': None, 'currency': 'RUB'}}\n"
        "{'salary': {'from': 100, 'to': None, 'currency': 'RUB'}}\n"
    )


def test_print_vacancies_not_list(capsys):
    print_vacancies([])
    captured = capsys.readouterr()
    assert captured.out == "Ничего не найдено!\n"
