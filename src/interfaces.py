from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractApi(ABC):
    """Абстрактный класс работы с API"""

    @abstractmethod
    def connect(self) -> Dict[Any, Any]:
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword) -> List[Dict[Any, Any]]:
        """Метод получения вакансий"""
        pass
