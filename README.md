# Сайт Foodgram
В проекте реализовано взаимодействие трёх сервисов: фронта, построенного на React, бекенда с API на фреймворке Django и конфигурации Nginx, а также базы данных PostgreSQL.
Функции сайта позволяют регистрировать пользователей, разделенных по правам доступа, создавать и изменять рецепты блюд. Дополнительными функциями являются: возможность подписаться на публикации автора, добавлять рецепты в избранное и в список покупок. Список покупок с необходимыми ингридиентами пользователь может скачать в формате .txt на своё устройство.
### Описание
В коде прописано автоматизированное развёртывания на удаленном сервере при помощи GitHub Actions. Добавлены команды последовательно запускающие после пушинга: проверку на стандартизацию pep8; загрузку на DockerHub образавов бэкэнда и фронтэнда, деплой контейнеров с DockerHub на боевой сервер и отправку оповещения в telegram об успешном запуске.
### Технологии
![bop](https://github.com/Polina1Kostina/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
- [Python 3.7]
- [Django 3.2.15]
- [Djoser]
- [Django REST Framework 3.12.4]
- [DRF multiple serializer 0.2.3]
- [Django-filters]
- [Docker-compose]
- [Nginx 1.21.3]
- [PostgreSQL 2.8.6]
- [Gunicorn 20.0.4]
- [GitHub Actions]

# Запуск проекта на удаленном сервере при помощи GitHub Actions:

Клонируйте репозиторий:
```
git clone git@github.com:Polina1Kostina/foodgram-project-react.git
```
Зайдите через консоль на свой удаленный сервер и установите дополнения docker:
```
ssh <username>@<host>
```
```
sudo systemctl stop nginx # если на сервере ранее были другие сервисы
```
```
sudo apt install docker.io 
```
Установите docker compose:
```
sudo apt -y install curl
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Сохраните ssh-ключ для подключения к боевому серверу:
```
cat ~/.ssh/id_rsa
```
Замените в файле nginx.conf "server_name" на соответствующий вашему адресу.
```
Скопируйте файлы docker-compose.yaml, nginx.conf и папку docs/ из проекта на сервер:
```
scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
```
```
scp -r docs/ <username>@<host>:/home/<username>/
```
```
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
Установите на сервер PostgreSQL:
```
sudo apt install postgresql postgresql-contrib -y
```
Создайте на GitHub в разделе settings переменные Secrets:
```
DOCKER_USERNAME # ваш username dockerhub
DOCKER_PASSWORD # ваш пароль dockerhub

HOST # IP-адрес вашего сервера
USER # имя пользователя для подключения к серверу
SSH_KEY
PASSPHRASE # если при создании ssh-ключа вы использовали фразу-пароль

DB_ENGINE
DB_NAME # имя базы данных
POSTGRES_USER # логин для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к БД
DB_HOST # название сервиса (контейнера)
DB_PORT # порт для подключения к БД

TELEGRAM_TO # ID вашего телеграм-аккаунта
TELEGRAM_TOKEN # токен вашего бота
```
После успешного деплоя создайте и выполните миграции:
```
sudo docker-compose exec web python manage.py makemigrations
```
```
sudo docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Соберите статические файлы:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Если вы хотите наполнить базу данными готовым спискои ингридиентов:
```
sudo docker-compose exec web python manage.py load_data
```
Запустить контейнеры:
```
sudo docker-compose start
```
Для остановки контейнеров:
```
sudo docker-compose stop
```
___
### Примеры GET запросов
Для получения списка доступных адресов отправьте запрос:
```
http://host/api/
```
Пример ответа на запрос о получении списка доступных адресов в формате json:
```
{
    "tags": "http://host/api/tags/",
    "ingredients": "http://host/api/ingredients/",
    "recipes": "http://host/api/recipes/",
    "users/subscriptions": "http://host/api/users/subscriptions/"
}
```
Для получения выбранного рецепта:
```
GET http://host/api/recipes/1/
```
Пример ответа на запрос о получении выбранного рецепта в формате json:
```
{
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "author": {
        "id": 1,
        "username": "polina",
        "first_name": "polina",
        "last_name": "kostina",
        "email": "kostina.polina@bk.ru",
        "is_subscribed": false
    },
    "image": "http://localhost/media/static/recipes/6405b885-f44e-4f6f-9dcf-1662147706d4.jpeg",
    "id": 1,
    "tags": [
        {
            "id": 1,
            "name": "Завтрак",
            "color": "#FF8F5A",
            "slug": "breakfast"
        }
    ],
    "ingredients": [
        {
            "id": 2182,
            "amount": 3,
            "name": "яйца куриные",
            "measurement_unit": "г"
        },
        {
            "id": 1647,
            "amount": 50,
            "name": "сливочное масло",
            "measurement_unit": "г"
        }
    ],
    "name": "Яичница",
    "text": "Пожарить на среднем огне",
    "cooking_time": 25
}
```
```
Добавить рецепт в избранное:
```
POST http://host/api/recipes/1/favorite/
```
Пример ответа на запрос добавить рецепт в избранное в формате json:
```
{
    "id": 1,
    "name": "Яичница",
    "cooking_time": 25,
    "image": "media/recipes/6405b885-f44e-4f6f-9dcf-1662147706d4.jpeg"
}
```
Все виды запросов и их описание доступно в документации по адресу:
```
http://host/api/docs/redoc.html
```
### Автор
- [Полина Костина], студентка Яндекс Практикума
#### [Мой проект на удаленном сервере](http://62.84.119.149/)

[//]: # (Ниже находятся справочные ссылки)

   [Python 3.7]: <https://www.python.org/downloads/release/python-370/>
   [Django 3.2.15]: <https://www.djangoproject.com/download/>
   [Djoser]: <https://djoser.readthedocs.io/en/latest/introduction.html>
   [Django REST Framework 3.12.4]: <https://www.django-rest-framework.org/community/release-notes/>
   [DRF multiple serializer 0.2.3]: <https://pypi.org/project/drf-multiple-serializer/>
   [Django-filters]: <https://django-filter.readthedocs.io/en/stable/guide/install.html>
   [Docker-compose]: <https://docs.docker.com/compose/gettingstarted/>
   [Nginx 1.21.3]: <https://nginx.org/ru/docs/beginners_guide.html>
   [PostgreSQL 2.8.6]: <https://www.postgresql.org/docs/>
   [Gunicorn 20.0.4]: <https://docs.gunicorn.org/en/stable/install.html>
   [GitHub Actions]: <https://docs.github.com/en/actions>
   [Полина Костина]: <https://github.com/Polina1Kostina>
