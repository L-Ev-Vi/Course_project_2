from typing import Any

from accessify import private

from src.base_filling_in_data import FillingInData


class FillingInJobInformation(FillingInData):
    """Класс для заполнения данных о вакансии"""

    def __init__(self) -> None:
        """Инициализация объекта класса"""

    @private
    def filling_in_data(self) -> list:
        """Метод для заполнения параметров"""
        name = input("Введите название вакансии\n" "->")
        while True:
            if name == "" or len(name) < 2:
                name = input("Введите корректное название вакансии\n" "->")
            else:
                break
        link = input("Укажите ссылку на вакансию\n" "->")
        while True:
            if link == "":
                link = input("Укажите корректную ссылку на вакансию\n" "->")
            else:
                break
        salary = input("Укажите заработную плату или диапазон заработной платы\n" "->")
        description = input("Введите описание вакансии\n" "->")
        while True:
            if description == "" or len(description) < 2:
                description = input("Введите корректное описание вакансии\n" "->")
            else:
                break
        return [name, link, description, salary]

    def getting_data(self) -> Any:
        """Метод для получения параметров"""
        return self.filling_in_data()
