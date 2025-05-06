from typing import Any, Optional
from unittest.mock import MagicMock, patch

import pytest

from src.validates import ValidVacancy


@patch.object(ValidVacancy, "_ValidVacancy__valid_salary_to")
@patch.object(ValidVacancy, "_ValidVacancy__valid_salary_from")
@patch.object(ValidVacancy, "_ValidVacancy__valid_url")
@patch.object(ValidVacancy, "_ValidVacancy__valid_name")
def test_validate(
    mock_name: MagicMock, mock_url: MagicMock, mock_salary_from: MagicMock, mock_salary_to: MagicMock
) -> None:
    """Тестирование получения валидных данных в виде словаря"""
    name = "Python Developer"
    url = "https://hh.ru/vacancy/123456"
    salary_from = 100000
    salary_to = 150000

    mock_name.return_value = name
    mock_url.return_value = url
    mock_salary_from.return_value = salary_from
    mock_salary_to.return_value = salary_to

    valid = ValidVacancy()
    result = valid.validate_vacancy_to_dict(name, url, salary_from, salary_to)
    expected = {
        "name": "Python Developer",
        "url": "https://hh.ru/vacancy/123456",
        "salary_from": 100000,
        "salary_to": 150000,
    }
    assert result == expected


def test_valid_name() -> None:
    """Тестирование валидности name"""
    name = "Python Developer"
    vacancy = ValidVacancy()
    result = vacancy.valid_name(name)
    assert result == name


@pytest.mark.parametrize(
    "name, expected, exc_message",
    [(123, TypeError, "Название не является строкой"), ("Q", ValueError, "Название вакансии не бывает с 1 символом")],
)
def test_valid_name_error(name: str, expected: type[Exception], exc_message: str) -> None:
    """Тестирование ошибки валидации name"""
    with pytest.raises(expected) as exc_info:
        ValidVacancy._ValidVacancy__valid_name(name)  # type: ignore
    assert exc_message == str(exc_info.value)


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://hh.ru/vacancy/123456", "https://hh.ru/vacancy/123456"),
        ("http://hh.ru/vacancy/123456", "http://hh.ru/vacancy/123456"),
        ("hh.ru/vacancy/123456", "hh.ru/vacancy/123456"),
    ],
)
def test_valid_url(url: str, expected: str) -> None:
    """Тестирование валидации 'ссылки'"""
    vacancy = ValidVacancy()
    result = vacancy.valid_url(url)
    assert result == expected


@pytest.mark.parametrize(
    "url, expected, exc_message",
    [
        (1, TypeError, "Ссылка не является строкой"),
        ("https://hh.ru/vacancy/", ValueError, "Ссылка не подходит под формат"),
    ],
)
def test_valid_url_error(url: Any, expected: type[Exception], exc_message: str) -> None:
    """Тестирование валидации 'наименования вакансии' с ошибкой"""
    with pytest.raises(expected) as exc_info:
        ValidVacancy._ValidVacancy__valid_url(url)  # type: ignore
    assert exc_message == str(exc_info.value)


@pytest.mark.parametrize("salary_from, expected", [(100000, 100000), (None, 0)])
def test_valid_salary_from(salary_from: Optional[int], expected: str) -> None:
    """Тестирование валидации 'зарплаты <от>'"""
    vacancy = ValidVacancy()
    result = vacancy.valid_salary_from(salary_from)
    assert result == expected


@pytest.mark.parametrize(
    "salary_from, expected, exc_message",
    [
        ("100000", TypeError, "Зарплата 'от' не является числом"),
        (-100000, ValueError, "Зарплата 'от' не может быть отрицательным числом"),
    ],
)
def test_valid_salary_from_error(salary_from: Any, expected: type[Exception], exc_message: str) -> None:
    """Тестирование валидации 'зарплаты <от>' с ошибкой"""
    with pytest.raises(expected) as exc_info:
        ValidVacancy._ValidVacancy__valid_salary_from(salary_from)  # type: ignore
    assert exc_message == str(exc_info.value)


@pytest.mark.parametrize("salary_to, salary_from, expected", [(150000, 100000, 150000), (None, 100000, 0)])
def test_valid_salary_to(salary_to: Optional[int], salary_from: int, expected: str) -> None:
    """Тестирование валидации 'зарплаты <до>'"""
    vacancy = ValidVacancy()
    result = vacancy.valid_salary_to(salary_to, salary_from)
    assert result == expected


@pytest.mark.parametrize(
    "salary_to, salary_from, expected, exc_message",
    [
        ("150000", 100000, TypeError, "Зарплата 'до' не является числом"),
        (-150000, 100000, ValueError, "Зарплата 'до' не может быть отрицательным числом или меньше зарплаты 'от'"),
        (50000, 100000, ValueError, "Зарплата 'до' не может быть отрицательным числом или меньше зарплаты 'от'"),
    ],
)
def test_valid_salary_to_error(salary_to: Any, salary_from: int, expected: type[Exception], exc_message: str) -> None:
    """Тестирование валидации 'зарплаты <до>' с ошибкой"""
    with pytest.raises(expected) as exc_info:
        ValidVacancy._ValidVacancy__valid_salary_to(salary_to, salary_from)  # type: ignore
    assert exc_message == str(exc_info.value)
