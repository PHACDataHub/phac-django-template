# Django template project

## Configuring dev environment

1. install python3.10 and postgresql as specified [here](https://github.com/PHACDataHub/phac-django-docs/blob/master/local-dev.md#installing-and-using-postgres-wout-sci-ops-on-windows)

**setup virtualenv**

In repo root, 

1. `python -m venv venv`
2. `venv\Scripts\activate` (windows) or `source venv/bin/activate` (linux)
3. `pip install -r requirements.txt -r requirements_dev.txt`

**Set up DB and user**

1. psql -U postgres -c "CREATE ROLE sample_db_user with login"
2. psql -U postgres -c "ALTER ROLE sample_db_user createdb"
3. createdb -U sample_db_user sample_db

**populate DB**

1. `python manage.py migrate`
2. `python manage.py loaddata myapp/fixtures/lookups.yaml`
3. `python manage.py runscript myapp.scripts.dev`

# Adapting this template to your new project

TODO: consider making this a cookie-cutter template? Might not be worth it...

1. Delete the myapp stuff,
    - myapp dir
    - tests/myapp/
    - loaddata and runscript steps in populate-db instructions above 
2. use `django-admin startapp <newapp>` to create your own app (or do this later)
3. Replace the following strings (search/replace) everywhere, including your .env and this README
    - `myapp` -> `<newapp>`
    - `sample_db` -> `<your_db_name>`
    - `sample_db_user` -> `<your_db_user>`
    - `sample_db_test` -> `<your_db_test_name>` (just add `_test` as a suffix to DB name)
4. Follow the instructions in the "Configuring dev environment" section above and check that everything works 
5. Delete this section of the README
6. remove the .env file from the repo (you probably want to keep it locally though, maybe `git rm –cached .env`?)

