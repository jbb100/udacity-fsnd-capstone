import sys
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import yaml
from database.models import setup_db, db_drop_and_create_all, Movie, Actor
from agency_api import app, format_date, format_age, format_gender


class ExecutiveProducerTestCase(unittest.TestCase):

    def setUp(self):
        '''
            Define test variables and initialize app.
        '''
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

        # insert sample rows
        actor = Actor(name='first_actor', age=30, gender='M')
        actor.insert()
        movie = Movie(title='first_movie',
                      release_date=format_date('2010-10-08'))
        movie.insert()

    def tearDown(self):
        pass

    '''
        GET
    '''

    def test_get_actors(self):
        # success
        res = self.client().get('/actors', headers=self.headers)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['actors']), 0)

    def test_error_get_actors(self):
        # no permission (w/o headers)
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        # success
        res = self.client().get('/movies', headers=self.headers)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['movies']), 0)

    def test_error_get_movies(self):
        # no permission (w/o headers)
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    '''
        POST
    '''

    def test_error_post_actors(self):
        # no permission
        req_data = {
            'name': 'Actor1',
            'age': 30,
            'gender': 'F'
        }
        res = self.client().post('/actors', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 401)


    def test_error_post_movies(self):
        # no permission
        req_data = {
            'title': 'Movie1',
            'release_date': '2020-12-12'
        }
        res = self.client().post('/movies', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 401)

    '''
        PATCH
    '''

    def test_error_patch_actors(self):
        # no permission
        req_data = {
            'name': 'Actor11',
            'age': 80,
            'gender': 'M'
        }
        target_id = Actor.query.all()[-1].id
        res = self.client().patch(
            f'/actors/{target_id}', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 401)

    def test_error_patch_movies(self):
        # no permission
        req_data = {
            'title': 'Movie11',
            'release_date': '2000-09-22'
        }
        target_id = Movie.query.all()[-1].id
        res = self.client().patch(
            f'/movies/{target_id}', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 401)

    '''
        DELETE
    '''

    def test_error_delete_actors(self):
        # no permission
        target_id = Actor.query.all()[-1].id
        res = self.client().delete(
            f'/actors/{target_id}', headers=self.headers)
        self.assertEqual(res.status_code, 401)

    def test_error_delete_movies(self):
        # no permission
        target_id = Movie.query.all()[-1].id
        res = self.client().delete(
            f'/movies/{target_id}', headers=self.headers)
        self.assertEqual(res.status_code, 401)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
