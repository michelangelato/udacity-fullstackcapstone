# Udacity Full Stack Web Dev Capstone - Casting Agency

A Flask API project to manage a casting agency movies and actors.

It exposes endpoints to perform CRUD operations over actors and movies of the Agency based on role of the user that requests the resource.

Users can get the JWT for authentication via a Auth0 API.
The URL for authenticate and get the JWT is this:

[URL for authentication with Auth0](https://michelangelomarani.eu.auth0.com/authorize?response_type=token&client_id=xZ0hNhLgnpfQ9p68hMKHVI3BsSmBSxIU&redirect_uri=http://127.0.0.1:5000/profile&audience=cinema)

Roles are the following:
* Casting Assistant (can view actors and movies)
* Casting Director (as previous, plus can add/delete an actor and modify actors or movies)
* Executive Producer (as previous, plus can add/delete a movie)

Website URL:

https://udacity-fullstack-capstone-ef56c3f3fb4c.herokuapp.com

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

@TODO


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