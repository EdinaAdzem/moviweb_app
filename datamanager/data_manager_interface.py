from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Retrieve all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies for a given user."""
        pass

    @abstractmethod
    def add_movie(self, movie_data):
        """Add a new movie to the database."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, movie_data):
        """Update an existing movie."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        pass
