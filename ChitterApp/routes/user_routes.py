from flask import Blueprint, request, render_template, redirect, flash, session, jsonify
from flask_login import current_user, logout_user
import os
from redis import StrictRedis
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_TIMEOUT = int(os.environ.get('REDIS_TIMEOUT', 600))
redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)
import secrets
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.constants import timeout, all_moods, months, add_zero
import json


user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/user/<user_name>')
def user(user_name):
    session['saved_tag_number'] = 0

    if not current_user.is_authenticated:
        flash("Log in or sign up to view user profiles!", "log_in_needed")
        return redirect('/')

    key_moods = {v: k for k, v in all_moods.items()}
    mood_key = key_moods.get(current_user.current_mood)

    connection = get_flask_database_connection(user_routes)

    tags = redis.get(f"all_tags")
    if tags:
        all_tags = {int(k): v for k, v in json.loads(tags.decode('utf-8')).items()}
    else:
        tags_repo = TagRepository(connection)
        all_tags = tags_repo.get_all()
        redis.setex(f"all_tags", 7200, json.dumps(all_tags))

    user_repo = UserRepository(connection)
    v_user = user_repo.get(user_name=user_name)
    peep_repo = PeepRepository(connection)
    peeps_by_v_user = peep_repo.get(user_id=v_user.id, current_user_id=current_user.id)

    return render_template('user.html', user=current_user, v_user=v_user, moods=all_moods,
                            current_mood=mood_key, tags=all_tags, peeps=peeps_by_v_user,
                            months=months, add_zero=add_zero)


@user_routes.route('/change_mood', methods=['POST'])
def change_mood():

    if not current_user.is_authenticated:
        return jsonify(success=False, error="Something wasn't right there...")
    
    mood_value = request.form.get('mood')

    connection = get_flask_database_connection(user_routes)
    repo = UserRepository(connection)
    repo.update(current_user.id, current_mood=all_moods[int(mood_value)])

    return jsonify(success=True)


@user_routes.route('/amend_user_tags', methods=['POST'])
def amend_user_tags():
    user_data = request.form['user']
    user_dict = json.loads(user_data)

    if not current_user.is_authenticated or int(user_dict["user_id"]) != current_user.id:
        return redirect('/')
    
    no_of_tags = int(request.form['no_of_tags'])
    tags_for_user = []
    for num in range(1, no_of_tags+1):
        try:
            request.form[f'tag{num}']
            tags_for_user.append(num)
        except:
            pass

    tags_to_remove = []
    for tag in user_dict['user_tags']:
        if int(tag) not in tags_for_user:
            tags_to_remove.append(int(tag))
    
    tags_to_add = []
    for tag in tags_for_user:
        if str(tag) not in user_dict['user_tags']:
            tags_to_add.append(tag)

    connection = get_flask_database_connection(user_routes)
    user_repo = UserRepository(connection)
    user_repo.update_tags(current_user.id, tags_to_remove, tags_to_add)

    return redirect(f'/user/{current_user.user_name}')


@user_routes.route('/change_password', methods=['GET', 'POST'])
def change_password():

    if not current_user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        success = redis.get(f"{current_user.id}_success")
        if success != None and success.decode('utf-8') == "success":
            password_changed = True
        else:
            password_changed = False
        return render_template('change_password.html', user=current_user, password_changed=password_changed)

    security_check = timeout(current_user.user_name, "change_password", 5, 120)
    if security_check != True:
        flash(security_check, "cp_error")
        return redirect('/change_password')

    current_password = request.form['old_password']
    if current_password == None or current_password.strip() == "":
        flash("Enter your current password.", "cp_error")
        return redirect('/change_password')
    
    new_password = request.form['new_password']
    confirm_new_password = request.form['c_new_password']
    if new_password == None or new_password.strip() == "" or \
        confirm_new_password == None or confirm_new_password.strip() == "":
        flash("Enter your new password twice to confirm.", "cp_error")
        return redirect('/change_password')
    
    connection = get_flask_database_connection(user_routes)
    user_repo = UserRepository(connection)
    result = user_repo.update(current_user.id, current_password=current_password,
                            new_password=new_password, confirm_password=confirm_new_password)
    
    if result == None:  # Password change successful
        success = redis.setex(f"{current_user.id}_success", 3, "success")
        return redirect('/change_password')
    if '<br>' in result:
        for line in result.split('<br>'):
            flash(line, "cp_error")
    else:
        flash(result, "cp_error")
    return redirect('/change_password')


