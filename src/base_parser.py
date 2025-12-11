from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    """Абстрактный класс для работы с API сервисами"""

    @callable
    @abstractmethod
    def __connecting_to_api(self) -> Any:
        """Метод подключения к API в абстрактном классе"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> Any:
        """Метод получения данных в абстрактном классе"""
        pass
