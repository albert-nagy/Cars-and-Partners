## Description

In this task I had to create a Django REST API.

According to the story, the users visit their business partners by car. So a user can have partners and cars and we have to able to specify, which cars are used for visiting a specific partner.

According to the specification users should be able to log in and

- create,
- read,
- delete,
- or connect

their cars and partners via respective JSON endpoints.
Regarding the user management a login endpoint is enough.
All entities have automatically filled *created_at*, *modify_at* and *deleted_at* fields, storing time in unix timestamp. If the *deleted_at* field's value is not 0, the entity is considered deleted.
The car-partner connection should be saved from the car's side when cars and partners already exist, and stored in array fields in both car and partner models.

> *I have to admit that I would do this differently: I would use a separate table to store car-partner connections, instead of storing the same information in two places. With a separate "connections" table it would be easier to create, delete connections or just making them dormant. This model would enable saving time informations about creation, modification, deletion or last usage of the connection as well.*

The view has to contain a decorator that binds entity methods to authentication.
All car and partner entity methods should have unit tests.
The system has to log all requests using a middleware.

The environment was specified as following:

- Python 3.6
- PostgreSQL 10
- Django 1.11.20

The application should prefferrably run in a docker.

### Technologies used to complete this task

* Python 3
* Django
* Django REST Framework
* Django REST Auth
* PostgreSQL
* Docker

## Installation

Intstall and start using the attached docker:

```bash
docker-compose build
docker-compose up -d
```

## Endpoints

### Users

#### Add new user

`/api/v1/add_user/  [POST]` 

Using this endpoint you can add a new user with username and password from the command line:

```bash
curl -X POST -H "Content-type: application/json" -d '{"username": "USERNAME", "password": "PASSWORD"}' 'http://127.0.0.1:8000/api/v1/add_user/'
```

#### User Login

`/api/v1/rest-auth/login/  [POST]` 

Get your authorization token by signing in with your credentials. Paste the token (key) you get in the response into the request wherever it is required.

```bash
curl -X POST -H "Content-type: application/json" -d '{"username": "USERNAME", "password": "PASSWORD"}' 'http://127.0.0.1:8000/api/v1/rest-auth/login/'
```


### Partners

#### List all partners in JSON

`/api/v1/partners/ [GET]`

#### Add new partner

`/api/v1/partners/ [POST]`

Add a new partner from the command line. Replace the XXXXXXXXXXXXX... with your auth token.

```bash
curl -X POST -H "Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" -H "Content-type: application/json" -d '{"name": "NAME", "city": "CITY", "address": "ADDRESS", "company_name": "COMPANY_NAME"}' 'http://127.0.0.1:8000/api/v1/partners/'
```

#### Get a specific partner by Id in JSON

`/api/v1/partners/(\d+)/ [GET]`

#### Delete partner by ID

`/api/v1/partners/(\d+)/ [DELETE]`

This endpoint sets the 'deleted_at' field of a partner to the current time. Partners whose 'deleted_at' is not 0.0 are considered deleted.
If there are connections with cars, the referring values get changed to negative on both sides to archive the connection.
This enables a possible future restoration of the instance along with its archived connections. 

```bash
curl -X DELETE -H "Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 'http://127.0.0.1:8000/api/v1/partners/ID/'
```

### Cars

#### List all cars in JSON

`/api/v1/cars/ [GET]`

#### Add new car

`/api/v1/cars/ [POST]`

Add a new car from the command line:

```bash
curl -X POST -H "Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" -H "Content-type: application/json" -d '{"average_fuel": NUM, "driver": "DRIVER", "owner": "OWNER", "type": "pr"/"co"}' 'http://127.0.0.1:8000/api/v1/cars/'
```

#### Get a specific car by Id in JSON

`/api/v1/cars/(\d+)/ [GET]`

#### Delete car by ID

`/api/v1/cars/(\d+)/ [DELETE]`

This endpoint sets the 'deleted_at' field of a car to the current time. Cars whose 'deleted_at' is not 0.0 are considered deleted.
If there are connections with partners, the referring values get changed to negative on both sides to archive the connection.
This enables a possible future restoration of the instance along with its archived connections

```bash
curl -X DELETE -H "Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 'http://127.0.0.1:8000/api/v1/cars/ID/'
```

#### Assign partner to car

`/api/v1/cars/(\d+)/ [PATCH]`

The partner's ID gets stored in the car's respective array field and vice versa.

```bash
curl -X PATCH -H "Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" -H "Content-type: application/json" -d '{"partner": PARTNER_ID}' 'http://127.0.0.1:8000/api/v1/cars/ID/'
```

## Unit testing

Run tests with the following command:

```bash
docker-compose exec app python manage.py test
```