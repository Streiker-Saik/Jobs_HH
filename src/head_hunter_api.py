from typing import Any, Dict, List

import requests

from src.exceptions import APIError
from src.interfaces import AbstractApi


class HeadHunterAPI(AbstractApi):
    """
    Класс работы с HeadHunter
    Атрибуты:
        __url(str): Базовый url (private);
        __headers(dict): Заголовки запроса (private);
        __params(dict): Параметры запроса (private);
        __vacancies(list): Список вакансий (private);
        per_page(int): Количество элементов со станицы(по умолчанию и максимум 100)
    Методы:
        __init__(self, per_page: int = 100) -> None:
            Инициализатор экземпляра класса HeadHunterAPI.
        connect(self) -> Dict[Any, Any]:
            Метод подключения к API
        __connect(self) -> Dict[Any, Any]:
            Приватный метод подключения к Head_Hunter_API
            :raise APIError: Ошибка запроса API
            :raise ValueError: Если API выдает не словарь
        get_vacancies(self, keyword: str) -> List[Dict[Any, Any]]:
            Метод получения вакансий
        __valid_per_page(per_page: int) -> int:
            Статический метод проверки корректности аргумента
            TypeError: Если аргумент не является целым числом
            ValueError: Если аргумент равен 0 или отрицательный
    """

    per_page: int

    def __init__(self, per_page: int = 100) -> None:
        """
        Инициализация класса HeadHunterAPI
        :param per_page: Количество страниц вакансий (по умолчанию 100)
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.per_page = self.__valid_per_page(per_page)
        self.__params: Dict[str, Any] = {"text": "", "page": 0, "per_page": self.per_page}
        self.__vacancies: List[Dict[str, Any]] = []

    def connect(self) -> Dict[Any, Any]:
        """Метод подключения к API"""
        return self.__connect()

    def __connect(self) -> Dict[str, Any]:
        """
        Приватный метод подключения к Head_Hunter_API
        :return: Словарь ответа от API
        :raise APIError: Ошибка запроса API
        :raise ValueError: Если API выдает не словарь
        """
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code != 200:
            error_message = f"Ошибка API: {response.status_code} - {response.text}"
            raise APIError(error_message)
        else:
            result = response.json()
            if not isinstance(result, Dict):
                raise ValueError("API выдает не словарь")
            return dict(result)

    def get_vacancies(self, keyword: str, max_per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Метод получения вакансий
        :param keyword: Ключевое слово
        :param max_per_page: Максимальное количество страниц (по умолчанию 20)
        :return: Список словарей вакансий
        """
        self.__params["text"] = keyword
        self.__params["page"] = 0
        self.__vacancies.clear()
        while self.__params.get("page", 0) < max_per_page:
            data = self.connect()
            vacancy = data.get("items", [])
            if not vacancy:
                break
            self.__vacancies.extend(vacancy)
            self.__params["page"] += 1  # Увеличение номера страницы
        return self.__vacancies

    @staticmethod
    def __valid_per_page(per_page: int) -> int:
        """Проверка корректности количества страниц"""
        if not isinstance(per_page, int):
            raise TypeError("Атрибут не является целым числом")
        if per_page <= 0:
            raise ValueError("Параметр не может быть положительным и 0")
        elif per_page > 100:
            raise ValueError("Параметр не может быть больше 100")
        else:
            return per_page
