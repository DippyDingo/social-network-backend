# Social Network Backend

Backend API социальной сети на Django REST Framework.

## Реализовано

- Публикации (посты) с текстом и изображениями.
- Несколько изображений к одному посту:
  - основное изображение `image` (опционально);
  - дополнительные изображения `uploaded_images` (список файлов).
- Валидация: при создании поста должно быть хотя бы одно изображение (`image` или `uploaded_images`).
- Комментарии к постам.
- Лайки постов.
- Токен-авторизация (DRF Token).
- Геоданные поста:
  - входное поле `location` (строка локации);
  - сохранение `latitude`/`longitude` через `geopy.geocode()`;
  - отображение `location_name` через `geopy.reverse()`.
- Django Admin для управления моделями.

## Технологии

- Python 3.12+
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL
- Pillow
- geopy

## Запуск проекта

1. Создать и активировать виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Установить зависимости:

```powershell
pip install -r requirements.txt
```

3. Настроить подключение к PostgreSQL в [social_network/settings.py](social_network/settings.py).

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
- Получение токена: `POST http://127.0.0.1:8000/api/token/`
- Посты: `http://127.0.0.1:8000/api/posts/`

## Авторизация

Получить токен:

```http
POST /api/token/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "username": "admin",
  "password": "admin12345"
}
```

Использовать токен в запросах:

```http
Authorization: Token <your_token>
```

## API эндпоинты

- `GET/POST /api/posts/`
- `GET/PATCH/DELETE /api/posts/<id>/`
- `GET/POST /api/posts/<post_id>/comments/`
- `GET/PATCH/DELETE /api/posts/<post_id>/comments/<id>/`
- `POST/DELETE /api/posts/<post_id>/like/`

## Пример создания поста с несколькими изображениями и геолокацией

Запрос `multipart/form-data`:

- `text`: текст поста
- `image`: основной файл (опционально)
- `uploaded_images`: один или несколько файлов (можно передать ключ несколько раз)
- `location`: строка локации, например `Moscow, Red Square`

Пример `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <your_token>" \
  -F "text=Мой пост" \
  -F "uploaded_images=@C:/path/photo1.jpg" \
  -F "uploaded_images=@C:/path/photo2.jpg" \
  -F "location=Moscow, Red Square"
```

## Медиа-файлы

В режиме разработки медиа раздаются через `MEDIA_URL` при `DEBUG=True`.

Проверка:

- `http://127.0.0.1:8000/media/posts/<filename>`

## Модели

- `Post`
- `PostImage`
- `Comment`
- `Like`

## Примечания

- `token_settings.md` содержит отдельную инструкцию по VK access token и не требуется для DRF-токена проекта.
