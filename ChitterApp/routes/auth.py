from datetime import datetime
from flask import Blueprint, request, render_template, redirect, flash, session
from flask_login import current_user, login_user, logout_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.models.user import User
import os
from redis import StrictRedis
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_TIMEOUT = int(os.environ.get('REDIS_TIMEOUT', 120))
redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():

    redirect_to = redirect('/sign_up') if request.form.get('from') == "1" else redirect('/')

    user_name = request.form.get('user_name')

    if redis.get(f"{user_name}_password_attempt") == None:
        redis.setex(f"{user_name}_password_attempt", REDIS_TIMEOUT, 1)
    else:
        attempts = int(redis.get(f"{user_name}_password_attempt").decode('utf-8'))
        attempts += 1
        if attempts >= 5:
            flash("Too many tries! Wait 2 minutes.", "log_in_error")
            return redirect_to
        redis.setex(f"{user_name}_password_attempt", REDIS_TIMEOUT, attempts)

    password = request.form.get('password')

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
    user = repo.user_name_password_match(user_name, password)

    if isinstance(user, User):
        login_user(user)
        flash(f"Welcome to your Chitter, {user.user_name}!", "log_in_success")
        return redirect('/')
    else:
        flash("Something doesn't match there!", "log_in_error")
        return redirect_to


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
    user = repo.create(name, user_name, password, confirm_password,
                            [birth_day, birth_month, birth_year])
    
    if not isinstance(user, User):
        errors = [error for error in user.values()]
        for error in errors:
            if isinstance(error, list):
                for item in error:
                    flash(item, "sign_up_error")
            else:
                flash(error, "sign_up_error")
        return redirect('/sign_up')
        
    login_user(user)
    flash(f"Welcome to your Chitter, {user.user_name}!", "log_in_success")
    return redirect('/')
