def get_top_vacancies(sorted_vacancies: list, top_n: int = 5) -> list:
    """
    Функция принимает отсортированный по убыванию список вакансий и целое число 'top_n',
    и возвращает 'top_n'(по умолчанию 5) число вакансий в виде списка.
    Если число 'top_n' превышает количество вакансий в переданном списке, то будет возвращаться всё содержимое списка.
    В случае если список пуст то будет возвращаться пустой список.
    """
    try:
        if not isinstance(top_n, int):
            raise TypeError(
                "Для определения количества топовых вакансий, в качестве второго аргумента, \n"
                "необходимо передать целое число"
            )
        if len(sorted_vacancies) <= top_n:
            result = sorted_vacancies
        else:
            result = sorted_vacancies[:top_n]
    except TypeError as e:
        print(e)
        return []
    return result
