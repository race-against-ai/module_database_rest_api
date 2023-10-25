from dataclasses import dataclass
from datetime import date

import psycopg2

class DriverNotFound(Exception):
    def __init__(self, driver_id: str) -> None:
        self.id = driver_id
        super().__init__(f"Driver not found with ID: {driver_id}")



def post_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_name: str, 
        driver_email: str = None
        ) -> dict:
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

        return {
            "driver_id": driver_id,
            "name": driver_name,
            "email": driver_email,
            "created": driver_created.strftime("%Y-%m-%d-%h-%m-%s"),
        }
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int
        ) -> dict:
    try:
        sql_query = "SELECT * FROM drivers WHERE id = %s"
        cursor.execute(sql_query, (driver_id,))
        try:
            driver_id, driver_name, driver_email, driver_created = cursor.fetchone()

        except TypeError:
            raise DriverNotFound(driver_id)
        
        else:
            connection.commit()

            return {
            "driver_id": driver_id,
            "name": driver_name,
            "email": driver_email,
            "created": driver_created.strftime("%Y-%m-%d-%h-%m-%s"),
        }
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_drivers(
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor
        ) -> list:
    try: 
        sql_query = "SELECT * FROM drivers"
        cursor.execute(sql_query)
        drivers = []
        for driver_id, driver_name, driver_email, driver_created in cursor.fetchall():
            drivers.append({
            "driver_id": driver_id,
            "name": driver_name,
            "email": driver_email,
            "created": driver_created.strftime("%Y-%m-%d-%h-%m-%s"),
        })
        connection.commit()
        return drivers
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def update_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: str,
        values: dict
        ) -> dict:
    if not values:
        raise ValueError("No valid values to update.")
    try:
        get_driver(connection, cursor, driver_id)
        try:
            if "email" in values.keys() and "name" in values.keys():
                driver_email = values["email"]
                driver_name = values["name"]
                sql_query = "UPDATE drivers SET email = %s, name = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_email, driver_name, driver_id))


            elif "email" in values.keys():
                driver_email = values["email"]
                sql_query = "UPDATE drivers SET email = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_email, driver_id))

            
            elif "name" in values.keys():
                driver_name = values["name"]
                sql_query = "UPDATE drivers SET name = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_name, driver_id))


            else:
                raise ValueError("No valid values to update.")


            driver_id, driver_name, driver_email, driver_created = cursor.fetchone()
            connection.commit()

            return {
                "driver_id": driver_id,
                "name": driver_name,
                "email": driver_email,
                "created": driver_created.strftime("%Y-%m-%d-%h-%m-%s"),
            }
        
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
        


    
