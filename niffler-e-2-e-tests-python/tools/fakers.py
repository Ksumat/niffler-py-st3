import datetime
from random import choice
from decimal import Decimal
from faker import Faker


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker, который будет использоваться для генерации данных.
        """
        self.faker = faker

    def user_name(self) -> str:
        """
        Генерирует случайное имя.
        :return: Случайное имя.
        """
        return self.faker.user_name()

    def password(self) -> str:
        """
        Генерирует случайный пароль.
        :return: Случайный пароль.
        """
        return self.faker.password()

    def word(self):
        """
        Генерирует случайное слово.
        :return: Случайное слово
        """
        return self.faker.word()

    def text(self) -> str:
        """
        Генерирует случайный текст.
        :return: Случайный текст.
        """
        return self.faker.city()

    def integer(self, start: int = 1, end: int = 100) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.
        :param start: Начало диапазона (включительно).
        :param end: Конец диапазона (включительно).
        :return: Случайное целое число.
        """
        return self.faker.random_int(start, end)

    def sentence(self, nb_words: int = 6) -> str:
        """Генерирует случайное предложение (без точки в конце)."""
        return self.faker.sentence(nb_words=nb_words).rstrip(".")

    def float_amount(self, min_value: float = 1.0, max_value: float = 10000.0, decimals: int = 2) -> str:
        """
        Генерирует случайную денежную сумму как строку с фиксированным числом знаков после запятой.
        :return: Строка вида "123.45"
        """
        value = self.faker.pydecimal(
            left_digits=len(str(int(max_value))) + 1,
            right_digits=decimals,
            min_value=Decimal(str(min_value)),
            max_value=Decimal(str(max_value)),
            positive=True
        )
        return f"{value:.{decimals}f}"

    def currency(self, choices: list[str] = None) -> str:
        """Возвращает случайную валюту из заданного списка."""
        choices = choices or ["KZT", "RUB", "EUR", "USD"]
        return choice(choices)

    def past_datetime(self, days: int = 1) -> str:
        """
        Генерирует дату и время в прошлом (относительно now).
        :param days: Сколько дней назад (может быть float: 0.5 → 12 часов назад)
        :return: ISO-строка вида "2025-06-14T10:30:45.123456"
        """
        delta = datetime.timedelta(days=days)
        past = datetime.datetime.now() - delta
        return past.isoformat()


fake = Fake(faker=Faker())