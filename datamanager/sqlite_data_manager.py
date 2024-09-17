from flask import current_app
from modelsDB import db, User, Movie


class SQLiteDataManager:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def get_all_users(self):
        with current_app.app_context():
            return User.query.all()

    def get_user_movies(self, user_id):
        with current_app.app_context():
            user = User.query.get(user_id)
            return user.movies if user else []

    def add_user(self, user_data):
        with current_app.app_context():
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()

    def add_movie(self, movie_data):
        with current_app.app_context():
            movie = Movie(**movie_data)
            db.session.add(movie)
            db.session.commit()

    def get_movie(self, movie_id):
        with current_app.app_context():
            return Movie.query.get(movie_id)

    def update_movie(self, movie_id, movie_data):
        with current_app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                for key, value in movie_data.items():
                    setattr(movie, key, value)
                db.session.commit()

    def delete_movie(self, movie_id):
        with current_app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
