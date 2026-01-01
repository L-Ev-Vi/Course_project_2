from unittest.mock import patch

from src.greeting_time_day import GreetingTimeDay


@patch("builtins.int")
def test_get_a_greeting_morning(int_mock):
    int_mock.return_value = 7
    assert GreetingTimeDay.get_a_greeting() == "Доброе утро"


@patch("builtins.int")
def test_get_a_greeting_day(int_mock):
    int_mock.return_value = 14
    assert GreetingTimeDay.get_a_greeting() == "Добрый день"


@patch("builtins.int")
def test_get_a_greeting_evening(int_mock):
    int_mock.return_value = 19
    assert GreetingTimeDay.get_a_greeting() == "Доброй вечер"


@patch("builtins.int")
def test_get_a_greeting_night(int_mock):
    int_mock.return_value = 2
    assert GreetingTimeDay.get_a_greeting() == "Доброй ночи"
