# from src.validates import
from typing import Any, Optional
from unittest.mock import MagicMock, patch

import pytest

from src.vacancies import Vacancy


@patch.object(Vacancy, "_Vacancy__valid_salary_to")
@patch.object(Vacancy, "_Vacancy__valid_salary_from")
@patch.object(Vacancy, "_Vacancy__valid_url")
@patch.object(Vacancy, "_Vacancy__valid_name")
def test_vacancies_init(
    mock_name: MagicMock, mock_url: MagicMock, mock_salary_from: MagicMock, mock_salary_to: MagicMock
) -> None:
    """Тестирование инициализации класса"""
    name = "Python Developer"
    url = "https://hh.ru/vacancy/123456"
    salary_from = 100000
    salary_to = 150000
    experience = "От 1 года до 3 лет"

    mock_name.return_value = name
    mock_url.return_value = url
    mock_salary_from.return_value = salary_from
    mock_salary_to.return_value = salary_to
    vacancy = Vacancy(name, url, salary_from, salary_to, experience)

    assert vacancy.name == name
    assert vacancy.url == url
    assert vacancy.salary_from == salary_from
    assert vacancy.salary_to == salary_to
    assert vacancy.experience == experience

    # Проверка, что все моки были вызваны ровно один раз
    mock_name.assert_called_once_with(name)
    mock_url.assert_called_once_with(url)
    mock_salary_from.assert_called_once_with(salary_from)
    mock_salary_to.assert_called_once_with(salary_to, salary_from)


@pytest.mark.parametrize(
    "salary_from, salary_to, experience, expected",
    [
        (
            None,
            None,
            None,
            "Python Developer (https://hh.ru/vacancy/123456). Зарплата: не указана. Требуемый опыт: не указан",
        ),
        (
            100000,
            None,
            None,
            "Python Developer (https://hh.ru/vacancy/123456). Зарплата: от 100000. Требуемый опыт: не указан",
        ),
        (
            None,
            150000,
            None,
            "Python Developer (https://hh.ru/vacancy/123456). Зарплата: до 150000. Требуемый опыт: не указан",
        ),
        (
            100000,
            150000,
            None,
            "Python Developer (https://hh.ru/vacancy/123456). Зарплата: от 100000 до 150000. "
            "Требуемый опыт: не указан",
        ),
        (
            100000,
            150000,
            "От 1 года до 3 лет",
            "Python Developer (https://hh.ru/vacancy/123456). Зарплата: от 100000 до 150000. "
            "Требуемый опыт: От 1 года до 3 лет",
        ),
    ],
)
def test_vacancy_string(salary_from: Optional[int], salary_to: Optional[int], experience: str, expected: str) -> None:
    """Тестирование строкового отображения класса"""
    name = "Python Developer"
    url = "https://hh.ru/vacancy/123456"
    vacancy = Vacancy(name, url, salary_from, salary_to, experience)
    assert str(vacancy) == expected


@pytest.mark.parametrize(
    "salary_from, salary_to, expected",
    [(None, None, 0), (100000, None, 100000), (None, 150000, 150000), (100000, 150000, 125000)],
)
def test_salary_average(salary_from: int, salary_to: int, expected: int) -> None:
    """Тестирование получение средней зарплаты"""
    name = "Python Developer"
    url = "https://hh.ru/vacancy/123456"
    vacancy = Vacancy(name, url, salary_from, salary_to)
    result = vacancy.salary_average()
    assert result == expected


def test_comparison(vacancy_one: Vacancy, vacancy_two: Vacancy, vacancy_three: Vacancy) -> None:
    """Тестирование, сравнения экземпляров класса"""
    assert vacancy_one < vacancy_two
    assert not vacancy_one > vacancy_two
    assert vacancy_one <= vacancy_three
    assert vacancy_one >= vacancy_three


def test_created_vacancy() -> None:
    """Тестирование создания класса из словаря"""
    vacancy_dict = {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123456",
        "salary": {
            "from": 100000,
            "to": 150000,
        },
        "experience": {"name": "От 1 года до 3 лет"},
    }
    vacancy = Vacancy.created_vacancy(vacancy_dict)
    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123456"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.experience == "От 1 года до 3 лет"


