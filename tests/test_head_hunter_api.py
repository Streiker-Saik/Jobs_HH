from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from src.exceptions import APIError
from src.head_hunter_api import HeadHunterAPI


def test_hh_api_init() -> None:
    """Тестирование инициализации класса"""
    hh_api = HeadHunterAPI()
    assert hh_api.per_page == 100
    hh_api = HeadHunterAPI(1)
    assert hh_api.per_page == 1


@pytest.mark.parametrize(
    "attribute, expected, exc_message",
    [
        ("string", TypeError, "Атрибут не является целым числом"),
        (0, ValueError, "Параметр не может быть положительным и 0"),
        (-1, ValueError, "Параметр не может быть положительным и 0"),
        (101, ValueError, "Параметр не может быть больше 100"),
    ],
)
def test_invalid_per_page(attribute: Any, expected: type[Exception], exc_message: str) -> None:
    """Тестирование валидации аргумента класса"""
    with pytest.raises(expected, match=exc_message):
        HeadHunterAPI(attribute)


@patch.object(HeadHunterAPI, "_HeadHunterAPI__connect")
def test_connect(mock_connect: MagicMock) -> None:
    """Тестирование, работы запроса API"""
    expected_result: Dict[str, Any] = {}
    mock_connect.return_value = expected_result
    hh_api = HeadHunterAPI()
    assert hh_api.connect() == expected_result


@patch("requests.get")
def test_private_connect(mock_request: MagicMock) -> None:
    """Тестирование, работы приватного запроса API"""
    expected_result = {"items": [{"id": "123"}, {"id": "321"}]}
    mock_request.return_value.json.return_value = expected_result
    mock_request.return_value.status_code = 200
    hh_api = HeadHunterAPI()
    assert hh_api.connect() == expected_result

    mock_request.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": "", "page": 0, "per_page": 100},
    )


@patch("requests.get")
def test_private_connect_invalid(mock_request: MagicMock) -> None:
    """Тестирование, работы приватного запроса API, если выдается не словарь"""
    with pytest.raises(ValueError) as exc_info:
        expected_result = "Error"
        mock_request.return_value.result = expected_result
        mock_request.return_value.status_code = 200
        hh_api = HeadHunterAPI()
        hh_api.connect()
    assert str(exc_info.value) == "API выдает не словарь"


@patch("requests.get")
def test_private_connect_error(mock_request: MagicMock) -> None:
    """Тестирование, работы приватного запроса API с ошибкой статуса"""
    expected_result = "Параметры переданы с ошибкой"
    mock_request.return_value.json.return_value = expected_result
    mock_request.return_value.status_code = 400
    mock_request.return_value.text = expected_result

    hh_api = HeadHunterAPI()

    with pytest.raises(APIError, match=f"Ошибка API: 400 - {expected_result}"):
        hh_api.connect()

    mock_request.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": "", "page": 0, "per_page": 100},
    )


@patch.object(HeadHunterAPI, "_HeadHunterAPI__connect")
def test_get_vacancies(mock_response: MagicMock) -> None:
    """Тестирование метода get_vacancies"""
    mock_response.return_value = {"items": [{"id": "123"}]}

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("123", 1)

    assert len(vacancies) == 1
    assert vacancies[0]["id"] == "123"

    mock_response.assert_called_once_with()


@patch.object(HeadHunterAPI, "_HeadHunterAPI__connect")
def test_get_vacancies_none_key(mock_response: MagicMock) -> None:
    """Тестирование метода get_vacancies при отсутствии данных"""
    mock_response.return_value = {"error": "error message"}

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("123", 1)

    assert len(vacancies) == 0

    mock_response.assert_called_once_with()
