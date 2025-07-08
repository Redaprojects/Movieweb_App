from flask import Flask
from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    # data_manager_interface.py
    from abc import ABC, abstractmethod

    class DataManagerInterface(ABC):
        """Abstract interface for all data managers."""

        @abstractmethod
        def get_all_users(self):
            """Return a list of all users."""
            pass

        @abstractmethod
        def get_user_movies(self, user_id):
            """Return a list of all movies for a given user."""
            pass

        @abstractmethod
        def add_user(self, user):
            """Add a new user."""
            pass

        @abstractmethod
        def add_movie(self, user_id, movie):
            """Add a new movie to a user's list."""
            pass

        @abstractmethod
        def update_movie(self, movie_id, updated_data):
            """Update the details of a specific movie."""
            pass

        @abstractmethod
        def delete_movie(self, movie_id):
            """Delete a movie from the database."""
            pass
