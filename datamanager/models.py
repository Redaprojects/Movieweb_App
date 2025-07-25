from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class User(db.Model):
    """Represents a user of the MoviWeb app."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    movies = db.relationship('Movie', backref='user', cascade="all, delete", lazy=True)


class Movie(db.Model):
    """Represents a movie associated with a user."""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)  # star rating out of 5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='reviews')
    movie = db.relationship('Movie', backref='reviews')

    def __repr__(self):
        return f"<Review user={self.user_id} movie={self.movie_id} rating={self.rating}>"
