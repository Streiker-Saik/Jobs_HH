import os
from typing import Generator, List

import pytest

from src.settings import BASE_DIR
from src.vacancies import Vacancy


@pytest.fixture
def vacancy_one() -> Vacancy:
    return Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123456",
        salary_from=100000,
        salary_to=150000,
        experience="От 1 года до 3 лет",
    )


@pytest.fixture
def vacancy_two() -> Vacancy:
    return Vacancy(
        name="QA engineer",
        url="https://hh.ru/vacancy/119246134",
        salary_from=150000,
        salary_to=230000,
        experience="От 3 лет",
    )


@pytest.fixture
def vacancy_three() -> Vacancy:
    return Vacancy(
        name="Тестировщик (middle QA Engineer)",
        url="https://hh.ru/vacancy/119270456",
        salary_to=125000,
        experience="От 1 года",
    )


@pytest.fixture
def vacancy_list(vacancy_one: Vacancy, vacancy_two: Vacancy, vacancy_three: Vacancy) -> List[Vacancy]:
    return [vacancy_one, vacancy_two, vacancy_three]


@pytest.fixture
def json_file() -> Generator:
    file_path = BASE_DIR / "data" / "data_test.json"
    yield file_path
    if file_path.exists():
        os.remove(file_path)
