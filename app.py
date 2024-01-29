# Libraries
import os
import json
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

# App Modules
from models import setup_db, Actor, Movie
from auth import requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS configuration using after_request
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,PATCH,DELETE'
        )
        return response

    # GET /actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        try:
            # get results from db
            actors = Actor.query.order_by(Actor.id).all()

            # return results as json
            return jsonify({
                'success': True,
                'total': len(actors),
                'actors': [ actor.short() for actor in actors ]
            })
        except Exception as error:
            # internal server error
            print(f'GET /actors error: {error}')
            abort(500)
    
    # GET /actors/<actor_id>
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_detail(actor_id):
        # check if the actor with the given ID exists
        actor = Actor.query.get(actor_id)

        if actor is None:
            # not found
            abort(404, 'Actor not found')
        
        try:
            return jsonify({
                'success': True,
                'actor': actor.long()
            })
        except Exception as error:
            # internal server error
            print(f'GET /actors/{actor_id} error: {error}')
            abort(500)

    # POST /actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors():
        # get body
        body = request.get_json()
        if body is None:
            abort(422)
        
        # check for mandatory parameters
        missing_params = [
            param for param in [
                'firstname', 'lastname', 'birthdate'
            ] if param not in body
        ]
        if missing_params:
            abort(400, f'Bad Request - Missing required parameters: {", ".join(missing_params)}')

        try:
            # get body parameters
            firstname = body.get('firstname', None)
            lastname = body.get('lastname', None)
            stagename = body.get('stagename', None)
            gender = body.get('gender', None)
            birthdate = body.get('birthdate', None)

            # add actor
            actor = Actor(
                firstname=firstname,
                lastname=lastname,
                stagename=stagename,
                gender=gender,
                birthdate=birthdate
            )
            actor.insert()

            # created
            return jsonify({
                'created': actor.id
            }), 201
        except Exception as error:
            # internal server error
            print(f'POST /actors error: {error}')
            abort(500)
    
    # PATCH /actors/<actor_id>
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(actor_id):
        # check if the actor with the given ID exists
        actor = Actor.query.get(actor_id)

        if actor is None:
            # not found
            abort(404, 'Actor not found')
        
        # get the data for update
        data = request.get_json()
        if data is None:
            abort(400, 'The body is empty or incorrect.')

        try:
            # update the actor
            if 'stagename' in data:
                actor.stagename = data['stagename']
            if 'gender' in data:
                actor.gender = data['gender']

            # commit the changes to the database
            actor.update()

            # ok
            return jsonify({
                'success': True,
                'actor': actor.long()
            }), 200
        except Exception as error:
            print(f'PATCH /actors/{actor_id} - error: {error}')

            # Return internal server error
            abort(500)
    
    # DELETE /actors/<actor_id>
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(actor_id):
        # check if the actor with the given ID exists
        actor = Actor.query.get(actor_id)

        if actor is None:
            # not found
            abort(404, 'Actor not found')
        
        try:
            # commit the changes to the database
            actor.delete()

            # ok
            return jsonify({
                'success': True,
                'delete': actor_id
            }), 200
        except Exception as error:
            print(f'DELETE /actors/{actor_id} - error: {error}')

            # internal server error
            abort(500)
    
    # GET /movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        try:
            # get results from db
            movies = Movie.query.order_by(Movie.id).all()

            # return results as json
            return jsonify({
                'success': True,
                'total': len(movies),
                'movies': [ movie.short() for movie in movies ]
            })
        except Exception as error:
            # internal server error
            print(f'GET /movies error: {error}')
            abort(500)
    
    # GET /movies/<movie_id>
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_detail(movie_id):
        # check if the movie with the given ID exists
        movie = Movie.query.get(movie_id)

        if movie is None:
            # not found
            abort(404, 'Movie not found')
        
        try:
            return jsonify({
                'success': True,
                'movie': movie.long()
            })
        except Exception as error:
            # internal server error
            print(f'GET /movies/{movie_id} error: {error}')
            abort(500)

    # POST /movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies():
        # get body
        body = request.get_json()
        if body is None:
            abort(422)
        
        # check for mandatory parameters
        missing_params = [
            param for param in [
                'title', 'year', 'duration'
            ] if param not in body
        ]
        if missing_params:
            abort(400, f'Bad Request - Missing required parameters: {", ".join(missing_params)}')

        try:
            # get body parameters
            title = body.get('title', None)
            genre = body.get('genre', None)
            year = body.get('year', None)
            duration = body.get('duration', None)

            # add movie
            movie = Movie(
                title=title,
                genre=genre,
                year=year,
                duration=duration
            )
            movie.insert()

            # created
            return jsonify({
                'created': movie.id
            }), 201
        except Exception as error:
            # internal server error
            print(f'POST /movies error: {error}')
            abort(500)
    
    # PATCH /movies/<movie_id>
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(movie_id):
        # check if the movie with the given ID exists
        movie = Movie.query.get(movie_id)

        if movie is None:
            # not found
            abort(404, 'Movie not found')
        
        # get the data for update
        data = request.get_json()
        if data is None:
            abort(400, 'The body is empty or incorrect.')

        try:
            # update the movie
            if 'title' in data:
                movie.title = data['title']
            if 'genre' in data:
                movie.genre = data['genre']

            # commit the changes to the database
            movie.update()

            # ok
            return jsonify({
                'success': True,
                'movie': movie.long()
            }), 200
        except Exception as error:
            print(f'PATCH /movies/{movie_id} - error: {error}')

            # Return internal server error
            abort(500)
    
    # DELETE /movies/<movie_id>
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(movie_id):
        # check if the movie with the given ID exists
        movie = Movie.query.get(movie_id)

        if movie is None:
            # not found
            abort(404, 'Movie not found')
        
        try:
            # commit the changes to the database
            movie.delete()

            # ok
            return jsonify({
                'success': True,
                'delete': movie_id
            }), 200
        except Exception as error:
            print(f'DELETE /movies/{movie_id} - error: {error}')

            # internal server error
            abort(500)
    
    # GET /
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = 'Hello' 
        if excited == 'true': 
            greeting = greeting + '!!!!! You are doing great in this Udacity project.'
        return greeting

    # GET /coolkids
    @app.route('/coolkids')
    def be_cool():
        return 'Be cool, man, be coooool! You''re almost a FSND grad!'


    # Error Handlers

    # 401 Error Handler
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': json.dumps(error)
        }), 401
    
    # 403 Error Handler
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': json.dumps(error)
        }), 403

    # 404 Error Handler
    @app.errorhandler(404)
    def not_found(error):
        print(error)
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    # 405 Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(error):
        print(error)
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    # 422 Error Handler
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    # 500 Error Handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': str(error)
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
