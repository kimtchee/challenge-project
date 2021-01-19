import person_service.config as cf
import person_service.dal.people as pf
import person_service.db as db

from flask import Flask
from flask import request


def check_args(expected_list_of_args, args, at_least_one=False):
    args_required = []
    for expected_arg in expected_list_of_args:
        if expected_arg not in args and not at_least_one:
            args_required.append(expected_arg)
        if at_least_one and expected_arg in args:
            return True
    return args_required


config = cf.get_config()
conn, cursor = db.make_db_connection(config=config)


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello World!'

    @app.route('/person', methods=['POST'])
    def create_person():
        expected_list_of_args = ['first_name', 'last_name', 'age', 'email']
        required_args = check_args(expected_list_of_args, request.json)
        if required_args:
            return {'success': False,
                    'message': 'Missing fields',
                    'fields': required_args}, 400
        person_to_create = request.json
        person = pf.create_person(cursor, person_to_create)
        conn.commit()
        return {'created': bool(person), 'person': person}, 200

    @app.route('/person/<person_id>', methods=['GET'])
    def get_person(person_id):
        if not person_id:
            return {'success': False,
                    'message': 'Missing request argument person_id in path'}, 400
        person = pf.get_person_by_id(cursor, person_id)
        return {'success': True, 'person': person}, 200

    @app.route('/person_by_version/<person_id>', methods=['GET'])
    def get_person_by_version(person_id):
        expected_list_of_args = ['version']
        required_args = check_args(expected_list_of_args, request.args)
        if required_args:
            return {'success': False,
                    'message': 'Missing fields',
                    'fields': required_args}, 400
        person_version = request.args['version']
        person = pf.get_person_by_id_and_version(cursor,
                                                 person_id,
                                                 person_version)
        return {'success': True, 'person': person}, 200

    @app.route('/person/all', methods=['GET'])
    def get_all_persons():
        persons = pf.get_all_people(cursor)
        return {'success': True, 'people': persons}, 200

    @app.route('/person', methods=['PUT'])
    def update_person():
        expected_list_of_args = ['id']
        editable_list_of_args = ['first_name',
                                 'last_name',
                                 'age',
                                 'email']

        required_args = check_args(expected_list_of_args, request.json)
        if required_args:
            return {'success': False,
                    'message': 'Missing required fields',
                    'fields': required_args}, 400

        if not check_args(editable_list_of_args, request.json, at_least_one=True):
            return {'success': False,
                    'message': (f'Missing at least one of expected args '
                                f'{editable_list_of_args}')}, 400
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
        return {'updated': bool(person_updated), 'person': person_updated}, 200

    @app.route('/person', methods=['DELETE'])
    def delete_person():
        expected_list_of_args = ['id']
        required_args = check_args(expected_list_of_args, request.json)
        if required_args:
            return {'message': 'Missing fields',
                    'fields': required_args}, 400

        person_id = request.json['id']
        pf.delete_person(cursor, person_id)
        conn.commit()
        return {'deleted': True, 'id': person_id}, 200

    @app.route('/latest_person_version', methods=['DELETE'])
    def delete_person_version():
        expected_list_of_args = ['id']

        if not check_args(expected_list_of_args, request.json):
            return 'Missing id', 400

        person_id = request.json['id']
        person = pf.get_person_by_id(cursor, person_id)
        if not person:
            return {'message': 'No such person'}, 404
        pf.delete_person_with_version(cursor, person_id, person['version'])
        conn.commit()
        return {'deleted': True, 'id': person_id, 'version': person['version']}, 200
    return app


if __name__ == '__main__':
    print('derp')
