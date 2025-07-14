from flask import Flask, render_template, request, flash, redirect, url_for, or_

from Movie_Web_App.datamanager.models import db, User, Movie
import os

from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)

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
def add_movie():
    """
    Display form to add a movie (GET) and handle submission (POST).
    Args:
    user_id (int): ID of the user adding a movie.
    Returns:
    On GET: Rendered form.
    On POST: Redirect to user's movie page.
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
#     pass

# @app.route('/users/<user_id>/delete_movie/<movie_id>')
# def delete_movie():
#     pass


if __name__ == '__main__':
    app.run(debug=True)