from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from src.vacancies import Vacancy
from src.validates import ValidVacancy


@patch.object(ValidVacancy, "validate_vacancy_to_dict")
def test_vacancies_init(mock_valid: MagicMock) -> None:
    """Тестирование инициализации класса"""
    name = "Python Developer"
    url = "https://hh.ru/vacancy/123456"
    salary_from = 100000
    salary_to = 150000
    experience = "От 1 года до 3 лет"

    mock_valid.return_value = {"name": name, "url": url, "salary_from": salary_from, "salary_to": salary_to}
    vacancy = Vacancy(name, url, salary_from, salary_to, experience)

    assert vacancy.name == name
    assert vacancy.url == url
    assert vacancy.salary_from == salary_from
    assert vacancy.salary_to == salary_to
    assert vacancy.experience == experience

    # Проверка, что все мок был вызван ровно один раз
    mock_valid.assert_called_once_with(name, url, salary_from, salary_to)


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


def test_vacancy_to_dict(vacancy_one: Vacancy) -> None:
    """Тестирование, получение словаря из экземпляра класса"""
    expected = {
        "name": "Python Developer",
        "url": "https://hh.ru/vacancy/123456",
        "salary_from": 100000,
        "salary_to": 150000,
        "experience": "От 1 года до 3 лет",
    }
    assert vacancy_one.to_dict() == expected


def test_created_vacancy() -> None:
    """Тестирование создания класса из словаря"""
    vacancy_dict = {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123456",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
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
