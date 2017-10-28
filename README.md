[![codecov](https://codecov.io/gh/sohjunjie/the7chefs_backend/branch/master/graph/badge.svg?token=Yc1VJMeHV9)](https://codecov.io/gh/sohjunjie/the7chefs_backend)

# the7chefs backend

Link to our [frontend](https://github.com/sohjunjie/the7chefs_frontend.git) code.


## Quick start (backend)
- Install postgres
- Install python
- Install pip
- Install virtual environment

#### 1. Activate virtual environment and change directory to `the7chefs` folder and install related packages using the following command on `command prompt`
```
        $ pip install -r requirements.txt
```

#### 2. Create a database on postgres on the `postgres` console using the following command
```
# CREATE USER the7chefsapp WITH PASSWORD 'qwe123qwe123';
# CREATE DATABASE the7chefs OWNER the7chefsapp;
# ALTER ROLE the7chefsapp superuser;
# ALTER ROLE the7chefsapp SET client_encoding TO 'utf8';
# ALTER ROLE the7chefsapp SET default_transaction_isolation TO 'read committed';
# ALTER ROLE the7chefsapp SET timezone TO 'UTC';
# GRANT ALL PRIVILEGES ON DATABASE the7chefs TO the7chefsapp;
```

#### 3. Run migrations to create the database schemas
```
        $ python manage.py makemigrations
        $ python manage.py migrate
```

#### 4. Start the server on your local machine with
```
        $ python manage.py runserver
```
You can create your database objects such as users manually from http://127.0.0.1:8000/admin after running the server instance with ur local machine
