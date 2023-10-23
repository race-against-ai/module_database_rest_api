from dataclasses import dataclass
from datetime import date

import psycopg2

class DriverNotFound(Exception):
    def __init__(self, *args: object) -> None:
        self.args = args
        super().__init__(f"Driver not found: {args}")

@dataclass
class Driver:
    driver_id: int
    name: str
    email: str | None
    created: date

def post_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_name: str, 
        driver_email: str = None
        ) -> Driver:
    try:    

        sql_query = ""
        if driver_email is None:
            sql_query = "INSERT INTO drivers (name) VALUES (%s) RETURNING *"
            cursor.execute(sql_query, (driver_name,))
            

        else:
            sql_query = "INSERT INTO drivers (name, email) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_query, (driver_name, driver_email))

        driver_id, driver_name, driver_email, driver_created = cursor.fetchone()
        connection.commit()

        return Driver(
            driver_id=driver_id,
            name=driver_name,
            email=driver_email,
            created=driver_created,
        )
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int
        ) -> Driver:
    try:
        sql_query = "SELECT * FROM drivers WHERE id = %s"
        cursor.execute(sql_query, (driver_id,))
        driver_id, driver_name, driver_email, driver_created = cursor.fetchone()

        if driver_id is None:
            raise DriverNotFound(driver_id)
        
        else:
            connection.commit()

            return Driver(
                driver_id=driver_id,
                name=driver_name,
                email=driver_email,
                created=driver_created,
            )
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_drivers(
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor
        ) -> Driver:
    try: 
        sql_query = "SELECT * FROM drivers"
        cursor.execute(sql_query)
        drivers = []
        for driver_id, driver_name, driver_email, driver_created in cursor.fetchall():
            drivers.append(Driver(
                driver_id=driver_id,
                name=driver_name,
                email=driver_email,
                created=driver_created,
            ))
        connection.commit()
        return drivers
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def update_driver_email(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int,
        driver_email: str
        ) -> Driver:
    try:
        get_driver(connection, cursor, driver_id)
        try:
            sql_query = "UPDATE drivers SET email = %s WHERE id = %s RETURNING *"
            cursor.execute(sql_query, (driver_email, driver_id))
            driver_id, driver_name, driver_email, driver_created = cursor.fetchone()
            connection.commit()

            return Driver(
                driver_id=driver_id,
                name=driver_name,
                email=driver_email,
                created=driver_created,
            )
        
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except DriverNotFound:
        raise DriverNotFound(driver_id)

def update_driver_name(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int,
        driver_name: str
        ) -> Driver:
    try:
        get_driver(connection, cursor, driver_id)
        try:
            sql_query = "UPDATE drivers SET name = %s WHERE id = %s RETURNING *"
            cursor.execute(sql_query, (driver_name, driver_id))
            driver_id, driver_name, driver_email, driver_created = cursor.fetchone()
            connection.commit()

            return Driver(
                driver_id=driver_id,
                name=driver_name,
                email=driver_email,
                created=driver_created,
            )
        
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except DriverNotFound:
        raise DriverNotFound(driver_id)
    

def delete_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int
        ) -> str:
        try:
            get_driver(connection, cursor, driver_id)
            try: 
                sql_query = "DELETE FROM drivers WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_id,))
                connection.commit()

                return f'Driver deleted with id: {driver_id}'
            except psycopg2.Error as e:
                connection.rollback()
                raise e
        
        except DriverNotFound:
            raise DriverNotFound(driver_id)
        


    
