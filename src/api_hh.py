import requests

from src.api_request_error import ApiRequestError, ApiRequestError400, ApiRequestError500
from src.base_parser import Parser


class HH(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        """Конструктор объекта класса"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"page": 0, "per_page": 0, "text": "", "area": 1, "period": 1, "search_field": "name"}
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__vacancies = []

    def __connecting_to_api(self) -> list:
        """Метод подключения к API HH.ru для получать вакансии"""
        try:
            while True:
                response = requests.get(url=self.__url, params=self.__params)
                if response.status_code >= 500:
                    raise ApiRequestError500
                if response.status_code >= 400:
                    raise ApiRequestError400
                if response.status_code != 200:
                    raise ApiRequestError
                result = response.json()
                self.__vacancies.extend(result['items'])
                if result["pages"] == self.__params["page"]:
                    break
                else:
                    self.__params["page"] += 1
        except ApiRequestError500 as e:
            print(e)
            return []
        except ApiRequestError400 as e:
            print(e)
            return []
        except ApiRequestError as e:
            print(e)
            return []
        return self.__vacancies

    def get_vacancies(self, keyword: str, per_page: int = 50) -> list:
        """Метод получения вакансии с сервиса HeadHunter.ru"""
        try:
            if type(keyword) != str:
                raise TypeError
            self.__params["text"] = keyword
            self.__params["per_page"] = per_page
            result = self.__connecting_to_api()
        except TypeError:
            print("Для поиска вакансий необходимо указать ключевое слово или фразу")
            return []
        return result


if __name__ == '__main__':
    r = HH()
    x = r.get_vacancies("python")
    print(x)
