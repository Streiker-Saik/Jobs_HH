import re
from pathlib import Path
from typing import List, Tuple, Union

from src.job_files import JSONSaver
from src.vacancies import Vacancy


def user_response_top_n(numb_attempts: int = 5) -> int:
    """
    Функция запроса у пользователя то n вакансий
    :param numb_attempts: Количество попыток (по умолчанию 5)
    :return: Положительное число
    """
    numb_count = 0
    while numb_count < numb_attempts:
        try:
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            if top_n > 0:
                return top_n
            else:
                numb_count += 1
                print("Ошибка, вы ввели отрицательное число")
        except ValueError:
            numb_count += 1
            print("Ошибка, введено не корректное значение")
    return 0


def user_response_salary_range(numb_attempts: int = 5) -> Tuple[int, int]:
    """
    Функция запроса у пользователя диапазон цен
    :param numb_attempts: Количество попыток (по умолчанию 5)
    :return: Кортеж из минимальной и максимальной зарплаты
    """
    numb_count = 0
    while numb_count < numb_attempts:
        salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
        numbers = re.findall(r"\d+", salary_range)
        if len(numbers) == 2:
            salary_min, salary_max = map(int, numbers)
            if salary_min < salary_max:
                return salary_min, salary_max
            else:
                numb_count += 1
                print("Минимальная зарплата должна быть меньше максимальной")
        else:
            numb_count += 1
            print(f"Ошибка {salary_range}. Пример: 100000 - 150000")
    return 0, 0


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_min: int, salary_max: int) -> List[Vacancy]:
    """
    Функция получение зарплаты в указанном диапазоне
    :param vacancies: Список экземпляров класса Vacancy
    :param salary_min: Минимальная необходимая зарплата
    :param salary_max: Максимальная необходимая зарплата
    :return: Отфильтрованный список по зарплате
    """
    result = []
    for vacancy in vacancies:
        if salary_min <= vacancy.salary_average() <= salary_max:
            result.append(vacancy)
    return result


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Функция получения топ-'n' вакансий из списка
    :param vacancies: Список экземпляров класса Vacancy
    :param top_n: Количество в списке
    :return: Список согласно топ N
    :raise ValueError: Если в списке меньше позиций, чем необходимо
    """
    sorted_vacancies = sorted(vacancies, reverse=True)
    if len(vacancies) < top_n:
        raise ValueError("В списке вакансий меньше чем необходимо")
    return sorted_vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Функция вывода в консоль вакансий
    :param vacancies: Список экземпляров класса Vacancy
    """
    for vacancy in vacancies:
        print(vacancy)


def safe_json(vacancies: List[Vacancy], file_path: Union[str, Path]) -> None:
    """
    Функция записи экземпляров класса в JSON файл
    :param vacancies: Список экземпляров класса Vacancy
    :param file_path: Путь к файлу
    """
    json_saver = JSONSaver(file_path)
    for vacancy in vacancies:
        json_saver.add_data(vacancy.to_dict())
