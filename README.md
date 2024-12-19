# Database REST API Module 

The RAAI Database REST API provides endpoints for managing and interacting with driver data, drivertimes, and conventions in the database. This API allows for operations such as retrieving, creating, updating, and deleting records. It is designed to support applications that require structured and efficient management of racing-related data.  

## Overview  

- **Driver Management**: Retrieve, create, update, and delete drivers in the database.  
- **Drivertime Management**: Handle drivetime records, including best sector times and lap times.  
- **Convention Management**: Manage conventions with details like name, location, and date.  

The following sections detail the available endpoints, their behavior, and the query parameters that can be used to customize requests.  

<details>  
 <summary>
  <h2>Documentation</h2>
 </summary>  

## Driver  

### Get Drivers  

```
/api/drivers
```  

A successful GET request will have a **200 OK** status and return drivers from the database in JSON format.  

Query parameters can help manage the received data by sorting it by a specified value, arranging it in descending or ascending order, and limiting the number of results.  

#### Query Params  
- **sorted_by***: Sort the received values (type: string).  
- **order***: Specify `asc` or `desc` for result order (type: string).  
- **limit***: Limit the number of received data entries (type: int).  


### Get Driver  

```
/api/driver
```  

A successful GET request will have a **200 OK** status and return a specific driver from the database in JSON format.  

#### Query Params  
- **id**: The UUID of the requested driver (type: string, UUID).  


### Create Driver (POST)  

```
/api/driver
```  

A successful POST request will have a **201 Created** status and return the created driver in JSON format.  

#### Query Params  
- **name**: Name of the new driver (type: string).  
- **id***: Optional hard input for the ID, useful for transferring data from local to online database (type: string, UUID).  
- **email***: Optional email address of the driver (type: string).  


### Update Driver (PUT)  

```
/api/driver
```  

A successful PUT request will have a **200 OK** status and return the updated driver in JSON format.  

#### Query Params  
- **id**: The ID of the driver (type: string, UUID).  
- **name**: The new name of the driver (type: string).  
- **email**: The new email of the driver (type: string).  


### Delete Driver  

```
/api/driver
```  

A successful DELETE request will have a **200 OK** status and return a string containing the deleted driver's ID.  

#### Query Params  
- **id**: The ID of the driver (type: string, UUID).  


## Drivertime  

### Get Drivertimes  

```
/api/drivertimes
```  

A successful GET request will have a **200 OK** status and return drivertimes from the database in JSON format.  

Query parameters can manage received data by sorting, limiting results, or filtering by driver or convention.  

#### Query Params  
- **sorted_by***: Sort the received values (type: string).  
- **order***: Specify `asc` or `desc` for result order (type: string).  
- **limit***: Limit the number of received data entries (type: int).  
- **driver_id***: ID of the driver (type: string, UUID).  
- **convention_id***: ID of the convention (type: int).  


### Get Best Sectors  

```
/api/drivertimes/bestsectors
```  

A successful GET request will have a **200 OK** status and return best sector times, including lap times, in JSON format.  

#### Query Params  
- **driver_id***: ID of the driver (type: string, UUID).  
- **convention_id***: ID of the convention (type: int).  


### Create Drivertime (POST)  

```
/api/drivertime
```  

A successful POST request will have a **201 Created** status and return the created drivertime in JSON format.  

#### Query Params  
- **sector1**: Time for the first sector (type: float).  
- **sector2**: Time for the second sector (type: float).  
- **sector3**: Time for the third sector (type: float).  
- **laptime**: Time for the completed lap (type: float).  
- **driver_id***: Optional ID of the driver (type: string, UUID).  
- **convention_id***: Optional ID of the convention (type: int).  


### Delete Drivertime  

```
/api/drivertime
```  

A successful DELETE request will have a **200 OK** status and return a string containing the deleted drivertime's ID.  

#### Query Params  
- **id**: ID of the drivertime (type: int).  


## Convention  

### Get Conventions  

```
/api/conventions
```  

A successful GET request will have a **200 OK** status and return conventions from the database in JSON format.  

Query parameters can help manage received data by sorting, limiting results, or specifying order.  

#### Query Params  
- **sorted_by***: Sort the received values (type: string).  
- **order***: Specify `asc` or `desc` for result order (type: string).  
- **limit***: Limit the number of received data entries (type: int).  
 

### Get Convention  

```
/api/convention
```  

A successful GET request will have a **200 OK** status and return the requested convention in JSON format.  

#### Query Params  
- **id**: ID of the convention (type: int).  


### Create Convention (POST)  

```
/api/convention
```  

A successful POST request will have a **201 Created** status and return the created convention in JSON format.  

#### Query Params  
- **name**: Name of the convention (type: string).  
- **location***: Optional location of the convention (type: string).  
- **date***: Optional date of the convention (type: string).  


### Update Convention (PUT)  

```
/api/convention
```  

A successful PUT request will have a **200 OK** status and return the updated convention in JSON format.  

#### Query Params  
- **id**: ID of the convention (type: int).  
- **name***: New name of the convention (type: string).  
- **location***: New location of the convention (type: string).  
- **date***: New date of the convention (type: string).  


### Delete Convention  

```
/api/convention
```  

A successful DELETE request will have a **200 OK** status and return a string containing the deleted convention's ID.  

#### Query Params  
- **id**: ID of the convention (type: int).  

</details> 
