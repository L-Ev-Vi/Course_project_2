def print_vacancies(top_vacancies: list) -> None:
    """Функция принимает список с топ вакансиями по ЗП и выводит их в виде строк.
    Если список пуст, то функция ничего не возвращает."""
    if len(top_vacancies) == 0:
        print("Ничего не найдено!")
    else:
        print(*top_vacancies, sep="\n")


if __name__ == "__main__":
    d = [
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
            "salary": {"from": 300000, "to": None, "currency": "RUB"},
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

    print_vacancies(d)
