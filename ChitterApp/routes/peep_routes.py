import os
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, request, redirect, flash
from flask_login import current_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.lib.repositories.peeps_images_repository import PeepsImagesRepository
from ChitterApp.constants import allowed_file


peep_routes = Blueprint('peep', __name__)


@peep_routes.route('/new_peep', methods=['POST'])
def add_new_peep():

    if not current_user.is_authenticated:
        return redirect('/')
    
    content = request.form['content']
    uploaded_files = request.files.getlist("files")

    valid_files = False
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            valid_files = True
    if valid_files == False and (content.strip() == "" or content == None):
        flash("Peeps need literate or visual content!", "peep_error")
        if request.form['from'] == 'user':
            return redirect(f'/user/{current_user.user_name}')
        return redirect('/')
    
    connection = get_flask_database_connection(peep_routes)
    tags_repo = TagRepository(connection)
    tags = tags_repo.get_all()
    tags_for_peep = []
    for num in range(1, len(tags)+1):
        try:
            request.form[f'tag{num}']
            tags_for_peep.append(num)
        except:
            pass
    
    peep_repo = PeepRepository(connection)
    peep_id = peep_repo.add_peep(content, current_user.id, tags_for_peep)

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            peeps_images_repo = PeepsImagesRepository(connection)
            peeps_images_repo.add_image_for_peep(filename, peep_id)

    if request.form['from'] == 'user':
        return redirect(f'/user/{current_user.user_name}')
    return redirect('/')


@peep_routes.route('/amend_peep_tags', methods=['POST'])
def amend_peep_tags():
    peep_id = int(request.form['peep_id'])
    connection = get_flask_database_connection(peep_routes)

    peep_repo = PeepRepository(connection)
    if not current_user.is_authenticated or peep_repo.find_by_id(peep_id).user_id != current_user.id:
        return redirect('/')
    
    tags_repo = TagRepository(connection)
    tags = tags_repo.get_all()
    for num in range(1, len(tags)+1):
        try:
            request.form[f'tag{num}']
            tags_repo.add_tag_to_peep(peep_id, num)
        except:
            tags_repo.remove_tag_from_peep(peep_id, num)

    if request.form['from'] == "user":
        return redirect(f'/user/{current_user.user_name}')
    return redirect('/')


@peep_routes.route('/delete_peep', methods=['POST'])
def delete_peep():
    peep_id = int(request.form['peep_id'])
    connection = get_flask_database_connection(peep_routes)

    peep_repo = PeepRepository(connection)
    if not current_user.is_authenticated or peep_repo.find_by_id(peep_id).user_id != current_user.id:
        return redirect('/')

    image_ids = peep_repo.find_by_id(peep_id).images
    image_file_names = []
    if len(image_ids) > 0:
        peeps_images_repo = PeepsImagesRepository(connection)
        image_file_names = [peeps_images_repo.get_image_file_name(image_id) for image_id in image_ids]
    
    peep_repo.delete(peep_id)

    if len(image_file_names) > 0:
        all_images = peeps_images_repo.get_all()
        all_file_names = [image['file_name'] for image in all_images]
        for image in image_file_names:
            if image not in all_file_names:
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
                os.remove(file_path)

    if request.form['from'] == "user":
        return redirect(f'/user/{current_user.user_name}')
    return redirect('/')


@peep_routes.route('/like', methods=['POST'])
def reverse_like():
    user_id = request.form['user_id']
    peep_id = request.form['peep_id']
    connection = get_flask_database_connection(peep_routes)

    if not current_user.is_authenticated or int(user_id) != current_user.id:
        return redirect('/')

    peep_repo = PeepRepository(connection)
    peep_repo.update_likes(user_id, peep_id)

    user_repo = UserRepository(connection)
    if "user" in request.form['from']:
        return_to_user = int(request.form['from'][4:])
        return redirect(f'/user/{user_repo.find_by_id(return_to_user).user_name}')
    return redirect('/')