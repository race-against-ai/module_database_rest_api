from pathlib import Path

SQL_DIR_PATH = Path(__file__).parent / "sql_queries"

def read_query(filename: str) -> str:
    return open(SQL_DIR_PATH / filename, "r").read()

QUERY_GET_ALL_DRIVERS = read_query("drivers/get_all_drivers.sql")
QUERY_GET_DRIVER = read_query("drivers/drivers_get.sql")
QUERY_CREATE_DRIVER = read_query("drivers/drivers_create.sql")
QUERY_UPDATE_DRIVER = read_query("drivers/drivers_update.sql")
QUERY_DELETE_DRIVER = read_query("drivers/drivers_delete.sql")

QUERY_GET_ALL_CONVENTIONS = read_query("conventions/get_all_conventions.sql")
QUERY_GET_CONVENTION = read_query("conventions/conventions_get.sql")
QUERY_CREATE_CONVENTION = read_query("conventions/conventions_create.sql")
QUERY_UPDATE_CONVENTION = read_query("conventions/conventions_update.sql")
QUERY_DELETE_CONVENTION = read_query("conventions/conventions_delete.sql")

QUERY_GET_ALL_DRIVERTIMES = read_query("drivertimes/get_all_drivertimes.sql")
QUERY_GET_DRIVERTIME = read_query("drivertimes/drivertimes_get.sql")
QUERY_CREATE_DRIVERTIME = read_query("drivertimes/drivertimes_create.sql")
QUERY_UPDATE_DRIVERTIME = read_query("drivertimes/drivertimes_update.sql")
QUERY_DELETE_DRIVERTIME = read_query("drivertimes/drivertimes_delete.sql")


