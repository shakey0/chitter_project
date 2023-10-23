from flask import Blueprint, request, render_template, redirect, flash, session, jsonify
from flask_login import current_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.lib.repositories.peeps_images_repository import PeepsImagesRepository
from ChitterApp.constants import all_moods, months, add_zero


user_routes = Blueprint('user_routes', __name__)


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


# @user_routes.route('/change_mood', methods=['POST'])
# def change_mood():
#     user_id = request.form.get('user_id')
#     if not current_user.is_authenticated or int(user_id) != current_user.id:
#         return redirect('/')
    
#     mood_value = request.form.get('mood')
#     from_page = request.form.get('from')
#     connection = get_flask_database_connection(user_routes)
#     repo = UserRepository(connection)
#     repo.update(current_user.id, current_mood=all_moods[int(mood_value)])
#     if from_page == "user":
#         return redirect(f'/user/{current_user.user_name}')
#     return redirect('/')

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
    user_id = int(request.form['user_id'])

    if not current_user.is_authenticated or user_id != current_user.id:
        return redirect('/')

    connection = get_flask_database_connection(user_routes)
    tags_repo = TagRepository(connection)
    tags = tags_repo.get_all()
    for num in range(1, len(tags)+1):
        try:
            request.form[f'tag{num}']
            tags_repo.add_tag_to_user(user_id, num)
        except:
            tags_repo.remove_tag_from_user(user_id, num)
    return redirect(f'/user/{current_user.user_name}')


@user_routes.route('/change_password')
def change_password():
    if not current_user.is_authenticated:
        return redirect('/')
    success = request.args.get('success')
    password_changed = True if success == "1" else False
    return render_template('change_password.html', user=current_user,
                            password_changed=password_changed)


@user_routes.route('/validate_new_password', methods=['POST'])
def validate_new_password():
    if not current_user.is_authenticated:
        return redirect('/')

    old_password = request.form['old_password']
    if old_password != current_user.password:
        flash("Old password did not match!", "cp_error")
        return redirect('/change_password')
    new_password = request.form['new_password']
    confirm_new_password = request.form['c_new_password']
    connection = get_flask_database_connection(user_routes)
    user_repo = UserRepository(connection)
    result = user_repo.update(current_user.id, password=new_password,
                                confirm_password=confirm_new_password)
    if result == None:
        return redirect('/change_password?success=1')
    if isinstance(result, list):
        for error in result:
            flash(error, "cp_error")
    else:
        flash("New p" + result[1:], "cp_error")
    return redirect('/change_password')

# DELETE PROFILE NEEDS TO BE ADDED !!!!!