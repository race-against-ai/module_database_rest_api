import psycopg2


class DriverNotFound(Exception):
    def __init__(self, driver_id: str) -> None:
        self.id = driver_id
        super().__init__(f"Driver not found with ID: {driver_id}")


def post_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_name: str, 
        driver_id: str = None,
        driver_email: str = None
        ) -> dict:
    """Post a new driver to the database."""
    try:    
        # -- Check if values are valid and create SQL Query according to it --
        sql_query = ""
        if driver_name is None:
            raise ValueError("No valid values to post.")
        
        elif driver_id is None and driver_email is None:
            sql_query = "INSERT INTO drivers (name) VALUES (%s) RETURNING *"
            cursor.execute(sql_query, (driver_name,))
        
        elif driver_id is None:
            sql_query = "INSERT INTO drivers (name, email) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_query, (driver_name, driver_email))

        elif driver_email is None:
            sql_query = "INSERT INTO drivers (name, id) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_query, (driver_name, driver_id))
        
        else:
            sql_query = "INSERT INTO drivers (name, id, email) VALUES (%s, %s, %s) RETURNING *"
            cursor.execute(sql_query, (driver_name, driver_id, driver_email))

        driver_id, driver_name, driver_email, driver_created = cursor.fetchone()
        connection.commit()

        return {
            "id": driver_id,
            "name": driver_name,
            "email": driver_email,
            "created": driver_created.strftime("%Y-%m-%d-%H-%M-%S"),
        }
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int
        ) -> dict:
    """Get a driver from the database."""
    try:
        # -- Check if driver exists --
        sql_query = "SELECT * FROM drivers WHERE id = %s"
        cursor.execute(sql_query, (driver_id,))
        try:
            driver_id, driver_name, driver_email, driver_created = cursor.fetchone()

        except TypeError:
            raise DriverNotFound(driver_id)
        
        else:
            connection.commit()

            return {
            "id": driver_id,
            "name": driver_name,
            "email": driver_email,
            "created": driver_created.strftime("%Y-%m-%d-%H-%M-%S"),
        }
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_drivers(
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor,
        sorted_by: str = None,
        order: str = None,
        limit: int = None
        ) -> list:
    """Get all drivers from the database."""
    try: 
        # -- Create SQL Query --
        sql_query = "SELECT * FROM drivers"

        # -- Add sorting, ordering and limiting --
        if sorted_by is not None:
            sql_query += f" ORDER BY {sorted_by}"

            if order is not None and order.lower() in ["asc", "desc"]:
                sql_query += f" {order}"
        
        if limit is not None:
            sql_query += f" LIMIT {limit}"

        cursor.execute(sql_query)

        drivers = []
        for driver_id, driver_name, driver_email, driver_created in cursor.fetchall():
            drivers.append({
            "id": driver_id,
            "name": driver_name,
            "email": driver_email,
            "created": driver_created.strftime("%Y-%m-%d-%H-%M-%S"),
        })
        connection.commit()
        return drivers
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e
    
    except Exception as e:
        connection.rollback()
        raise e

def put_driver(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: str,
        values: dict
        ) -> dict:
    """Update a driver in the database."""
    # -- Check if values are given --
    if not values:
        raise ValueError("No Values given")
    
    try:
        # -- Check if driver exists --
        get_driver(connection, cursor, driver_id)
        # -- Create Key list for given Values --
        key_list = list(values.keys())
        # -- Create SQL Query and adapt it to given Values--
        try:
            if "email" in key_list and "name" in key_list:
                driver_email = values["email"]
                driver_name = values["name"]
                sql_query = "UPDATE drivers SET email = %s, name = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_email, driver_name, driver_id))


            elif "email" in key_list:
                driver_email = values["email"]
                sql_query = "UPDATE drivers SET email = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_email, driver_id))

            
            elif "name" in key_list:
                driver_name = values["name"]
                sql_query = "UPDATE drivers SET name = %s WHERE id = %s RETURNING *"
                cursor.execute(sql_query, (driver_name, driver_id))


            else:
                raise ValueError("No valid values to update.")


            driver_id, driver_name, driver_email, driver_created = cursor.fetchone()
            connection.commit()

            return {
                "id": driver_id,
                "name": driver_name,
                "email": driver_email,
                "created": driver_created.strftime("%Y-%m-%d-%H-%M-%S"),
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
    """Delete a driver from the database."""
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
        


    
