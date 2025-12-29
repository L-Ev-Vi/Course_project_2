from src.currency_exchange import CurrencyExchange


def sort_vacancies(ranged_vacancies: list, reverse: bool = True) -> list:
    """
    Функция для сортировки списка вакансий. Функция принимает список вакансий и
    необязательный аргумент указывающий порядок сортировки (по умолчанию 'True', что означает в порядке убывания),
    и возвращает список отсортированный по значению заработной платы, согласно указанного порядка.
    В случае если список пуст то будет выводиться соответствующее сообщение и возвращаться пустой список.
    """
    sorting_vacancies_by_salary = []
    try:
        if len(ranged_vacancies) == 0:
            raise ValueError("Список вакансий пуст.")
        else:
            for vacancy in ranged_vacancies:
                if vacancy["salary"] == "Зарплата не указана":
                    vacancy["max_salary"] = 0
                    sorting_vacancies_by_salary.append(vacancy)
                else:
                    if vacancy["salary"].get("to"):
                        if vacancy["salary"]["currency"] != "RUB":
                            currency = CurrencyExchange(vacancy["salary"]["currency"])
                            vacancy["max_salary"] = currency.get_currency_exchange(vacancy["salary"]["to"])
                        else:
                            vacancy["max_salary"] = vacancy["salary"]["to"]
                        sorting_vacancies_by_salary.append(vacancy)
                    else:
                        if vacancy["salary"]["currency"] != "RUB":
                            currency = CurrencyExchange(vacancy["salary"]["currency"])
                            vacancy["max_salary"] = currency.get_currency_exchange(vacancy["salary"]["from"])
                        else:
                            vacancy["max_salary"] = vacancy["salary"]["from"]
                        sorting_vacancies_by_salary.append(vacancy)
            sorting_vacancies_by_salary = sorted(ranged_vacancies, key=lambda x: x["max_salary"], reverse=reverse)
            for vacancy in sorting_vacancies_by_salary:
                del vacancy["max_salary"]
    except ValueError as e:
        print(e)
    return sorting_vacancies_by_salary


if __name__ == "__main__":
    data = [
        {
            "id": "128762270",
            "name": "Python разработчик (Middle+/Senior)",
            "salary": {"from": 300000, "to": None, "currency": "USD"},
            "alternate_url": "https://hh.ru/vacancy/128762270",
            "relations": [],
            "snippet": {"requirement": "Опыт коммерческой разработки"},
        },
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
            "salary": "Зарплата не указана",
            "alternate_url": "https://hh.ru/vacancy/128762270",
            "relations": [],
            "snippet": {"requirement": "Опыт коммерческой разработки"},
        },
    ]
    print(sort_vacancies(data))
