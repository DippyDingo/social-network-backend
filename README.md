# Social Network Backend

Backend API для социальной сети на Django + Django REST Framework.

## Стек

- Python 3.12+
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL

## Установка

1. Создать и активировать виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Установить зависимости:

```powershell
pip install -r requirements.txt
```

3. Настроить PostgreSQL в файле `social_network/settings.py` (`NAME`, `USER`, `PASSWORD`).

4. Применить миграции:

```powershell
python manage.py migrate
```

5. Создать суперпользователя:

```powershell
python manage.py createsuperuser
```

6. Запустить сервер:

```powershell
python manage.py runserver
```

## Полезные URL

- Админка: `http://127.0.0.1:8000/admin/`
- API posts: `http://127.0.0.1:8000/api/posts/`
- Получение токена: `http://127.0.0.1:8000/api/token/`

## Основные API-эндпоинты

- `GET/POST /api/posts/`
- `GET/PATCH/DELETE /api/posts/<id>/`
- `GET/POST /api/posts/<post_id>/comments/`
- `GET/PATCH/DELETE /api/posts/<post_id>/comments/<id>/`
- `POST/DELETE /api/posts/<post_id>/like/`

