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