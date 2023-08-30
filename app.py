import os
from flask import Flask, request, redirect, render_template, flash
from lib.database_connection import get_flask_database_connection
from flask_login import LoginManager, login_user, logout_user, current_user
from lib.user_repository import *
from lib.peep_repository import *
from lib.tag_repository import *


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.jinja_env.autoescape = True

login_manager = LoginManager()
login_manager.init_app(app)
all_moods = {1:'content', 2:'excited', 3:'fabulous'}


@login_manager.user_loader
def load_user(user_id):
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    return repo.find_by_id(user_id)


@app.route('/')
def home():
    connection = get_flask_database_connection(app)
    repo = TagRepository(connection)
    all_tags = repo.get_all()
    current_tag_no = 9
    current_mood = 2
    return render_template('index.html', tags=all_tags, current_tag_no=current_tag_no,
                            moods=all_moods, current_mood=current_mood,
                            user_is_logged_in=current_user.is_authenticated, user=current_user)


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    if user_name == "" and password == "":
        flash("Enter your username and password.", "error")
        return redirect('/')
    if user_name == "":
        flash("Enter your username.", "error")
        return redirect('/')
    if password == "":
        flash("Enter your password.", "error")
        return redirect('/')

    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    user_id = repo.user_name_password_match(user_name, password)
    
    if isinstance(user_id, int):  # If we got an integer, it's the user's ID, which means authentication succeeded
        user = repo.find_by_id(user_id)
        login_user(user)
        flash(f"Welcome to your Chitter, {user.user_name}!", "success")
        return redirect('/')
    elif user_id == "Incorrect password.":
        flash("Incorrect password. Please try again.", "error")
    elif user_id == "Username does not exist.":
        flash("Username does not exist. Please try again.", "error")
    return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
