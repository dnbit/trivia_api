# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation

### List of endpoints

[GET '/categories'](#get_categories)

[GET '/questions?page={page_number}'](#get_questions)

[DELETE '/questions/{id}'](#delete_questions)

[POST '/questions'](#post_questions)

[POST '/questions/search'](#search_questions)

[GET '/categories/{id}/questions'](#get_question_by_category)

[POST '/quizzes'](#post_quizzes)

### Endpoints details

<a name="get_categories"></a>GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a success key that contains a boolean and a categories key, that contains a object of id: category_string key:value pairs. 
```
{
    "success": True,
    "categories": {
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    }
}
```

<a name="get_questions"></a>GET '/questions'
- Fetches a paginated list of questions
- Request Arguments: Page number (optional, default = 1)
- Returns: An object with the sucess result, the list of categories, current category, questions for the given page and total number of questions
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 20
}
```

<a name="delete_questions"></a>DELETE '/questions/{id}'
- Deletes a question with a given id
- Request Arguments: Question id
- Returns: An object with the sucess result and the deleted id
```
{
    "success": True,
    "deleted": "1"
}
```

<a name="post_questions"></a>POST '/questions'
- Creates a new question
- Request Arguments: An object with the question, answer, difficulty and category
```
{
    "question": "What is the symbol for Silver?",
    "answer": "Ag",
    "difficulty": "1",
    "category": "1"
}
```
- Returns: An object with the sucess result and the new question
```
{
    "item": {
        "answer": "Ag",
        "category": "1",
        "difficulty": "1",
        "id": "25",
        "question": "What is the symbol for Silver?"
    },
    "success": true
}
```

<a name="search_questions"></a>POST '/questions/search'
- Search questions that include a given term
- Request Arguments: An object with the search term
```
{
    "search_term": "title"
}
```
- Returns: An object with the sucess result, list of categories, current category, matching questions and total number of matching questions
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```


<a name="get_question_by_category"></a>GET '/categories/{id}/questions'
- Fetches questions for a given category
- Request Arguments: Category id
-  Returns: An object with the sucess result, the list of categories, current category, questions for the given page and total number of questions for that category
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": 1,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 20
}
```

<a name="post_quizzes"></a>POST '/quizzes'
- Fetches the next question for the quizz
- Request Arguments: An object with the list of previous questions used and the category.
```
{
	"previous_questions": [25],
    "quiz_category": {
    	"id": "1"
    	
    }
}
```
- Returns: An object with the sucess result and the next question
```
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```


