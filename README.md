# Проект "Вакансии с HH"

## Описание:

Программа, получает информацию о вакансиях с платформы hh.ru в России, 
сохранять ее в файл и позволять удобно работать с ней: добавлять, фильтровать, удалять

## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

## Установка Poetry:
Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Проверить Poetry добавлен в ваш PATH.
```bash
poetry --version
```

## Установка:
- Клонируйте репозиторий:
```bash
git clone git@github.com:Streiker-Saik/CourseProject2.git
```
- Перейдите в директорию проекта:
```
cd "ваш-репозиторий"
```
- Установите необходимые зависимости:
```bash
poetry add pip requests
poetry add --group lint flake8 black isort mypy
poetry add --group dev pytest pytest-cov
```

# Модули:

## src.interfaces.py
class AbstractApi(ABC)
```
Абстрактный класс работы с API
    connect(self) -> Dict[Any, Any]:
        Метод подключения к API
    get_vacancies(self, keyword) -> List[Dict[Any, Any]]:
        Метод получения вакансий 
```

## src.exceptions.py
class APIError(Exception)
```
Исключение, ошибки статуса API
    __init__(self, message: Optional[str] = None) -> None:
        Инициализация исключения APIError
```

## src.head_hunter_api.py
class HeadHunterAPI(AbstractApi):
```
Класс работы с HeadHunter

Атрибуты:
    __url(str): Базовый url (private); 
    __headers(dict): Заголовки запроса (private); 
    __params(dict): Параметры запроса (private); 
    __vacancies(list): Список вакансий (private);
    per_page(int): Количество элементов(по умолчанию и максимум 100)
Методы:
    __init__(self, per_page: int = 100) -> None:
        Инициализатор экземпляра класса HeadHunterAPI.
    connect(self) -> Dict[Any, Any]:
        Метод подключения к API
    __connect(self) -> Dict[Any, Any]:
        Приватный метод подключения к Head_Hunter_API
    get_vacancies(self, keyword: str, max_per_page: int = 1000) -> List[Dict[Any, Any]]:
        Метод получения вакансий
    __valid_per_page(per_page: int) -> int:
        Статический метод проверки корректности аргумента
        TypeError: Если аргумент не является целым числом
        ValueError: Если аргумент равен 0 или отрицательный
```

## src.vacancies.py
class Vacancy
```
Класс представление вакансии

Атрибуты:
    name(str): Наименование вакансии
    url(str): Ссылка на вакансию
    salary_from(int): Зарплата "от" (по умолчанию None)
    salary_to(int): Зарплата "до" (по умолчанию None)
    experience(str): Требуемый опыт (по умолчанию "")

Методы:
    __init__(self, name: str, url: str, salary_from: Optional[int] = None, salary_to: Optional[int] = None,
    experience: str = "") -> None:
        Инициализация класса Vacancy
    __str__(self) -> str:
        Магический метод, строковое отображение класса. Формат:
        "name (url). Зарплата: salary_range. Требуемый опыт: {experience_str}"
    __lt__(self, other) -> bool:
        Магический метод, сравнения "меньше" средней зарплаты
        :raise TypeError: Не является классом Vacancy
    __le__(self, other) -> bool:
        Магический метод, сравнения "меньше или равно" средней зарплаты
        :raise TypeError: Не является классом Vacancy
    __gt__(self, other) -> bool:
        Магический метод сравнения "больше" средней зарплаты
        :raise TypeError: Не является классом Vacancy
    __ge__(self, other) -> bool:
        Магический метод сравнения "больше или равно" средней зарплаты
        :raise TypeError: Не является классом Vacancy
    to_dict(self) -> Dict[str, Any]:
        Метод получение словаря из экземпляра класса. Формат:
        {"name": ..., "url": ..., "salary_from": ..., "salary_to": ..., "experience": ...}
    salary_average(self) -> Union[int, float]:
        Метод расчета средней зарплаты
    created_vacancy(cls, vacancy_data: Dict[Any, Any]) -> "Vacancy":
        Классовый метод создание экземпляра класса из словаря.
    cast_to_object_list(cls, vacancy_data: List[Dict[Any, Any]]) -> List["Vacancy"]:
        Классовый метод создание списка экземпляров класса из списка словарей
    __valid_name(name: str) -> str:
        (private) Статический метод, проверка корректности наименования вакансии
        :raise TypeError: Название не является строкой
        :raise ValueError: Название вакансии не бывает с 1 символом
    __valid_url(url: str) -> str:
        (private) Статический метод, проверка корректности ссылки
        :raise TypeError: Ссылка не является строкой
        :raise ValueError: Ссылка не подходит под формат
    __valid_salary_from(salary_from: Optional[int] = None) -> int:
        (private) Проверка корректности зарплаты 'от'
        :raise TypeError: Зарплата 'от' не является числом
        :raise ValueError: Зарплата 'от' не может быть отрицательным числом
    __valid_salary_to(salary_to: Optional[int], salary_from: int) -> int:
        (private) Проверка корректности зарплаты 'до'
        :raise TypeError: Зарплата 'до' не является числом
        :raise ValueError: Зарплата 'до' не может быть отрицательным числом или меньше зарплаты 'от'
    __valid_class(other: "Vacancy") -> "Vacancy":
        (private) Статический метод, проверка корректности экземпляра класса
        :raise TypeError: Не является классом Vacancy
```

## src._____.py
```
```

## Тестирование:
Этот проект использует pytest для тестирования. Чтобы запустить тесты, выполните следующие шаги:

- Запустите тесты с помощью команды:
```bash
pytest
```
- Для получения подробного отчета о тестировании запустите:
```bash
pytest -v
```
- Запустите mypy для проверки типов:
```
mypy "ваш_скрипт".py
```