# Libraries
import os
import unittest
import json

# Modules
from app import create_app
from models import setup_db


class CinemaTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        # define test variables and initialize app
        self.database_path = os.environ.get('DATABASE_URL')
        test_jwt = os.environ.get('TEST_JWT')
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.headers = { 'Authorization': test_jwt }

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test GET /actors - success
    def test_get_actors_success(self):
        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('actors' in data)
        actors = data['actors']
        self.assertTrue(isinstance(actors, list))
        for actor in actors:
            self.assertTrue(isinstance(actor, dict))

    # Test GET /actors - fail
    def test_get_actors_fail(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])

    # Test GET /actors/1 - success
    def test_get_single_actor_success(self):
        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)
        actors = data['actors']
        self.assertTrue(len(actors) > 0)
        actor_id = actors[0]['id']

        response = self.client().get(f'/actors/{actor_id}', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('actor' in data)
        actor = data['actor']
        self.assertTrue(isinstance(actor, dict))

    # Test GET /actors - fail
    def test_get_single_actor_fail(self):
        response = self.client().get('/actors/a', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Test POST /actors - success
    def test_post_actors_success(self):
        body = {
            "firstname": "Carla",
            "lastname": "Rossi",
            "stagename": "Malesia",
            "gender": "female",
            "birthdate": "1999-01-01"
        }
        res = self.client().post('/actors', headers=self.headers, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['created'])

    # Test POST /actors - fail
    def test_post_actors_fail(self):
        body = {
            "bad": "property"
        }
        res = self.client().post('/actors', headers=self.headers, json=body)
        self.assertEqual(res.status_code, 400)

    # Test PATCH /actors/1 - success
    def test_patch_actor_success(self):
        # get an existing ID
        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)
        actors = data['actors']
        self.assertTrue(len(actors) > 0)
        actor_id = actors[0]['id']

        # make the patch request
        body = {
            "stagename": "Malesia",
            "gender": "female"
        }
        response = self.client().patch(f'/actors/{actor_id}', headers=self.headers, json=body)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Test PATCH /actors - fail
    def test_patch_actor_fail(self):
        response = self.client().patch('/actors/a', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Test DELETE /actors - success
    def test_delete_actor_success(self):
        # create a new element
        body = {
            "firstname": "Carla",
            "lastname": "Rossi",
            "stagename": "Malesia",
            "gender": "female",
            "birthdate": "1999-01-01"
        }
        res = self.client().post('/actors', headers=self.headers, json=body)
        data = json.loads(res.data)
        actor_id = data['created']

        # delete the newly created element
        res = self.client().delete('/actors/' + str(actor_id), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['delete'])

    # Test DELETE /actors - fail
    def test_delete_actor_fail(self):
        response = self.client().delete('/actors/a')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])


    # Test GET /movies - success
    def test_get_movies_success(self):
        response = self.client().get('/movies', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movies' in data)
        movies = data['movies']
        self.assertTrue(isinstance(movies, list))
        for movie in movies:
            self.assertTrue(isinstance(movie, dict))

    # Test GET /movies - fail
    def test_get_movies_fail(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])

    # Test GET /movies/1 - success
    def test_get_single_movie_success(self):
        response = self.client().get('/movies', headers=self.headers)
        data = json.loads(response.data)
        movies = data['movies']
        self.assertTrue(len(movies) > 0)
        movie_id = movies[0]['id']

        response = self.client().get(f'/movies/{movie_id}', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movie' in data)
        movie = data['movie']
        self.assertTrue(isinstance(movie, dict))

    # Test GET /movies - fail
    def test_get_single_movie_fail(self):
        response = self.client().get('/movies/a', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Test POST /movies - success
    def test_post_movie_success(self):
        body = {
            "title": "Orange Juice 2",
            "genre": "Comedy",
            "year": 2024,
            "duration": 120
        }
        res = self.client().post('/movies', headers=self.headers, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['created'])

    # Test POST /movies - fail
    def test_post_movie_fail(self):
        body = {
            "bad": "property"
        }
        res = self.client().post('/movies', headers=self.headers, json=body)
        self.assertEqual(res.status_code, 400)

    # Test PATCH /movies/1 - success
    def test_patch_movie_success(self):
        # get an existing ID
        response = self.client().get('/movies', headers=self.headers)
        data = json.loads(response.data)
        movies = data['movies']
        self.assertTrue(len(movies) > 0)
        movie_id = movies[0]['id']

        # make the patch request
        body = {
            "title": "Apple Pie",
            "genre": "Adventure"
        }
        response = self.client().patch(f'/movies/{movie_id}', headers=self.headers, json=body)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Test PATCH /movies - fail
    def test_patch_movie_fail(self):
        response = self.client().patch('/movies/a', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Test DELETE /movies - success
    def test_delete_movie_success(self):
        # create a new element
        body = {
            "title": "Orange Juice 2",
            "genre": "Comedy",
            "year": 2024,
            "duration": 120
        }
        res = self.client().post('/movies', headers=self.headers, json=body)
        data = json.loads(res.data)
        movie_id = data['created']

        # delete the newly created element
        res = self.client().delete('/movies/' + str(movie_id), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['delete'])

    # Test DELETE /movies - fail
    def test_delete_movie_fail(self):
        response = self.client().delete('/movies/a')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
