from flask import Blueprint, current_app, request, render_template, redirect, flash, session, jsonify
from flask_login import current_user, logout_user
import os
from redis import StrictRedis
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_TIMEOUT = int(os.environ.get('REDIS_TIMEOUT', 600))
redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.lib.repositories.peeps_images_repository import PeepsImagesRepository
from ChitterApp.constants import all_moods, months, add_zero


user_routes = Blueprint('user_routes', __name__)

limiter = Limiter(key_func=get_remote_address)


@user_routes.route('/user/<user_name>')
def user(user_name):
    session['saved_tag_number'] = 0

    if not current_user.is_authenticated:
        flash("Log in or sign up to view user profiles!", "log_in_error")
        return redirect('/')

    connection = get_flask_database_connection(user_routes)

    key_moods = {v: k for k, v in all_moods.items()}
    mood_key = key_moods.get(current_user.current_mood)

    user_repo = UserRepository(connection)
    viewing_user = user_repo.find_by_user_name(user_name)

    tags_repo = TagRepository(connection)
    all_tags = tags_repo.get_all()
    v_user_tags = []
    for tag in all_tags:
        if tags_repo.does_user_favour_tag(viewing_user.id, tag):
            v_user_tags.append(tag)

    peep_repo = PeepRepository(connection)
    all_peeps_by_v_user = peep_repo.get_all_by_user(viewing_user.id)
    liked = peep_repo.does_user_like_peep

    peeps_images_repo = PeepsImagesRepository(connection)
    peep_images = {}
    for peep in all_peeps_by_v_user:
        image_ids = peep.images
        if len(image_ids) > 0:
            image_file_names = [peeps_images_repo.get_image_file_name(image_id) for image_id in image_ids]
            peep_images[peep.id] = image_file_names

    return render_template('user.html', user=current_user, v_user=viewing_user, moods=all_moods,
                            current_mood=mood_key, tags=all_tags, v_user_tags=v_user_tags,
                            peeps=all_peeps_by_v_user, months=months, add_zero=add_zero,
                            liked=liked, images=peep_images)


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
    if not current_user.is_authenticated:
        return redirect('/')

    connection = get_flask_database_connection(user_routes)
    tags_repo = TagRepository(connection)
    tags = tags_repo.get_all()
    for num in range(1, len(tags)+1):
        try:
            request.form[f'tag{num}']
            tags_repo.add_tag_to_user(current_user.id, num)
        except:
            tags_repo.remove_tag_from_user(current_user.id, num)
    return redirect(f'/user/{current_user.user_name}')


@user_routes.route('/change_password', methods=['GET', 'POST'])
@limiter.limit("12 per minute")
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
    if isinstance(result, list):
        for error in result:
            flash(error, "cp_error")
    else:
        flash(result, "cp_error")
    return redirect('/change_password')


