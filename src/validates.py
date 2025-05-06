import re
from typing import Any, Dict, Optional

from src.interfaces import Valid


class ValidVacancy(Valid):
    """
    Класс валидации аргументов вакансии

    Методы:
        validate_vacancy_to_dict(
        self, name: str, url: str, salary_from: Optional[int], salary_to: Optional[int]
        ) -> Dict[str, Any]:
            Метод получения валидные данных вакансии выводит в виде словаря
        valid_name(self, name: str) -> str:
            Getter получения валидного наименования вакансии
        valid_url(self, url: str) -> str:
            Getter получения валидной ссылки
        valid_salary_from(self, salary_from: Optional[int] = None) -> int:
            Getter получения валидной зарплаты 'от'
        valid_salary_to(self, salary_to: Optional[int], salary_from: int) -> int:
            Getter получения валидной зарплаты 'до'
        __valid_name(name: str) -> str:
            Статический метод, проверка корректности наименования вакансии
            :raise TypeError: Название не является строкой
            :raise ValueError: Название вакансии не бывает с 1 символом
        __valid_url(url: str) -> str:
            Статический метод, проверка корректности ссылки
            :raise TypeError: Ссылка не является строкой
            :raise ValueError: Ссылка не подходит под формат
        __valid_salary_from(salary_from: Optional[int] = None) -> int:
            Проверка корректности зарплаты 'от'
            :raise TypeError: Зарплата 'от' не является числом
            :raise ValueError: Зарплата 'от' не может быть отрицательным числом
        __valid_salary_to(salary_to: Optional[int], salary_from: int) -> int:
            Проверка корректности зарплаты 'до'
            :raise TypeError: Зарплата 'до' не является числом
            :raise ValueError: Зарплата 'до' не может быть отрицательным числом или меньше зарплаты 'от'
    """

    def validate_vacancy_to_dict(self, name: str, url: str, salary_from: Optional[int], salary_to: Optional[int]) -> Dict[str, Any]:
        """
        Метод получения валидные данных вакансии выводит в виде словаря
        :param name: Название вакансии
        :param url: Ссылка на вакансию
        :param salary_from: Зарплата "от" (по умолчанию None)
        :param salary_to: Зарплата "до" (по умолчанию None)
        :return: Словарь валидных данных. Формат:
            {"name": ..., "url": ..., "salary_from": ..., "salary_to": ...}
        """
        name = self.valid_name(name)
        url = self.valid_url(url)
        salary_from = self.valid_salary_from(salary_from)
        salary_to = self.valid_salary_to(salary_to, salary_from)
        return {
            "name": name,
            "url": url,
            "salary_from": salary_from,
            "salary_to": salary_to,
        }

    def valid_name(self, name: str) -> str:
        """Метод получения валидного наименования вакансии"""
        return self.__valid_name(name)

    def valid_url(self, url: str) -> str:
        """Метод получения валидной ссылки"""
        return self.__valid_url(url)

    def valid_salary_from(self, salary_from: Optional[int] = None) -> int:
        """Метод получения валидной зарплаты 'от'"""
        return self.__valid_salary_from(salary_from)

    def valid_salary_to(self, salary_to: Optional[int], salary_from: int) -> int:
        """Метод получения валидной зарплаты 'до'"""
        return self.__valid_salary_to(salary_to, salary_from)

    @staticmethod
    def __valid_name(name: str) -> str:
        """
        Проверка корректности наименования вакансии
        :param name: Наименования вакансии
        :return: Наименования вакансии
        :raise TypeError: Название не является строкой
        :raise ValueError: Название вакансии не бывает с 1 символом
        """
        if not isinstance(name, str):
            raise TypeError("Название не является строкой")
        if len(name) <= 1:
            raise ValueError("Название вакансии не бывает с 1 символом")
        return name

    @staticmethod
    def __valid_url(url: str) -> str:
        """
        Проверка корректности ссылки
        :param url: Строка ссылки
        :return: Строка ссылки
        :raise TypeError: Ссылка не является строкой
        :raise ValueError: Ссылка не подходит под формат
        """
        if not isinstance(url, str):
            raise TypeError("Ссылка не является строкой")
        if not re.fullmatch(r"^(https?://)?hh\.ru/vacancy/\d+$", url):
            raise ValueError("Ссылка не подходит под формат")
        return url

    @staticmethod
    def __valid_salary_from(salary_from: Optional[int] = None) -> int:
        """
        Проверка корректности зарплаты 'от'
        :param salary_from: Зарплата 'от'
        :return: Зарплата 'от'
        :raise TypeError: Зарплата 'от' не является числом
        :raise ValueError: Зарплата 'от' не может быть отрицательным числом
        """
        if salary_from is None:
            return 0
        if not isinstance(salary_from, int):
            raise TypeError("Зарплата 'от' не является числом")
        if salary_from < 0:
            raise ValueError("Зарплата 'от' не может быть отрицательным числом")
        return salary_from

    @staticmethod
    def __valid_salary_to(salary_to: Optional[int], salary_from: int) -> int:
        """
        Проверка корректности зарплаты 'до'
        :param salary_to: Зарплата 'до'
        :param salary_from: Зарплата 'от'
        :return: Зарплата 'до'
        :raise TypeError: Зарплата 'до' не является числом
        :raise ValueError: Зарплата 'до' не может быть отрицательным числом или меньше зарплаты 'от'
        """
        if salary_to is None:
            return 0
        if not isinstance(salary_to, int):
            raise TypeError("Зарплата 'до' не является числом")
        if salary_to < 0 or salary_to < salary_from:
            raise ValueError("Зарплата 'до' не может быть отрицательным числом или меньше зарплаты 'от'")
        return salary_to

        # validate: Valid = ValidVacancy(),

    # validate_data = validate.validate(name, url, salary_from, salary_to)
    # self.name = validate_data["name"]
    # self.url = validate_data["url"]
    # self.salary_from = validate_data["salary_from"]
    # self.salary_to = validate_data["salary_to"]
