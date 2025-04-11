from typing import Any, Dict, List, Union, Optional
import re


class Vacancy:
    """
    Класс представление вакансии

    Атрибуты:
        name(str): Наименование вакансии
        url(str): Ссылка на вакансию
        salary_from(int): Зарплата "от" (по умолчанию None)
        salary_to(int): Зарплата "до" (по умолчанию None)
        experience(str): Требуемый опыт (по умолчанию "")

    Методы:
        __init__(self, name: str, url: str, salary_from: Optional[int] = None, salary_to: Optional[int] = None,
        experience: str = "") -> None:
            Инициализация класса Vacancy
        __str__(self) -> str:
            Магический метод, строковое отображение класса. Формат:
            "name (url). Зарплата: salary_range. Требуемый опыт: {experience_str}"
        __lt__(self, other) -> bool:
            Магический метод, сравнения "меньше" средней зарплаты
            :raise TypeError: Не является классом Vacancy
        __le__(self, other) -> bool:
            Магический метод, сравнения "меньше или равно" средней зарплаты
            :raise TypeError: Не является классом Vacancy
        __gt__(self, other) -> bool:
            Магический метод сравнения "больше" средней зарплаты
            :raise TypeError: Не является классом Vacancy
        __ge__(self, other) -> bool:
            Магический метод сравнения "больше или равно" средней зарплаты
            :raise TypeError: Не является классом Vacancy
        salary_average(self) -> Union[int, float]:
            Метод расчета средней зарплаты
        created_vacancy(cls, vacancy_data: Dict[Any, Any]) -> "Vacancy":
            Классовый метод создание экземпляра класса из словаря.
        cast_to_object_list(cls, vacancy_data: List[Dict[Any, Any]]) -> List["Vacancy"]:
            Классовый метод создание списка экземпляров класса из списка словарей
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
        __valid_class(other: "Vacancy") -> "Vacancy":
            Статический метод, проверка корректности экземпляра класса
            :raise TypeError: Не является классом Vacancy
    """
    name: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    experience: str
    __slots__ = ("name", "url", "salary_from", "salary_to", "experience")

    def __init__(
        self,
        name: str,
        url: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        experience: str = "",
    ) -> None:
        """Инициализация класса Vacancy"""

        self.name = self.__valid_name(name)
        self.url = self.__valid_url(url)
        self.salary_from = self.__valid_salary_from(salary_from)
        self.salary_to = self.__valid_salary_to(salary_to, self.salary_from)
        self.experience = experience

    def __str__(self) -> str:
        """Строковое отображение класса"""
        if self.salary_to == 0 and self.salary_from == 0:
            salary_range = "не указана"
        elif self.salary_from == 0:
            salary_range = f"до {self.salary_to}"
        elif self.salary_to == 0:
            salary_range = f"от {self.salary_from}"
        else:
            salary_range = f"от {self.salary_from} до {self.salary_to}"
        if self.experience is None:
            experience_str = "не указан"
        else:
            experience_str = self.experience
        result = f"{self.name} ({self.url}). Зарплата: {salary_range}. Требуемый опыт: {experience_str}"
        return result

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнения "меньше"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() < other.salary_average()


    def __le__(self, other) -> bool:
        """
        Магический метод сравнения "меньше или равно"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() <= other.salary_average()

    def __gt__(self, other) -> bool:
        """
        Магический метод сравнения "больше"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() > other.salary_average()

    def __ge__(self, other) -> bool:
        """
        Магический метод сравнения "больше или равно"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() >= other.salary_average()

    def salary_average(self) -> Union[int, float]:
        """Метод расчета средней зарплаты"""
        if self.salary_to == 0 and self.salary_from == 0:
            return 0
        elif self.salary_to == 0:
            return self.salary_from
        elif self.salary_from == 0:
            return self.salary_to
        return (self.salary_to + self.salary_from) / 2

    @classmethod
    def created_vacancy(cls, vacancy_data: Dict[Any, Any]) -> "Vacancy":
        """
        Классовый метод создание экземпляра класса из словаря
        :param vacancy_data: Словарь с параметрами вакансии
            Ожидаемые ключи: name, url, salary: from, to, experience: name
        :return: Экземпляр класса Vacancy
        """
        name = vacancy_data.get("name", "")
        url = vacancy_data.get("url", "")

        salary_info = vacancy_data.get("salary", {})
        salary_from = salary_info.get("from", 0)
        salary_to = salary_info.get("to", 0)

        experience_info = vacancy_data.get("experience", {})
        experience_name = experience_info.get("name", "")

        return cls(
            name=name,
            url=url,
            salary_from=salary_from,
            salary_to=salary_to,
            experience=experience_name
        )

    @classmethod
    def cast_to_object_list(cls, vacancy_data: List[Dict[Any, Any]]) -> List["Vacancy"]:
        """
        Классовый метод создание списка экземпляров класса из списка словарей
        :param vacancy_data: Список словарей с параметрами вакансии
        :return: Список экземпляров класса Vacancy
        """
        result = []
        for vacancy in vacancy_data:
            result.append(cls.created_vacancy(vacancy))
        return result

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

    @staticmethod
    def __valid_other(class_date: "Vacancy") -> "Vacancy":
        """
        Проверка корректности другого класса
        :param class_date: экземпляр класса
        :return: экземпляр класса
        :raise TypeError: Не является классом Vacancy
        """
        if not isinstance(class_date, Vacancy):
            raise TypeError("Не является классом Vacancy")
        return class_date
