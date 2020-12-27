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
                "Authorization": f"Bearer {data['executive_producer']}"
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

    def test_post_actors(self):
        # success
        req_data = {
            'name': 'Actor1',
            'age': 30,
            'gender': 'F'
        }
        res = self.client().post('/actors', headers=self.headers, json=req_data)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['name'], req_data['name'])
        self.assertEqual(data['actor']['age'], req_data['age'])
        self.assertEqual(data['actor']['gender'], req_data['gender'])

    def test_error_post_actors(self):
        # age is not integer
        req_data = {
            'name': 'Actor11',
            'age': 'eighty',
            'gender': 'M'
        }
        res = self.client().post(
            '/actors', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['message'], 'age must be Integer')

        # age is negative number
        req_data = {
            'name': 'Actor12',
            'age': -100,
            'gender': 'M'
        }
        res = self.client().post(
            '/actors', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['message'],
                         'age must be Pos. Integer (0 > age)')

        # gender is wrong
        req_data = {
            'name': 'Actor13',
            'age': 80,
            'gender': 'MALE'
        }
        res = self.client().post(
            '/actors', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['message'],
                         'gender must be "M" or "F"')

    def test_post_movies(self):
        # success
        req_data = {
            'title': 'Movie1',
            'release_date': '2020-12-12'
        }
        res = self.client().post('/movies', headers=self.headers, json=req_data)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], req_data['title'])
        self.assertEqual(data['movie']['release_date'], format_date(
            req_data['release_date']).strftime('%Y-%m-%d'))

    def test_error_post_movies(self):
        # wrong date format
        req_data = {
            'title': 'Movie12',
            'release_date': '20201212'
        }
        res = self.client().post('/movies', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['message'],
                         'invalid date format. it must be %Y-%m-%d')

    '''
        PATCH
    '''

    def test_patch_actors(self):
        # success
        req_data = {
            'name': 'Actor11',
            'age': 80,
            'gender': 'M'
        }
        target_id = Actor.query.all()[-1].id
        res = self.client().patch(
            f'/actors/{target_id}', headers=self.headers, json=req_data)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['name'], req_data['name'])
        self.assertEqual(data['actor']['age'], req_data['age'])
        self.assertEqual(data['actor']['gender'], req_data['gender'])

    def test_error_patch_actors(self):
        # age is not integer
        req_data = {
            'name': 'Actor11',
            'age': 'eighty',
            'gender': 'M'
        }
        target_id = Actor.query.all()[-1].id
        res = self.client().patch(
            f'/actors/{target_id}', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)

        # age is negative number
        req_data = {
            'name': 'Actor11',
            'age': -100,
            'gender': 'M'
        }
        target_id = Actor.query.all()[-1].id
        res = self.client().patch(
            f'/actors/{target_id}', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)

        # gender is wrong
        req_data = {
            'name': 'Actor11',
            'age': 80,
            'gender': 'MALE'
        }
        target_id = Actor.query.all()[-1].id
        res = self.client().patch(
            f'/actors/{target_id}', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)

    def test_patch_movies(self):
        # success
        req_data = {
            'title': 'Movie11',
            'release_date': '2000-09-22'
        }
        target_id = Movie.query.all()[-1].id
        res = self.client().patch(
            f'/movies/{target_id}', headers=self.headers, json=req_data)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], req_data['title'])
        self.assertEqual(data['movie']['release_date'],
                         req_data['release_date'])

    def test_error_patch_movies(self):
        # wrong date format
        req_data = {
            'title': 'Movie11',
            'release_date': '20000922'
        }
        target_id = Movie.query.all()[-1].id
        res = self.client().patch(
            f'/movies/{target_id}', headers=self.headers, json=req_data)
        self.assertEqual(res.status_code, 400)

    '''
        DELETE
    '''

    def test_delete_actors(self):
        # success
        target_id = Actor.query.all()[-1].id
        res = self.client().delete(
            f'/actors/{target_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_error_delete_actors(self):
        # wrong id
        target_id = -1
        res = self.client().delete(
            f'/actors/{target_id}', headers=self.headers)
        self.assertEqual(res.status_code, 404)

    def test_delete_movies(self):
        # success
        target_id = Movie.query.all()[-1].id
        res = self.client().delete(
            f'/movies/{target_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_error_delete_movies(self):
        # wrong id
        target_id = -1
        res = self.client().delete(
            f'/movies/{target_id}', headers=self.headers)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
