# Udacity Full Stack Web Dev Capstone - Cinema App

## Run it locally (python 3.9)

* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt
* source setup.sh
* python app.py

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