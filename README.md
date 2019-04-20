## Installation

```bash
pip install psycopg2-binary django==1.11.20 djangorestframework django-unixtimestampfield

```

## Endpoints

### Add new user

`/cp/add_user`

Using this endpoint you can add a new user with username and password from the command line:

```bash
curl -X POST -H "Content-type: application/json" -d '{"username": "USERNAME", "password": "PASSWORD"}' 'http://127.0.0.1:8000/cp/add_user'
```
### Add new partner

`/cp/partners/add`

Add a new partner from the command line:

```bash
curl --user USERNAME:PASSWORD -X POST -H "Content-type: application/json" -d '{"name": "NAME", "city": "CITY", "address": "ADDRESS", "company_name": "COMPANY_NAME"}' 'http://127.0.0.1:8000/cp/partners/add'
```

### List all partners in JSON

`/cp/partners/`


### Get a specific partner by Id in JSON

`/cp/partners/(\d+)`