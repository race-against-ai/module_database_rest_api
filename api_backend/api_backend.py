# Copyright (c) 2023 NGITL

import psycopg2
import psycopg2.extras
import json
import logging
from datetime import date

from api_backend.entities import (
    driver,
    drivertime,
    convention
) 

class Backend:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        self.cursor_dict = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        logging.info("Connected to database")
    
    # Utility Functions
    def check_correct_datatypes(self, values: dict, required_datatypes: dict):
        for key, value in values.items():
            if not isinstance(value, required_datatypes[key]):
                raise TypeError(f"Expected {required_datatypes[key]} for {key} but got {type(value)}")

    # Driver Functions
    def get_drivers(self):
        logging.info("Get all drivers was called.")
        return driver.get_all_drivers(self.conn, self.cursor_dict)

    def get_driver(self, driver_id: str):
        logging.info(f"Get driver with id: {driver_id} was called.")
        return driver.get_driver(self.conn, self.cursor_dict, driver_id)
    
    def post_driver(self, driver_name: str, driver_email: str = None):
        logging.info(f"Post driver with name: {driver_name} was called.")
        return driver.post_driver(self.conn, self.cursor, driver_name, driver_email)
    
    def update_driver(self, driver_id: str, values: dict):
        logging.info(f"Update driver with id: {driver_id} was called.")
        return driver.update_driver(self.conn, self.cursor, driver_id=driver_id, values=values)
    
    def delete_driver(self, driver_id: str):
        logging.info(f"Delete driver with id: {driver_id} was called.")
        return driver.delete_driver(self.conn, self.cursor, driver_id)

    # Drivertime Functions
    def get_drivertimes(self):
        logging.info("Get all drivertimes was called.")
        return drivertime.get_drivertimes(self.conn, self.cursor_dict)
    
    def get_drivertime(self, drivertime_id: int):
        logging.info(f"Get drivertime with id: {drivertime_id} was called.")
        return drivertime.get_drivertime(self.conn, self.cursor_dict, drivertime_id)
    
    def post_drivertime(self, driver_id: str, convention_id: int, drivertime_sector1: float, drivertime_sector2: float, drivertime_sector3: float, drivertime_laptime: float):
        logging.info(f"Post drivertime with driver_id: {driver_id} and convention_id: {convention_id} was called.")
        return drivertime.post_drivertime(self.conn, self.cursor, driver_id, convention_id, drivertime_sector1, drivertime_sector2, drivertime_sector3, drivertime_laptime)
    
    def delete_drivertime(self, drivertime_id):
        logging.info(f"Delete drivertime with id: {drivertime_id} was called.")
        return drivertime.delete_drivertime(self.conn, self.cursor, drivertime_id)

    # Convention Functions
    def get_conventions(self):
        logging.info("Get all conventions was called.")
        return convention.get_all_conventions(self.conn, self.cursor_dict)
    
    def get_convention(self, convention_id: int):
        logging.info(f"Get convention with id: {convention_id} was called.")
        return convention.get_convention(self.conn, self.cursor_dict, convention_id)
    
    def post_convention(self, convention_name: str, convention_location: str, convention_date: date):
        logging.info(f"Post convention with name: {convention_name} was called.")
        return convention.post_convention(self.conn, self.cursor, convention_name, convention_location)
    
    def delete_convention(self, convention_id: int):
        logging.info(f"Delete convention with id: {convention_id} was called.")
        return convention.delete_convention(self.conn, self.cursor, convention_id)
    
    def update_convention(self, convention_id: int, values: dict):
        logging.info(f"Update convention with id: {convention_id} was called.")
        return convention.update_convention_name(self.conn, self.cursor, convention_id, values)
    
    
    def close(self):
        self.cursor.close()
        self.cursor_dict.close()
        self.conn.close()
        logging.info("Disconnected from database")


