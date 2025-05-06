from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from src.exceptions import APIError
from src.twelve_data_api import CurrencyConversion, TwelveDataApiExchangeRate


@pytest.fixture
def api_key() -> str:
    return "test_api_key"


@pytest.fixture
def api_client(api_key: str) -> TwelveDataApiExchangeRate:
    return TwelveDataApiExchangeRate(api_key)


@pytest.fixture
def conversion(api_client: TwelveDataApiExchangeRate) -> CurrencyConversion:
    return CurrencyConversion(api_client)


def test_twelve_data_api_init(api_key: str) -> None:
    """Тестирование инициализации класса"""
    api_data = TwelveDataApiExchangeRate(api_key)
    assert api_data._TwelveDataApiExchangeRate__api_key == api_key  # type: ignore


def test_twelve_data_api_init_error() -> None:
    """Тестирование инициализации класса при пустом ключе"""
    with pytest.raises(ValueError) as exc_info:
        TwelveDataApiExchangeRate("")
    assert "Ключ не может быть пустым" == str(exc_info.value)


@patch.object(TwelveDataApiExchangeRate, "_TwelveDataApiExchangeRate__connect")
def test_connect(mock_connect: MagicMock, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование, работы запроса API"""
    expected_result: Dict[str, Any] = {}
    mock_connect.return_value = expected_result
    assert api_client.connect() == expected_result


@patch("requests.get")
def test_private_connect(mock_request: MagicMock, api_client: TwelveDataApiExchangeRate, api_key: str) -> None:
    """Тестирование, работы приватного запроса API"""
    expected_result = {"symbol": "USD/RUB", "rate": 82.13, "timestamp": 1744792740}
    mock_request.return_value.json.return_value = expected_result
    mock_request.return_value.status_code = 200
    assert api_client.connect() == expected_result

    mock_request.assert_called_once_with(f"https://api.twelvedata.com/exchange_rate?symbol=RUB/RUB&apikey={api_key}")


@patch("requests.get")
def test_private_connect_invalid(mock_request: MagicMock, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование, работы приватного запроса API, если выдается не словарь"""
    with pytest.raises(ValueError) as exc_info:
        expected_result = "Error"
        mock_request.return_value.result = expected_result
        mock_request.return_value.status_code = 200
        api_client.connect()
    assert str(exc_info.value) == "API выдает не словарь"


@patch("requests.get")
def test_private_connect_error(mock_request: MagicMock, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование, работы приватного запроса API с ошибкой статуса"""
    expected_result = "Параметры переданы с ошибкой"
    mock_request.return_value.json.return_value = expected_result
    mock_request.return_value.status_code = 400
    mock_request.return_value.text = expected_result
    with pytest.raises(APIError, match=f"Ошибка API: 400 - {expected_result}"):
        api_client.connect()


@patch.object(TwelveDataApiExchangeRate, "connect")
def test_get_rate(mock_connect: MagicMock, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование метода get_rate"""
    mock_connect.return_value = {"symbol": "USD/RUB", "rate": 82.13, "timestamp": 1744792740}
    assert api_client.get_rate("USD", "RUB") == 82.13


@patch.object(TwelveDataApiExchangeRate, "connect")
def test_get_rate_empty(mock_connect: MagicMock, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование метода get_rate если курс не найден"""
    mock_connect.return_value = {"symbol": "USD/RUB", "timestamp": 1744792740}
    with pytest.raises(ValueError) as exc_info:
        api_client.get_rate("USD", "RUB")
    assert "Курс валюты не найдет в API" == str(exc_info.value)


@patch.object(TwelveDataApiExchangeRate, "connect")
def test_get_rate_type(mock_connect: MagicMock, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование метода get_rate курс не является числом"""
    mock_connect.return_value = {"symbol": "USD/RUB", "rate": "82.13", "timestamp": 1744792740}
    with pytest.raises(TypeError) as exc_info:
        api_client.get_rate("USD", "RUB")
    assert "Стоимость не является числом" == str(exc_info.value)


def test_conversion_init(conversion: CurrencyConversion, api_client: TwelveDataApiExchangeRate) -> None:
    """Тестирование инициализации класса"""
    conversion = CurrencyConversion(api_client)
    assert conversion.api_client == api_client


@patch.object(TwelveDataApiExchangeRate, "get_rate")
def test_conversion_in_rub(mock_rate: MagicMock, conversion: CurrencyConversion) -> None:
    """Тестирование конвертации валюты"""
    mock_rate.return_value = 82.48
    result = conversion.conversion_in_rub("USD", "RUB", 100)
    assert result == 8248.0
