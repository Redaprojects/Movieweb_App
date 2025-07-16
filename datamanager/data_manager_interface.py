from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """Abstract interface for movie/user data operations."""

    @abstractmethod
    def add_user(self, username: str):
        """Add a new user to the database."""
        pass

    @abstractmethod
    def get_users(self):
        """Retrieve a list of all users."""
        pass
    @abstractmethod
    def get_user(self, user_id: int):
        """Retrieve a specific user"""
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        """Delete a user by ID."""
        pass

    @abstractmethod
    def add_movie(self, user_id: int, title: str):
        """Add a favorite movie to a user."""
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, updated_data: str):
        """Update an existing movie's fields."""

    @abstractmethod
    def get_user_movies(self, user_id: int):
        """Retrieve all movies for a given user."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        """Delete a movie by ID."""
        pass

    @abstractmethod
    def get_users_with_movie_count(self):
        """Return all users along with the count of their movies."""
        pass