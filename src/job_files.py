import json
from pathlib import Path
from typing import Any, Dict, List

from src.interfaces import AbstractJobFiles


class JSONSaver(AbstractJobFiles):
    """
    Класс работы с JSON файлами

    Атрибуты:
        file_path(str): путь к файлу

    Методы:
        __init__(self, file_path: str):
            Инициализация класса JSONSaver
        read_data(self) -> List[Dict[str, Any]]:
            Метод получения данных из JSON файла
            :raise FileNotFoundError: Если файл не найден. Обходит исключение.
                Выводит пустой список
            :raise json.JSONDecodeError: Ошибка форматирования JSON файла. Обходит исключение.
                Выводит пустой список
        add_data(self, data: Dict[str, Any]) -> None:
            Метод добавления данных в файл (добавляет, а не перезаписывает)
        del_data(self, vacancy: Dict[str, Any]) -> None:
            Метод удаления данных из файла
            :raise ValueError: Вызывается, если удаляемые данные не найдены. Обходит исключение.
                Выводит в консоль 'Вакансия не найдена'
    """

    file_path: str

    def __init__(self, file_path: str | Path) -> None:
        """
        Инициализация класса JSONSaver
        :param file_path: Путь к файлу
        """
        self.__file_path = file_path

    def read_data(self) -> List[Dict[str, Any]]:
        """
        Метод получения данных из JSON файла
        :return: Список словарей
        :raise FileNotFoundError: Если файл не найден. Выводит пустой список
        :raise json.JSONDecodeError: Ошибка форматирования JSON файла. Выводит пустой список
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                if isinstance(data, List):
                    return data
                return []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def add_data(self, data: Dict[str, Any]) -> None:
        """
        Метод добавления данных в файл (добавляет, а не перезаписывает)
        :param data: Словарь с данными
        """
        file_data = self.read_data()
        if data not in file_data:
            file_data.append(data)
        with open(self.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(file_data, json_file, indent=4, ensure_ascii=False)

    def del_data(self, data: Dict[str, Any]) -> None:
        """
        Метод удаления данных из файла
        :param data: Словарь с данными
        :raise ValueError: Вызывается, если удаляемые данные не найдены, с выводом в консоль 'Вакансия не найдена'
        """
        file_data = self.read_data()
        try:
            file_data.remove(data)
        except ValueError:
            print("Вакансия не найдена")
        else:
            with open(self.__file_path, "w", encoding="utf-8") as json_file:
                json.dump(file_data, json_file, indent=4, ensure_ascii=False)
