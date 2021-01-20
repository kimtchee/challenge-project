import random

import person_service.app as app
from faker import Faker

fake = Faker()
Faker.seed(4321)


def test_check_args():
    assert app.check_args(['a', 'f'], ['a']) == ['f']
    assert app.check_args(['a', 'f'], ['a'], at_least_one=True)


def test_app_works(test_client):
    res = test_client.get('/')
    assert res.get_data(as_text=True) == 'Hello World!'


def test_get_person(test_client):
    id = 'ceb5770f-c4e3-4ad7-bc5e-4e32e8047e63'
    res = test_client.get(f'/person/{id}')
    response = res.get_json()
    person = response['person']
    assert response['success']
    assert person['first_name'] == 'Mary'
    assert person['middle_name'] == 'Eugene'
    assert person['last_name'] == 'Smith'
    assert person['person_id'] == id
    assert person['version']


def test_create_person(test_client):
    person_to_create = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'age': 25,
        'email': fake.email()}
    res = test_client.post('/person', json=person_to_create)
    response = res.get_json()
    person = response['person']
    assert person['first_name'] == person_to_create['first_name']
    assert response['created']
    assert person['person_id']


def test_create_person_bad_request(test_client):
    person_to_create = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'age': 25,
        'email': None}
    res = test_client.post('/person', json=person_to_create)
    assert res.status_code == 400
    response = res.get_json()
    assert not response['success']
    assert response['message'] == 'Missing fields'
    assert response['fields'] == ['email']


def test_update_person(test_client):
    person_id = 'ceb5770f-c4e3-4ad7-bc5e-4e32e8047e63'
    age = random.randint(0, 100)
    person_to_update = {'age': age}
    res = test_client.put(f'/person/{person_id}',
                          json=person_to_update)
    response = res.get_json()
    person = response['person']
    assert person['age'] == age


def test_get_person_by_version(test_client):
    id = 'ceb5770f-c4e3-4ad7-bc5e-4e32e8047e63'
    version = 1
    res = test_client.get(f'/person_by_version/{id}?version={version}')
    response = res.get_json()
    person = response['person']
    assert response['success']
    assert person['first_name'] == 'Mary'
    assert person['middle_name'] == 'Eugene'
    assert person['last_name'] == 'Smith'
    assert person['person_id'] == id
    assert person['version'] == version


def test_get_all_persons(test_client):
    res = test_client.get('/person/all')
    response = res.get_json()
    people = response['people']
    assert people


def test_delete_person(test_client):
    person_to_create = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'age': 25,
        'email': fake.email()}
    res = test_client.post('/person', json=person_to_create)
    response = res.get_json()
    person = response['person']
    person_id = person['person_id']

    res = test_client.delete(f'/person/{person_id}')
    response = res.get_json()
    assert response['deleted']


def test_delete_latest_version(test_client):
    person_to_create = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'age': 25,
        'email': fake.email()}
    res = test_client.post('/person', json=person_to_create)
    response = res.get_json()
    person = response['person']
    person_id = person['person_id']

    person_update = {'age': 30}
    test_client.put(f'/person/{person_id}', json=person_update)

    res = test_client.delete(f'/latest_person_version/{person_id}')
    response = res.get_json()
    assert response['deleted']
    assert response['person_id'] == person_id
    assert response['version']
    