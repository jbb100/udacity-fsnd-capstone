# Full Stack Capstone API

## Getting Started

### Installing Dependencies

#### Python 3.6

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
cd backend
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
sh server.sh
```

## Endpoints
### Actor
GET '/actors'
- Get an Actor list
- Request Arguments: None
- Returns: an Actor list
```javascript
{
    "actors": [
        {
            "age": 30,
            "gender": "F",
            "id": 1,
            "name": "Actor1"
        }
    ],
    "success": true
}
```

POST '/actors'
- Add an actor
- Request Arguments
- Content-Type: application/json

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
name | STRING | YES | name of an actor
age | INT | YES | age of an actor
gender | STRING | YES | gender of an actor

- Returns: An object with two keys, success and actor.
```javascript
{
    "actor": {
        "age": 30,
        "gender": "F",
        "id": 1,
        "name": "Actor1"
    },
    "success": true
}
```

PATCH '/actors'
- Modify actor's information
- Request Arguments
- Content-Type: application/json

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
name | STRING | NO | name of an actor
age | INT | NO | age of an actor
gender | STRING | NO | gender of an actor

- Returns: An object with two keys, success and actor.
```javascript
{
    "actor": {
        "age": 40,
        "gender": "M",
        "id": 1,
        "name": "Actor11"
    },
    "success": true
}
```

DELETE '/actors/<id>'
- Delete an actor by id
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
id | INT | YES | a actor id to delete (path variable)

- Returns: 
```javascript
{
    "delete": "1",
    "success": true
}
```

### Movie

## Error Codes
Errors consist of three parts: a success flag, an error code and a message.
Here is the error JSON payload:
```javascript
{
  'success': False,
  'error': 400,
  'message':"bad request"
}
```

#### 400 bad request
 * types of request values is wrong or some mandatory fields are missing.

#### 404 resource not found
 * an url is wrong or there are no object to process in the database.
 
#### 405 method not allowed
 * access with wrong method. check your http method again.
 
#### 422 unprocessable
 * unable to process the request.
 
#### 500 internal server error
 * An unknown error occured while processing the request.

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
