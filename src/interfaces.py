from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class AbstractApi(ABC):
    """
    Абстрактный класс работы с API
        connect(self) -> Dict[Any, Any]:
            Метод подключения к API
        get_vacancies(self, keyword) -> List[Dict[Any, Any]]:
            Метод получения вакансий
    """

    @abstractmethod
    def connect(self) -> Dict[Any, Any]:
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[Any, Any]]:
        """Метод получения вакансий"""
        pass


class AbstractJobFiles(ABC):
    """
    Абстрактный класс работы с файлами
    Методы:
        read_data(self) -> List[Dict[str, Any]]:
            Метод получения данных из файла
        add_data(self, data: Dict[str, Any]) -> None:
            Метод добавления данных в файл
        del_data(self, data: Dict[str, Any]) -> None:
            Метод удаления данных из файла
    """

    @abstractmethod
    def read_data(self) -> List[Dict[str, Any]]:
        """Метод получения данных из файла"""
        pass

    @abstractmethod
    def add_data(self, data: Dict[str, Any]) -> None:
        """Метод добавления данных в файл"""
        pass

    @abstractmethod
    def del_data(self, data: Dict[str, Any]) -> None:
        """Метод удаления данных из файла"""
        pass


class Valid(ABC):
    """
    Абстрактный класс валидации
    Метод:
        validate_vacancy_to_dict(self, *args, **kwargs) -> Dict[str, Any]:
            Метод получения валидные данных вакансии выводит в виде словаря
    """

    @abstractmethod
    def validate_vacancy_to_dict(
            self, name: str, url: str, salary_from: Optional[int], salary_to: Optional[int]
    ) -> Dict[str, Any]:
        """Метод получения валидных данных вакансии выводит в виде словаря"""
        pass


class AbsTwelveDataApi(ABC):
    """
    Абстрактный класс интерфейса работы с TwelveData_API
    Методы:
        connect(self) -> Dict[str, Any]:
            Метод подключения к API
        get_rate(self, currency_from: str, currency_to: str) -> Union[int, float]:
            Метод получения стоимости валюты
    """

    @abstractmethod
    def connect(self) -> Dict[str, Any]:
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_rate(self, currency_from: str, currency_to: str) -> Union[int, float]:
        """Метод получения стоимости валюты"""
        pass
