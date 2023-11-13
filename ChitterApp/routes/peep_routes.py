import os
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, request, redirect, flash, jsonify
from flask_login import current_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.lib.repositories.peeps_images_repository import PeepsImagesRepository
from ChitterApp.constants import allowed_file
import json


peep_routes = Blueprint('peep', __name__)


@peep_routes.route('/new_peep', methods=['POST'])
def add_new_peep():

    if not current_user.is_authenticated:
        return redirect('/')
    
    redirect_to = redirect(f'/user/{current_user.user_name}') if request.form['from'] == 'user' else redirect('/')

    content = request.form['content']
    uploaded_files = request.files.getlist("files")

    valid_files = False
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            valid_files = True
    if valid_files == False and (content.strip() == "" or content == None):
        flash("Peeps need literate or visual content!", "peep_error")
        return redirect_to
    
    connection = get_flask_database_connection(peep_routes) # TRY SENDING THE LEN OF THE TAGS TO THE BACKEND
    # AND THEN DOING A TRY EXCEPT FOR THE NUMBERS UNTIL THE LEN IS REACHED
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
    peep_id = peep_repo.create(content, current_user.id, tags_for_peep)

    if isinstance(peep_id, list):
        for word in peep_id:
            flash(f"The word(s) '{word}' is not allowed in peeps!", "peep_error")
        return redirect_to

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename, file_extension = os.path.splitext(file.filename)
            new_filename = f"{filename}_{peep_id}{file_extension}"
            secure_new_filename = secure_filename(new_filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_new_filename)
            file.save(file_path)
            peeps_images_repo = PeepsImagesRepository(connection)
            peeps_images_repo.add_image_for_peep(secure_new_filename, peep_id)

    return redirect_to


@peep_routes.route('/amend_peep_tags', methods=['POST'])
def amend_peep_tags():
    peep_id = int(request.form['peep_id'])
    connection = get_flask_database_connection(peep_routes)

    peep_repo = PeepRepository(connection)
    if not current_user.is_authenticated or peep_repo.get(peep_id=peep_id).user_id != current_user.id:
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
    peep_data = request.form['peep']
    peep_dict = json.loads(peep_data)

    if not current_user.is_authenticated or int(peep_dict["user_id"]) != current_user.id:
        return redirect('/')
    
    connection = get_flask_database_connection(peep_routes)
    peep_repo = PeepRepository(connection)
    peep_repo.delete(int(peep_dict["peep_id"]))

    if len(peep_dict["peep_images"]) > 0:
        for image in peep_dict["peep_images"]:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
            os.remove(file_path)

    if request.form['from'] == "user":
        return redirect(f'/user/{current_user.user_name}')
    return redirect('/')


@peep_routes.route('/like', methods=['POST'])
def reverse_like():
    
    success = True
    if not current_user.is_authenticated:
        success = False
    
    peep_id = request.form['peep_id']
    liked = True if request.form['liked'] == "yes" else False

    connection = get_flask_database_connection(peep_routes)
    peep_repo = PeepRepository(connection)
    new_likes = peep_repo.update_likes(current_user.id, peep_id, liked)

    if success:
        return jsonify(success=True, newLikeCount=new_likes)
    else:
        return jsonify(success=False, error="Something wasn't right there...")
