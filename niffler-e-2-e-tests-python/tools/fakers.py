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


fake = Fake(faker=Faker())