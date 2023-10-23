import azure.functions as func
import logging
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

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
    logging.info("Get all drivers was called.")
    return func.HttpResponse("Function should return all drivers.")

@app.route(route="drivers/{id}", methods=["GET"])
def drivers_get_driver(req: func.HttpRequest) -> func.HttpResponse:
    driver_id = req.route_params.get("id")
    return func.HttpResponse(f"return Driver with name: {driver_id}")

@app.route(route="drivers/{name}", methods=["POST"])
def drivers_create_driver(req: func.HttpRequest) -> func.HttpResponse:
    name = req.route_params.get("name")
    return func.HttpResponse(f"Driver with name: {name} created successfully.")


@app.route(route="drivers/{id}", methods=["PUT"])
def drivers_update_driver(req: func.HttpRequest) -> func.HttpResponse:
    driver_id = req.route_params.get("id")
    data = req.get_json()
    return func.HttpResponse(f"Driver with id: {driver_id} updated with data {data} successfully.")

@app.route(route="drivers/{id}", methods=["DELETE"])
def drivers_delete_driver(req: func.HttpRequest) -> func.HttpResponse:
    driver_id = req.route_params.get("id")
    return func.HttpResponse(f"Driver with id: {driver_id} deleted successfully.")


# Convention Specific Functions

@app.route(route="conventions", methods=["GET"])
def conventions_get_all(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Function should return all conventions.")

@app.route(route="conventions/{id}", methods=["GET"])
def conventions_get_convention(req: func.HttpRequest) -> func.HttpResponse:
    conv_id = req.route_params.get("id")
    return func.HttpResponse(f"return Convention with the ID: {conv_id}")

@app.route(route="conventions/{name}", methods=["POST"])
def conventions_create_convention(req: func.HttpRequest) -> func.HttpResponse:
    name = req.route_params.get("name")
    return func.HttpResponse(f"Convention with name: {name} created successfully.")

@app.route(route="conventions/{id}", methods=["PUT"])
def conventions_update_convention(req: func.HttpRequest) -> func.HttpResponse:
    convention_id = req.route_params.get("id")
    data = req.get_json()
    return func.HttpResponse(f"Convention with id: {convention_id} updated with data {data} successfully.")

@app.route(route="conventions/{id}", methods=["DELETE"])
def conventions_delete_convention(req: func.HttpRequest) -> func.HttpResponse:
    convention_id = req.route_params.get("id")
    return func.HttpResponse(f"Convention with id: {convention_id} deleted successfully.")


# Drivertimes Specific Functions

@app.route(route="drivertimes", methods=["GET"])
def drivertimes_get_all(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Function should return all drivertimes.")

@app.route(route="drivertimes/{name}", methods=["GET"])
def drivertimes_get_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    name = req.route_params.get("name")
    return func.HttpResponse(f"return Drivertime with name: {name}")

@app.route(route="drivertimes/{name}", methods=["POST"])
def drivertimes_create_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    name = req.route_params.get("name")
    return func.HttpResponse(f"Drivertime with name: {name} created successfully.")

@app.route(route="drivertimes/{id}", methods=["PUT"])
def drivertimes_update_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    drivertime_id = req.route_params.get("id")
    data = req.get_json()
    return func.HttpResponse(f"Drivertime with id: {drivertime_id} updated with data {data} successfully.")

@app.route(route="drivertimes/{id}", methods=["DELETE"])
def drivertimes_delete_drivertime(req: func.HttpRequest) -> func.HttpResponse:
    drivertime_id = req.route_params.get("id")
    return func.HttpResponse(f"Drivertime with id: {drivertime_id} deleted successfully.")


