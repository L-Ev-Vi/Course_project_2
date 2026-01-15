def print_vacancies(top_vacancies: list) -> None:
    """Функция принимает список с топ вакансиями по ЗП и выводит их в виде строк.
    Если список пуст, то функция ничего не возвращает."""
    if len(top_vacancies) == 0:
        print("Ничего не найдено!")
    else:
        print(*top_vacancies, sep="\n")
