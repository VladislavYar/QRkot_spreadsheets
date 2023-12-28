# QRkot_spreadsheets
## приложение для Благотворительного фонда поддержки котиков QRKot
Проект представляет из себя API, сделанный на фреймворке FastAPI. 

## Как запустить проект:
### Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:VladislavYar/cat_charity_fund.git
```

### Создать и активировать виртуальное окружение:
```
python -m venv env
source env/scripts/activate
```

### Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

## Запуск приложение
```
uvicorn app.main:app
```

## Cтек проекта
Python v3.9, FastAPI, SQLAlchemy, Google API

## Ручки:
### Auth
```
POST
/auth/jwt/login - аутентификация

POST
/auth/jwt/logout - выход

POST
/auth/register - регистрация
```
### Users
```
GET
/users/me - получить данные свого профиля

PATCH
/users/me - обновить данные своей профиля

GET
/users/{id} - получить данные другого пользователя
```
### Donation
```
GET
/donation/ - получить все пожертвования

POST
/donation/ - создать пожертвование

GET
/donation/my - получить личные пожертвования
```
### Charity Project
```
GET
/charity_project/ - получить все проекты

POST
/charity_project/ - создать проект

DELETE
/charity_project/{project_id} - удалить проект

PATCH
/charity_project/{project_id} - обновить данные по проекту
```
### Google
```
POST
/google/ - cоздать отчёт в Google-таблице с закрытми проектами отсортированными по времени сбора пожертвований.
