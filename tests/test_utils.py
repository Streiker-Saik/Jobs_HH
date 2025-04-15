from unittest.mock import MagicMock, patch
from src.utils import (
    user_response_top_n,
    user_response_salary_range,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
)
import pytest
from src.vacancies import Vacancy
from typing import List


@patch("builtins.input")
def test_user_response_top_n(mock_input: MagicMock) -> None:
    """Тестирование функции получения корректного числа от пользователя"""
    mock_input.side_effect = "3"
    assert user_response_top_n() == 3


@patch("builtins.input")
def test_user_response_top_n_negative(mock_input: MagicMock, capsys: pytest.CaptureFixture) -> None:
    """Тестирование функции получения отрицательного числа от пользователя"""
    mock_input.side_effect = ["-5", "3"]
    user_response_top_n()
    message = capsys.readouterr().out.strip()
    assert "Ошибка, вы ввели отрицательное число" in message


@patch("builtins.input")
def test_user_response_top_n_invalid(mock_input: MagicMock, capsys: pytest.CaptureFixture) -> None:
    """Тестирование функции получения не числа от пользователя"""
    mock_input.side_effect = ["a", "3"]
    user_response_top_n()
    message = capsys.readouterr().out.strip()
    assert "Ошибка, введено не корректное значение" in message


@patch("builtins.input")
def test_user_response_salary_range(mock_input: MagicMock) -> None:
    """Тестирование функции получения корректного ответа от пользователя"""
    mock_input.side_effect = ["100 - 500"]
    assert user_response_salary_range() == (100, 500)


@patch("builtins.input")
def test_user_response_salary_range_invalid(mock_input: MagicMock, capsys: pytest.CaptureFixture) -> None:
    """Тестирование функции получения не корректного ответа от пользователя"""
    mock_input.side_effect = ["100", "100 - 500"]
    user_response_salary_range()
    message = capsys.readouterr().out.strip()
    assert "Ошибка 100. Пример: 100000 - 150000" in message


@patch("builtins.input")
def test_user_response_salary_range_invalid_min(mock_input: MagicMock, capsys: pytest.CaptureFixture) -> None:
    """Тестирование функции получения не корректного ответа от пользователя, если минимальное больше максимальной"""
    mock_input.side_effect = ["500-100", "100-500"]
    user_response_salary_range()
    message = capsys.readouterr().out.strip()
    assert "Минимальная зарплата должна быть меньше максимальной" in message


def test_get_vacancies_by_salary(vacancy_list: List[Vacancy]) -> None:
    """Тестирование фильтрации экземпляров класса по зарплате"""
    assert len(vacancy_list) == 3
    ranged_vacancies = get_vacancies_by_salary(vacancy_list, 100000, 140000)
    assert len(ranged_vacancies) == 2


def test_get_top_vacancies(vacancy_list: List[Vacancy]) -> None:
    """Тестирование получения топ 'n' вакансий"""
    assert len(vacancy_list) == 3
    assert vacancy_list[0].salary_from == 100000
    assert vacancy_list[0].salary_to == 150000
    top_vacancies = get_top_vacancies(vacancy_list, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0].salary_from == 150000
    assert top_vacancies[0].salary_to == 230000
    assert top_vacancies[1].salary_from == 100000
    assert top_vacancies[1].salary_to == 150000


def test_get_top_vacancies_error(vacancy_list: List[Vacancy]) -> None:
    """Тестирование при превышении желаемого топа с возможным списком"""
    with pytest.raises(ValueError) as exc_info:
        get_top_vacancies(vacancy_list, 4)
    assert "В списке вакансий меньше чем необходимо" == str(exc_info.value)


def test_print_vacancies(vacancy_list: List[Vacancy], capsys: pytest.CaptureFixture) -> None:
    """Тестирование вывода в консоль вакансий"""
    print_vacancies(vacancy_list)
    message = capsys.readouterr().out.strip().split("\n")
    assert (
        message[0]
        == "Python Developer (https://hh.ru/vacancy/123456). Зарплата: от 100000 до 150000. "
           "Требуемый опыт: От 1 года до 3 лет"
    )
    assert (
        message[1]
        == "QA engineer (https://hh.ru/vacancy/119246134). Зарплата: от 150000 до 230000. "
           "Требуемый опыт: От 3 лет"
    )
    assert (
        message[2]
        == "Тестировщик (middle QA Engineer) (https://hh.ru/vacancy/119270456). Зарплата: до 125000. "
           "Требуемый опыт: От 1 года"
    )
