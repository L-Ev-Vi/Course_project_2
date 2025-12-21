from abc import ABC, abstractmethod


class FileSaver(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: object) -> None:
        """Абстрактный метод добавления данных в файл"""

    @abstractmethod
    def get_job_information(self, vacancy: object) -> list:
        """Абстрактный метод получения данных из файла"""

    @abstractmethod
    def delete_vacancy(self, vacancy: object) -> None:
        """Абстрактный метод удаления данных из файла"""
