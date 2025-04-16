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
poetry add --group lint flake8 black isort mypy types-requests
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
class AbstractJobFiles(ABC)
```
Абстрактный класс аботы с файлами
    read_data(self) -> List[Dict[str, Any]]:
        Метод получения данных из файла
    add_data(self, data: Dict[str, Any]) -> None:
        Метод добавления данных в файл
    del_data(self, data: Dict[str, Any]) -> None:
        Метод удаления данных из файла
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

## src.job_files.py
class JSONSaver(AbstractJobFiles)
```
Класс работы с JSON файлами

Атрибуты:
    file_path(str): путь к файлу

Методы:
    __init__(self, file_path: str):
        Инициализация класса JSONSaver
    read_data(self) -> List[Dict[str, Any]]:
        Метод получения данных из JSON файла
        :raise FileNotFoundError: Если файл не найден. Обходит исключение.
            Выводит пустой список
        :raise json.JSONDecodeError: Ошибка форматирования JSON файла. Обходит исключение.
            Выводит пустой список
    add_data(self, data: Dict[str, Any]) -> None:
        Метод добавления данных в файл (добавляет, а не перезаписывает)
    del_data(self, vacancy: Dict[str, Any]) -> None:
        Метод удаления данных из файла
        :raise ValueError: Вызывается, если удаляемые данные не найдены. Обходит исключение.
            Выводит в консоль 'Вакансия не найдена'
```

## src.utils.py
user_response_top_n 
Функция запроса у пользователя то n вакансий
- принимает: Количество попыток (по умолчанию 5)
- возвращает: Положительное число
При не положительном числе, запрашивает еще раз ввод информации
```
user_response_top_n()
>>>
Введите количество вакансий для вывода в топ N: 5
>>>
5
```
user_response_salary_range
Функция запроса у пользователя диапазон цен
- принимает: Количество попыток (по умолчанию 5)
- возвращает: Кортеж из минимальной и максимальной зарплаты
При вводе не двух чисел или если первое число больше второго, запрашивает еще раз ввод информации
```
user_response_salary_range()
>>>
Введите диапазон зарплат: 10-50
>>>
(10, 50)
```
get_vacancies_by_salary
Функция получение зарплаты в указанном диапазоне
- принимает:
- - Список экземпляров класса Vacancy
- - Минимальная необходимая зарплата
- - Максимальная необходимая зарплата
- возвращает: Отфильтрованный список по зарплате
```
vacancy_one = Vacancy("Python Developer", "https://hh.ru/vacancy/123456", 100000, 150000, "От 1 года до 3 лет")
vacancy_two = Vacancy("QA engineer", "https://hh.ru/vacancy/119246134", 150000, 230000, "От 3 лет")
vacancy_three = Vacancy("Тестировщик (middle QA Engineer)", "https://hh.ru/vacancy/119270456", 125000, "От 1 года")
vacancy_list = [vacancy_one, vacancy_two, vacancy_three]
get_vacancies_by_salary(vacancy_list, 100000, 150000)
>>>
vacancy_one - входит в диапозон
vacancy_two - не входит в диапозон
vacancy_three - входит в диапозон
[vacancy_one, vacancy_three]
```
get_top_vacancies
Функция получения топ-'n' вакансий из списка
- принимает: 
- - Список экземпляров класса Vacancy
- - Количество в списке
- возвращает: Список согласно топ N
ValueError: Если в списке меньше позиций, чем необходимо
```
get_top_vacancies(vacancy_list, 2)
>>>
[vacancy_two, vacancy_one]
```
print_vacancies
Функция вывода в консоль вакансий
- принимает: Список экземпляров класса Vacancy
```
print_vacancies(vacancy_list)
>>>
Python Developer (https://hh.ru/vacancy/123456). Зарплата: от 100000 до 150000. Требуемый опыт: От 1 года до 3 лет
QA engineer (https://hh.ru/vacancy/119246134). Зарплата: от 150000 до 230000. Требуемый опыт: От 3 лет
Тестировщик (middle QA Engineer) (https://hh.ru/vacancy/119270456). Зарплата: до 125000. Требуемый опыт: От 1 года"
```
safe_json
Функция записи экземпляров класса в JSON файл
- принимает: 
- - Список экземпляров класса Vacancy
- - Путь к файлу
```
file_path = BASE_DIR / "data" / "vacancies.json"
safe_json(vacancy_list, file_path)
>>>vacancies.json>>>
[
    {
        "name": Python Developer
    }, ...
]
```
## src.twelve_dat_api.py
class AbsTwelveDataApi(ABC)
```
Интерфейс работы с TwelveData_API
Методы
    connect(self) -> Dict[str, Any]:
        Метод подключения к API
```
class TwelveDataAPIExchangeRate(AbsTwelveDataApi)
```
Класс работы с TwelveData_API_ExchangeRate
    Атрибуты:
        __api_key(str) Ключ для API
        __currency(str) Код валюты
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
```
class CurrencyConversion
```
Класс конвертации валюты
Атрибуты:
    api_client(TwelveDataApi): Класс подключения к API
Методы:
    __init__(self, api_client: TwelveDataApi) -> None:
        Инициализация класс CurrencyConversion
    conversion_in_rub(self, currency_from: str, currency_to: str, amount: int) -> float:
        Метод конвертации валюты
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