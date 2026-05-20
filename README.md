# Project23 — Django-проект каталога товаров

Проект представляет собой учебное веб-приложение на Django с каталогом товаров, блогом и пользовательскими аккаунтами.

## Основные функции

- Регистрация и аутентификация пользователей.
- Каталог товаров:
  - просмотр списка и карточки товара,
  - создание товара авторизованным пользователем,
  - редактирование/удаление только владельцем,
  - модерация товара через права доступа.
- Система ролей и прав для группы **«Модератор продуктов»**:
  - право `can_unpublish_product`,
  - право `delete_product`.
- Блог с CRUD-операциями (в рамках приложения `blog`).

## Стек

- Python 3.13+
- Django 6
- PostgreSQL
- Pillow
- python-decouple

## Установка и запуск

### 1) Клонирование репозитория

```bash
git clone <repo_url>
cd Project23
```

### 2) Установка зависимостей

Через Poetry:

```bash
poetry install
```

Или через pip (если используете экспортированный requirements):

```bash
pip install -r requirements.txt
```

### 3) Настройка переменных окружения

Скопируйте пример и заполните значения:

```bash
cp myproject/.env.example myproject/.env
```

Минимально необходимы параметры БД:

- `DB_ENGINE` (например, `django.db.backends.postgresql`)
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

### 4) Применение миграций

```bash
cd myproject
python manage.py migrate
```

### 5) Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6) Создание группы модераторов продуктов

В проекте есть кастомная команда:

```bash
python manage.py create_moderator_group.py
```

Она создает/обновляет группу **«Модератор продуктов»** и назначает ей права:

- `store.can_unpublish_product`
- `store.delete_product`

### 7) Запуск сервера

```bash
python manage.py runserver
```

Откройте в браузере: `http://127.0.0.1:8000/`

## Структура приложений

- `myproject/store` — каталог товаров и права модерации.
- `myproject/blog` — блог.
- `myproject/users` — кастомная модель пользователя и связанные формы/представления.

## Проверки

Базовые команды для проверки проекта:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```
