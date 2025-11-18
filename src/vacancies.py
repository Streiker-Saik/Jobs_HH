from typing import Any, Dict, List, Optional, Union

from src.validates import Valid, ValidVacancy


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
        validate: Optional[Valid] = None,
    ) -> None:
        """Инициализация класса Vacancy"""
        if validate is None:
            validate = ValidVacancy()
        validate_data = validate.validate_vacancy_to_dict(name, url, salary_from, salary_to)
        self.name = validate_data["name"]
        self.url = validate_data["url"]
        self.salary_from = validate_data["salary_from"]
        self.salary_to = validate_data["salary_to"]
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

    def __le__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнения "меньше или равно"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() <= other.salary_average()

    def __gt__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнения "больше"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() > other.salary_average()

    def __ge__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнения "больше или равно"
        :param other: класс для сравнения
        :return: True или False
        """
        other.__valid_other(other)
        return self.salary_average() >= other.salary_average()

    def to_dict(self) -> Dict[str, Any]:
        """
        Метод перевода экземпляра класса в словарь
        :return: Словарь вакансии. Формат:
            {"name": ..., "url": ..., "salary_from": ..., "salary_to": ..., "experience": ...}
        """
        return {
            "name": self.name,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "experience": self.experience,
        }

    def salary_average(self) -> Union[int, float]:
        """Метод расчета средней зарплаты"""
        # Есть от и до, то берем среднее
        if self.salary_to and self.salary_from:
            return (self.salary_to + self.salary_from) / 2
        # Если есть только до
        elif self.salary_to:
            return self.salary_to
        # Если есть только от
        elif self.salary_from:
            return self.salary_from
        else:
            return 0

    @classmethod
    def created_vacancy(cls, vacancy_data: Dict[Any, Any]) -> "Vacancy":
        """
        Классовый метод создание экземпляра класса из словаря
        :param vacancy_data: Словарь с параметрами вакансии
            Ожидаемые ключи: name, url, salary: from, to, experience: name
        :return: Экземпляр класса Vacancy
        """
        name = vacancy_data.get("name", "")
        url = vacancy_data.get("alternate_url", "")

        salary_info = vacancy_data.get("salary", {})
        if salary_info is not None and salary_info.get("currency") == "RUR":
            salary_from = salary_info.get("from", 0)
            salary_to = salary_info.get("to", 0)
        else:
            salary_from = None
            salary_to = None
        experience_info = vacancy_data.get("experience", {})
        if experience_info is not None:
            experience_name = experience_info.get("name", "")
        else:
            experience_name = ""

        return cls(name=name, url=url, salary_from=salary_from, salary_to=salary_to, experience=experience_name)

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
