# Prerequesites for local development
1. Have Python 3.x installed
2. Have Postgresql 13.x installed

# Setup DB
1. use `psql -U postgres`
2. create a database called `test` (or whatever you want, this will be used by the app)
3. create user called `test` (used by app) with password `test`
4. copy paste the `person_service/db_scripts/deploy` scripts to initialize the database OR use `psql -U postgres -d test -f person_service/db_scripts/deploy/0001_create_person_tables.sql` and `psql -U postgres -d test -f person_service/db_scripts/deploy/0002_create_person_fixtures.sql`

# How to run
1. Download the repository by using `git clone`
### On windows (git bash)
1. Initialize virtual environment: `python -m venv venv-proj` then `source venv-proj\Scripts\activate.bat`
2. `pip install -r requirements.txt`
3. Create `.env` file with the following keys: `pg_user`, `pg_db`, `pg_password` that map to the database credentials you created above
4. Make `run_dev.sh` executable by using `chmod +x run_dev.sh`
5. To start the application: `./run_dev.sh`
6. The url of this application should be: `http://localhost:5000`
### On Mac 
1. Initialize virtual environment: `python -m venv venv-proj` then `source venv-proj/bin/activate`
2. `pip install -r requirements.txt`
3. Create `.env` file with the following keys: `pg_user`, `pg_db`, `pg_password` that map to the database credentials you created above
4. Make `run_dev.sh` executable by using `chmod +x run_dev.sh`
5. To start the application: `./run_dev.sh`
6. The url of this application should be: `http://localhost:5000`

## How to run tests
Due to time limitations, I just used the same development database to write tests against. This project uses `pytest` which should run with the command:
`pytest tests`
