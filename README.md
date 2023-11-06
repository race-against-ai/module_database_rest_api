# RAAI Database Rest API
## Documentation

Params marked with a * are optional 

---

## Driver
### Get Drivers

```
/api/drivers
```
A successful GET request will have a **200 ok** status and returns the Drivers from the Database
in a Json Format

Query Params can help in managing received Data with sorting them by a specified value, having it Descending or Ascending and limit the amount of results

#### Query Params
 - sorted_by*:      sort the received values : string
 - order*:          asc or desc for result order : string
 - limit*:          limit the amount of received Data : int


### GET Driver
```
/api/driver
```
A successful GET request will have a **200 ok** status and returns the Driver from the Database
in a Json Format


#### Query Params

 - id:              The UUID of the wanted driver: string(UUID)

### POST
```
/api/driver
```
A succesfull POST request will have a **201 created** status and returns the created Driver
in a Json format

#### Query Params

 - name:            Name of the new driver: string
 - id*:             Hard Input for the ID, used for transfering from Local to Online Database: string(UUID)
 - email*:          Email Address of the Driver: string

### PUT Driver
```
/api/driver
```
A succesfull PUT request will have a **200 ok** status and returns the changed Driver 
in a Json format

#### Query Params

 - id:              The ID of the Driver: string(UUID)
 - name:            The new Name of the Driver: string
 - email:           The new Email of the Driver: string

### DEL Driver
```
/api/driver
```
A succesfull DEL request will have a **200 ok** status and returns a String with the deleted Driver ID

#### Query Params

 - id:              The ID of the Driver: string(UUID)


---

## Drivertime


### Get Drivertimes
```
/api/drivertimes
```

A successful GET request from /api/drivers will have a **200 ok** status and returns the Drivertimes from the Database
in a Json Format

Query Params can help in managing received Data with sorting them by a specified value, having it Descending or Ascending and limit the amount of results
Also receive Drivertimes for a specific Driver or Convention

##### Query Params
 - sorted_by*:      sort the received values: string
 - order*:          asc or desc for result order: string
 - limit*:          limit the amount of received Data: int
 - driver_id*:      ID the Driver: string(UUID)
 - convention_id*:  ID of the Convention: int

### GET Best Sectors
```
/api/drivertimes/bestsectors
```
A successful GET request from /api/drivers will have a **200 ok** status and returns the Best Sectors including Laptime 
from the Database in a Json Format

Query Params can help in managing received Data by receiving the best Sectors for a Driver and or Convention

##### Query Params

 - driver_id*:      ID the Driver: string(UUID)
 - convention_id*:  ID of the Convention: int



#### GET
```
/api/drivertime
```
A successful GET request will have a **200 ok** status and returns the Drivertime from the Database
in a Json Format


##### Query Params

 - id:              ID of the Drivertime: int

#### POST
```
/api/drivertime
```
A succesfull POST request will have a **201 created** status and returns the created Driver
in a Json format

##### Query Params

 - sector1:         Time for the first Sector: float
 - sector2:         Time for the second Sector: float
 - sector3:         Time for the third Sector: float
 - laptime:         Time for the finished Lap: float
 - driver_id*:      ID of the Driver: string(UUID)
 - convention_id*:  ID of the Convention

#### DEL
```
/api/drivertime
```
A succesfull DEL request will have a **200 ok** status and returns a String with the deleted Drivertime ID

##### Query Params

 - id:              The ID of the Drivertime

---

## Convention

### GET Conventions

```
/api/conventions
```
A successful GET request will have a **200 ok** status and returns the Conventions from the Database
in a Json Format

Query Params can help in managing received Data with sorting them by a specified value, having it Descending or Ascending and limit the amount of results

#### Query Params
 - sorted_by*:      sort the received values: string
 - order*:          asc or desc for result order: string
 - limit*:          limit the amount of received Data: int


### GET Convention
```
/api/convention
```
A successful GET request will have a **200 ok** status and returns the requested Convention in a Json Format

#### Query Params
 - id:              ID of the Convention: int

### POST Convention
```
/api/convention
``` 
A successful POST request will have a **201 created** status and returns the created Convention in a Json Format

#### Query Params
 - name:             name of the Convention: string
 - location*:        location of the Convention: string
 - date*:            date the Convention was held at

### PUT Convention
```
/api/convention
```
A successful PUT request will have a **200 ok** status and returns the changed Convention in a Json Format

#### Query Params
 - id:              ID of the Convention
 - name*:           new name of the Convention
 - location*:       new location of the Convention
 - date*:           new date of the Convention

### DEL Convention
```
/api/convention
```
A successful DEL request will have a **200 ok** status and returns a string with the deleted Convention id

#### Query Params
 - id:              ID of the Convention