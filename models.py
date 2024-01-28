import os
from sqlalchemy import Column, Integer, String, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()


'''
"recitations" Table
'''
recitations = db.Table(
    'recitations',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'))
)


'''
"actors" Table
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  firstname = Column(String)
  lastname = Column(String)
  stagename = Column(String)
  gender = Column(String)
  birthdate = Column(Date)
  movies = db.relationship(
    'Movie',
    secondary=recitations,
    back_populates='actors'
  )

  def __init__(
    self,
    firstname,
    lastname,
    birthdate,
    gender="unknow",
    stagename="",
    catchphrase=""):
    self.fistname = firstname
    self.lastname = lastname
    self.birthdate = birthdate
    self.gender = gender
    self.stagename = stagename
    self.catchphrase = catchphrase

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'firstname': self.firstname,
      'lastname': self.lastname,
      'stagename': self.stagename,
      'gender': self.gender,
      'catchphrase': self.catchphrase
    }

'''
"movies" Table
'''
class Movie(db.Model):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  genre = Column(String)
  year = Column(Integer)
  duration = Column(Integer)
  actors = db.relationship(
    'Actor',
    secondary=recitations,
    back_populates='movies'
  )

  def __init__(self, title, genre, year, duration):
    self.title = title
    self.genre = genre
    self.year = year
    self.duration = duration

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'genre': self.genre,
      'year': self.year,
      'duration': self.duration
    }
