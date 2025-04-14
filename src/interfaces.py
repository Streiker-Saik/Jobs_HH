from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractApi(ABC):
    """Абстрактный класс работы с API"""

    @abstractmethod
    def connect(self) -> Dict[Any, Any]:
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[Any, Any]]:
        """Метод получения вакансий"""
        pass


class AbstractJobFiles(ABC):
    """Абстрактный класс работы с файлами"""

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
