import person_service.app as app
from faker import Faker

fake = Faker()
Faker.seed(4321)


def test_app_works(test_client):
    res = test_client.get('/')
    assert res.get_data(as_text=True) == 'Hello World!'


def test_get_person(test_client):
    id = 'ceb5770f-c4e3-4ad7-bc5e-4e32e8047e63'
    res = test_client.get(f'/person/{id}')
    response = res.get_json()
    person = response['person']
    assert response['success']
    assert person['age'] == 40
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
