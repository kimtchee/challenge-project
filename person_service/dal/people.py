from uuid import uuid4


def insert_person_guid(cur, person):
    query = '''\
        INSERT INTO people.people_guids (person_id)
          VALUES (%(person_id)s)
        '''
    cur.execute(query, person)


def insert_person(cur, person):
    query = '''\
        INSERT INTO people.people
          (person_id, first_name, middle_name, last_name, email, age)
        VALUES (%(person_id)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, %(age)s)
        '''
    cur.execute(query, person)


def create_person(cur, person_info):
    person_id = uuid4()
    person = {'person_id': person_id}
    insert_person_guid(cur, person)
    person.update(person_info)
    if not person.get('middle_name'):
        person['middle_name'] = None
    insert_person(cur, person)
    return person


def delete_person(cursor, person_id):
    query = '''\
        INSERT INTO people.deleted_people
          (person_id)
        VALUES (%(person_id)s);
        '''

    cursor.execute(query, {'person_id': person_id})


def delete_person_with_version(cursor, person_id, version):
    query = '''\
        DELETE FROM people.people
          WHERE person_id = %(person_id)s
            AND person_version = %(version)s
        '''

    cursor.execute(query, {'person_id': person_id, 'version': version})


def get_person_by_id(cursor, person_id):
    query = '''\
        SELECT pg.person_id,
        p.first_name,
        p.middle_name,
        p.last_name,
        p.email,
        p.age,
        p.person_version as version
        FROM people.people_guids pg
        JOIN people.people p ON p.person_id = pg.person_id
        LEFT JOIN people.deleted_people dp ON pg.person_id = dp.person_id
        WHERE pg.person_id = %(person_id)s
          AND dp.person_id IS NULL
        ORDER BY p.person_version DESC
        LIMIT 1;
        '''
    cursor.execute(query, {'person_id': person_id})
    person = cursor.fetchone()
    return person


def get_person_by_id_and_version(cursor, person_id, version):
    query = '''\
        SELECT pg.person_id,
        p.first_name,
        p.middle_name,
        p.last_name,
        p.email,
        p.age,
        p.person_version as version
        FROM people.people_guids pg
        JOIN people.people p ON p.person_id = pg.person_id
        LEFT JOIN people.deleted_people dp ON pg.person_id = dp.person_id
        WHERE pg.person_id = %(person_id)s
          AND p.person_version = %(version)s
          AND dp.person_id IS NULL
        ORDER BY p.person_version DESC
        LIMIT 1;
        '''
    cursor.execute(query, {'person_id': person_id, 'version': version})
    return cursor.fetchone()


def get_all_people(cursor):
    query = '''\
        SELECT pg.person_id,
        p.first_name,
        p.middle_name,
        p.last_name,
        p.email,
        p.age,
        p.person_version as version
        FROM people.people_guids pg
        JOIN people.people p ON p.person_id = pg.person_id
        LEFT JOIN people.deleted_people dp ON pg.person_id = dp.person_id
        WHERE dp.person_id IS NULL
        ORDER BY p.person_version
        '''
    cursor.execute(query)
    return cursor.fetchall()


def update_person(cursor, person_updates):
    print(person_updates)
    query = '''\
        INSERT INTO people.people
          (person_id, first_name, middle_name, last_name, email, age)
        VALUES (%(person_id)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, %(age)s)
        '''
    cursor.execute(query, person_updates)
    row = get_person_by_id(cursor, person_updates['person_id'])
    return row
