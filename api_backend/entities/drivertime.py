from dataclasses import dataclass

import psycopg2
import uuid

import json
from jsonschema import validate, ValidationError

class DriverTimeNotFound(Exception):
    def __init__(self, *args: object) -> None:
        self.args = args
        super().__init__(f"Drivertime not found: {args}")
@dataclass
class DriverTime:
    driver_id: str
    convention_id: int
    drivertime_id: int
    sector1: float
    sector2: float
    sector3: float
    laptime: float

def post_drivertime(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        driver_id: int, 
        convention_id: int,
        drivertime_sector1: float,
        drivertime_sector2: float,
        drivertime_sector3: float,
        drivertime_laptime: float
        ) -> DriverTime:
    try:    
        sql_query = "INSERT INTO drivertimes (driver, convention, sector1, sector2, sector3, laptime) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"
        cursor.execute(sql_query, (driver_id, convention_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime))

        driver_id, convention_id, drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime = cursor.fetchone()
        connection.commit()

        return DriverTime(
            driver_id=driver_id,
            convention_id=convention_id,
            drivertime_id=drivertime_id,
            sector1=drivertime_sector1,
            sector2=drivertime_sector2,
            sector3=drivertime_sector3,
            laptime=drivertime_laptime
        )
    

    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_drivertime(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor,
        drivertime_id: int
        ) -> DriverTime:
    try:
        sql_query = "SELECT * FROM drivertimes WHERE id = %s"
        cursor.execute(sql_query, (drivertime_id,))
        driver_id, convention_id, drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime = cursor.fetchone()
        if drivertime_id is None: 
            raise DriverTimeNotFound(drivertime_id)
        
        return DriverTime(
            driver_id=driver_id,
            convention_id=convention_id,
            drivertime_id=drivertime_id,
            sector1=drivertime_sector1,
            sector2=drivertime_sector2,
            sector3=drivertime_sector3,
            laptime=drivertime_laptime
        )
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e

def get_all_drivertimes(
        connection: psycopg2.extensions.connection, 
        cursor: psycopg2.extensions.cursor
        ) -> DriverTime:
    try:
        sql_query = "SELECT * FROM drivertimes"
        cursor.execute(sql_query)
        drivertimes = []

        for driver_id, convention_id, drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime in cursor.fetchall():
            drivertimes.append(DriverTime(
                driver_id=driver_id,
                convention_id=convention_id,
                drivertime_id=drivertime_id,
                sector1=drivertime_sector1,
                sector2=drivertime_sector2,
                sector3=drivertime_sector3,
                laptime=drivertime_laptime
            ))
        connection.commit()
        return drivertimes
    
    except psycopg2.Error as e:
        connection.rollback()
        raise e
    
def update_drivertime(
        value, 
        key: str, 
        time_id: int,
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor,
        ) -> DriverTime:
    
    try: 
        get_drivertime(connection, cursor, time_id)
        try: 
            sql_query = f"UPDATE drivertimes SET {key} = %s WHERE id = %s RETURNING *"
            cursor.execute(sql_query, (value, time_id))
            driver_id, convention_id, drivertime_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime = cursor.fetchone()
            connection.commit()
            return DriverTime(
                driver_id=driver_id,
                convention_id=convention_id,
                drivertime_id=drivertime_id,
                sector1=drivertime_sector1,
                sector2=drivertime_sector2,
                sector3=drivertime_sector3,
                laptime=drivertime_laptime
            )

        except psycopg2.Error as e:
            connection.rollback()
            raise e

    except DriverTimeNotFound:
        raise DriverTimeNotFound(time_id)
    
def delete_driver(
        connection: psycopg2.extensions.connection,
        cursor: psycopg2.extensions.cursor,
        driver_id: int
        ) -> None:
    
    try:
        get_drivertime(connection, cursor, driver_id)
        try:
            sql_query = "DELETE FROM drivers WHERE id = %s"
            cursor.execute(sql_query, (driver_id,))
            connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            raise e
    except DriverTimeNotFound:
        raise DriverTimeNotFound(driver_id)
