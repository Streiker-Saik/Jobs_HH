import json
from pathlib import Path
from typing import List

import pytest

from src.job_files import JSONSaver
from src.settings import BASE_DIR


def test_read_data(json_file: Path) -> None:
    """Тестирование чтения файла"""

    test_data = [{"name": "Python"}]
    with open(json_file, "w", encoding="utf-8") as file_json:
        json.dump(test_data, file_json, indent=4, ensure_ascii=False)
    json_saver = JSONSaver(json_file)
    assert json_saver.read_data() == test_data


def test_read_data_error(json_file: Path) -> None:
    """Тестирование открытия не корректного json файла"""
    test_data = "Error"
    with open(json_file, "w", encoding="utf-8") as file_text:
        file_text.write(test_data)
    json_saver = JSONSaver(json_file)
    assert json_saver.read_data() == []


def test_read_missing_file() -> None:
    """Тестирование открытия не существующего файла"""
    file_path = BASE_DIR / "data" / "data_test.json"
    json_saver = JSONSaver(file_path)
    assert json_saver.read_data() == []


def test_add_data(json_file: Path) -> None:
    """Тестирование добавление данных в файл"""
    test_data = [{"name": "Python"}]
    with open(json_file, "w", encoding="utf-8") as file_json:
        json.dump(test_data, file_json, indent=4, ensure_ascii=False)
    json_saver = JSONSaver(json_file)
    json_saver.add_data({"name": "Java"})
    assert json_saver.read_data() == [{"name": "Python"}, {"name": "Java"}]


def test_add_data_duplicate(json_file: Path) -> None:
    """Тестирование, не добавление, при наличие таких данных"""
    test_data = [{"name": "Python"}]
    with open(json_file, "w", encoding="utf-8") as file_json:
        json.dump(test_data, file_json, indent=4, ensure_ascii=False)
    json_saver = JSONSaver(json_file)
    json_saver.add_data({"name": "Python"})
    assert json_saver.read_data() == [{"name": "Python"}]


def test_del_data(json_file: Path) -> None:
    """Тестирование удаление данных из файла"""
    test_data = [{"name": "Python"}]
    with open(json_file, "w", encoding="utf-8") as file_json:
        json.dump(test_data, file_json, indent=4, ensure_ascii=False)
    json_saver = JSONSaver(json_file)
    json_saver.del_data({"name": "Python"})
    assert json_saver.read_data() == []


def test_del_data_not_found(json_file: Path, capsys: pytest.CaptureFixture) -> None:
    """Тестирование удаления данных, при отсутствии данных"""
    test_data: List = []
    with open(json_file, "w", encoding="utf-8") as file_json:
        json.dump(test_data, file_json, indent=4, ensure_ascii=False)
    json_saver = JSONSaver(json_file)
    json_saver.del_data({"name": "Python"})
    message = capsys.readouterr()
    assert message.out.strip() == "Вакансия не найдена"
