from flask import Flask, render_template

from Movie_Web_App.datamanager.models import db
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
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)

# @app.route('/users/<user_id>')
# def user_movies():
#     users = data_manager.get_all_users()
#     return str(users)  # Temporarily returning users as a string
#
#
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     users = data_manager.get_all_users()
#     return str(users)  # Temporarily returning users as a string
#
#
# @app.route('/users/<user_id>/add_movie', methods=['POST'])
# def add_movie():
#     users = data_manager.get_all_users()
#     return str(users)  # Temporarily returning users as a string
#
#
# @app.route('/users/<user_id>/update_movie/<movie_id>')
# def update_movie():
#     users = data_manager.get_all_users()
#     return str(users)  # Temporarily returning users as a string
#
#
# @app.route('/users/<user_id>/delete_movie/<movie_id>')
# def delete_movie():
#     users = data_manager.get_all_users()
#     return str(users)  # Temporarily returning users as a string
#






if __name__ == '__main__':
    app.run(debug=True)