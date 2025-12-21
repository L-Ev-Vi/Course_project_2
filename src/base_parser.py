from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    """Абстрактный класс для работы с API сервисами"""

    @classmethod
    @abstractmethod
    def __connecting_to_api(cls) -> list[Any]:
        """Метод подключения к API в абстрактном классе"""

    @abstractmethod
    def get_vacancies(self, keyword: str) -> Any:
        """Метод получения данных в абстрактном классе"""
