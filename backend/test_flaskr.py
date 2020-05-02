import os
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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Get Questions tests

    def test_get_questions_first_page(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)

    def test_404_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=10')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)

    # Get Categories tests

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_404_delete_question_not_exists(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)

    def test_create_new_question(self):
        body = {
            "question": "What is the symbol for Silver?",
            "answer": "Ag",
            "difficulty": "1",
            "category": "1"
        }
        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_400_create_new_question_bad_request(self):
        body = {}
        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_404_get_question_by_category_not_exists(self):
        res = self.client().get('/category/100/questions')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)

    def test_search_questions(self):
        body = {
            "search_term": "title"
        }
        res = self.client().post('/questions/search', json=body)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_400_search_questions_wrong_body(self):
        body = {}
        res = self.client().post('/questions/search', json=body)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)

    def test_play_quizz(self):
        body = {
            "previous_questions": [],
            "quiz_category": {
                "id": "1"
            }
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_400_play_quiz_wrong_body(self):
        body = {}
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
