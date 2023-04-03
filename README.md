# Adverity python challenge
This project required python3.10 and poetry to be installed.

Tested in Ubuntu 22.04

Visit https://python-poetry.org/docs/ for poetry official documentation.

## Install
```
$ git clone https://github.com/mainden7/adverity-python-challenge.git
$ cd adverity-python-challenge
$ poetry install
```

## Run migrations and dev server
```
$ python manage.py migrate
$ python manage.py runserver
```

## TODO
1. Run fetching functionality in background with celery/dramatiq and Redis/RMQ
2. Add unit tests to the services module
3. Add proper type annotations where they're missed. (Haven't enough time to add correct types). `mypy` may be used for static types checking
4. Write project code standards and add pre-commit configs to check code quality (flake8, mypy, bandit, isort etc)
5. There are few more TODOs in project source code for the detailed improvements.