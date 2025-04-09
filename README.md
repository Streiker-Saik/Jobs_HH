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
    get_vacancies(self, keyword: str) -> List[Dict[Any, Any]]:
        Метод получения вакансий
    __valid_per_page(per_page: int) -> int:
        Статический метод проверки корректности аргумента
        TypeError: Если аргумент не является целым числом
        ValueError: Если аргумент равен 0 или отрицательный
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