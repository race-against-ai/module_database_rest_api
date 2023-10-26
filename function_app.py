import azure.functions as func
import logging
import json
import os
import psycopg2.errors
from datetime import date, datetime
import uuid

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

# Driver Specific Functions

@app.route(route="drivers", methods=["GET"])
def drivers_get_all(req: func.HttpRequest) -> func.HttpResponse:

    try:
        sorted_by = req.params.get("sorted_by")
        order = req.params.get("order")
        limit = req.params.get("limit")
        try:
            limit = int(limit)
        except TypeError:
            return func.HttpResponse(
                "Invalid limit. Expected integer.",
                status_code=400
            )
        result = json.dumps(backend.get_drivers(sorted_by=sorted_by, order= order, limit=limit))
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

@app.route(route="driver", methods=["GET"])
def drivers_get_driver(req: func.HttpRequest) -> func.HttpResponse:
    try:
        driver_id = req.params.get("id")
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
def drivers_post_driver(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")
    email = req.params.get("email")
    driver_id = req.params.get("id")
    logging.info(f"Name: {name}, Email: {email}")
    if not name:
        return func.HttpResponse(
            f"No Valid Name Given.",
            status_code=400
            )
    if driver_id:
        try: 
            if not driver_id == str(uuid.UUID(driver_id)):
                return func.HttpResponse(
                    f"Invalid UUID: {driver_id}",
                    status_code=400
                    )
        except ValueError:
            return func.HttpResponse(
                f"Invalid UUID: {driver_id}",
                status_code=400
                )
    try:
        result = backend.post_driver(name, driver_id, email)
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


@app.route(route="driver", methods=["PUT"])
def drivers_update_driver(req: func.HttpRequest) -> func.HttpResponse:
    try:
        driver_id = req.params.get("id")
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


@app.route(route="driver", methods=["DELETE"])
def drivers_delete_driver(req: func.HttpRequest) -> func.HttpResponse:
    try:
        driver_id = req.params.get("id")
        if not driver_id:
            return func.HttpResponse(
                "No Driver ID provided.",
                status_code=400
            )
        result = backend.delete_driver(driver_id)
        return func.HttpResponse(
            f"Driver with id: {driver_id} deleted successfully.",
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
            "Could not delete driver.",
            status_code=400
        )

# Convention Specific Functions

@app.route(route="conventions", methods=["GET"])
def conventions_get_all(req: func.HttpRequest) -> func.HttpResponse:
    try: 
        sorted_by = req.params.get("sorted_by")
        order = req.params.get("order")
        limit = req.params.get("limit")
        if limit:
            try:
                limit = int(limit)
            except TypeError:
                return func.HttpResponse(
                    "Invalid limit. Expected integer.",
                    status_code=400
                )
        result = json.dumps(backend.get_conventions(sorted_by=sorted_by, order= order, limit=limit))

        return func.HttpResponse(
            result,
            status_code=200
            )
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get all conventions.",
            status_code=400
        )

@app.route(route="convention", methods=["GET"])
def conventions_get_convention(req: func.HttpRequest) -> func.HttpResponse:
    try:
        conv_id = req.params.get("id")
        if not conv_id:
            return func.HttpResponse(
                "No Convention ID provided.",
                status_code=400
            )
        convention = backend.get_convention(conv_id)
        return func.HttpResponse(
            json.dumps(convention),
            status_code=200
            )
    
    except ConventionNotFound as e:
        return func.HttpResponse(
            f"{e}",
            status_code=404
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get convention.",
            status_code=400
        )
    

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
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not create convention.",
            status_code=400
        )

@app.route(route="convention", methods=["PUT"])
def conventions_update_convention(req: func.HttpRequest) -> func.HttpResponse:
    try: 
        convention_id = req.params.get("id")
        new_name = req.params.get("name")
        new_location = req.params.get("location")
        date = req.params.get("date")
        values = {}
        if new_name:
            values["name"] = new_name
        if new_location:
            values["location"] = new_location
        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                values["date"] = date
            except ValueError:
                return func.HttpResponse(
                    f"Invalid date format. Expected format: YYYY-MM-DD",
                    status_code=400
                    )
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


