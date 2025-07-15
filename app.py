from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from Movie_Web_App.datamanager.models import db, User, Movie
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env into os.environ

from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

basedir = os.path.dirname(os.path.abspath(__file__)) # dirname replace it with abspath
data_dir = os.path.join(basedir, 'data')  # '..'
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, 'moviewebapp.db')

data_manager = SQLiteDataManager(db_path, app)  # Use the appropriate path to your Database

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    """
    Retrieve all users from the database to make a preview for the
    user and return it by navigating to the users template file.
    """
    users = data_manager.get_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Display all movies for a specific user, then render the HTML page and show the user's movies.
    """
    # user = db.session.get(User, user_id)
    user = User.query.get_or_404(user_id)
    if not user:
        return f"User with ID {user_id} not found.", 404
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Display a form to add a new user and handle form submission.
    If the method is a POST, validate the input and add the user to the database.
    Otherwise, it returns a get and shows the form.
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()

        # Validate name input
        if not name:
            flash("User name is required.", "error")
            return render_template('add_user.html')

        # Save user
        new_user = data_manager.add_user({'name': name})
        flash(f"User '{new_user.name}' added successfully!", "success")
        return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Display form to add a movie (GET) and handle submission (POST).
    It returns a GET-rendered form.
    Otherwise, a POST request: Redirect to the user's movie page.
    """
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        rating = request.form.get('rating', '').strip()

        # Input validation
        if not name or not director or not year or not rating:
            flash('All fields are required!', 'error')
        elif not year.isdigit() or not (1800 <= int(year) <= 2100):
            flash('Year must be a valid number between 1800 and 2100.', 'error')
        elif not rating.replace('.', '', 1).isdigit() or not (0 <= float(rating) <= 10):
            flash('Rating must be a number between 0 and 10.', 'error')
        else:
            movie_data = {
                'name': name,
                'director': director,
                'year': int(year),
                'rating': float(rating)
            }
            data_manager.add_movie(user_id, movie_data)
            flash(f'Movie "{name}" added successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user)
#
# @app.route('/users/<user_id>/update_movie/<movie_id>')
# def update_movie():
@app.route('/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """
    Show the edit form (GET) and handle the update logic (POST).
    Then return: Rendered form or redirect after successful update.
    """
    movie = Movie.query.get_or_404(movie_id)
    user_id = movie.user_id

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        rating = request.form.get('rating', '').strip()

        # Validation
        if not name or not director or not year or not rating:
            flash('All fields are required.', 'error')
        elif not year.isdigit() or not (1800 <= int(year) <= 2100):
            flash('Year must be between 1800 and 2100.', 'error')
        elif not rating.replace('.', '', 1).isdigit() or not (0 <= float(rating) <= 10):
            flash('Rating must be a number between 0 and 10.', 'error')
        else:
            updated_data = {
                'name': name,
                'director': director,
                'year': int(year),
                'rating': float(rating)
            }
            data_manager.update_movie(movie_id, updated_data)
            flash('Movie updated successfully.', 'success')
            return redirect(url_for('user_movies', user_id=user_id))

    return render_template('edit_movie.html', movie=movie)


# @app.route('/users/<user_id>/delete_movie/<movie_id>')
@app.route('/movies/<int:movie_id>/delete', methods=['GET', 'POST'])
def delete_movie(movie_id):
    """
    Confirm and delete a movie from the database based on the movie ID,
    then return to the user's movie list after deletion.
    """
    movie = Movie.query.get_or_404(movie_id)
    user_id = movie.user_id

    if request.method == 'POST':
        data_manager.delete_movie(movie_id)
        flash(f'Movie "{movie.name}" has been deleted.', 'success')
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('confirm_delete.html', movie=movie)


@app.errorhandler(404)
def page_not_found(e):
    """Render custom page when a route is not found (404)."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Render custom page for internal server errors (500)."""
    return render_template('500.html'), 500


@app.route('/users/<int:user_id>')
def view_user(user_id):
    try:
        user = data_manager.get_user(user_id)
        if not user:
            flash("User not found.", "warning")
            return redirect(url_for('home'))
        return render_template('user_detail.html', user=user)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)