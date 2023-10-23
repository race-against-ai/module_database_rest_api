from dataclasses import dataclass
from datetime import date

import psycopg2

class ConventionNotFound(Exception):
    def __init__(self, *args: object) -> None:
        self.args = args
        super().__init__(f"Driver not found: {args}")

@dataclass
class Convention:
    convention_id: int
    name: str
    location: str
    created: date

def post_convention(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_name: str, 
        convention_location: str
        ) -> Convention:
    try:    

        sql_query = ""
        if convention_location is None:
            sql_query = "INSERT INTO conventions (name) VALUES (%s) RETURNING *"
            cursor.execute(sql_query, (convention_name,))
            

        else:
            sql_query = "INSERT INTO conventions (name, location) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_query, (convention_name, convention_location))

        convention_id, convention_name, convention_location, convention_created = cursor.fetchone()
        connection.commit()

        return Convention(
            convention_id=convention_id,
            name=convention_name,
            location=convention_location,
            created=convention_created,
        )
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_convention(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_id: int
        ) -> Convention:
    try:
        sql_query = "SELECT * FROM conventions WHERE id = %s"
        cursor.execute(sql_query, (convention_id,))
        convention_id, convention_name, convention_location, convention_created = cursor.fetchone()
        if convention_id is None: 
            raise ConventionNotFound(convention_id)
        else:
            connection.commit()

            return Convention(
                convention_id=convention_id,
                name=convention_name,
                location=convention_location,
                created=convention_created,
            )
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_conventions(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor
        ) -> Convention:
    try:
        sql_query = "SELECT * FROM conventions"
        cursor.execute(sql_query)
        conventions = []
        for convention_id, convention_name, convention_location, convention_created in cursor.fetchall():
            conventions.append(Convention(
                convention_id=convention_id,
                name=convention_name,
                location=convention_location,
                created=convention_created,
            ))
        connection.commit()
        return conventions
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def update_convention_name(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_id: int,
        convention_name: str
        ) -> Convention:
    try:
        get_convention(connection, cursor, convention_id)
        try:
            sql_query = "UPDATE conventions SET name = %s WHERE id = %s RETURNING *"
            cursor.execute(sql_query, (convention_name, convention_id))
            convention_id, convention_name, convention_location, convention_created = cursor.fetchone()
            connection.commit()

            return Convention(
                convention_id=convention_id,
                name=convention_name,
                location=convention_location,
                created=convention_created,
            )
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except ConventionNotFound as e:
        raise e

def update_convention_location(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_id: int,
        convention_location: str
        ) -> Convention:
    try:
        get_convention(connection, cursor, convention_id)
        try:
            sql_query = "UPDATE conventions SET location = %s WHERE id = %s RETURNING *"
            cursor.execute(sql_query, (convention_location, convention_id))
            convention_id, convention_name, convention_location, convention_created = cursor.fetchone()
            connection.commit()

            return Convention(
                convention_id=convention_id,
                name=convention_name,
                location=convention_location,
                created=convention_created,
            )
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except ConventionNotFound as e:
        raise e

def delete_convention(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_id: int
        ) -> str:
    try:
        get_convention(connection, cursor, convention_id)
        try:
            sql_query = "DELETE FROM conventions WHERE id = %s RETURNING *"
            cursor.execute(sql_query, (convention_id,))
            connection.commit()

            return f'Convention deleted with id: {convention_id}'
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except ConventionNotFound as e:
        raise e
