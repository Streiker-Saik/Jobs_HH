import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Union

import requests
from dotenv import load_dotenv

from src.exceptions import APIError
from src.settings import BASE_DIR


class AbsTwelveDataApi(ABC):
    """
    Интерфейс работы с TwelveData_API
    Методы:
        connect(self) -> Dict[str, Any]:
            Метод подключения к API
    """

    @abstractmethod
    def connect(self) -> Dict[str, Any]:
        """Метод подключения к API"""
        pass


class TwelveDataApiExchangeRate(AbsTwelveDataApi):
    """
    Класс работы с TwelveData_API_ExchangeRate

    Атрибуты:
        __api_key(str) Ключ для API

    Методы:
        __init__(self, __api_key: str) -> None:
            Инициализация класс TwelveData
            :raise ValueError: Если ключ пустой
        connect(self) -> Dict[str, Any]:
            Метод подключения к API
        __connect(self) -> Dict[str, Any]:
            Приватный метод подключения к Twelve_Data_Api
            :raise APIError: Ошибка запроса API
            :raise ValueError: Если API выдает не словарь
        get_rate(self, currency_from: str, currency_to: str) -> float:
            Метод получения стоимости валюты
            :raise ValueError: Курс валюты не найдет в API
            :raise TypeError: Стоимость не является числом
    """

    __api_key: str

    def __init__(self, __api_key: str) -> None:
        """
        Инициализация класс TwelveData
        :param __api_key: Ключ для API
        :raise ValueError: Если ключ пустой
        """
        if not __api_key:
            raise ValueError("Ключ не может быть пустым")
        self.__api_key = __api_key
        self.__currency_from = "RUB"
        self.__currency_to = "RUB"

    def connect(self) -> Dict[str, Any]:
        """Метод подключения к API"""
        return self.__connect()

    def __connect(self) -> Dict[str, Any]:
        """
        Приватный метод подключения к Twelve_Data_Api
        :return: Словарь ответа от API
        :raise APIError: Ошибка запроса API
        :raise ValueError: Если API выдает не словарь
        """ ""
        self.__url = (
            f"https://api.twelvedata.com/exchange_rate?symbol={self.__currency_from}/"
            f"{self.__currency_to}&apikey={self.__api_key}"
        )

        response = requests.get(self.__url)
        if response.status_code != 200:
            error_message = f"Ошибка API: {response.status_code} - {response.text}"
            raise APIError(error_message)

        result = response.json()
        if not isinstance(result, Dict):
            raise ValueError("API выдает не словарь")
        return dict(result)

    def get_rate(self, currency_from: str, currency_to: str) -> Union[int, float]:
        """
        Метод получения стоимости валюты
        :param currency_from: код валюты конвертируемой
        :param currency_to: код валюты
        :return: стоимость валюты
        :raise ValueError: Курс валюты не найдет в API
        :raise TypeError: Стоимость не является числом
        """
        self.__currency_from = currency_from
        self.__currency_to = currency_to
        result = self.connect()
        currency_price = result.get("rate")
        if currency_price is None:
            raise ValueError("Курс валюты не найдет в API")
        elif not isinstance(currency_price, (int, float)):
            raise TypeError("Стоимость не является числом")
        return currency_price


class CurrencyConversion:
    """
    Класс конвертации валюты

    Атрибуты:
        api_client(TwelveDataApi): Класс подключения к API

    Методы:
        __init__(self, api_client: TwelveDataApi) -> None:
            Инициализация класс CurrencyConversion
        conversion_in_rub(self, currency: str, amount: int) -> float:
            Метод конвертации валюты в рубли
    """

    api_client: TwelveDataApiExchangeRate

    def __init__(self, api_client: TwelveDataApiExchangeRate) -> None:
        """Инициализация класс CurrencyConversion"""
        self.api_client = api_client

    def conversion_in_rub(self, currency_from: str, currency_to: str, amount: int) -> float:
        """
        Метод конвертации валюты в рубли
        :param currency_from: код валюты, конвертируемой
        :param currency_to: код валюты
        :param amount: сумма для перевода
        :return: сумма в рублях
        """
        currency_price = self.api_client.get_rate(currency_from, currency_to)
        result = round(amount * currency_price, 2)
        return result


if __name__ == "__main__":
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("API_TWELVEDATA_KEY")
    api_data = TwelveDataApiExchangeRate(api_key)
    conversion = CurrencyConversion(api_data)
    amount_in_rub = conversion.conversion_in_rub("USD", "RUB", 100)
    print(amount_in_rub)
