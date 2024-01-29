# Udacity Full Stack Web Dev Capstone - Casting Agency

A Flask API project to manage a casting agency movies and actors.

It exposes endpoints to perform CRUD operations over actors and movies of the Agency based on role of the user that requests the resource.

Website URL:

https://udacity-fullstack-capstone-ef56c3f3fb4c.herokuapp.com

## Roles and Credentials

Users can get the JWT for authentication via a Auth0 API.
The URL for authenticate and get the JWT is this:

[URL for authentication with Auth0](https://michelangelomarani.eu.auth0.com/authorize?response_type=token&client_id=xZ0hNhLgnpfQ9p68hMKHVI3BsSmBSxIU&redirect_uri=http://127.0.0.1:5000/profile&audience=cinema)

Roles are the following:

### Casting Assistant

Can view actors and movies

username: castingassistant@mailinator.com

password: casting123$

### Casting Director

As previous, plus can add/delete an actor and modify actors or movies.

username: castingdirector@mailinator.com

password: casting123$

### Executive Producer

As previous, plus can add/delete a movie.

username: executiveproducer@mailinator.com

password: casting123$

## Setting Up Local Environment

python version: 3.9

* create a virtual environment with the proper python version
```bash
python3 -m venv venv
```
or
```bash
python3.9 -m venv venv
```
* activate the virtual environment
```bash
source venv/bin/activate
```
* install the requirements
```bash
pip install -r requirements.txt
```
* launch the script to add the env variables and create the local database
```bash
source setup.sh
```
* run the flask app
```bash
python app.py
```

## APIs

`GET '/actors'`

- Fetches the list of actors.
- Returns: An object with `actors` with minimal details, the `total` number of results and `success`.

```json
{
    "actors": [
        {
            "firstname": "Maela",
            "id": 2,
            "lastname": "Shivangani",
            "stagename": "White Lotus"
        },
        ...
    ],
    "success": true,
    "total": 2
}
```

---

`GET '/actors/<int:author_id>'`

- Get a single author by ID.
- Request Arguments: you have to pass "author_id" parameter
- Returns: An object with `actor` with full details and `success`.

```json
{
    "actor": {
        "birthdate": "Mon, 03 Apr 2000 00:00:00 GMT",
        "firstname": "Maela",
        "gender": "female",
        "id": 2,
        "lastname": "Shivangani",
        "stagename": "White Lotus"
    },
    "success": true
}
```

---

`POST '/actors'`

- Add a new actor
- Request Body:

```json
{
    "firstname": "Maela",
    "lastname": "Shivangani",
    "stagename": "Shiva",
    "gender": "female",
    "birthdate": "2000-04-03"
}
```

- Returns: `created` with the id of the new actor,

```json
{
    "created": 3
}
```

---

`PATCH '/actors/<int:actor_id>'`

- Update a single actor by ID.
- Request Arguments: you have to pass "author_id" by query parameter and the following body:

```json
{
    "stagename": "White Lotus",
    "gender": "female"
}
```

- Returns: An object with `actor` with full details and `success`.

```json
{
    "actor": {
        "birthdate": "Mon, 03 Apr 2000 00:00:00 GMT",
        "firstname": "Maela",
        "gender": "female",
        "id": 2,
        "lastname": "Shivangani",
        "stagename": "White Lotus"
    },
    "success": true
}
```

---

`DELETE '/actors/<int:actor_id>'`

- Deletes a specified actor by ID
- Request Arguments: `actor_id` - integer
- Returns: It returns the id of the deleted actor.

```json
{
  "deleted": 4
}
```

---

`GET '/movies'`

- Fetches the list of movies.
- Returns: An object with `movies` with minimal details, the `total` number of results and `success`.

```json
{
    "movies": [
        {
            "id": 1,
            "title": "Orange Juice",
            "year": 2024
        },
        ...
    ],
    "success": true,
    "total": 2
}
```

---

`GET '/movies/<int:movie_id>'`

- Get a single movie by ID.
- Request Arguments: you have to pass "movie_id" parameter
- Returns: An object with `movie` with full details and `success`.

```json
{
    "movie": {
        "duration": 120,
        "genre": "Comedy",
        "id": 1,
        "title": "Orange Juice",
        "year": 2024
    },
    "success": true
}
```

---

`POST '/movies'`

- Add a new movie
- Request Body:

```json
{
    "title": "Orange Juice 2",
    "genre": "Comedy",
    "year": 2024,
    "duration": 120
}
```

- Returns: `created` with the id of the new movie,

```json
{
    "created": 2
}
```

---

`PATCH '/movies/<int:movie_id>'`

- Update a single movie by ID.
- Request Arguments: you have to pass "movie_id" by query parameter and the following body:

```json
{
    "title": "Orange Juice",
    "genre": "Drama"
}
```

- Returns: An object with `movie` with full details and `success`.

```json
{
    "movie": {
        "duration": 120,
        "genre": "\"Drama\"",
        "id": 1,
        "title": "Orange Juice",
        "year": 2024
    },
    "success": true
}
```

---

`DELETE '/movies/<int:movie_id>'`

- Deletes a specified movie by ID
- Request Arguments: `movie_id` - integer
- Returns: It returns the id of the deleted movie.

```json
{
  "deleted": 1
}
```

---

## Tests

Import on Postman the file `udacity-cinema.postman_collection.json` to test all endpoints with different profiles.

To run unit tests instead just run:
```bash
python tests.py
```

## Flask Migrations

* init database
```bash
python manage.py db init
```
* create a migration
```bash
python manage.py db migrate
```
* apply the migration
```bash
python manage.py db upgrade
```

## Heroku

* run the bash
```bash
heroku run bash
```
* apply migration
```bash
heroku run python manage.py db upgrade --app udacity-fullstack-capstone
```
* deploy app
```bash
git push heroku main
```