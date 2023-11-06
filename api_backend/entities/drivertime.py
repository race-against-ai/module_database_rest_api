import psycopg2
import logging
import uuid

class DriverTimeNotFound(Exception):
    def __init__(self, *args: object) -> None:
        self.args = args
        super().__init__(f"Drivertime not found: {args}")

def post_drivertime(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int, 
        convention_id: int,
        drivertime_sector1: float,
        drivertime_sector2: float,
        drivertime_sector3: float,
        drivertime_laptime: float
        ) -> dict:
    """Post a new drivertime to the database."""
    try:
        sql_query = "INSERT INTO drivertimes (driver, convention, sector1, sector2, sector3, laptime) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"
        cursor.execute(sql_query, (driver_id, convention_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime))

        driver_id, convention_id, drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime = cursor.fetchone()
        connection.commit()

        return {
            "drivertime_id": drivertime_id,
            "sector1": drivertime_sector1,
            "sector2": drivertime_sector2,
            "sector3": drivertime_sector3,
            "laptime": drivertime_laptime,
            "driver_id": driver_id,
            "convention_id": convention_id
        }
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_drivertime(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        drivertime_id: int
        ) -> dict:
    """Get a drivertime from the database."""
    try:
        sql_query = "SELECT * FROM drivertimes WHERE id = %s"
        cursor.execute(sql_query, (drivertime_id,))
        driver_id, convention_id, drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime = cursor.fetchone()
        if drivertime_id is None: 
            raise DriverTimeNotFound(drivertime_id)
        
        return {
            "drivertime_id": drivertime_id,
            "sector1": drivertime_sector1,
            "sector2": drivertime_sector2,
            "sector3": drivertime_sector3,
            "laptime": drivertime_laptime,
            "driver_id": driver_id,
            "convention_id": convention_id
        }
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_drivertimes(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        sorted_by: str = None,
        order: str = None,
        limit: int = None,
        driver_id: str = None,
        convention_id: int = None
        ) -> list:
    """Get all drivertimes from the database."""
    try:
        def expand_sql_query(query ,sorted_by, order, limit) -> str:
            if sorted_by is not None:
                query += f" ORDER BY {sorted_by}"
                if order is not None:
                    query += f" {order}"
            
            if limit is not None:
                query += f" LIMIT {limit}"

            return query

        if driver_id is None and convention_id is None:
            sql_query = "SELECT * FROM drivertimes"

            sql_query = expand_sql_query(sql_query, sorted_by, order, limit)
            cursor.execute(sql_query)
        
        elif driver_id is not None and convention_id is None:
            sql_query = "SELECT * FROM drivertimes WHERE driver = %s"

            sql_query = expand_sql_query(sql_query, sorted_by, order, limit)
            cursor.execute(sql_query, (driver_id,))
        
        elif driver_id is None and convention_id is not None:
            sql_query = "SELECT * FROM drivertimes WHERE convention = %s"

            sql_query = expand_sql_query(sql_query, sorted_by, order, limit)
            cursor.execute(sql_query, (convention_id,))

        elif driver_id is not None and convention_id is not None:
            sql_query = "SELECT * FROM drivertimes WHERE driver = %s AND convention = %s"

            sql_query = expand_sql_query(sql_query, sorted_by, order, limit)
            cursor.execute(sql_query, (driver_id, convention_id))

        drivertimes = []

        for drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime, driver_id, convention_id in cursor.fetchall():
            drivertimes.append({
            "drivertime_id": drivertime_id,
            "sector1": drivertime_sector1,
            "sector2": drivertime_sector2,
            "sector3": drivertime_sector3,
            "laptime": drivertime_laptime,
            "driver_id": driver_id,
            "convention_id": convention_id
        })
        connection.commit()
        return drivertimes
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_best_sectors(
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor,
        driver_id: str = None,
        convention_id: int = None
        ) -> dict:
    """Get the best sectors for a driver or convention."""
    try:
        sql_query = """
            SELECT 
            MIN(sector1) AS best_sector1,
            MIN(sector2) AS best_sector2,
            MIN(sector3) AS best_sector3,
            MIN(laptime) AS best_laptime
            FROM drivertimes
            """
        if driver_id is None and convention_id is None:
            cursor.execute(sql_query)

        else:
            if driver_id is not None and convention_id is None:
                sql_query += " WHERE driver = %s"
                cursor.execute(sql_query, (driver_id,))

            elif driver_id is None and convention_id is not None:
                sql_query += " WHERE convention = %s"
                cursor.execute(sql_query, (convention_id,))
            
            else:
                sql_query += " WHERE driver = %s AND convention = %s"
                cursor.execute(sql_query, (driver_id, convention_id))
            
    
        best_sector1, best_sector2, best_sector3, best_laptime = cursor.fetchone()
        connection.commit()
        return {
            "sector_1_best_time": best_sector1,
            "sector_2_best_time": best_sector2,
            "sector_3_best_time": best_sector3,
            "lap_best_time": best_laptime
        }
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def delete_drivertime(
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor,
        drivertime_id: int
        ) -> None:
    """Delete a drivertime from the database."""
    try:
        get_drivertime(connection, cursor, drivertime_id)
        try:
            sql_query = "DELETE FROM drivertimes WHERE id = %s"
            cursor.execute(sql_query, (drivertime_id,))
            connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except DriverTimeNotFound:
        raise DriverTimeNotFound(drivertime_id)
