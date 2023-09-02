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
all_moods = {1:'content', 2:'excited', 3:'fabulous', 4:'angry', 5:'let down',
            6:'lucky', 7:'anxious', 8:'worried', 9:'scared', 10:'sad',
            11:'calm', 12:'buzzing', 13:'happy', 14:'okay', 15:'bored'}
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
        7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

def add_zero(number):
    if len(str(number)) == 1:
        return f"0{number}"
    return str(number)





@login_manager.user_loader
def load_user(user_id):
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    return repo.find_by_id(user_id)


@app.route('/')
def home():
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    all_users = user_repo.get_all()
    peep_repo = PeepRepository(connection)
    all_peeps = peep_repo.get_all()
    tags_repo = TagRepository(connection)
    all_tags = tags_repo.get_all()
    current_tag_no = request.args.get('by_tag')
    if current_tag_no == None:
        current_tag_no = 0
    if current_user.is_authenticated:
        key_moods = {v: k for k, v in all_moods.items()}
        mood_key = key_moods.get(current_user.current_mood)
        liked = peep_repo.does_user_like_peep
    else:
        mood_key = 1
        liked = False
    user_id_to_user_name = {user.id:user.user_name for user in all_users}
    return render_template('index.html', tags=all_tags, current_tag_no=int(current_tag_no),
                            moods=all_moods, current_mood=mood_key,
                            user_is_logged_in=current_user.is_authenticated, user=current_user,
                            peeps=all_peeps, users=user_id_to_user_name, months=months,
                            add_zero=add_zero, liked=liked)


@app.route('/like', methods=['POST'])
def reverse_like():
    user_id = request.form['user_id']
    peep_id = request.form['peep_id']
    connection = get_flask_database_connection(app)
    peep_repo = PeepRepository(connection)
    peep_repo.update_likes(user_id, peep_id)
    return redirect('/')


@app.route('/change_mood', methods=['POST'])
def change_mood():
    mood_value = request.form.get('mood')
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    repo.update(current_user.id, current_mood=all_moods[int(mood_value)])
    return redirect('/')

'''
@app.route('/view_tags_by', methods=['POST'])
def view_tags_by():
'''


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


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
