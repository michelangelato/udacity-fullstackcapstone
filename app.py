# Libraries
import os
import json
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

# App Modules
from models import setup_db
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
    # @TODO
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        return jsonify({
            'success': True,
            'actors': []
        })
    
    # POST /actors
    # @TODO
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors():
        return None
    
    # PATCH /actors/<actor_id>
    # @TODO
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(actor_id):
        return None
    
    # DELETE /actors/<actor_id>
    # @TODO
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(actor_id):
        return None
    
    # GET /movies
    # @TODO
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        return jsonify({
            'success': True,
            'movies': []
        })
    
    # POST /movies
    # @TODO
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies():
        return None
    
    # PATCH /movies/<movie_id>
    # @TODO
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(movie_id):
        return None
    
    # DELETE /movies/<movie_id>
    # @TODO
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(movie_id):
        return None
    
    # GET /
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    # GET /coolkids
    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"


    # Error Handlers

    # 401 Error Handler
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": json.dumps(error)
        }), 401
    
    # 403 Error Handler
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": json.dumps(error)
        }), 403

    # 404 Error Handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    # 422 Error Handler
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # 500 Error Handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": str(error)
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
