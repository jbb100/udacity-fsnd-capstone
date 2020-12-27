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
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```javascript
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

GET '/questions'
- Fetches a dictionary of questions
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
page | INT | NO | query string (Default: 1)

- Returns: An object with three keys, questions, total_questions, and categories.
```javascript
{
  'success': True,
  'questions': [
     {
      'id': 5, 
      'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", 
      'answer': 'Maya Angelou', 
      'category': 4, 
      'difficulty': 2
    }, 
    {
      'id': 9, 
      'question': "What boxer's original name is Cassius Clay?", 
      'answer': 'Muhammad Ali', 
      'category': 4, 
      'difficulty': 1
     }
   ], 
   'total_questions': 19, 
     'categories': {
       '1': 'Science', 
       '2': 'Art', 
       '3': 'Geography', 
       '4': 'History', 
       '5': 'Entertainment', 
       '6': 'Sports'
      }
}
```

DELETE '/questions/<question_id>'
- Delete a question by id
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
question_id | INT | YES | a question id to delete (path variable)

- Returns: 
```javascript
{
  'question_id': 1, 
  'success': True
}
```

POST '/questions/create'
- Create new question
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
question | STRING | YES | question text (json body)
answer | STRING | YES | answer text (json body)
category | INT | YES | category id (json body)
difficulty | INT | YES | difficulty of the question (json body)

- Returns: 
```javascript
{'success': True}
```

POST '/questions'
- Search questions by a search term
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
searchTerm | STRING | YES | term for search questions (json body)


- Returns: 
```javascript
{
  'questions': [
    {
      'id': 9, 
      'question': "What boxer's original name is Cassius Clay?", 
      'answer': 'Muhammad Ali', 
      'category': 4, 
      'difficulty': 1
    }, 
    {
      'id': 2,
      'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 
      'answer': 'Apollo 13', 
      'category': 5, 
      'difficulty': 4
    },
    {
      'id': 4, 
      'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 
      'answer': 'Tom Cruise', 
      'category': 5, 
      'difficulty': 4
    }
  ], 
  'total_questions': 8, 
  'categories': {
    '1': 'Science', 
    '2': 'Art', 
    '3': 'Geography', 
    '4': 'History', 
    '5': 'Entertainment', 
    '6': 'Sports'
   }, 
  'success': True
}
```

GET '/categories/<category_id>/questions'
- Get questions in a category
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
category_id | INT | YES | category id for filtering questions


- Returns: 
```javascript
{
  'questions': [
    {
      'id': 13, 
      'question': 'What is the largest lake in Africa?', 
      'answer': 'Lake Victoria', 
      'category': 3, 
      'difficulty': 2
    }, 
    {
      'id': 14, 
      'question': 'In which royal palace would you find the Hall of Mirrors?', 
      'answer': 'The Palace of Versailles', 
      'category': 3, 
      'difficulty': 3
    },
    {
      'id': 15, 
      'question': 'The Taj Mahal is located in which Indian city?', 
      'answer': 'Agra', 
      'category': 3, 
      'difficulty': 2
    }
  ], 
  'total_questions': 3, 
  'categories': {
    '1': 'Science', 
    '2': 'Art', 
    '3': 'Geography', 
    '4': 'History', 
    '5': 'Entertainment', 
    '6': 'Sports'
  }, 
  'success': True
}
```

POST '/quizzes'
- Get a question for a quizze game
- Request Arguments

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
previous_questions | LIST<INT> | YES | a list of question ids to avoid duplicated questions (json body)
quiz_category | INT | YES | a category for next quiz. 0 means "ALL" categories (json body)


- Returns: 
```javascript
{
  'question': {
    'id': 20, 
    'question': 'What is the heaviest organ in the human body?', 
    'answer': 'The Liver', 
    'category': 1, 
    'difficulty': 4
  },
  'success': True
}
```

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
