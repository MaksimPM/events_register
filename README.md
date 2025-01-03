<h1 align="center">Events Register</h1> 

<h2 align="center">Сервис для регистрации на мероприятие</h2> 

  
 Основной стек проекта:
  
      1. Python==3.11
      
      2. Django==4.1.13

      4. Djangorestframework==3.15.1

      5. Djangorestframework-simplejwt==5.3.1

      6. Celery==5.3.6

      7. Redis==5.0.3
      
      8. PostgreSQL

<h2 align="left">Для запуска проекта необходимо:</h2>
  
• Установить виртуальное окружение в корневой папке проекта командой:
```shell
python3.11 -m venv venv
```

• Создать в корне проекта файл ```.env``` и заполнить данные по образцу из файла ```.env.sample```

• Установить все необходимые зависимости, указанные в файле ```requirements.txt```:
```shell
pip install -r requirements.txt
```
• Выполнить создание и применение миграций командами:
```shell
python manage.py makemigration
```
```shell
python manage.py migrate
```
   
• Создать суперпользователя командой:
```shell
python manage.py csu
```

• Запустить сервер командой
```shell
python manage.py runserver
```

• Запустить Celery командой:
```shell
celery -A config worker -l INFO
```

<h2 align="left">Для запуска проекта через Docker необходимо:</h2>

Создать и заполнить файл ```.env``` по шаблону файла ```.env.sample```

Создать и заполнить файл ```.env.docker``` по шаблону файла ```.env.docker.sample```

Создать Docker контейнер командой:
```shell
docker-compose build
```
Запустить Docker контейнер командой:
```shell
docker-compose up
```

    Для тестирования сервиса рекомендуется использовать ```Postman```

________________________________________
## Эндпоинты (Endpoints)

### Регистрация пользователя

URL: /users/sign-up/

Метод: ```POST```

Пример запроса:

{
    "name": "......",
    "email": "......",
}

Ответ:
- Получаем сообщение на почту с приветствием и первичным паролем для входа на площадку (Celery)
________________________________________
### Авторизация пользователя

URL: /users/sign-in/

Метод: ```POST```

Пример запроса:

{
    "email": "......",
    "password": "......" (При первичном входе тот, что отправлен на почту)
}

Ответ:

{
    "JWT Token": "......"
}
________________________________________
### Запрос на смену пароля

URL: /users/recovery/

Метод: ```POST```

Пример запроса:

{
    "email": "......"
}

Ответ:
- Получаем сообщение на почту с ссылкой на смену пароля (Celery)
________________________________________
### Смена пароля

URL: /users/recovery/:hash/ - (ссылка отправленная на почту)

Метод: ```PATCH```

Пример запроса:

{
    "password": "......"
}  

Ответ:
- Смена пароля успешно выполнена
________________________________________
### Получение списка/создание мероприятий (Требуется авторизация)

URL: /events/

Метод: ```GET```

Ответ:
- Выводит список мероприятий

Метод: ```POST```

Пример запроса:

{
    "title": "......",
    "description": "......",
    "date": "......",
    "location": "......",
    "organizer": user.pk
}  

Ответ:
- Мероприятие создано (Отправляется сообщение на почту всем зарегистрированным на платформе пользователям (Celery))
________________________________________
### Детальный просмотр/изменение/удаления мероприятия (Требуется авторизация)

URL: /events/<int:pk>/

Метод: ```GET```

Пример запроса:

Ответ:
- Выводит выбранное мероприятие к просмотру

Метод: ```PUT```

Пример запроса:

{
    "title": "......",
    "description": "......",
    "date": "......",
    "location": "......",
    "organizer": user.pk
} 

Ответ:
- Мероприятие изменено

Метод: ```DELETE```

Ответ:
- Мероприятие удалено
________________________________________
### Запись на мероприятие (Требуется авторизация)

URL: /<int:event_id>/register/

Метод: ```POST```

Пример запроса:

{
    "user": user.pk,
    "event": event.pk
} 

Ответ:
- Отправляется сообщение на почту пользователю, кто оставил запись (Celery)
________________________________________
### Получение списка записей пользователя на мероприятия (Требуется авторизация)

URL: /register/

Метод: ```GET```

Ответ:
- Выводит список всех записей пользователя на мероприятия
________________________________________
### Отмена записи пользователя на мероприятия (Требуется авторизация)

URL: /<int:event_id>/cancel-registration/<int:registration_id>/

Метод: ```DELETE```

Ответ:
- Запись отменена
________________________________________
- К проекту написаны тесты и подключен Swagger, дополнительную информацию можно найти по URL: ```/docs/```

### Удачи!
