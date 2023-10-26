from datetime import date

import psycopg2

class ConventionNotFound(Exception):
    def __init__(self, con_id) -> None:
        self.args = con_id
        super().__init__(f"Driver not found: {self.args}")

def post_convention(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_name: str, 
        convention_location: str = None,
        convetion_date: date = None
        ) -> dict:
    try:    

        sql_query = ""

        if convention_name is None:
            raise ValueError("No valid values to update.")

        elif convention_location is None and convention_date is None:
            sql_query = "INSERT INTO conventions (name) VALUES (%s) RETURNING *"
            cursor.execute(sql_query, (convention_name,))
        
        elif convention_location is None:
            sql_query = "INSERT INTO conventions (name, date) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_query, (convention_name, convetion_date))
        
        elif convetion_date is None:
            sql_query = "INSERT INTO conventions (name, location) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_query, (convention_name, convention_location))
        
        else:
            sql_query = "INSERT INTO conventions (name, location, date) VALUES (%s, %s, %s) RETURNING *"
            cursor.execute(sql_query, (convention_name, convention_location, convetion_date))


        convention_id, convention_name, convention_location, convention_date = cursor.fetchone()
        connection.commit()

        return {
            "convention_id": convention_id,
            "name": convention_name,
            "location": convention_location,
            "created": convention_date.strftime("%Y-%m-%d"),
        }
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

    except Exception as e:
        raise e
    
def get_convention(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_id: int
        ) -> dict:
    try:
        sql_query = "SELECT * FROM conventions WHERE id = %s"
        cursor.execute(sql_query, (convention_id,))
        convention_id, convention_name, convention_location, convention_created = cursor.fetchone()
        if convention_id is None: 
            raise ConventionNotFound(convention_id)
        else:
            connection.commit()
            if convention_created is not None:
                convention_created = convention_created.strftime("%Y-%m-%d")
            return {
                "convention_id": convention_id,
                "name": convention_name,
                "location": convention_location,
                "created": convention_created,
            }
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_conventions(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        sorted_by: str = None,
        order: str = None,
        limit: int = None
        ) -> dict:
    try:
        sql_query = "SELECT * FROM conventions"

        if sorted_by is not None:
            sql_query += f" ORDER BY {sorted_by}"
            if order is not None:
                sql_query += f" {order}"
        
        if limit is not None:
            sql_query += f" LIMIT {limit}"

        cursor.execute(sql_query)
        conventions = []
        for convention_id, convention_name, convention_location, convention_created in cursor.fetchall():
            if convention_created is not None:
                convention_created = convention_created.strftime("%Y-%m-%d")
            conventions.append({
                "convention_id": convention_id,
                "name": convention_name,
                "location": convention_location,
                "created": convention_created,
            })
        connection.commit()
        return conventions
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def update_convention(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        convention_id: int,
        values: dict
        ) -> dict:
    if not values:
        raise ValueError("No valid values to update.")

    try:
        get_convention(connection, cursor, convention_id)
        key_list = list(values.keys())
        try:
            if "name" in key_list and "location" in key_list and "date" in key_list:
                sql_query = "UPDATE conventions SET name = %s, location = %s, date = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["name"], values["location"], values["date"], convention_id))
            
            elif "name" in key_list and "location" in key_list:
                sql_query = "UPDATE conventions SET name = %s, location = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["name"], values["location"], convention_id))
            
            elif "name" in key_list and "date" in key_list:
                sql_query = "UPDATE conventions SET name = %s, date = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["name"], values["date"], convention_id))
            
            elif "location" in key_list and "date" in key_list:
                sql_query = "UPDATE conventions SET location = %s, date = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["location"], values["date"], convention_id))
            
            elif "name" in key_list:
                sql_query = "UPDATE conventions SET name = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["name"], convention_id))
            
            elif "location" in key_list:
                sql_query = "UPDATE conventions SET location = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["location"], convention_id))
            
            elif "date" in key_list:
                sql_query = "UPDATE conventions SET date = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (values["date"], convention_id))

            else:
                raise ValueError("No valid values to update.")
            
            convention_id, convention_name, convention_location, convention_created = cursor.fetchone()
            connection.commit()
            
            return {
                "convention_id": convention_id,
                "name": convention_name,
                "location": convention_location,
                "created": convention_created.strftime("%Y-%m-%d"),
            }

        except psycopg2.Error as e:
            connection.rollback()
            raise e
        
    except ConventionNotFound as e:
        raise e(convention_id)

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
        raise e(convention_id)

    except Exception as e:
        raise e
