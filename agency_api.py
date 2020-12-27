import os
from flask import (
    Flask,
    request,
    jsonify,
    abort,
    make_response
)
from sqlalchemy import exc
import json
from flask_cors import (
    CORS,
    cross_origin
)
from database.models import (
    db_drop_and_create_all,
    setup_db,
    db,
    Actor,
    Movie
)
from auth.auth import (
    AuthError,
    requires_auth
)
import sys
import datetime
import traceback

app = Flask(__name__)
setup_db(app)
GENDER_SET = set(['M', 'F'])  # define gender values
MODELS_PER_PAGE = 10  # for paging result

'''
    Formatting & Validatinga Date
'''


def format_date(date_str, date_format='%Y-%m-%d'):
    try:
        formatted_date = datetime.datetime.strptime(date_str, date_format)
    except Exception:
        print(sys.exc_info())
        abort(status=400,
              description='invalid date format. it must be %Y-%m-%d')

    return formatted_date


'''
    Formatting & Validating Age
'''


def format_age(age):
    try:
        age = int(age)
    except Exception:
        print(sys.exc_info())
        abort(status=400, description='age must be Integer')

    if age < 0:
        abort(status=400, description='age must be Pos. Integer (0 > age)')

    return age


'''
    Formatting & Validating Gender
'''


def format_gender(gender):
    gender = gender.upper()
    if gender not in GENDER_SET:
        abort(status=400, description='gender must be "M" or "F"')

    return gender


'''
    Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
'''
cors = CORS(app, resources={r"/*": {"origins": "*"}})

'''
    Use the after_request decorator to set Access-Control-Allow
'''
# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response


# ROUTES
'''
    GET /
        return a welcome message
'''


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Welcome to My Agency API'
    })


'''
    GET /actors
        return actor lists
'''


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
@cross_origin()
def get_actors(payload):
    if request:
        page = request.args.get('page', 1, type=int)
    else:
        page = 1
    start = (page - 1) * MODELS_PER_PAGE
    end = start + MODELS_PER_PAGE

    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]
    current_selected = formatted_actors[start:end]

    return jsonify({"success": True, "actors": current_selected})


'''
    GET /movies
        return movie lists
'''


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
@cross_origin()
def get_movies(payload):
    if request:
        page = request.args.get('page', 1, type=int)
    else:
        page = 1
    start = (page - 1) * MODELS_PER_PAGE
    end = start + MODELS_PER_PAGE

    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]
    current_selected = formatted_movies[start:end]

    return jsonify({"success": True, "movies": current_selected})


'''
    POST /actors
        add new Actor
'''


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
@cross_origin()
def post_actors(payload):

    error = False

    # get new values
    request_json = request.get_json()
    name = request_json['name'] if 'name' in request_json \
        else abort(400, 'name is empty')
    age = request_json['age'] if 'age' in request_json \
        else abort(400, 'age is empty')
    gender = request_json['gender'] if 'gender' in request_json \
        else abort(400, 'gender is emtpy')

    # validate age value
    age = format_age(age)

    # validate gender value (M,F)
    gender = format_gender(gender)

    try:
        # create a new row in the drinks table
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        formatted_actor = actor.format()
    except Exception:
        print(sys.exc_info())
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        # on successful db insert
        return jsonify({"success": True, "actor": formatted_actor})


'''
    POST /movies
        add new movie
'''


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
@cross_origin()
def post_movies(payload):

    error = False
    # get new values
    request_json = request.get_json()
    title = request_json['title'] if 'title' in request_json \
        else abort(400, description='title is empty')
    release_date = format_date(request_json['release_date']) \
        if 'release_date' in request_json \
        else abort(400, description='release_date is empty')
    try:

        # create a new row in the drinks table
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        formatted_movie = movie.format()
    except Exception:
        print(sys.exc_info())
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(status=400, description='bad request')
    else:
        # on successful db insert
        return jsonify({"success": True, "movie": formatted_movie})


'''
    PATCH /actors/<id>
        update actor info
'''


@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
@cross_origin()
def patch_actors(payload, id):
    success = False

    # get a actor object corresponding to given id
    try:
        actor = Actor.query.get(id)
    except Exception:
        print(sys.exc_info())
        abort(404)  # it should respond with a 404 error if <id> is not found

    print('columns = ', actor.__table__.columns)

    # get new values
    request_json = request.get_json()
    if 'name' in request_json:
        # update field values
        name = request_json['name']
        actor.name = name

    if 'age' in request_json:
        # validate age value
        age = request_json['age']
        age = format_age(age)

        # update field values
        actor.age = age

    if 'gender' in request_json:
        # validate gender value (M,F)
        gender = request_json['gender']
        gender = format_gender(gender)

        # update field values
        actor.gender = gender

    try:
        actor.update()

        # mark success
        success = True
        formatted_actor = actor.format()
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({"success": success, "actor": formatted_actor})


'''
    PATCH /movies/<id>
        update movie info
'''


@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movies')
@cross_origin()
def patch_movies(payload, id):
    success = False

    try:
        # get a movie object corresponding to given id
        movie = Movie.query.get(id)
    except Exception:
        print(sys.exc_info())
        abort(404)  # it should respond with a 404 error if <id> is not found

    # get new values
    request_json = request.get_json()
    if 'title' in request_json:
        # update field values
        title = request_json['title']
        movie.title = title

    if 'release_date' in request_json:
        # update field values
        release_date = format_date(request_json['release_date'])
        movie.release_date = release_date

    try:
        movie.update()

        # mark success
        success = True
        formatted_movie = movie.format()
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        abort(404)  # it should respond with a 404 error if <id> is not found
    finally:
        db.session.close()

    return jsonify({"success": success, "movie": formatted_movie})


'''
    DELETE /actors/<id>
        delete actor by id
'''


@app.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actors')
@cross_origin()
def delete_actors(payload, id):
    success = False
    try:
        drink = Actor.query.get(id)
        drink.delete()
        success = True
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        abort(404)  # it should respond with a 404 error if <id> is not found
    finally:
        db.session.close()

    return jsonify({"success": success, "delete": id})


'''
    DELETE /movies/<id>
        delete movie by id
'''


@app.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
@cross_origin()
def delete_movies(payload, id):
    success = False
    try:
        movie = Movie.query.get(id)
        movie.delete()
        success = True
    except Exception:
        print(sys.exc_info())
        db.session.rollback()
        abort(404)  # it should respond with a 404 error if <id> is not found
    finally:
        db.session.close()

    return jsonify({"success": success, "delete": id})


'''
    error handling
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500
