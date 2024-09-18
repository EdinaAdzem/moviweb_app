from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from modelsDB import db  # Import db here

def create_app():
    app = Flask(__name__)

    # Set up configuration
    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database", "moviweb.db")}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy
    db.init_app(app)

    # Import models here to avoid circular imports
    with app.app_context():
        from modelsDB import User, Movie
        db.create_all()  # Create database tables

    # Initialize SQLiteDataManager
    data_manager = SQLiteDataManager(app)

    # routes
    @app.route('/')
    def home():
        return render_template('home_page.html')

    @app.route('/users')
    def list_users():
        users = data_manager.get_all_users()
        return render_template('users_page.html', users=users)

    @app.route('/user/<int:user_id>/movies')
    def user_movies(user_id):
        movies = data_manager.get_user_movies(user_id)
        return render_template('movies.html', movies=movies, user_id=user_id)

    @app.route('/add_user', methods=['GET', 'POST'])
    def add_user():
        if request.method == 'POST':
            user_name = request.form['name']
            data_manager.add_user({'name': user_name})
            return redirect(url_for('list_users'))
        return render_template('add_user.html')

    @app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
    def add_movie(user_id):
        if request.method == 'POST':
            title = request.form['title'].strip()
            movie_details = data_manager.fetch_movie_details(title)

            if movie_details.get('Response') == 'True':
                movie_data = {
                    'name': movie_details['Title'],
                    'director': movie_details['Director'],
                    'year': movie_details['Year'],
                    'rating': request.form['rating'] or movie_details['imdbRating'],
                    'user_id': user_id
                }
                data_manager.add_movie(movie_data)
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                error = movie_details.get('Error', 'Movie was not found.')
                return render_template('add_movie.html', user_id=user_id, error=error)

        return render_template('add_movie.html', user_id=user_id)

    @app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
    def update_movie(user_id, movie_id):
        movie = data_manager.get_movie(movie_id)
        if movie is None:
            return "Movie is not found", 404

        if request.method == 'POST':
            movie_data = {
                'name': request.form['name'] or movie.name,
                'director': request.form['director'] or movie.director,
                'year': request.form['year'] or movie.year,
                'rating': request.form['rating'] or movie.rating,
                'user_id': user_id
            }
            data_manager.update_movie(movie_id, movie_data)
            return redirect(url_for('user_movies', user_id=user_id))

        return render_template('update_movie.html', movie=movie, user_id=user_id)

    @app.route('/user/<int:user_id>/movies/delete/<int:movie_id>')
    def delete_movie(user_id, movie_id):
        data_manager.delete_movie(movie_id)
        return redirect(url_for('user_movies', user_id=user_id))

    return app

    #error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('template404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('template500.html'), 500

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
