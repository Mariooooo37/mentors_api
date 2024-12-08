# Тестовое задание в компанию Red Soft.
### Сервис по организации наставничества.

### Технологии используемые в проекте:
- Python 3.12
- Django 5.1.4
- djangorestframework 3.15.2
- djangorestframework-simplejwt 5.3.1
- drf-spectacular 0.28.0

Необходимые для работы проекта зависимости описаны в файле requirements.txt

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Mariooooo37/mentors_api
```

```
cd mentors
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### После запуска проекта будут доступны:
Админка: http://localhost:8000/admin/

Документация Swagger: http://localhost:8000/api/docs/


### Автор:
Иванов Роман