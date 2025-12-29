import datetime


class GreetingTimeDay:
    """Класс для работы с приветствием относительно времени суток"""

    @classmethod
    def get_a_greeting(cls) -> str:
        """Метод возвращает приветствие относительно времени суток"""
        greeting = ""
        time_is_now = int(datetime.datetime.time(datetime.datetime.now()).strftime("%H"))
        if 6 < time_is_now <= 12:
            greeting = "Доброе утро"
        elif 12 < time_is_now < 18:
            greeting = "Добрый день"
        elif 18 <= time_is_now < 24:
            greeting = "Доброй вечер"
        elif 0 < time_is_now <= 6:
            greeting = "Доброй ночи"
        return greeting