@user_routes.route('/delete_user', methods=['GET', 'POST'])
@limiter.limit("12 per minute")
def delete_user():
    if not current_user.is_authenticated:
        return redirect('/')

    stage = 1  # Default stage
    if request.method == 'POST':
        connection = get_flask_database_connection(user_routes)
        user_repo = UserRepository(connection)

        stage = int(request.form.get('stage', 1))
        if stage == 1:
            try:
                stage_1_auth = redis.get(f"{current_user.id}_stage_1_auth").decode('utf-8')
            except AttributeError:
                return render_template('delete_user.html', auths=[], stage=10, user=current_user)

            stages_valid = stage_1_auth == request.form['stage_1_auth']

            if stages_valid:
                stage_2_auth = secrets.token_hex(16)
                redis.setex(f"{current_user.id}_stage_2_auth", REDIS_TIMEOUT, stage_2_auth)
                return render_template('delete_user.html', auths=[stage_1_auth, stage_2_auth],
                                        stage=2, user=current_user)

        elif stage == 2:
            try:
                stage_1_auth = redis.get(f"{current_user.id}_stage_1_auth").decode('utf-8')
                stage_2_auth = redis.get(f"{current_user.id}_stage_2_auth").decode('utf-8')
            except AttributeError:
                return render_template('delete_user.html', auths=[], stage=10, user=current_user)

            stages_valid = stage_1_auth == request.form['stage_1_auth'] and stage_2_auth == request.form['stage_2_auth']

            if stages_valid and user_repo.check_user_password(current_user.id, request.form.get('password')):
                stage_3_auth = secrets.token_hex(16)
                redis.setex(f"{current_user.id}_stage_3_auth", REDIS_TIMEOUT, stage_3_auth)
                return render_template('delete_user.html', auths=[stage_1_auth, stage_2_auth, stage_3_auth],
                                        stage=3, user=current_user)
            elif stages_valid:
                flash("Password did not match!", "cp_error")
                return render_template('delete_user.html', auths=[stage_1_auth, stage_2_auth],
                                        stage=2, user=current_user)

        elif stage == 3:
            try:
                stage_1_auth = redis.get(f"{current_user.id}_stage_1_auth").decode('utf-8')
                stage_2_auth = redis.get(f"{current_user.id}_stage_2_auth").decode('utf-8')
                stage_3_auth = redis.get(f"{current_user.id}_stage_3_auth").decode('utf-8')
            except AttributeError:
                return render_template('delete_user.html', auths=[], stage=10, user=current_user)

            stages_valid = stage_1_auth == request.form['stage_1_auth'] and stage_2_auth == request.form['stage_2_auth'] \
            and stage_3_auth == request.form['stage_3_auth']

            birth_year = request.form.get('birth_year')

            if stages_valid and birth_year.isnumeric() and int(birth_year) == current_user.d_o_b.year:
                stage_4_auth = secrets.token_hex(16)
                redis.setex(f"{current_user.id}_stage_4_auth", REDIS_TIMEOUT, stage_4_auth)
                return render_template('delete_user.html', auths=[stage_1_auth, stage_2_auth, stage_3_auth, stage_4_auth],
                                        stage=4, user=current_user)
            elif stages_valid:
                flash("Year of birth did not match!", "cp_error")
                return render_template('delete_user.html', auths=[stage_1_auth, stage_2_auth, stage_3_auth],
                                        stage=3, user=current_user)

        elif stage == 4:
            try:
                stage_1_auth = redis.get(f"{current_user.id}_stage_1_auth").decode('utf-8')
                stage_2_auth = redis.get(f"{current_user.id}_stage_2_auth").decode('utf-8')
                stage_3_auth = redis.get(f"{current_user.id}_stage_3_auth").decode('utf-8')
                stage_4_auth = redis.get(f"{current_user.id}_stage_4_auth").decode('utf-8')
            except AttributeError:
                return render_template('delete_user.html', auths=[], stage=10, user=current_user)

            stages_valid = stage_1_auth == request.form['stage_1_auth'] and stage_2_auth == request.form['stage_2_auth'] \
            and stage_3_auth == request.form['stage_3_auth'] and stage_4_auth == request.form['stage_4_auth']

            confirmation = request.form['user_name_confirm']
            confirmation_message = f"I, {current_user.user_name}, confirm that I want to delete my profile."

            if stages_valid and confirmation == confirmation_message:
                
                user_id = current_user.id
                logout_user()

                peep_repo = PeepRepository(connection)
                peeps_by_user = peep_repo.get_all_by_user(user_id)

                all_images_from_user = []
                for peep in peeps_by_user:
                    image_ids = peep_repo.find_by_id(peep.id).images
                    image_file_names = []
                    if len(image_ids) > 0:
                        peeps_images_repo = PeepsImagesRepository(connection)
                        image_file_names = [peeps_images_repo.get_image_file_name(image_id) for image_id in image_ids]
                        all_images_from_user += image_file_names

                result = user_repo.delete(user_id)

                if result == None:
                    if len(all_images_from_user) > 0:
                        all_images = peeps_images_repo.get_all()
                        all_file_names = [image['file_name'] for image in all_images]
                        for image in all_images_from_user:
                            if image not in all_file_names:
                                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
                                os.remove(file_path)
                    return render_template('delete_user.html', auths=[], stage=5, user=current_user)
                else:  # For some kind of very unexpected error
                    return render_template('delete_user.html', auths=[], stage=7, user=current_user)

            elif stages_valid:
                flash("Your final confirmation did not match!", "cp_error")
                return render_template('delete_user.html', auths=[stage_1_auth, stage_2_auth, stage_3_auth, stage_4_auth],
                                        stage=4, user=current_user)
        
    stage_1_auth = secrets.token_hex(16)
    redis.setex(f"{current_user.id}_stage_1_auth", REDIS_TIMEOUT, stage_1_auth)
    return render_template('delete_user.html', auths=[stage_1_auth], stage=stage, user=current_user)
