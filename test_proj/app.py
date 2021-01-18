import test_proj.config as cf
import test_proj.dal.people as pf

from flask import Flask
from flask import request


def check_args(expected_list_of_args, args, at_least_one=False):
    for expected_arg in expected_list_of_args:
        if expected_arg not in args and not at_least_one:
            return False
        if at_least_one and expected_arg in args:
            return True
    return not at_least_one


def create_app():
    app = Flask(__name__)
    try:
        conn, cursor = cf.make_db_connection()
    except Exception as e:
        print('error while connecting to db')
        print(e)

    @app.route('/hello')
    def hello_world():
        return 'Hello World!'

    @app.route('/person', methods=['POST'])
    def create_person():
        expected_list_of_args = ['first_name', 'last_name', 'age', 'email']
        if not check_args(expected_list_of_args, request.json):
            return 'Missing request argument', 400
        person_to_create = request.json
        person = pf.create_person(cursor, person_to_create)
        conn.commit()
        person['created'] = True
        return {'person': person}, 200

    @app.route('/person/<person_id>', methods=['GET'])
    def get_person():
        expected_list_of_args = ['person_id']
        if not check_args(expected_list_of_args, request.args):
            return 'Missing request argument', 400
        person_id = request.args['person_id']
        person = pf.get_person_by_id(cursor, person_id)
        return {'person': person}, 200

    @app.route('/person_by_version', methods=['GET'])
    def get_person_by_version():
        expected_list_of_args = ['id', 'version']
        if not check_args(expected_list_of_args, request.args):
            return 'Missing request argument', 400
        person_id = request.args['id']
        person_version = request.args['version']
        person = pf.get_person_by_id_and_version(cursor,
                                                 person_id,
                                                 person_version)
        return person, 200

    @app.route('/person/all', methods=['GET'])
    def get_all_persons():
        persons = pf.get_all_people(cursor)
        return {'people': persons}, 200

    @app.route('/person', methods=['PUT'])
    def update_person():
        expected_list_of_args = ['id']
        editable_list_of_args = ['first_name',
                                 'last_name',
                                 'age',
                                 'email']
        if not check_args(expected_list_of_args, request.json):
            return 'Missing id', 400
        if not check_args(editable_list_of_args, request.json, at_least_one=True):
            return (f'Missing at least one of expected args '
                    f'{editable_list_of_args}',
                    400)
        person_edits = request.json
        person_id = person_edits['id']
        del person_edits['id']
        for key in person_edits:
            if person_edits[key] is None:
                del person_edits[key]

        person = pf.get_person_by_id(cursor, person_id)
        person.update(person_edits)
        person_updated = pf.update_person(cursor, person)
        conn.commit()
        return {'person': person_updated}, 200

    @app.route('/person', methods=['DELETE'])
    def delete_person():
        expected_list_of_args = ['id']

        if not check_args(expected_list_of_args, request.json):
            return 'Missing id', 400

        person_id = request.json['id']
        pf.delete_person(cursor, person_id)
        conn.commit()
        return {'deleted': True}, 200
    return app


if __name__ == '__main__':
    print('derp')
