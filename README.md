# the7chefs backend
[![Build Status](https://travis-ci.org/sohjunjie/the7chefs_backend.svg?branch=master)](https://travis-ci.org/sohjunjie/the7chefs_backend) [![codecov](https://codecov.io/gh/sohjunjie/the7chefs_backend/branch/master/graph/badge.svg?token=Yc1VJMeHV9)](https://codecov.io/gh/sohjunjie/the7chefs_backend)

*the7chefs_backend* is a provider of RESTful backend services for the mobile application [CookTasty](https://github.com/hoohoo-b/CookTasty).


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

#### 5. Before that...
You might not be able to successfully run the server in step 4 as you will need an environment file containing the configuration variables required by the code. You the format of the environment file can be found in this [dot.env file](dot.env). You will need to rename `dot.env` to `.env`.

You can now create your database objects such as users manually from http://127.0.0.1:8000/admin after running the server instance with ur local machine through the command in step 4.
