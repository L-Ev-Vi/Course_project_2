import json
import os
from json import JSONDecodeError
from typing import Any

from src.base_file_saver import FileSaver
from src.currency_exchange import CurrencyExchange
from src.vacancy import Vacancy


class JSONSaver(FileSaver):
    """Класс для работы с json-файлом"""

    __BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, name_file: str = "job_information") -> None:
        """Конструктор объекта класса"""
        path = os.path.join(self.__BASE_DIR, "data", f"{name_file}.json")
        if not os.path.exists(path):
            file = os.open(path, os.O_CREAT)
            os.close(file)
        self.__name_file = name_file
        self.__path_file = path

    def add_vacancy(self, vacancy: object) -> None:
        """Метод добавления данных в файл. Метод принимает объект класса вакансия,
        и производит сохранение его данных в файл."""
        try:
            if not isinstance(vacancy, Vacancy):
                raise TypeError(f"Добавляемый объект реализован от {type(vacancy)}, а не от класса Vacancy(Вакансия)!")
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
                        f"В файл не сохраняются дубликаты вакансий, {str(vacancy)} уже содержится в файле."
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

    def get_job_information(
        self, keyword: Any = None, salary_range_min: Any = None, salary_range_max: Any = None
    ) -> list:
        """Метод получения данных из файла. Метод возвращает данные о вакансиях из файла по параметрам выборки,
        таким как ключевые слова, минимальная и максимальная заработная плата.
        Где:
        'keyword' - ключевое слово или несколько ключевых слов записанных через пробел,
        для поиска в названии вакансий и в описании к ним, если не передавать ключевое слово
        то по умолчанию будет выводиться весь список содержащийся в файле.
        'salary_range_min' - не обязательный параметр обозначающий минимальную заработную плату.
        'salary_range_max' - не обязательный параметр обозначающий максимальную заработную плату."""
        result = []
        try:
            if keyword is not None:
                if type(keyword) is not str:
                    raise TypeError(
                        "Ключевое слово для поиска должно иметь тип 'str'. \n"
                        "Если не указывать ключевое слово, \n"
                        "то по умолчанию результатом будет содержимое всего файла."
                    )
            if salary_range_min is not None:
                if not isinstance(salary_range_min, int):
                    raise TypeError(
                        "Не обязательный параметр обозначающий минимальную заработную плату, \n"
                        "должен быть целым числом и иметь тип 'int'."
                    )
                elif salary_range_min < 0:
                    raise ValueError("Сумма заработной платы не может быть отрицательной.")
            if salary_range_max is not None:
                if not isinstance(salary_range_max, int):
                    raise TypeError(
                        "Не обязательный параметр обозначающий максимальную заработную плату, \n"
                        "должен быть целым числом и иметь тип 'int'."
                    )
                elif salary_range_max < 0:
                    raise ValueError("Сумма заработной платы не может быть отрицательной.")
            if isinstance(salary_range_min, int) and isinstance(salary_range_max, int):
                if salary_range_min > salary_range_max:
                    raise ValueError(
                        "Не корректно указанны суммы обозначающие границы оплаты труда, \n"
                        "значение минимальной оплаты не может быть больше "
                        "значения максимальной оплаты."
                    )
            with open(self.__path_file, "r", encoding="utf=8") as file:
                data = json.load(file)
            if keyword is None:
                if salary_range_min is None:
                    if salary_range_max is None:
                        result = data
                    else:
                        for vacancy in data:
                            if vacancy["salary"] != "Зарплата не указана":
                                if not vacancy["salary"]["to"]:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if (
                                            currency.get_currency_exchange(vacancy["salary"]["from"])
                                            <= salary_range_max
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if vacancy["salary"]["from"] <= salary_range_max:
                                            result.append(vacancy)
                                else:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if currency.get_currency_exchange(vacancy["salary"]["to"]) <= salary_range_max:
                                            result.append(vacancy)
                                    else:
                                        if vacancy["salary"]["to"] <= salary_range_max:
                                            result.append(vacancy)
                else:
                    for vacancy in data:
                        if vacancy["salary"] != "Зарплата не указана":
                            if salary_range_max is None:
                                if not vacancy["salary"]["from"]:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if currency.get_currency_exchange(vacancy["salary"]["to"]) >= salary_range_min:
                                            result.append(vacancy)
                                    else:
                                        if vacancy["salary"]["to"] >= salary_range_min:
                                            result.append(vacancy)
                                else:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if (
                                            currency.get_currency_exchange(vacancy["salary"]["from"])
                                            >= salary_range_min
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if vacancy["salary"]["from"] >= salary_range_min:
                                            result.append(vacancy)
                            else:
                                if not vacancy["salary"]["from"]:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if (
                                            salary_range_max
                                            >= currency.get_currency_exchange(vacancy["salary"]["to"])
                                            >= salary_range_min
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if salary_range_max >= vacancy["salary"]["to"] >= salary_range_min:
                                            result.append(vacancy)
                                elif not vacancy["salary"]["to"]:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if (
                                            salary_range_max
                                            >= currency.get_currency_exchange(vacancy["salary"]["from"])
                                            >= salary_range_min
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if salary_range_max >= vacancy["salary"]["from"] >= salary_range_min:
                                            result.append(vacancy)
                                else:
                                    if vacancy["salary"]["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["salary"]["currency"])
                                        if salary_range_max >= currency.get_currency_exchange(
                                            vacancy["salary"]["to"]
                                        ) and salary_range_min <= currency.get_currency_exchange(
                                            vacancy["salary"]["from"]
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if (
                                            salary_range_max >= vacancy["salary"]["to"]
                                            and salary_range_min <= vacancy["salary"]["from"]
                                        ):
                                            result.append(vacancy)
            else:
                words = keyword.split()
                for vacancy in data:
                    counter = 0
                    for word in words:
                        if (
                            word.lower() in vacancy["name"].lower().split()
                            or word.lower() in vacancy["description"].lower().split()
                        ):
                            counter += 1
                            if counter == len(words):
                                if salary_range_min is None:
                                    if salary_range_max is None:
                                        result.append(vacancy)
                                    else:
                                        if vacancy["salary"] != "Зарплата не указана":
                                            if not vacancy["salary"]["to"]:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["salary"]["from"])
                                                        <= salary_range_max
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["salary"]["from"] <= salary_range_max:
                                                        result.append(vacancy)
                                            else:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["salary"]["to"])
                                                        <= salary_range_max
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["salary"]["to"] <= salary_range_max:
                                                        result.append(vacancy)
                                else:
                                    if vacancy["salary"] != "Зарплата не указана":
                                        if salary_range_max is None:
                                            if not vacancy["salary"]["from"]:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["salary"]["to"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["salary"]["to"] >= salary_range_min:
                                                        result.append(vacancy)
                                            else:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["salary"]["from"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["salary"]["from"] >= salary_range_min:
                                                        result.append(vacancy)
                                        else:
                                            if not vacancy["salary"]["from"]:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if (
                                                        salary_range_max
                                                        >= currency.get_currency_exchange(vacancy["salary"]["to"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if salary_range_max >= vacancy["salary"]["to"] >= salary_range_min:
                                                        result.append(vacancy)
                                            elif not vacancy["salary"]["to"]:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if (
                                                        salary_range_max
                                                        >= currency.get_currency_exchange(vacancy["salary"]["from"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if (
                                                        salary_range_max
                                                        >= vacancy["salary"]["from"]
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                            else:
                                                if vacancy["salary"]["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["salary"]["currency"])
                                                    if salary_range_max >= currency.get_currency_exchange(
                                                        vacancy["salary"]["to"]
                                                    ) and salary_range_min <= currency.get_currency_exchange(
                                                        vacancy["salary"]["from"]
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if (
                                                        salary_range_max >= vacancy["salary"]["to"]
                                                        and salary_range_min <= vacancy["salary"]["from"]
                                                    ):
                                                        result.append(vacancy)
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)
        return result

    def delete_vacancy(self, vacancy: object) -> None:
        """Метод удаления данных из файла. Метод принимает объекта класса вакансия,
        и производит удаление его данных их в файл, но только при условии,
        что данные этого объекта содержатся в файле"""
        try:
            if not os.path.getsize(self.__path_file):
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла")
            with open(self.__path_file, "r", encoding="utf=8") as file:
                data = json.load(file)
            if len(data) == 0:
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла")
            if not isinstance(vacancy, Vacancy):
                raise TypeError(
                    f"Не возможно выполнить удаление, "
                    f"объект реализован от {type(vacancy)}, а не от класса Vacancy(Вакансия)!"
                )
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

    def delete_content(self) -> None:
        """Метод удаления всех данных из файла. Метод удаляет все данные из файла оставляя пустой список."""
        try:
            if not os.path.getsize(self.__path_file):
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла!")
            with open(self.__path_file, "r", encoding="utf=8") as file:
                data = json.load(file)
            if len(data) == 0:
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла!")
            else:
                with open(self.__path_file, "w", encoding="utf=8") as file:
                    json.dump([], file, ensure_ascii=False, indent=4)
                print("Выполнена очистка файла!")
        except FileNotFoundError as e:
            print(e)
        except JSONDecodeError:
            print("Ошибка: не возможно декодировать JSON-данные")
        except Exception as e:
            print(e)
