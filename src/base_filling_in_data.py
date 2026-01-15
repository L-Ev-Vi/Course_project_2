from abc import ABC, abstractmethod


class FillingInData(ABC):
    """Абстрактный класс для заполнения данных"""

    @abstractmethod
    def filling_in_data(self) -> list:
        """Абстрактный метод для заполнения параметров"""

    @abstractmethod
    def getting_data(self) -> list:
        """Абстрактный метод для получения параметров"""
