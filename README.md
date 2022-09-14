![example workflow](https://github.com/SinitsyNik/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Foodgram

## Описание:
«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект запущен по адресу:
<http://51.250.106.212/>
<http://foodgram-project.hopto.org/>

Админ панель:
<http://51.250.106.212/admin/>
<http://foodgram-project.hopto.org/admin/>


## Как запустить:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:SinitsyNik/foodgram-project-react.git
```

Подключиться к серверу
```
ssh username@server_address
```

Устанавливаем докер
```
sudo apt install docker.io
```

Скопируйте файлы ```docker-compose.yaml``` и ```nginx.conf``` проекта на сервер
```
/home/<ваш_username>/docker-compose.yaml и /home/<ваш_username>/nginx.conf```
```

Заполнить env/github secrets:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - секретный ключ приложения django
ALLOWED_HOSTS - список разрешённых адресов
TELEGRAM_TO - id своего телеграм-аккаунта
TELEGRAM_TOKEN - токен бота
DB_NAME - postgres 
POSTGRES_USER - postgres
POSTGRES_PASSWORD - postgres
DEBUG - True
```

## Локальный запуск :
Перейти в папку с docker-compose:
```
cd infra
```

Развернуть контейнеры:
```
sudo docker-compose up -d --build
```

Выполнить миграции:
```
sudo docker-compose exec web python manage.py migrate
```

Подключить статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input 
```

Импорт ингридиентов:
```
sudo docker-compose exec backend python manage.py import_ingredients
```

Создайть суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```

Остановить контейнеры:
```
sudo docker-compose down -v 
```

## Дополнительно:
В директории infra создать фаил .env и заполнить
```
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password # укажите свой пароль
DB_HOST=db
DB_PORT=5432
```

## Технологии:
- python
- django
- django rest framework
- django-filter
- docker
- gunicorn
- nginx
- postgreSQL


## Автор:

### Никита Синицын
