from typing import Any

from accessify import private

from src.base_filling_in_data import FillingInData


class FillingInRequestData(FillingInData):
    """Класс для взаимодействия с пользователем при выполнении поиска по вакансиям на платформе hh.ru."""

    def __init__(self) -> None:
        """Инициализация объекта класса"""

    @private
    def filling_in_data(self) -> list:
        """Метод для заполнения параметров. Метод запрашивает параметры для выполнения поиска."""
        search_query = input("Введите поисковый запрос\n" "->")
        while True:
            if search_query == "" or len(search_query) < 2:
                search_query = input("Введите корректный поисковый запрос\n" "->")
            else:
                break
        top = input(
            "Введите количество вакансий для вывода в топ (не обязательный параметр, "
            "по умолчанию выводится топ 5 вакансий)\n"
            "->"
        )
        while True:
            if top == "":
                top_n = 5
                break
            elif not top.isdigit():
                top = input(
                    "Введите корректное количество вакансий для вывода в топ"
                    "(не обязательный параметр,по умолчанию выводится топ 5 вакансий)\n"
                    "->"
                )
            else:
                top_n = int(top)
                break
        word = input(
            "Введите ключевые слова для фильтрации вакансий, \n"
            "используя в качестве разделителя пробел (не обязательный параметр)\n"
            "->"
        )
        if not word:
            keyword = None
        else:
            keyword = word.replace(",", " ")
        salary_min = input("Введите минимальную заработную плату (Пример: 100000) \n" "(не обязательный параметр)\n->")
        while True:
            if not salary_min:
                salary_range_min = None
                break
            elif not salary_min.isdigit():
                salary_min = input(
                    "Введите корректную минимальную заработную плату (Пример: 100000) \n"
                    "(не обязательный параметр)\n"
                    "->"
                )
            else:
                salary_range_min = int(salary_min)
                break
        salary_max = input(
            "Введите максимальную заработную плату (Пример: 150000) \n" "(не обязательный параметр)\n->"
        )
        while True:
            if not salary_max:
                salary_range_max = None
                break
            elif not salary_max.isdigit():
                salary_max = input(
                    "Введите корректную максимальную заработную плату (Пример: 150000) \n"
                    "(не обязательный параметр)\n"
                    "->"
                )
            else:
                salary_range_max = int(salary_max)
                break
        return [search_query, top_n, keyword, salary_range_min, salary_range_max]

    def getting_data(self) -> Any:
        """Метод для получения параметров"""
        return self.filling_in_data()
