import os
from typing import Any

import numpy as np
import pandas as pd

from src.base_file_saver import FileSaver
from src.currency_exchange import CurrencyExchange
from src.vacancy import Vacancy


class XLSXSaver(FileSaver):
    """Класс для работы с json-файлом"""

    __BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, name_file: str = "job_information") -> None:
        """Конструктор объекта класса"""
        path = os.path.join(self.__BASE_DIR, "data", f"{name_file}.xlsx")
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
            data = vacancy.get_job_properties
            if isinstance(data["salary"], str):
                data_vacancy = {
                    "id": [data["id"]],
                    "name": [data["name"]],
                    "from": [None],
                    "to": [None],
                    "currency": [None],
                    "url": [data["url"]],
                    "description": [data["description"]],
                }
            else:
                data_vacancy = {
                    "id": [data["id"]],
                    "name": [data["name"]],
                    "from": [data["salary"]["from"]],
                    "to": [data["salary"]["to"]],
                    "currency": [data["salary"]["currency"]],
                    "url": [data["url"]],
                    "description": [data["description"]],
                }
            if not os.path.getsize(self.__path_file):
                df = pd.DataFrame(data_vacancy)
                df.set_index("id", inplace=True)
                df.to_excel(self.__path_file)
            else:
                df = pd.read_excel(self.__path_file)
                vacancies = df.to_dict(orient="records")
                data_file = []
                for vac in vacancies:
                    data_file.append((vac["name"], vac["description"]))
                if (data["name"], data["description"]) in data_file:
                    raise OverflowError(
                        f"В файл не сохраняются дубликаты вакансий, {str(vacancy)} уже содержится в файле."
                    )
                else:
                    columns = pd.read_excel(self.__path_file).to_dict("list")
                    for column, value in zip(columns, data_vacancy):
                        columns[str(column)].append(data_vacancy[str(value)][0])
                    df = pd.DataFrame(columns)
                    df.set_index("id", inplace=True)
                    df.to_excel(self.__path_file)
        except TypeError as e:
            print(e)
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
            data = pd.read_excel(self.__path_file).to_dict(orient="records")
            if keyword is None:
                if salary_range_min is None:
                    if salary_range_max is None:
                        result = data
                    else:
                        for vacancy in data:
                            if vacancy["currency"]:
                                if np.isnan(vacancy["to"]):
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if currency.get_currency_exchange(vacancy["from"]) <= salary_range_max:
                                            result.append(vacancy)
                                    else:
                                        if vacancy["from"] <= salary_range_max:
                                            result.append(vacancy)
                                else:
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if currency.get_currency_exchange(vacancy["to"]) <= salary_range_max:
                                            result.append(vacancy)
                                    else:
                                        if vacancy["to"] <= salary_range_max:
                                            result.append(vacancy)
                else:
                    for vacancy in data:
                        if vacancy["currency"]:
                            if salary_range_max is None:
                                if np.isnan(vacancy["from"]):
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if currency.get_currency_exchange(vacancy["to"]) >= salary_range_min:
                                            result.append(vacancy)
                                    else:
                                        if vacancy["to"] >= salary_range_min:
                                            result.append(vacancy)
                                else:
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if currency.get_currency_exchange(vacancy["from"]) >= salary_range_min:
                                            result.append(vacancy)
                                    else:
                                        if vacancy["from"] >= salary_range_min:
                                            result.append(vacancy)
                            else:
                                if np.isnan(vacancy["to"]):
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if (
                                            salary_range_max
                                            >= currency.get_currency_exchange(vacancy["from"])
                                            >= salary_range_min
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if salary_range_max >= vacancy["from"] >= salary_range_min:
                                            result.append(vacancy)
                                elif np.isnan(vacancy["from"]):
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if (
                                            salary_range_max
                                            >= currency.get_currency_exchange(vacancy["to"])
                                            >= salary_range_min
                                        ):
                                            result.append(vacancy)
                                    else:
                                        if salary_range_max >= vacancy["to"] >= salary_range_min:
                                            result.append(vacancy)
                                else:
                                    if vacancy["currency"] != "RUB":
                                        currency = CurrencyExchange(vacancy["currency"])
                                        if salary_range_max >= currency.get_currency_exchange(
                                            vacancy["to"]
                                        ) and salary_range_min <= currency.get_currency_exchange(vacancy["from"]):
                                            result.append(vacancy)
                                    else:
                                        if salary_range_max >= vacancy["to"] and salary_range_min <= vacancy["from"]:
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
                                        if vacancy["currency"]:
                                            if np.isnan(vacancy["to"]):
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["from"])
                                                        <= salary_range_max
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["from"] <= salary_range_max:
                                                        result.append(vacancy)
                                            else:
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["to"])
                                                        <= salary_range_max
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["to"] <= salary_range_max:
                                                        result.append(vacancy)
                                else:
                                    if vacancy["currency"]:
                                        if salary_range_max is None:
                                            if np.isnan(vacancy["from"]):
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["to"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["to"] >= salary_range_min:
                                                        result.append(vacancy)
                                            else:
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if (
                                                        currency.get_currency_exchange(vacancy["from"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if vacancy["from"] >= salary_range_min:
                                                        result.append(vacancy)
                                        else:
                                            if np.isnan(vacancy["from"]):
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if (
                                                        salary_range_max
                                                        >= currency.get_currency_exchange(vacancy["to"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if salary_range_max >= vacancy["to"] >= salary_range_min:
                                                        result.append(vacancy)
                                            elif np.isnan(vacancy["to"]):
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if (
                                                        salary_range_max
                                                        >= currency.get_currency_exchange(vacancy["from"])
                                                        >= salary_range_min
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if salary_range_max >= vacancy["from"] >= salary_range_min:
                                                        result.append(vacancy)
                                            else:
                                                if vacancy["currency"] != "RUB":
                                                    currency = CurrencyExchange(vacancy["currency"])
                                                    if salary_range_max >= currency.get_currency_exchange(
                                                        vacancy["to"]
                                                    ) and salary_range_min <= currency.get_currency_exchange(
                                                        vacancy["from"]
                                                    ):
                                                        result.append(vacancy)
                                                else:
                                                    if (
                                                        salary_range_max >= vacancy["to"]
                                                        and salary_range_min <= vacancy["from"]
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
            data = pd.read_excel(self.__path_file).to_dict(orient="records")
            if len(data) == 0:
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла")
            if not isinstance(vacancy, Vacancy):
                raise TypeError(
                    f"Не возможно выполнить удаление, "
                    f"объект реализован от {type(vacancy)}, а не от класса Vacancy(Вакансия)!"
                )
            else:
                vacancy_df = vacancy.get_job_properties
                if isinstance(vacancy_df["salary"], str):
                    data_vacancy = {
                        "id": vacancy_df["id"],
                        "name": vacancy_df["name"],
                        "from": None,
                        "to": None,
                        "currency": None,
                        "url": vacancy_df["url"],
                        "description": vacancy_df["description"],
                    }
                elif vacancy_df["salary"]["from"] is None:
                    data_vacancy = {
                        "id": vacancy_df["id"],
                        "name": vacancy_df["name"],
                        "from": None,
                        "to": vacancy_df["salary"]["to"],
                        "currency": vacancy_df["salary"]["currency"],
                        "url": vacancy_df["url"],
                        "description": vacancy_df["description"],
                    }
                elif vacancy_df["salary"]["to"] is None:
                    data_vacancy = {
                        "id": vacancy_df["id"],
                        "name": vacancy_df["name"],
                        "from": vacancy_df["salary"]["from"],
                        "to": None,
                        "currency": vacancy_df["salary"]["currency"],
                        "url": vacancy_df["url"],
                        "description": vacancy_df["description"],
                    }
                else:
                    data_vacancy = {
                        "id": vacancy_df["id"],
                        "name": vacancy_df["name"],
                        "from": vacancy_df["salary"]["from"],
                        "to": vacancy_df["salary"]["to"],
                        "currency": vacancy_df["salary"]["currency"],
                        "url": vacancy_df["url"],
                        "description": vacancy_df["description"],
                    }
                vacancies_df = []
                for vacancy_ in data:
                    if isinstance(vacancy_["currency"], float):
                        vacancy_["from"] = None
                        vacancy_["to"] = None
                        vacancy_["currency"] = None
                        vacancies_df.append(tuple(vacancy_.values()))
                    elif np.isnan(vacancy_["from"]):
                        vacancy_["from"] = None
                        vacancies_df.append(tuple(vacancy_.values()))
                    elif np.isnan(vacancy_["to"]):
                        vacancy_["to"] = None
                        vacancies_df.append(tuple(vacancy_.values()))
                    else:
                        vacancies_df.append(tuple(vacancy_.values()))
                if tuple(data_vacancy.values()) not in vacancies_df:
                    raise ValueError(f"Не возможно выполнить удаление, в файле отсутствует вакансия, {str(vacancy)}")
                else:
                    list_id = list()
                    list_name = list()
                    list_from = list()
                    list_to = list()
                    list_currency = list()
                    list_url = list()
                    list_description = list()
                    vacancies_df.pop(vacancies_df.index(tuple(data_vacancy.values())))
                    for vacancy_ty in vacancies_df:
                        list_id.append(vacancy_ty[0])
                        list_name.append(vacancy_ty[1])
                        list_from.append(vacancy_ty[2])
                        list_to.append(vacancy_ty[3])
                        list_currency.append(vacancy_ty[4])
                        list_url.append(vacancy_ty[5])
                        list_description.append(vacancy_ty[6])
                    df = pd.DataFrame(
                        {
                            "id": list_id,
                            "name": list_name,
                            "from": list_from,
                            "to": list_to,
                            "currency": list_currency,
                            "url": list_url,
                            "description": list_description,
                        }
                    )
                    df.set_index("id", inplace=True)
                    df.to_excel(self.__path_file)

        except TypeError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    def delete_content(self) -> None:
        """Метод удаления всех данных из файла. Метод удаляет все данные из файла оставляя пустой список."""
        try:
            if not os.path.getsize(self.__path_file):
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла!")
            data = pd.read_excel(self.__path_file).to_dict(orient="records")
            if len(data) == 0:
                raise FileNotFoundError("Не возможно выполнить удаление объекта из пустого файла!")
            else:
                df = pd.DataFrame(
                    {"id": [], "name": [], "from": [], "to": [], "currency": [], "url": [], "description": []}
                )
                df.set_index("id", inplace=True)
                df.to_excel(self.__path_file)
                print("Выполнена очистка файла!")
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
