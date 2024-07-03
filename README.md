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
2. `python manage.py loaddata my_app/fixtures/lookups.yaml`
3. `python manage.py runscript my_app.scripts.dev`


## Manually running auto-formatting

In the case your CI is failing due to formatting issues, you can run the following commands to fix them all.

1. `isort omd --settings-path pyproject.toml`
2. `black omd/ --config pyproject.toml`
3. `djlint --reformat omd --configuration pyproject.toml`


# Adapting this template to your new project

TODO: consider making this a cookie-cutter template? Might not be worth it...

1. Delete the my_app stuff,
    - my_app dir
    - tests/my_app/
    - loaddata and runscript steps in populate-db instructions above 
2. use `django-admin startapp <newapp>` to create your own app (or do this later)
3. Replace the following strings (search/replace) everywhere, including your .env and this README
    - `my_app` -> `<newapp>`
    - `sample_db` -> `<your_db_name>`
    - `sample_db_user` -> `<your_db_user>`
    - `sample_db_test` -> `<your_db_test_name>` (just add `_test` as a suffix to DB name)
4. Follow the instructions in the "Configuring dev environment" section above and check that everything works 
5. Delete this section and the next section of the README
6. remove the .env file from the repo (you probably want to keep it locally though, maybe `git rm –cached .env`?)


# TODO: things to add to this template project

- HTMX example w/ project tasks, maybe multiple examples
- extract utils into phac-helpers
- Add excel export



