from datetime import datetime
from flask import Blueprint, request, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    redirect_to = redirect('/sign_up') if request.form.get('from') == "1" else redirect('/')
    if user_name == "" and password == "":
        flash("Enter your username and password.", "log_in_error")
        return redirect_to
    if user_name == "":
        flash("Enter your username.", "log_in_error")
        return redirect_to
    if password == "":
        flash("Enter your password.", "log_in_error")
        return redirect_to

    connection = get_flask_database_connection(auth)
    repo = UserRepository(connection)
    user_id = repo.user_name_password_match(user_name, password)
    if isinstance(user_id, int):  # If we got an integer, it's the user's ID, which means authentication succeeded
        user = repo.find_by_id(user_id)
        login_user(user)
        flash(f"Welcome to your Chitter, {user.user_name}!", "log_in_success")
        return redirect('/')
    else:
        flash("Something doesn't match there!", "log_in_error")
        return redirect_to
    # elif user_id == "Incorrect password.":
    #     flash("Incorrect password. Please try again.", "error")
    # elif user_id == "Username does not exist.":
    #     flash("Username does not exist. Please try again.", "error")
    # return redirect('/')


@auth.route('/logout', methods=['POST'])
def logout():
    global saved_tag_number
    saved_tag_number = 0
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
    return render_template('sign_up.html', user=current_user, ten_years_ago=ten_years_ago,
                            months=months, from_sign_up=1)


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
    result = repo.add_user(name, user_name, password, confirm_password,
                            [birth_day, birth_month, birth_year])
    
    if not isinstance(result, int):
        errors = [error for error in result.values()]
        for error in errors:
            if isinstance(error, list):
                for item in error:
                    flash(item, "sign_up_error")
            else:
                flash(error, "sign_up_error")
        return redirect('/sign_up')
        
    user = repo.find_by_id(result)
    login_user(user)
    flash(f"Welcome to your Chitter, {user.user_name}!", "log_in_success")
    return redirect('/')