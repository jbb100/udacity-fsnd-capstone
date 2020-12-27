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
- Content-Type: application/json
- Request Arguments

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
- Content-Type: application/json
- Request Arguments

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
GET '/movies'
- Get an Movie list
- Request Arguments: None
- Returns: an Movie list
```javascript
{
    "movies": [
        {
            "title": "Movie1",
            "release_date": "2020-12-12"
        }
    ],
    "success": true
}
```

POST '/movies'
- Add an movie
- Content-Type: application/json
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
title | STRING | YES | title of an movie
release_date | STRING | YES | release date of an movie (date string format: %Y-%m-%d)

- Returns: An object with two keys, success and movie.
```javascript
{
    "movie": {
        "title": "Movie1",
        "release_date": "2020-12-12"
    },
    "success": true
}
```

PATCH '/movies'
- Modify movie's information
- Content-Type: application/json
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
title | STRING | NO | title of an movie
release_date | STRING | NO | release date of an movie (date string format: %Y-%m-%d)

- Returns: An object with two keys, success and movie.
```javascript
{
    "movie": {
        "title": "Movie11",
        "release_date": "2020-09-14"
    },
    "success": true
}
```

DELETE '/movies/<id>'
- Delete an movie by id
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
id | INT | YES | a movie id to delete (path variable)

- Returns: 
```javascript
{
    "delete": "1",
    "success": true
}
```

## Error Codes
Errors consist of three parts: a success flag, an error code and a message.
"message" can be different with each case.
Here is the error JSON payload:
```javascript
{
  "success": False,
  "error": 400,
  "message": "bad request"
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
cd backend
sh test.sh
```

test.sh
```
export PYTHONPATH=$PWD
python test/test_casting_assistant.py
python test/test_casting_director.py
python test/test_executive_producer.py
```

get access tokens for each role
```
cd backend/test
cat token.yml
```