@app.route(route="convention", methods=["DELETE"])
def conventions_delete_convention(req: func.HttpRequest) -> func.HttpResponse:
    try:
        convention_id = req.params.get("id")
        if not convention_id:
            return func.HttpResponse(
                "No Convention ID provided.",
                status_code=400
            )
        result = backend.delete_convention(convention_id)
        return func.HttpResponse(
            f"Convention with id: {convention_id} deleted successfully.",
            status_code=200
            )
    except ConventionNotFound as e:
        return func.HttpResponse(
            f"{e}",
            status_code=404
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not delete convention.",
            status_code=400
        )


# Drivertimes Specific Functions

@app.route(route="drivertimes", methods=["GET"])
def drivertimes_get_all(req: func.HttpRequest) -> func.HttpResponse:
    try:
        sorted_by = req.params.get("sorted_by")
        order = req.params.get("order")
        limit = req.params.get("limit")
        driver = req.params.get("driver_id")
        convention = req.params.get("convention_id")
        if limit:
            try:
                limit = int(limit)
            except TypeError:
                return func.HttpResponse(
                    "Invalid limit. Expected integer.",
                    status_code=400
                )
        
        result = json.dumps(backend.get_drivertimes(sorted_by=sorted_by, order=order, limit=limit, driver_id=driver, convention_id=convention))
        logging.info(result)
        return func.HttpResponse(
            result,
            status_code=200
            )

    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get all drivertimes.",
            status_code=400
        )

@app.route(route="drivertimes/bestsectors", methods=["GET"])
def drivertimes_get_best_sectors(req: func.HttpRequest) -> func.HttpResponse:
    try:
        driver = req.params.get("driver_id")
        convention = req.params.get("convention_id")

        result = json.dumps(backend.get_drivertimes_best_sectors(driver_id=driver, convention_id=convention))

        return func.HttpResponse(
            result,
            status_code=200
            )
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get best sectors.",
            status_code=400
        )

@app.route(route="drivertime", methods=["GET"])
def drivertimes_get_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    time_id = req.params.get("id")
    if not time_id:
        return func.HttpResponse(
            "No Drivertime ID provided.",
            status_code=400
        )
    try:
        drivertime = backend.get_drivertime(time_id)
        return func.HttpResponse(
            json.dumps(drivertime),
            status_code=200
            )
    except DriverTimeNotFound as e:
        return func.HttpResponse(
            f"{e}",
            status_code=404
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not get drivertime.",
            status_code=400
        )


@app.route(route="drivertime", methods=["POST"])
def drivertimes_create_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    sector1 = req.params.get("sector1")
    sector2 = req.params.get("sector2")
    sector3 = req.params.get("sector3")
    laptime = req.params.get("laptime")
    driver_id = req.params.get("driver_id")
    convention_id = req.params.get("convention_id")
    if not sector1 and not sector2 and not sector3 and not laptime:
        return func.HttpResponse(
            f"No Valid Data Given.",
            status_code=400
            )
    if not driver_id:
        logging.info("No driver_id given. using Dummy Driver.")
        driver_id = "4823662a-29c5-47d7-bdba-68baa2825990"
    if not convention_id:
        logging.info("No convention_id given. using Dummy Convention.")
        convention_id = 1
    try:
        result = backend.post_drivertime(driver_id, convention_id, sector1, sector2, sector3, laptime)
        return func.HttpResponse(
            f"Drivertime with driver_id: {driver_id} created successfully.",
            status_code=201
            )
    
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            f"Drivertime with driver_id: {driver_id} and convention_id: {convention_id} could not be created.",
            status_code=400
            )

@app.route(route="drivertime", methods=["DELETE"])
def drivertimes_delete_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    drivertime_id = req.params.get("id")
    if not drivertime_id:
        return func.HttpResponse(
            "No Drivertime ID provided.",
            status_code=400
        )
    try:
        result = backend.delete_drivertime(drivertime_id)
        return func.HttpResponse(
            f"Drivertime with id: {drivertime_id} deleted successfully.",
            status_code=200
            )
    except DriverTimeNotFound as e:
        return func.HttpResponse(
            f"{e}",
            status_code=404
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "Could not delete drivertime.",
            status_code=400
        )
    

