from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie
from data_manager_interface import DataManagerInterface
from flask import Flask

class SQLiteDataManager(DataManagerInterface):
    # def __init__(self, db_file_name):
    #     self.db = SQLAlchemy(db_file_name)
    #
    """SQLite implementation of DataManagerInterface using SQLAlchemy."""

    def __init__(self, app: Flask):
        """Initialize SQLite database with a Flask app."""
        self.app = app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

        with app.app_context():
            db.create_all()


    def get_all_users(self):
        """Return all users in the database."""
        with self.app.app_context():
            return User.query.all()


    def get_user_movies(self, user_id):
        """Return all movies for the given user."""
        with self.app.app_context():
            return Movie.query.filter_by(user_id=user_id).all()


    def add_user(self, user):
        """Add a new user to the database."""
        with self.app.app_context():
            new_user = User(name=user['name'])
            db.session.add(new_user)
            db.session.commit()
            return new_user


    def add_movie(self, user_id, movie):
        """Add a new movie for a specific user."""
        with self.app.app_context():
            new_movie = Movie(
                name=movie['name'],
                director=movie['director'],
                year=movie['year'],
                rating=movie['rating'],
                user_id=user_id
            )
            db.session.add(new_movie)
            db.session.commit()
            return new_movie


    def update_movie(self, movie_id, updated_data):
        """Update an existing movie's fields."""
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if not movie:
                return None
            for key, value in updated_data.items():
                setattr(movie, key, value)
            db.session.commit()
            return movie


    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return True
            return False
