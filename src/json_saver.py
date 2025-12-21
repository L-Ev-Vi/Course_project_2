import json
import os
from json import JSONDecodeError
from typing import Any

from src.base_file_saver import FileSaver
from src.vacancy import Vacancy


class JSONSaver(FileSaver):
    """Класс для работы с json-файлом"""

    def __init__(self, name_file: str = "job_information") -> None:
        """Конструктор объекта класса"""
        path = os.path.join(os.path.dirname(__file__)[:-3], "data", f"{name_file}.json")
        if not os.path.exists(path):
            file = os.open(path, os.O_CREAT)
            os.close(file)
        self.__name_file = name_file
        self.__path_file = path

    def add_vacancy(self, vacancy: object) -> None:
        """Метод добавления данных в файл"""
        try:
            if not isinstance(vacancy, Vacancy):
                raise TypeError(f"Добавляемый объект реализован от {vacancy}, а не от класса Vacancy(Вакансия)!")
            if not os.path.getsize(self.__path_file):
                data = [vacancy.get_job_properties]
                with open(self.__path_file, "a", encoding="utf=8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            else:
                with open(self.__path_file, "r", encoding="utf=8") as file:
                    data = json.load(file)
                value_ = [tuple(entity.values()) for entity in data]
                if tuple(vacancy.get_job_properties.values()) in value_:
                    raise OverflowError(
                        f"В файл не сохраняются дубликаты вакансий, " f"{str(vacancy)} уже содержится в файле."
                    )
                else:
                    data.append(vacancy.get_job_properties)
                    with open(self.__path_file, "w", encoding="utf=8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(e)
        except JSONDecodeError:
            print("Ошибка: не возможно декодировать JSON-данные")
        except OverflowError as e:
            print(e)

    def get_job_information(self, keyword: Any = None, minimum_wage: Any = None, maximum_salary: Any = None) -> list:
        """Метод получения данных из файла"""
        # keyword - ключевое слово для поиска в названии вакансий и в описании к ним, если не передавать ключевое слово
        # то по умолчанию будет выводиться весь список содержащийся в файле
        # minimum_wage - не обязательный параметр обозначающий минимальную заработную плату
        # maximum_salary - не обязательный параметр обозначающий максимальную заработную плату
        result = []
        try:
            if keyword is not None:
                if type(keyword) is not str:
                    raise TypeError(
                        "Ключевое слово для поиска должно иметь тип 'str'. \n"
                        "Если не указывать ключевое слово, \n"
                        "то по умолчанию результатом будет содержимое всего файла."
                    )
            if minimum_wage is not None:
                if type(minimum_wage) is not int:
                    raise TypeError(
                        "Не обязательный параметр обозначающий минимальную заработную плату, \n"
                        "должен быть целым числом и иметь тип 'int'."
                    )
                if minimum_wage < 0:
                    raise ValueError("Сумма заработной платы не может быть отрицательной.")
            if maximum_salary is not None:
                if type(maximum_salary) is not int:
                    raise TypeError(
                        "Не обязательный параметр обозначающий максимальную заработную плату, \n"
                        "должен быть целым числом и иметь тип 'int'."
                    )
                if maximum_salary < 0:
                    raise ValueError("Сумма заработной платы не может быть отрицательной.")
            with open(self.__path_file, "r", encoding="utf=8") as file:
                data = json.load(file)
            if keyword is None:
                if minimum_wage is None:
                    if maximum_salary is None:
                        result = data
                    else:
                        for vacancy in data:
                            if vacancy["salary"] != "Зарплата не указана":
                                if not vacancy["salary"]["to"]:
                                    if int(vacancy["salary"]["from"]) <= maximum_salary:
                                        result.append(vacancy)
                                else:
                                    if int(vacancy["salary"]["to"]) <= maximum_salary:
                                        result.append(vacancy)
                else:
                    for vacancy in data:
                        if vacancy["salary"] != "Зарплата не указана":
                            if maximum_salary is None:
                                if not vacancy["salary"]["from"]:
                                    if int(vacancy["salary"]["to"]) >= minimum_wage:
                                        result.append(vacancy)
                                else:
                                    if int(vacancy["salary"]["from"]) >= minimum_wage:
                                        result.append(vacancy)
                            else:
                                if minimum_wage > maximum_salary:
                                    raise ValueError(
                                        "Не корректно указанны суммы обозначающие границы оплаты труда, \n"
                                        "значение минимальной оплаты не может быть больше "
                                        "значения максимальной оплаты."
                                    )
                                if not vacancy["salary"]["from"]:
                                    if maximum_salary >= int(vacancy["salary"]["to"]) >= minimum_wage:
                                        result.append(vacancy)
                                elif not vacancy["salary"]["to"]:
                                    if maximum_salary >= int(vacancy["salary"]["from"]) >= minimum_wage:
                                        result.append(vacancy)
                                else:
                                    if maximum_salary >= int(vacancy["salary"]["to"]) and minimum_wage <= int(
                                        vacancy["salary"]["from"]
                                    ):
                                        result.append(vacancy)
            else:
                for vacancy in data:
                    if keyword.lower() in vacancy["name"].lower() or keyword.lower() in vacancy["description"].lower():
                        if minimum_wage is None:
                            if maximum_salary is None:
                                result.append(vacancy)
                            else:
                                if vacancy["salary"] != "Зарплата не указана":
                                    if not vacancy["salary"]["to"]:
                                        if int(vacancy["salary"]["from"]) <= maximum_salary:
                                            result.append(vacancy)
                                    else:
                                        if int(vacancy["salary"]["to"]) <= maximum_salary:
                                            result.append(vacancy)
                        else:
                            if vacancy["salary"] != "Зарплата не указана":
                                if maximum_salary is None:
                                    if not vacancy["salary"]["from"]:
                                        if int(vacancy["salary"]["to"]) >= minimum_wage:
                                            result.append(vacancy)
                                    else:
                                        if int(vacancy["salary"]["from"]) >= minimum_wage:
                                            result.append(vacancy)
                                else:
                                    if minimum_wage > maximum_salary:
                                        raise ValueError(
                                            "Не корректно указанны суммы обозначающие границы оплаты труда, \n"
                                            "значение минимальной оплаты не может быть больше "
                                            "значения максимальной оплаты."
                                        )
                                    if not vacancy["salary"]["from"]:
                                        if maximum_salary >= int(vacancy["salary"]["to"]) >= minimum_wage:
                                            result.append(vacancy)
                                    elif not vacancy["salary"]["to"]:
                                        if maximum_salary >= int(vacancy["salary"]["from"]) >= minimum_wage:
                                            result.append(vacancy)
                                    else:
                                        if maximum_salary >= int(vacancy["salary"]["to"]) and minimum_wage <= int(
                                            vacancy["salary"]["from"]
                                        ):
                                            result.append(vacancy)
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        return result

    def delete_vacancy(self, vacancy: object) -> None:
        """Метод удаления данных из файла"""
        try:
            if not isinstance(vacancy, Vacancy):
                raise TypeError(
                    f"Не возможно выполнить удаление, "
                    f"объект реализован от {vacancy}, а не от класса Vacancy(Вакансия)!"
                )
            elif not os.path.getsize(self.__path_file):
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла")
            else:
                with open(self.__path_file, "r", encoding="utf=8") as file:
                    data = json.load(file)
                value_ = [tuple(entity.values()) for entity in data]
                if tuple(vacancy.get_job_properties.values()) not in value_:
                    raise ValueError(f"Не возможно выполнить удаление, в файле отсутствует вакансия, {str(vacancy)}")
                else:
                    data.pop(value_.index(tuple(vacancy.get_job_properties.values())))
                    with open(self.__path_file, "w", encoding="utf=8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        except JSONDecodeError:
            print("Ошибка: не возможно декодировать JSON-данные")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    j = JSONSaver()
    v = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    # j.add_vacancy(v)
    v2 = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...")
    # j.add_vacancy(v2)

    j.delete_vacancy(v)

    # n = j.get_job_information(minimum_wage=160, maximum_salary=150)
    # print(n)
