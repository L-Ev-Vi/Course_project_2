import re
from string import ascii_letters
from typing import Any

from src.currency_exchange import CurrencyExchange


class Vacancy:
    """Класс для работы с вакансиями"""

    __S_RUS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    __S_RUS_UPPER = __S_RUS.upper()

    __slots__ = ("__name", "__link", "__salary", "__description")

    def __init__(self, name: str, link: str, description: str, salary: Any = None) -> None:
        """Конструктор объекта класса"""
        self.__validation_data(name)
        self.__name = name
        self.__validation_data(link)
        self.__link = link
        self.__salary = self.__validation_salary(salary)
        self.__validation_data(description)
        self.__description = description

    @classmethod
    def __validation_data(cls, value: Any) -> str:
        """Метод валидации данных, которыми инициализируются атрибут объекта-класса."""
        if type(value) is not str:
            raise TypeError(f"Значение {value} должно иметь тип 'str', а не {type(value)}")
        return value

    @classmethod
    def __validation_salary(cls, salary: str) -> Any:
        """Метод валидации данных, которыми инициализируются атрибут 'salary'."""
        pattern1 = re.compile(r"^\d+\s\-\s\d+$")
        pattern2 = re.compile(r"^\d+\-\d+$")
        pattern3 = re.compile(r"^\d+$")
        currencies = [" RUB", " USD", " EUR"]
        x = True
        salary_now = salary
        while x:
            try:
                if salary_now is None or salary_now == "":
                    salary_now = "Зарплата не указана"
                elif type(salary_now) is not str:
                    raise TypeError(f"Значение {salary_now} должно иметь тип 'str', а не {type(salary_now)}")
                elif pattern1.fullmatch(salary_now) or pattern2.fullmatch(salary_now):
                    currency = input(
                        "Выберите номер валюты, в которой будет производиться расчёт заработной платы:\n"
                        "1 - RUB\n"
                        "2 - USD\n"
                        "3 - EUR\n"
                        "->"
                    )
                    if currency not in ["1", "2", "3"] or currency == "":
                        salary_now = salary_now + " RUB"
                    else:
                        salary_now = salary_now + currencies[int(currency) - 1]
                elif pattern3.fullmatch(salary_now):
                    currency = input(
                        "Введите номер валюты, в которой будет производиться расчёт заработной платы:\n"
                        "1 - RUB\n"
                        "2 - USD\n"
                        "3 - EUR\n"
                        "->"
                    )
                    if currency not in ["1", "2", "3"] or currency == "":
                        salary_now = salary_now + " RUB"
                    else:
                        salary_now = salary_now + currencies[int(currency) - 1]
                else:
                    raise TypeError(
                        "Не корректно указана заработная плата, значение 'salary' должно быть целым числом, \n"
                        "или диапазоном чисел c разделителем '-', 'пример: 1000 или 1000-2000'"
                    )
            except TypeError as e:
                print(e)
                salary_now = input("Укажите значение заработной платы или оставьте атрибута пустым\n" "->")
                x = True
            else:
                x = False
        return salary_now

    def __get_minimum_wage(self) -> int:
        """Методы сравнения вакансий между собой по зарплате"""
        letters = ascii_letters + self.__S_RUS + self.__S_RUS_UPPER
        if self.__salary == "Зарплата не указана":
            salary = 0
        elif self.__salary.count("-") > 0:
            salary = self.__salary.strip(letters)
            salary = salary.replace(" ", "")
            salary = min(map(int, salary.split("-")))
        else:
            salary = int(self.__salary.strip(letters))
        if self.__salary.split(" ")[1] != "RUB":
            currency = CurrencyExchange(self.__salary.split(" ")[1])
            salary = currency.get_currency_exchange(salary)
        return salary

    def __lt__(self, other: object) -> bool:
        """Метод для операции сравнения «меньше»"""
        if not isinstance(other, Vacancy):
            raise TypeError("Переданный объект не является объектом класса 'Vacancy'")
        letters = ascii_letters + self.__S_RUS + self.__S_RUS_UPPER
        if other.__salary == "Зарплата не указана":
            salary = 0
        elif other.__salary.count("-") > 1:
            salary = other.__salary.strip(letters)
            salary = salary.replace(" ", "")
            salary = min(map(int, salary.split("-")))
        else:
            salary = int(other.__salary.strip(letters))
        if other.__salary.split(" ")[1] != "RUB":
            currency = CurrencyExchange(other.__salary.split(" ")[1])
            salary = currency.get_currency_exchange(salary)
        return self.__get_minimum_wage() < salary

    def __le__(self, other: object) -> bool:
        """Метод для операции сравнения «меньше или равно»"""
        if not isinstance(other, Vacancy):
            raise TypeError("Переданный объект не является объектом класса 'Vacancy'")
        letters = ascii_letters + self.__S_RUS + self.__S_RUS_UPPER
        if other.__salary == "Зарплата не указана":
            salary = 0
        elif other.__salary.count("-") > 1:
            salary = other.__salary.strip(letters)
            salary = salary.replace(" ", "")
            salary = min(map(int, salary.split("-")))
        else:
            salary = int(other.__salary.strip(letters))
        if other.__salary.split(" ")[1] != "RUB":
            currency = CurrencyExchange(other.__salary.split(" ")[1])
            salary = currency.get_currency_exchange(salary)
        return self.__get_minimum_wage() == salary

    def __gt__(self, other: object) -> bool:
        """Метод для операции сравнения «больше»"""
        if not isinstance(other, Vacancy):
            raise TypeError("Переданный объект не является объектом класса 'Vacancy'")
        letters = ascii_letters + self.__S_RUS + self.__S_RUS_UPPER
        if other.__salary == "Зарплата не указана":
            salary = 0
        elif other.__salary.count("-") > 1:
            salary = other.__salary.strip(letters)
            salary = salary.replace(" ", "")
            salary = min(map(int, salary.split("-")))
        else:
            salary = int(other.__salary.strip(letters))
        if other.__salary.split(" ")[1] != "RUB":
            currency = CurrencyExchange(other.__salary.split(" ")[1])
            salary = currency.get_currency_exchange(salary)
        return self.__get_minimum_wage() > salary


if __name__ == "__main__":
    v = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "10-2000")
    print(v._Vacancy__salary)
    c = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", 10)
    print(c._Vacancy__salary)

    # print(v <= c)
