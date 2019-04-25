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