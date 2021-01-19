# Prerequesites for local development
1. Have Python 3.x installed
2. Have Postgresql 13.x installed

# Setup DB
1. use `psql -U postgres`, create a database called `test` (or whatever you want, this will be used by the app) and user called `test` (used by app) and copy paste the `person_service/db_scripts/deploy` scripts to initialize the database.

# How to run
1. Download the repository by using `git clone`
### On windows (git bash)
1. Initialize virtual environment: `python -m venv venv-proj` then `source venv-proj\Scripts\activate.bat`
2. `pip install -r requirements.txt`
3. Create `.env` file
4. Make `run_dev.sh` executable by using `chmod +x run_dev.sh`
5. To start the application: `./run_dev.sh`
6. The url of this application should be: `http://localhost:5000`
### On Mac 
1. Initialize virtual environment: `python -m venv venv-proj` then `source venv-proj/bin/activate`
2. `pip install -r requirements.txt`
3. Create `.env` file
4. Make `run_dev.sh` executable by using `chmod +x run_dev.sh`
5. To start the application: `./run_dev.sh`
6. The url of this application should be: `http://localhost:5000`
