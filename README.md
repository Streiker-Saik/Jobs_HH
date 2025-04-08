# Проект "Вакансии с HH"

## Описание:



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

# Примеры работы функций:




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