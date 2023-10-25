import azure.functions as func
import logging
import json
import os
import psycopg2.errors
from datetime import date, datetime

from typing import Callable
from api_backend.api_backend import Backend
from api_backend.entities.driver import DriverNotFound
from api_backend.entities.drivertime import DriverTimeNotFound
from api_backend.entities.convention import ConventionNotFound

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

required_env_vars = ["PORT", "HOST", "USER", "PASSWORD", "DATABASE"]
for env_var in required_env_vars:
    if env_var not in os.environ:
        raise Exception(f"Environment variable {env_var} not found.")

PORT = os.environ["PORT"]
HOST = os.environ["HOST"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DATABASE = os.environ["DATABASE"]

backend = Backend(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# Driver Specific Functions

@app.route(route="drivers", methods=["GET"])
def drivers_get_all(req: func.HttpRequest) -> func.HttpResponse:

    try:
        result = json.dumps(backend.get_drivers())
        logging.info(result)
        return func.HttpResponse(
            result,
            status_code=200
            )

    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get all drivers.",
            status_code=400
        )

@app.route(route="driver/{id}", methods=["GET"])
def drivers_get_driver(req: func.HttpRequest) -> func.HttpResponse:
    try:
        driver_id = req.route_params.get("id")
        driver = backend.get_driver(driver_id)
        if not driver_id:
            return func.HttpResponse(
                "No Driver ID provided.",
                status_code=400
            )

        return func.HttpResponse(
            json.dumps(driver),
            status_code=200
            )
    
    except DriverNotFound as e:
        return func.HttpResponse(
            f"{e}",
            status_code=404
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get driver.",
            status_code=400
        )

@app.route(route="driver", methods=["POST"])
def drivers_create_driver(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")
    email = req.params.get("email")
    logging.info(f"Name: {name}, Email: {email}")
    if not name:
        return func.HttpResponse(
            f"No Valid Name Given.",
            status_code=400
            )
    try:
        result = backend.post_driver(name, email)
        return func.HttpResponse(
            f"Driver with name: {name} created successfully.",
            status_code=201
            )
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            f"Driver with name: {name} could not be created.",
            status_code=400
            )


@app.route(route="driver/{id}/update", methods=["PUT"])
def drivers_update_driver(req: func.HttpRequest) -> func.HttpResponse:
    try:
        driver_id = req.route_params.get("id")
        new_name = req.params.get("name")
        new_email = req.params.get("email")
        values = {}
        if new_name:
            values["name"] = new_name
        if new_email:
            values["email"] = new_email
        result = backend.update_driver(driver_id=driver_id, values=values)
        return func.HttpResponse(f"Driver with id: {driver_id} updated with data {result} successfully.")
    
    except DriverNotFound as e:
        return func.HttpResponse(
            f"Driver not found: {e.args}",
            status_code=404
        )

    except ValueError as e:
        return func.HttpResponse(
            f"Invalid data: {e.args}",
            status_code=400
        )
    
    except psycopg2.errors.CheckViolation as e:
        return func.HttpResponse(
            f"Invalid data: {e.args}",
            status_code=400
        )
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not update driver.",
            status_code=400
        )


@app.route(route="driver/{id}/delete", methods=["DELETE"])
def drivers_delete_driver(req: func.HttpRequest) -> func.HttpResponse:
    driver_id = req.route_params.get("id")
    return func.HttpResponse(f"Driver with id: {driver_id} deleted successfully.")


# Convention Specific Functions

@app.route(route="conventions", methods=["GET"])
def conventions_get_all(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Function should return all conventions.")

@app.route(route="convention/{id}", methods=["GET"])
def conventions_get_convention(req: func.HttpRequest) -> func.HttpResponse:
    conv_id = req.route_params.get("id")
    return func.HttpResponse(f"return Convention with the ID: {conv_id}")

@app.route(route="convention", methods=["POST"])
def conventions_create_convention(req: func.HttpRequest) -> func.HttpResponse:
    try:
        name = req.params.get("name")
        location = req.params.get("location")
        date = req.params.get("date")
        if date:
            try: 
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return func.HttpResponse(
                    f"Invalid date format. Expected format: YYYY-MM-DD",
                    status_code=400
                    )
        if not name:
            return func.HttpResponse(
                f"No Valid Name Given.",
                status_code=400
                )
        try:
            result = backend.post_convention(name, location, date)
            return func.HttpResponse(
                f"Convention with name: {name} created successfully.",
                status_code=201
                )
        
        except:
            return func.HttpResponse(
                f"Convention with name: {name} could not be created.",
                status_code=400
                )
    
    except ValueError:
        logging.info("No JSON data found.")

@app.route(route="convention/{id}/update", methods=["PUT"])
def conventions_update_convention(req: func.HttpRequest) -> func.HttpResponse:
    try: 
        convention_id = req.route_params.get("id")
        new_name = req.params.get("name")
        new_location = req.params.get("location")
        values = {}
        if new_name:
            values["name"] = new_name
        if new_location:
            values["location"] = new_location
        result = backend.update_convention(convention_id=convention_id, values=values)
        return func.HttpResponse(
            f"Convention with id: {convention_id} updated with data {values} successfully.",
            status_code=200
        )
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not update convention.",
            status_code=400
        )


@app.route(route="convention/{id}", methods=["DELETE"])
def conventions_delete_convention(req: func.HttpRequest) -> func.HttpResponse:
    convention_id = req.route_params.get("id")
    return func.HttpResponse(f"Convention with id: {convention_id} deleted successfully.")


# Drivertimes Specific Functions

@app.route(route="drivertimes", methods=["GET"])
def drivertimes_get_all(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Function should return all drivertimes.")

@app.route(route="drivertime/{name}", methods=["GET"])
def drivertimes_get_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    name = req.route_params.get("name")
    return func.HttpResponse(f"return Drivertime with name: {name}")

@app.route(route="drivertime", methods=["POST"])
def drivertimes_create_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")
    return func.HttpResponse(f"Drivertime with name: {name} created successfully.")

@app.route(route="drivertime/{id}", methods=["DELETE"])
def drivertimes_delete_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    drivertime_id = req.route_params.get("id")
    return func.HttpResponse(f"Drivertime with id: {drivertime_id} deleted successfully.")