# DELETE USER ROUTE

def validate_stage_tokens(stage):
    validations = []
    for num in range(stage):
        value = redis.get(f"{current_user.id}_stage_{num+1}_auth")
        if value == None:
            validations.append(None)
        elif value.decode('utf-8') == request.form[f'stage_{num+1}_auth']:
            validations.append(value.decode('utf-8'))
        else:
            validations.append(None)
    return validations

def get_stage_token(stage):
    token = secrets.token_hex(16)
    redis.setex(f"{current_user.id}_stage_{stage}_auth", REDIS_TIMEOUT, token)
    return token

def delete_user_process(stages):

    user_id = current_user.id
    logout_user()

    connection = get_flask_database_connection(user_routes)
    user_repo = UserRepository(connection)
    result = user_repo.delete(user_id, stages)

    if result == None:
        return True
    else:  # For some kind of very unexpected error
        return False

@user_routes.route('/delete_user', methods=['GET', 'POST'])
def delete_user():

    if not current_user.is_authenticated:
        return redirect('/')

    stage = 1  # Default stage
    if request.method == 'POST':

        auth_timeout = render_template('delete_user.html', auths=[], stage=10, user=current_user)

        stage = int(request.form.get('stage', 1))

        if stage == 1:
            stages = validate_stage_tokens(1)
            if all(stages):
                return render_template('delete_user.html', auths=stages+[get_stage_token(2)], stage=2,
                                        user=current_user)
            else:
                return auth_timeout

        elif stage == 2:
            security_check = timeout(current_user.user_name, "delete_profile_password", 5, 3600)
            if security_check != True:
                return render_template('delete_user.html', auths=[], stage=11, user=current_user)
            stages = validate_stage_tokens(2)
            connection = get_flask_database_connection(user_routes)
            user_repo = UserRepository(connection)
            if all(stages) and user_repo.check_user_password(current_user.id, request.form.get('password')):
                return render_template('delete_user.html', auths=stages+[get_stage_token(3)], stage=3,
                                        user=current_user)
            elif all(stages):
                flash("Password did not match!", "cp_error")
                return render_template('delete_user.html', auths=stages, stage=2, user=current_user)
            else:
                return auth_timeout

        elif stage == 3:
            security_check = timeout(current_user.user_name, "delete_profile_d_o_b", 5, 3600)
            if security_check != True:
                return render_template('delete_user.html', auths=[], stage=11, user=current_user)
            stages = validate_stage_tokens(3)
            birth_year = request.form.get('birth_year')
            if all(stages) and birth_year.isnumeric() and int(birth_year) == current_user.d_o_b.year:
                return render_template('delete_user.html', auths=stages+[get_stage_token(4)], stage=4,
                                        user=current_user)
            elif all(stages):
                flash("Year of birth did not match!", "cp_error")
                return render_template('delete_user.html', auths=stages, stage=3, user=current_user)
            else:
                return auth_timeout

        elif stage == 4:
            security_check = timeout(current_user.user_name, "delete_profile_confirm", 5, 3600)
            if security_check != True:
                return render_template('delete_user.html', auths=[], stage=11, user=current_user)
            stages = validate_stage_tokens(4)
            confirmation = request.form['user_name_confirm']
            confirmation_message = f"I, {current_user.user_name}, confirm that I want to delete my profile."
            if all(stages) and confirmation == confirmation_message:
                result = delete_user_process(stages)
                if result:  # Successful deletion
                    return render_template('delete_user.html', auths=[], stage=5, user=current_user)
                else:  # For some kind of very unexpected error
                    return render_template('delete_user.html', auths=[], stage=7, user=current_user)
            elif all(stages):
                flash("Your final confirmation did not match!", "cp_error")
                return render_template('delete_user.html', auths=stages, stage=4, user=current_user)
            else:
                return auth_timeout
        
    return render_template('delete_user.html', auths=[get_stage_token(1)], stage=stage, user=current_user)
