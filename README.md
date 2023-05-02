
# О проекте

Групповой проект разработки API для ресурса YamDB.
YamDB - сервис сбора отзывов и оценок пользователей на произведения в категориях: книги, кино и музыка.


## Команда проекта

- [@olees-orlenko](https://github.com/olees-orlenko)
- [@zvzdt](https://github.com/zvzdt)
- [@AlexFeev-S](https://github.com/AlexFeev-S)



## Технологии

Python, Django, Django REST Framework, SQLite3, JWT



### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/api_yamdb.git

```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    для bash: source venv/scripts/activate
    ```
    ```
    для cmd: C:\> <venv>\Scripts\activate.bat
    ```
    ```
    для PowerShell: C:\> <venv>\Scripts\Activate.ps1
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Для импорта данных из СSV-файлов и переноса этих данных в БД проекта
необходимо выполнить команду:

```
python manage.py loaddata
```

### Типовые запросы к API:

1. Запрос на получение всех пользователей:

```
GET http://localhost:8000/api/v1/users/
```
2. Запрос на получение всех жанров:

```
GET http://localhost:8000/api/v1/genres/
```
3. Запрос на получение всех категорий:

```
GET http://localhost:8000/api/v1/categories/
```
4. Запрос на получение всех титулов:

```
GET http://localhost:8000/api/v1/titles/
```
5. Запрос на получение всех отзывов для конкретного титула:

```
GET http://localhost:8000/api/v1/titles/<title_id>/reviews
```
6. Запрос на получение всех комментариев для конкретного отзыва:

```
GET http://localhost:8000/api/v1/titles/<title_id>/reviews/<review_id>/comments
```