def test_created_vacancy_salary_null() -> None:
    """Тестирование создания класса из словаря при отсутствии указанной зарплаты"""
    vacancy_dict = {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123456",
        "salary": None,
        "experience": {"name": "От 1 года до 3 лет"},
    }
    vacancy = Vacancy.created_vacancy(vacancy_dict)
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0


def test_created_vacancy_experience_null() -> None:
    """Тестирование создания класса из словаря при отсутствии указанной опыта"""
    vacancy_dict = {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123456",
        "salary": {
            "from": 100000,
            "to": 150000,
        },
        "experience": None,
    }
    vacancy = Vacancy.created_vacancy(vacancy_dict)
    assert vacancy.experience == ""


def test_cast_to_object_list() -> None:
    """Тестирование получение списка экземпляров класса из списка словарей"""
    vacancies = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123456",
            "salary": {
                "from": 100000,
                "to": 150000,
            },
            "experience": {"name": "От 1 года до 3 лет"},
        },
        {
            "name": "QA engineer",
            "alternate_url": "https://hh.ru/vacancy/119246134",
            "salary": {
                "from": 150000,
                "to": 230000,
            },
            "experience": {"name": "От 3 лет"},
        },
    ]
    test_list = Vacancy.cast_to_object_list(vacancies)
    assert len(test_list) == 2
    assert test_list[0].name == "Python Developer"
    assert test_list[1].name == "QA engineer"


# ValidVacancy
def test_valid_name() -> None:
    """Тестирование валидации 'наименования вакансии'"""
    name = "Python Developer"
    result = Vacancy._Vacancy__valid_name(name)  # type: ignore
    assert result == name


@pytest.mark.parametrize(
    "name, expected, exc_message",
    [
        (1, TypeError, "Название не является строкой"),
        ("Q", ValueError, "Название вакансии не бывает с 1 символом"),
    ],
)
def test_valid_name_error_type(name: Any, expected: type[Exception], exc_message: str) -> None:
    """Тестирование валидации 'наименования вакансии' с ошибкой"""
    with pytest.raises(expected) as exc_info:
        Vacancy._Vacancy__valid_name(name)  # type: ignore
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
    result = Vacancy._Vacancy__valid_url(url)  # type: ignore
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
        Vacancy._Vacancy__valid_url(url)  # type: ignore
    assert exc_message == str(exc_info.value)


@pytest.mark.parametrize("salary_from, expected", [(100000, 100000), (None, 0)])
def test_valid_salary_from(salary_from: Optional[int], expected: str) -> None:
    """Тестирование валидации 'зарплаты <от>'"""
    result = Vacancy._Vacancy__valid_salary_from(salary_from)  # type: ignore
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
        Vacancy._Vacancy__valid_salary_from(salary_from)  # type: ignore
    assert exc_message == str(exc_info.value)


@pytest.mark.parametrize("salary_to, salary_from, expected", [(150000, 100000, 150000), (None, 100000, 0)])
def test_valid_salary_to(salary_to: Optional[int], salary_from: int, expected: str) -> None:
    """Тестирование валидации 'зарплаты <до>'"""
    result = Vacancy._Vacancy__valid_salary_to(salary_to, salary_from)  # type: ignore
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
        Vacancy._Vacancy__valid_salary_to(salary_to, salary_from)  # type: ignore
    assert exc_message == str(exc_info.value)


def test__valid_other(vacancy_one: Vacancy) -> None:
    """Тестирование корректности другого класса"""
    result = Vacancy._Vacancy__valid_other(vacancy_one)  # type: ignore
    assert result == vacancy_one


def test__valid_other_error(vacancy_one: Vacancy) -> None:
    """Тестирование не корректного другого класса"""
    error_type = 1
    with pytest.raises(TypeError) as exc_info:
        Vacancy._Vacancy__valid_other(error_type)  # type: ignore
    assert "Не является классом Vacancy" == str(exc_info.value)
