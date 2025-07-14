from flask import Flask, render_template, request, flash, redirect, url_for

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

    user = db.session.get(User, user_id)
    if not user:
        return f"User with ID {user_id} not found.", 404
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Display a form to add a new user and handle form submission.
    GET: Show the form.
    POST: Validate input and add the user to the database.
    """
    if request.method = 'POST':
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

# @app.route('/users/<user_id>/add_movie', methods=['POST'])
# def add_movie():
#     pass
#
# @app.route('/users/<user_id>/update_movie/<movie_id>')
# def update_movie():
#     pass

# @app.route('/users/<user_id>/delete_movie/<movie_id>')
# def delete_movie():
#     pass


if __name__ == '__main__':
    app.run(debug=True)