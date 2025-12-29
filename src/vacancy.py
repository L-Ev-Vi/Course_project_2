import re
from typing import Any

from src.currency_exchange import CurrencyExchange


class Vacancy:
    """Класс для работы с вакансиями"""

    __ID_vacancy = 1

    __slots__ = ("__id", "__name", "__salary", "__link", "__description")

    def __init__(self, name: str, link: str, description: str, salary: Any = None) -> None:
        """Конструктор объекта класса"""
        self.__id = self.__ID_vacancy
        self.__validation_data(name)
        self.__name = name
        self.__salary = self.__validation_salary(salary)
        self.__validation_data(link)
        self.__link = link
        self.__validation_data(description)
        self.__description = description
        Vacancy.__ID_vacancy += 1

    def __repr__(self) -> str:
        """Метод возвращает информацию об экземпляре класса."""
        return f"{self.__class__.__name__}"

    def __str__(self) -> str:
        """Метод возвращает пользовательскую информацию об экземпляре класса."""
        return f"Вакансия({self.__name}...)"

    @classmethod
    def __validation_data(cls, value: Any) -> str:
        """Метод валидации данных, которыми инициализируются атрибут объекта-класса."""
        if type(value) is not str:
            raise TypeError(f"Значение {value} должно иметь тип 'str', а не {type(value)}")
        return value

    @classmethod
    def __validation_salary(cls, salary: str) -> dict:
        """Метод валидации данных, которыми инициализируются атрибут 'salary'."""
        pattern = re.compile(r"^\d+\s\d+\s\-\s\d+\s\d+$")
        pattern1 = re.compile(r"^\d+\s\-\s\d+$")
        pattern2 = re.compile(r"^\d+\-\d+$")
        pattern3 = re.compile(r"^\d+$")
        pattern4 = re.compile(r"^\d+\s\d+$")
        currencies = ["RUB", "USD", "EUR"]
        result: dict[Any, Any] = {}
        x = True
        while x:
            try:
                if salary is None or salary == "":
                    result = {"salary": "Зарплата не указана"}
                elif isinstance(salary, dict):
                    if salary["currency"]:
                        if salary["from"] or salary["to"]:
                            result = {"salary": salary}
                elif type(salary) is not str:
                    raise TypeError(f"Значение {salary} должно иметь тип 'str', а не {type(salary)}")
                elif pattern.fullmatch(salary) or pattern1.fullmatch(salary) or pattern2.fullmatch(salary):
                    initial_range = salary.replace(" ", "").split("-")[0]
                    final_range = salary.replace(" ", "").split("-")[1]
                    if int(final_range) <= int(initial_range):
                        raise ValueError(
                            "Не корректно указана заработная плата, сумма начальной границы, оплаты труда,\n "
                            "не должно быть больше конечной границы, пример указания корректной ЗП: '1000-2000', "
                            "'1000 - 2000' или '1 000 - 2 000'\n"
                        )
                    else:
                        choosing_currency = input(
                            "Выберите номер валюты, в которой будет производиться расчёт заработной платы.\n"
                            "Если ни чего не выбрано или был введён не верный вод, то\n"
                            "по умолчанию присваивается 'RUB'\n"
                            "1 - RUB\n"
                            "2 - USD\n"
                            "3 - EUR\n"
                            "->"
                        )
                        if choosing_currency not in ["1", "2", "3"] or choosing_currency == "":
                            result = {
                                "salary": {"from": int(initial_range), "to": int(final_range), "currency": "RUB"}
                            }
                        else:
                            result = {
                                "salary": {
                                    "from": int(initial_range),
                                    "to": int(final_range),
                                    "currency": currencies[int(choosing_currency) - 1],
                                }
                            }
                elif pattern3.fullmatch(salary) or pattern4.fullmatch(salary):
                    salary = salary.replace(" ", "")
                    choosing_currency = input(
                        "Выберите номер валюты, в которой будет производиться расчёт заработной платы.\n"
                        "Если ни чего не выбрано или был введён не верный вод, то\n"
                        "по умолчанию присваивается 'RUB'\n"
                        "1 - RUB\n"
                        "2 - USD\n"
                        "3 - EUR\n"
                        "->"
                    )
                    prefix_value = input(
                        "Выберите границу диапазона заработной платы где\n "
                        "1='от'\n "
                        "2='до' указанной суммы.\n"
                        "Если ни чего не выбрано или был введён не верный вод, то\n"
                        "по умолчанию присваивается диапазон 'до'\n"
                        "->"
                    )
                    if choosing_currency not in ["1", "2", "3"] or choosing_currency == "":
                        if prefix_value == "1":
                            result = {"salary": {"from": int(salary), "to": None, "currency": "RUB"}}
                        else:
                            result = {"salary": {"from": None, "to": int(salary), "currency": "RUB"}}
                    else:
                        if prefix_value == "1":
                            result = {
                                "salary": {
                                    "from": int(salary),
                                    "to": None,
                                    "currency": currencies[int(choosing_currency) - 1],
                                }
                            }
                        else:
                            result = {
                                "salary": {
                                    "from": None,
                                    "to": int(salary),
                                    "currency": currencies[int(choosing_currency) - 1],
                                }
                            }
                else:
                    raise TypeError(
                        "Не корректно указана заработная плата, значение 'salary' должно быть положительным, \n"
                        "иметь тип данных 'str' и быть целым числом, или диапазоном чисел c разделителем '-'.\n"
                        "Пример ввода: если указано одно значение ЗП '1000' или '1 000'\n "
                        "и '1000-2000', '1000 - 2000' или '1 000 - 2 000 если необходимо указать диапазон значений.'\n"
                    )
            except TypeError as e:
                print(e)
                salary = input("Укажите значение заработной платы или оставьте значение зарплаты пустым\n" "->")
                x = True
            except ValueError as e:
                print(e)
                salary = input("Укажите значение заработной платы или оставьте значение зарплаты пустым\n" "->")
                x = True
            else:
                x = False
        return result

    def __get_minimum_wage(self) -> int:
        """Метод для определения минимальной предлагаемой оплаты труда объекта класса"""
        if self.__salary["salary"] == "Зарплата не указана":
            salary = 0
        elif not self.__salary["salary"]["from"]:
            salary = self.__salary["salary"]["to"]
            if self.__salary["salary"]["currency"] != "RUB":
                currency = CurrencyExchange(self.__salary["salary"]["currency"])
                salary = currency.get_currency_exchange(salary)
        else:
            salary = self.__salary["salary"]["from"]
            if self.__salary["salary"]["currency"] != "RUB":
                currency = CurrencyExchange(self.__salary["salary"]["currency"])
                salary = currency.get_currency_exchange(salary)
        return salary

    @classmethod
    def __get_minimum_other(cls, other: object) -> int:
        """Метод для определения минимальной предлагаемой оплаты труда сравниваемого объекта класса"""
        if not isinstance(other, Vacancy):
            raise TypeError("Переданный объект не является объектом класса 'Vacancy'")
        if other.__salary["salary"] == "Зарплата не указана":
            salary = 0
        elif not other.__salary["salary"]["from"]:
            salary = other.__salary["salary"]["to"]
            if other.__salary["salary"]["currency"] != "RUB":
                currency = CurrencyExchange(other.__salary["salary"]["currency"])
                salary = currency.get_currency_exchange(salary)
        else:
            salary = other.__salary["salary"]["from"]
            if other.__salary["salary"]["currency"] != "RUB":
                currency = CurrencyExchange(other.__salary["salary"]["currency"])
                salary = currency.get_currency_exchange(salary)
        return salary

    def __lt__(self, other: object) -> bool:
        """Метод для операции сравнения «меньше»"""
        salary = self.__get_minimum_other(other)
        return self.__get_minimum_wage() < salary

    def __eq__(self, other: object) -> bool:
        """Метод для операции сравнения «меньше или равно»"""
        salary = self.__get_minimum_other(other)
        return self.__get_minimum_wage() == salary

    @property
    def get_job_properties(self) -> dict:
        """Метод возвращает словарь в котором содержатся публичная информация о свойствах объекта."""
        return {
            "id": self.__id,
            "name": self.__name,
            "salary": self.__salary["salary"],
            "url": self.__link,
            "description": self.__description,
        }

    @classmethod
    def cast_to_object_list(cls, list_vacancies: list) -> list:
        """Метод преобразование набора данных в список объектов"""
        result = []
        try:
            if not isinstance(list_vacancies, list):
                raise TypeError(f"Передаваемый аргумент должно быть списком вакансий а не {type(list_vacancies)}")
            elif len(list_vacancies) == 0:
                raise ValueError("Передаваемый список пуст")
            else:
                for vacancy in list_vacancies:
                    result.append(Vacancy(vacancy["name"], vacancy["url"], vacancy["description"], vacancy["salary"]))
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        return result


if __name__ == "__main__":
    # v = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100")
    # c = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100")
    # print(v == c)
    # print(v._Vacancy__salary)
    # print(v.get_job_properties)
    # print(v)
    # print(repr(v))

    d = [
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
            "salary": {"from": 300000, "to": None, "currency": "RUB"},
            "url": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
        {
            "id": "128762270",
            "name": "Python разработчик (Middle+/Senior)",
            "salary": None,
            "url": "https://hh.ru/vacancy/128762270",
            "description": "Опыт коммерческой разработки",
        },
    ]
