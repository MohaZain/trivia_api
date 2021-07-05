# Full Stack Trivia API 

### Interductions

This the second project from udacity FullStack nanodegree is website thets allow to create question with categories,
and quezz your self with these Various questions,

The main focus for the student is to complate the backend section,
- Design complate [API](https://medium.com/swlh/the-flavours-of-apis-c13552799645)
- Test diffrent senario with each Endpoing.

now for the rest of this Document, follow the each section to help you download the project also runnit in your local server 
to explore the website. 

Enjoye 

### Installing Dependencies for the Frontend

1. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**


### Running Your Frontend in Dev Mode


```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>


### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Running the server

From within the `./backend/flasker` directory.

To run the server, execute:

```bash
export FLASK_APP=__init__.py
export FLASK_ENV=development
flask run
```

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## API

```
GET '/categories'
- Fetches a list of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{
'success': True,
'categories':{
'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
}

```
```
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category list. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': ['History']
}
```
```
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Deleted id
{
'success': True,
'deleted': question_id
}
```
```
GET '/categories/${id}/questions'
- Fetches get questions by category id
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 
{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```
```
POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
- Returns: success
{
'success': True
}
```
```
POST '/questions/search_query'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
{
    'success':True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100
}
```
```
POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category':{
      'id':${'number'},
      'type':${string}
     }
}
- Returns: a random single new question object 
{
    'success':True,
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```

## Errors
`404
{
'success':False 
'error':404 
'message':'resource not found' }`

`422
{
'success':False 
'error':422 
'message':'unprocessable' }`

`400
{
'success':False 
'error':400 
'message':'bad request' }`

`500
{
'success':False 
'error':500 
'message':'internal server error' }`

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
