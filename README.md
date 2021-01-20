# Prerequesites for local development
1. Have Python 3.x installed
2. Have Postgresql 13.x installed
3. Use PGAdmin or psql for setup DB portion

# Setup DB
The first 3 instructions are very important!
1. use `psql -U postgres`
2. create a database called `test` (or whatever you want, this will be used by the app)
3. create user called `test` (used by app) with password `test`
4. Exit psql, Make `init_db.sh` executable by using `chmod +x init_db.sh` and run the script using `./init_db.sh` - This script is expecting your user to be `postgres`, so use the password (master password) for this.

# How to run
1. Download the repository by using `git clone`
### On windows (git bash)
1. Initialize virtual environment: `python -m venv venv-proj` then `source venv-proj\Scripts\activate`
2. `pip install -r requirements.txt`
3. Create `.env` file with the following keys: `pg_user`, `pg_db`, `pg_password` that map to the database credentials you created above
4. Make `run_dev.sh` executable by using `chmod +x run_dev.sh`
5. To start the application: `./run_dev.sh`
6. The url of this application should be: `http://localhost:5000`
### On Mac 
1. Initialize virtual environment: `python -m venv venv-proj` then `source venv-proj/bin/activate`
2. `pip install -r requirements.txt`
3. At least for me, I had trouble getting `psycopg2` to install. I worked around this by using this: `pip install psycopg2-binary`
3. Create `.env` file with the following keys: `pg_user`, `pg_db`, `pg_password` that map to the database credentials you created above. Example:
```.env
pg_user=test
pg_db=test
pg_password=test
```
4. Make `run_dev.sh` executable by using `chmod +x run_dev.sh`
5. To start the application: `./run_dev.sh`
6. The url of this application should be: `http://localhost:5000`

## How to run tests
Due to time limitations, I just used the same development database to write tests against. This project uses `pytest` which should run with the command:
`pytest tests`


### API Documentation
| endpoint                           | Method | Parameters / Request Body                                                                                                                                        | Example Request                                                                               | Example Response                                                                                                                                                                                                     |
| ---------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /person                            | POST   | `first_name`, `last_name`, `age`, `email`, optional: `middle_name`                                                                                               | `{"first_name": "Manda", "last_name": "Smith", "age": 30, "email": "manda_smith@email.com" }` | `{"created": true,  "person": { "age": 31,  "email": "manda_webb@email.com", "first_name": "Manda", "last_name": "Webb", "middle_name": null, "person_id": "ac96d01d-55d4-485f-8623-c99d07f34ae6"}} `                |
| /person/<person_id>                | GET    | `person_id` in path parameters                                                                                                                                   | GET `/person/ac96d01d-55d4-485f-8623-c99d07f34ae6`                                            | `{"success": true,  "person": { "age": 31,  "email": "manda_webb@email.com", "first_name": "Manda", "last_name": "Webb", "middle_name": null, "person_id": "ac96d01d-55d4-485f-8623-c99d07f34ae6", "version": 36}}`  |
| /person_by_version/<person_id>                | GET    | `person_id` in path parameters and `version` in query parameters                                                                                                 | GET `/person/ac96d01d-55d4-485f-8623-c99d07f34ae6?version=36`                                 | `{"success": true,  "person": { "age": 31,  "email": "manda_webb@email.com", "first_name": "Manda", "last_name": "Webb", "middle_name": null, "person_id": "ac96d01d-55d4-485f-8623-c99d07f34ae6", "version": 36}}`  |
| /person/<person_id>                | PUT    | `person_id` in path parameter, optional request body parameters: (Necessary for updates, at least 1 to make an update) `first_name`, `last_name`, `age`, `email` | PUT `/person/ac96d01d-55d4-485f-8623-c99d07f34ae6` --data `{"age": 32}`                       | `{ "person": { "age": 35,  "email": "manda_webb@email.com", "first_name": "Manda", "last_name": "Webb", "middle_name": null, "person_id": "ac96d01d-55d4-485f-8623-c99d07f34ae6", "version": 37 }, "updated": true}` |
| /person/<person_id>                | DELETE | `person_id` as path parameter                                                                                                                                    | DELETE `/person/e15ad746-db98-4ac8-a81d-b5bbd8a8b35c`                                         | `{"deleted": true, "person_id": "e15ad746-db98-4ac8-a81d-b5bbd8a8b35c"}`                                                                                                                                             |
| /latest_person_version/<person_id> | DELETE | `person_id` as path parameter                                                                                                                                    | DELETE `/person/d50c5529-61e4-4b13-bbb6-11aba327cb29`                                         | `{ "deleted": true, "person_id": "de9bad35-f3a4-4de8-a69b-49b0d08d8961",  "version": 41 }`                                                                                                                           |
