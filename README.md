# Django REST Framework LMS

Учебный проект по созданию системы управления курсами и уроками на Django + DRF. Реализованы: кастомный пользователь, CRUD API для курсов и уроков, PostgreSQL, .env-конфигурация, профиль пользователя.

Установка проекта:

git clone https://github.com/ViktorKarateev/DjangoRESTFrameworkHomeWork.git
cd DjangoRESTFrameworkHomeWork
poetry install

Создайте файл .env и укажите данные:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key

Примените миграции и запустите проект:

python manage.py migrate
python manage.py runserver