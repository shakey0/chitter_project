from datetime import datetime
from flask import Blueprint, request, render_template, redirect, jsonify, flash, session
from flask_login import current_user, login_user, logout_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.models.user import User
from ChitterApp.constants import timeout


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():

    user_name = request.form.get('user_name')

    security_check = timeout(user_name, "password", 5, 120)
    if security_check != True:
        return jsonify(success=False, error=security_check)

    password = request.form.get('password')

    if user_name == "" and password == "":
        return jsonify(success=False, error="Enter your username and password.")
    if user_name == "":
        return jsonify(success=False, error="Enter your username.")
    if password == "":
        return jsonify(success=False, error="Enter your password.")

    connection = get_flask_database_connection(auth)
    repo = UserRepository(connection)
    user = repo.user_name_password_match(user_name, password)

    if isinstance(user, User):
        login_user(user)
        return jsonify(success=True, message=f"Welcome to your Chitter, {user.user_name}!")
    else:
        return jsonify(success=False, error="Something doesn't match there!")


@auth.route('/logout', methods=['POST'])
def logout():
    session['saved_tag_number'] = 0
    logout_user()
    return redirect('/')


@auth.route('/sign_up')
def sign_up():
    if current_user.is_authenticated:
        return redirect('/')
    current_year = datetime.now().year
    ten_years_ago = current_year - 9
    months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
    return render_template('sign_up.html', user=current_user, ten_years_ago=ten_years_ago, months=months)


@auth.route('/sign_up_user', methods=['POST'])
def sign_up_user():

    name = request.form['name']
    user_name = request.form['user_name']
    password = request.form['password']
    confirm_password = request.form['c_password']
    birth_day = int(request.form['birth_day'])
    birth_month = request.form['birth_month']
    birth_year = int(request.form['birth_year'])

    connection = get_flask_database_connection(auth)
    repo = UserRepository(connection)
    user = repo.create(name, user_name, password, confirm_password,
                            [birth_day, birth_month, birth_year])
    
    if not isinstance(user, User):
        print(user)
        return jsonify(success=False, errors=user)
        
    login_user(user)
    return jsonify(success=True, message=f"Welcome to your Chitter, {user.user_name}!")
