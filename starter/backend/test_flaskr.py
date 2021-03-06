import os
from re import search
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        self.new_question = {
            'question': 'what is my name ?',
            'answer': 'mohammed zain',
            'difficulty': 5,
            'category': 1
        }
        self.new_question_fails= {
            'question': 'what is my name ?',
            'answer': 'mohammed zain',
            'difficulty': 5,
            'categoryy': 1
        }
        self.search_term = {
            'searchTerm': 'what'
        }
        self.quizzes = {
            'previous_questions':[17,18],
            'quiz_category': {
                'id': '2',
                'type':'Art'
            }
        }
        self.quizzes_fails = {
            'previous_questionss': 17,
            'quiz_category': {
                'id': 2,
                'type':'Art'
            }
        }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    # /////////////////////////////////////////////////////////////////////////
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        
    def test_404_not_found(self):
        res = self.client().get('/categoriess')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    # /////////////////////////////////////////////////////////////////////////
    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        question = Question.query.get(10)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)
        self.assertEqual(question, None)
        

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    # /////////////////////////////////////////////////////////////////////////
    def test_get_questions_by_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        
    def test_500_categories_not_exist(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')
    # /////////////////////////////////////////////////////////////////////////
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json=self.new_question_fails)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    # /////////////////////////////////////////////////////////////////////////
    def test_search_question(self):
        res = self.client().post('/questions/search_query', json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
    
    def test_422_if_search_term_unprocessable(self):
        res = self.client().post('/questions', json=99)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
     # /////////////////////////////////////////////////////////////////////////
    def test_play_quizzes(self):
        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
    def test_500_quizzes(self):
        res = self.client().post('/quizzess', json=self.quizzes_fails)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()