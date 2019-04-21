## Installation

```bash
pip install psycopg2-binary django==1.11.20 djangorestframework django-unixtimestampfield

```

## Endpoints

### Users

#### Add new user

`/cp/add_user  [POST]` 

Using this endpoint you can add a new user with username and password from the command line:

```bash
curl -X POST -H "Content-type: application/json" -d '{"username": "USERNAME", "password": "PASSWORD"}' 'http://127.0.0.1:8000/cp/add_user'
```

### Partners

#### List all partners in JSON

`/cp/partners/ [GET]`

#### Add new partner

`/cp/partners/ [POST]`

Add a new partner from the command line:

```bash
curl --user USERNAME:PASSWORD -X POST -H "Content-type: application/json" -d '{"name": "NAME", "city": "CITY", "address": "ADDRESS", "company_name": "COMPANY_NAME"}' 'http://127.0.0.1:8000/cp/partners/'
```

#### Get a specific partner by Id in JSON

`/cp/partners/(\d+) [GET]`

#### Delete partner by ID

`/cp/partners/(\d+) [DELETE]`

This endpoint sets the 'deleted_at' field of a partner to the current time. Partners whose 'deleted_at' is not 0.0 are considered deleted.
If there are connections with cars, the referring values get changed to negative on both sides to archive the connection.
This enables a possible future restoration of the instance along with its archived connections. 

```bash
curl --user USERNAME:PASSWORD -X DELETE 'http://127.0.0.1:8000/cp/partners/ID'
```

### Cars

#### List all cars in JSON

`/cp/cars/ [GET]`

#### Add new car

`/cp/cars/ [POST]`

Add a new car from the command line:

```bash
curl --user USERNAME:PASSWORD -X POST -H "Content-type: application/json" -d '{"average_fuel": NUM, "driver": "DRIVER", "owner": "OWNER", "type": "pr"/"co"}' 'http://127.0.0.1:8000/cp/cars/'
```

#### Get a specific car by Id in JSON

`/cp/cars/(\d+) [GET]`

#### Delete car by ID

`/cp/cars/(\d+) [DELETE]`

This endpoint sets the 'deleted_at' field of a car to the current time. Cars whose 'deleted_at' is not 0.0 are considered deleted.
If there are connections with partners, the referring values get changed to negative on both sides to archive the connection.
This enables a possible future restoration of the instance along with its archived connections

```bash
curl --user USERNAME:PASSWORD -X DELETE 'http://127.0.0.1:8000/cp/cars/ID'
```

#### Assign partner to car

`/cp/cars/(\d+) [PATCH]`

The partner's ID gets stored in the car's respective array field and vice versa.

```bash
curl  --user USERNAME:PASSWORD -X PATCH -H "Content-type: application/json" -d '{"partner": PARTNER_ID}' 'http://127.0.0.1:8000/cp/cars/CAR_ID'
```