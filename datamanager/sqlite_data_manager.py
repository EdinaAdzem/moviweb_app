from modelsDB import db, User, Movie
from .data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.app = app

    def get_all_users(self):
        with self.app.app_context():
            return User.query.all()

    def get_user_movies(self, user_id):
        with self.app.app_context():
            return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user_data):
        with self.app.app_context():
            new_user = User(name=user_data['name'])
            db.session.add(new_user)
            db.session.commit()

    def add_movie(self, movie_data):
        with self.app.app_context():
            new_movie = Movie(
                name=movie_data['name'],
                director=movie_data['director'],
                year=movie_data['year'],
                rating=movie_data['rating'],
                user_id=movie_data['user_id']
            )
            db.session.add(new_movie)
            db.session.commit()

    def update_movie(self, movie_id, movie_data):
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                movie.name = movie_data.get('name', movie.name)
                movie.director = movie_data.get('director', movie.director)
                movie.year = movie_data.get('year', movie.year)
                movie.rating = movie_data.get('rating', movie.rating)
                db.session.commit()

    def delete_movie(self, movie_id):
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
