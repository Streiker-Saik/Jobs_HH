import json

from src.head_hunter_api import HeadHunterAPI
from src.settings import BASE_DIR
from src.utils import (get_top_vacancies, get_vacancies_by_salary, print_vacancies, safe_json,
                       user_response_salary_range, user_response_top_n)
from src.vacancies import Vacancy

file_path = BASE_DIR / "data" / "top_vacancies.json"


def user_interaction() -> None:
    """Интерфейс работы с пользователем"""
    search_query = input("Введите поисковый запрос: ")
    top_n = user_response_top_n()
    salary_min, salary_max = user_response_salary_range()

    hh_api = HeadHunterAPI()
    # Выполняется получение вакансий с ключевыми словами
    hh_vacancies = hh_api.get_vacancies(search_query)
    # Получение списка вакансий списком экземпляров класса
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    # Получение вакансий в диапазоне зарплат
    ranged_vacancies = get_vacancies_by_salary(vacancies_list, salary_min, salary_max)
    # Получение топ N вакансий
    top_vacancies = get_top_vacancies(ranged_vacancies, top_n)
    # Вывод в консоль вакансии
    print_vacancies(top_vacancies)
    # Сохранение информации о вакансиях в файл
    safe_json(top_vacancies, file_path)


if __name__ == "__main__":
    user_interaction()
    with open(file_path):
        json.loads()
