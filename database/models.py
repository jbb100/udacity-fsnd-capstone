import os
from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    Date
)
from flask_sqlalchemy import SQLAlchemy
import json

project_dir = os.path.dirname(os.path.abspath(__file__))
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_filename=None):
    if database_filename is not None:
        # if database_filename exists, use sqllite
        database_path = "sqlite:///{}".format(
            os.path.join(project_dir, database_filename))
    else:
        # else use postgres
        database_path = os.environ.get('DATABASE_URI')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
BaseModel
implement base model contains common helper methods for models
'''
class BaseModel(db.Model):
    '''
    format()
        json representation of the model
        (must be implemented by sub class)
    '''
    
    def format(self):
        return {}

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Titanic'
            movie.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


'''
Movies
a persistent movie entity, extends the base SQLAlchemy Model
'''


class Movie(BaseModel):
    __tablename__ = 'Movie'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(100), nullable=False)
    # Date Release Date
    release_date = Column(Date, nullable=False)

    '''
    format()
        json representation of the Movies model
    '''

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d')
        }


'''
Actors
a persistent actor entity, extends the base SQLAlchemy Model
'''


class Actor(BaseModel):
    __tablename__ = 'Actor'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    name = Column(String(100), nullable=False)
    # Integer Age
    age = Column(Integer, nullable=False)
    #  Gender
    gender = Column(String(1), nullable=False)

    '''
    format()
        json representation of the Actor model
    '''

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
