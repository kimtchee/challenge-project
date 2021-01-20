from flask import Flask
from flask import request
import psycopg2

import person_service.config as cf
import person_service.dal.people as pf
import person_service.db as db


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


def clear_nones(d):
    return {k: v for k, v in d.items() if v is not None}


def create_app():
    app = Flask(__name__)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, psycopg2.Error):
            if conn:
                conn.rollback()
            return {'message': f'{e}', 'success': False}, 500
        return e

    @app.route('/')
    def hello():
        return 'Hello World!'

    @app.route('/person', methods=['POST'])
    def create_person():
        expected_list_of_args = ['first_name', 'last_name', 'age', 'email']

        person_to_create = clear_nones(request.json)
        required_args = check_args(expected_list_of_args, person_to_create)
        if required_args:
            return {'success': False,
                    'message': 'Missing fields',
                    'fields': required_args}, 400
        person = pf.create_person(cursor, person_to_create)
        conn.commit()
        return {'created': bool(person), 'person': person}, 200

    @app.route('/person/<person_id>', methods=['GET'])
    def get_person(person_id):
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

    @app.route('/person/<person_id>', methods=['PUT'])
    def update_person(person_id):
        editable_list_of_args = ['first_name',
                                 'last_name',
                                 'age',
                                 'email']

        if not check_args(editable_list_of_args, request.json, at_least_one=True):
            return {'success': False,
                    'message': (f'Missing at least one of expected args '
                                f'{editable_list_of_args}')}, 400
        person_edits = clear_nones(request.json)
        person = pf.get_person_by_id(cursor, person_id)
        person_copy = person.copy()
        person_copy.update(person_edits)

        if person == person_copy:
            return {'updated': False,
                    'person': person,
                    'message': 'No updated necessary with data passed in'}, 200
        person_updated = pf.update_person(cursor, person_copy)
        conn.commit()
        return {'updated': bool(person_updated), 'person': person_updated}, 200

    @app.route('/person/<person_id>', methods=['DELETE'])
    def delete_person(person_id):
        person = pf.get_person_by_id(cursor, person_id)
        if not person:
            return {'message': 'No such person'}, 404
        pf.delete_person(cursor, person_id)
        conn.commit()
        return {'deleted': True, 'person_id': person_id}, 200

    @app.route('/latest_person_version/<person_id>', methods=['DELETE'])
    def delete_person_version(person_id):
        person = pf.get_person_by_id(cursor, person_id)
        if not person:
            return {'message': 'No such person'}, 404
        pf.delete_person_with_version(cursor, person_id, person['version'])
        conn.commit()
        return {'deleted': True, 'person_id': person_id, 'version': person['version']}, 200
    return app


if __name__ == '__main__':
    print('Hello World!')
