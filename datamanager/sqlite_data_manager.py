from sqlalchemy import func
from Movie_Web_App.datamanager.data_manager_interface import DataManagerInterface
from Movie_Web_App.datamanager.models import db, User, Movie
from flask import Flask

class SQLiteDataManager(DataManagerInterface):
    # def __init__(self, db_file_name):
    #     self.db = SQLAlchemy(db_file_name)
    #
    # """SQLite implementation of DataManagerInterface using SQLAlchemy."""
    #
    def __init__(self, db_file, app: Flask):
        """Initialize SQLite database with a Flask app."""
        self.app = app # Save app reference
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # This prevents SQLAlchemy from expiring objects after commit, so
        # new_user.name is still accessible without needing to reload.
        app.config['SQLALCHEMY_EXPIRE_ON_COMMIT'] = False

        db.init_app(app)



    # def __init__(self, app: Flask):
    #     """Initialize SQLAlchemy with a Flask app."""
    #     self.db = SQLAlchemy()
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
    #     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #     self.db.init_app(app)

    def get_users(self):
        """Return all users in the database."""
        with self.app.app_context():
            return User.query.all()


    def get_user(self, user_id):
        """Retrieve a single user by ID from the database."""
        with self.app.app_context():
            return User.query.filter_by(id=user_id).first()


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
            db.session.refresh(new_user) # # Re-attaches and reloads the instance
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


    def delete_user(self, user_id):
        """Delete a movie from the database."""
        with self.app.app_context():
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False


    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return True
            return False


    def get_users_with_movie_count(self):
        """Return all users along with the count of their movies."""
        with self.app.app_context():
            # Query users and count movies per user
            results = (
                db.session.query(
                    User,
                    func.count(Movie.id).label('movie_count')
                )
                .outerjoin(Movie, User.id == Movie.user_id)
                .group_by(User.id)
                .all()
            )
            # Return list of tuples (User, movie_count)
            return results


    def add_review(self):
        pass