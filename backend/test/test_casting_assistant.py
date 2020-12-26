import sys
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import yaml
from database.models import setup_db, db_drop_and_create_all
from agency_api import app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app, database_filename="database_test.db")

        # set access token for this role
        with open('test/token.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {data['casting_assistant']}"
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    def test_get_actors(self):
        # success
        res = self.client().get('/actors', headers=self.headers)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['actors']), 0)

    def test_error_get_actors(self):
        # invalid method
        res = self.client().post('/actors', headers=self.headers)
        self.assertEqual(res.status_code, 405)

    def test_get_movies(self):
        # success
        res = self.client().get('/movies', headers=self.headers)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['movies']), 0)

    def test_error_get_movies(self):
        # invalid method
        res = self.client().post('/movies', headers=self.headers)
        self.assertEqual(res.status_code, 405)

    # def test_get_actors(self):
    #     # success
    #     res = self.client().get('/actors')
    #     data = res.get_json()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertGreater(len(data['actors']), 0)

    # def test_error_get_actors(self):
    #     # invalid method
    #     res = self.client().post('/actors')
    #     self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
