from typing import Any

import requests
from accessify import private

from src.api_request_error import ApiRequestError, ApiRequestError400, ApiRequestError500
from src.base_parser import Parser


class HH(Parser):
    """Класс для работы с API HeadHunter"""

    __vacancies: list
    __url: str
    __params: dict[str, Any]
    __headers: dict[str, str]

    def __init__(self) -> None:
        """Конструктор объекта класса"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"page": 0, "per_page": 0, "text": "", "area": 1, "period": 1, "search_field": "name"}
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__vacancies = []

    @private
    def connecting_to_api(self) -> list[Any]:
        """Метод подключения к API HH.ru для получать вакансии"""
        vacancies = []
        try:
            while True:
                response = requests.get(self.__url, params=self.__params)
                if response.status_code >= 500:
                    raise ApiRequestError500
                elif response.status_code >= 400:
                    raise ApiRequestError400
                elif response.status_code != 200:
                    raise ApiRequestError
                result = response.json()
                vacancies.extend(result["items"])
                if result["pages"] == self.__params["page"]:
                    break
                else:
                    self.__params["page"] += 1
        except ApiRequestError500 as e:
            print(e)
            return vacancies
        except ApiRequestError400 as e:
            print(e)
            return vacancies
        except ApiRequestError as e:
            print(e)
            return vacancies
        return vacancies

    def get_vacancies(self, keyword: str, per_page: int = 50) -> list:
        """Метод получения вакансии с сервиса HeadHunter.ru"""
        result = []
        try:
            if type(keyword) is not str:
                raise TypeError
            self.__params["text"] = keyword
            self.__params["per_page"] = per_page
            vacancies = self.connecting_to_api()
            for res in vacancies:
                if res["salary"]:
                    if res["salary"]["currency"] == "RUR":
                        res["salary"]["currency"] = "RUB"
                    result.append(
                        {
                            "id": res["id"],
                            "name": res["name"],
                            "salary": {
                                "from": res["salary"]["from"],
                                "to": res["salary"]["to"],
                                "currency": res["salary"]["currency"],
                            },
                            "url": res["alternate_url"],
                            "description": res["snippet"]["requirement"],
                        }
                    )
                else:
                    result.append(
                        {
                            "id": res["id"],
                            "name": res["name"],
                            "salary": None,
                            "url": res["alternate_url"],
                            "description": res["snippet"]["requirement"],
                        }
                    )
        except TypeError:
            print("Для поиска вакансий необходимо указать ключевое слово или фразу")
            return result
        return result


if __name__ == "__main__":
    a = HH()
    x = a.get_vacancies("python")
    print(*x, sep="\n")

# """
# {'id': '128762270', 'name': 'Python разработчик (Middle+/Senior)',
#  'salary': {'from': None, 'to': 410000, 'currency': 'RUB'},
#  'alternate_url': 'https://hh.ru/vacancy/128762270', 'relations': [],
#  'snippet': {
#     'requirement': 'Опыт коммерческой разработки'}
#  """

# """
# {'id': '128762270',
#  'name': 'Python разработчик (Middle+/Senior)',
#  'salary': {'from': None, 'to': 410000, 'currency': 'RUB'},
#  'url': 'https://hh.ru/vacancy/128762270',
#  'description': 'Опыт коммерческой разработки'}
#  """
