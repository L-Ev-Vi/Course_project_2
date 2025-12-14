from typing import Any


class ApiRequestError(Exception):
    """Класс исключения, который отвечает за обработку событий,
    когда статус-кода не равен 200"""

    def __init__(self, *args: Any) -> None:
        """Метод для инициализации текста исключения."""
        self.message = args[0] if args else "Ошибка при выполнении запроса на базовый URL."

    def __str__(self) -> str:
        """Метод выводит сообщение об ошибке."""
        return self.message


class ApiRequestError400(ApiRequestError):
    """Класс исключения, который отвечает за обработку событий,
    когда статус-кода от 400 да 500"""

    def __init__(self, *args: Any) -> None:
        """Метод для инициализации текста исключения."""
        self.message = args[0] if args else "Ошибка со стороны пользователя при выполнении запроса."


class ApiRequestError500(ApiRequestError):
    """Класс исключения, который отвечает за обработку событий,
    когда статус-кода от 500 и выше"""

    def __init__(self, *args: Any) -> None:
        """Метод для инициализации текста исключения."""
        self.message = args[0] if args else "Ошибка на стороне сервера при выполнении запроса."
