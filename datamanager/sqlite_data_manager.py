from flask import current_app
from modelsDB import db, User, Movie
import requests


class SQLiteDataManager:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app


    def get_all_users(self):
        """gets all users available in the db"""
        with current_app.app_context():
            return User.query.all()


    def get_user_movies(self, user_id):
        """fetches user movies"""
        with current_app.app_context():
            user = User.query.get(user_id)
            return user.movies if user else []


    def add_user(self, user_data):
        """add the users to the moviweb.db"""
        with current_app.app_context():
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()

    def add_movie(self, movie_data):
        """adding a movie with error handling"""
        try:
            with current_app.app_context():
                movie = Movie(**movie_data)
                db.session.add(movie)
                db.session.commit()
        except Exception as e:
            print(f"An error occurred while adding a movie: {e}")
            db.session.rollback()


    def get_movie(self, movie_id):
        """gets the user movies"""
        with current_app.app_context():
            movie = Movie.query.get(movie_id)
            return movie if movie else None


    def update_movie(self, movie_id, movie_data):
        """udpates movie, passes id """
        with current_app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                for key, value in movie_data.items():
                    setattr(movie, key, value)
                db.session.commit()


    def delete_movie(self, movie_id):
        """delete movie"""
        with current_app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()


    def fetch_movie_details(self, title):
        """handles fetching of movie detials from the api, passed title as param"""
        api_key = 'c3bb5c1c'
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {}