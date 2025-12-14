import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.api_request_error import ApiRequestError, ApiRequestError400, ApiRequestError500


class CurrencyExchange:
    """Класс для перевода иностранной волюты в 'RUB'"""

    def __init__(self, currency: str) -> None:
        """Конструктор объекта класса"""
        self.currency = currency

    def get_currency_exchange(self, amount_currency: int, base_currency: str = "RUB") -> Any:
        """Функция выполняет API запрос на внешний сервис для получения актуального курса валют, и возвращает сумму
        переданной валюты относительно 'RUB'."""
        try:
            load_dotenv("../.env")
            aip_key = os.getenv("EXC_AIP_KEY")
            url = (
                f"https://api.apilayer.com/exchangerates_data/convert?to={base_currency}&from={self.currency}"
                f"&amount={amount_currency}"
            )
            payload: dict = {}
            headers = {"apikey": f"{aip_key}"}
            response = requests.get(url, headers=headers, data=payload)
            if response.status_code >= 500:
                raise ApiRequestError500
            if response.status_code >= 400:
                raise ApiRequestError400
            if response.status_code != 200:
                raise ApiRequestError
            else:
                answer = response.json()
                result = round(answer["result"])
        except ApiRequestError500 as e:
            print(e)
            return 0
        except ApiRequestError400 as e:
            print(e)
            return 0
        except ApiRequestError as e:
            print(e)
            return 0
        else:
            return result


if __name__ == "__main__":
    a = CurrencyExchange("USD")
    print(a.get_currency_exchange(10))
