from flask import Blueprint, request, redirect, jsonify
from flask_login import current_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.constants import allowed_file, timeout
import json


peep_routes = Blueprint('peep', __name__)


@peep_routes.route('/new_peep', methods=['POST'])
def add_new_peep():

    if not current_user.is_authenticated:
        return redirect('/')

    content = request.form['content']
    uploaded_files = request.files.getlist("files")

    validated_files = []
    valid_files = False
    total_size = 0
    errors = {}

    for file in uploaded_files:
        file_size = len(file.read())
        file.stream.seek(0)
        if file and allowed_file(file.filename) and file_size <= 6 * 1024 * 1024:
            validated_files.append(file)
            valid_files = True
            total_size += file_size
        elif file and not allowed_file(file.filename):
            errors["peep_file_type"] = "Only images are allowed in peeps!"
        if file and file_size > 6 * 1024 * 1024:
            total_size += file_size
            errors["peep_file_size"] = "Maximum image size is 6 MB!"

    if total_size > 30 * 1024 * 1024:
        errors["peep_total_file_size"] = "Maximum total image size per peep is 30 MB!"

    if (not valid_files and len(errors) == 0) and (content.strip() == "" or content == None):
        errors["peep_content"] = "Peeps need literate or visual content!"

    if valid_files:
        if len(validated_files) > 6:
            errors["peep_file_number"] = "You can only post up to 6 images in a peep!"
            return jsonify(success=False, errors=errors)
        if errors:
            return jsonify(success=False, errors=errors)
        security_check = timeout(current_user.id, "upload_images", 3, 86400)
        if security_check != True:
            errors["peep_security"] = "You can only post peeps with images twice in 24 hours!"
            return jsonify(success=False, errors=errors)

    if errors:
        return jsonify(success=False, errors=errors)
    
    security_check = timeout(current_user.id, "peep_posts", 6, 86400)
    if security_check != True:
        errors["peep_security"] = "You can only post up to 5 peeps in 24 hours!"
        return jsonify(success=False, errors=errors)

    no_of_tags = int(request.form['no_of_tags'])
    tags_for_peep = []
    for num in range(1, no_of_tags+1):
        try:
            request.form[f'tag{num}']
            tags_for_peep.append(num)
        except:
            pass
    
    connection = get_flask_database_connection(peep_routes)
    peep_repo = PeepRepository(connection)
    peep_id = peep_repo.create(content, current_user.id, tags_for_peep, validated_files)

    if isinstance(peep_id, list):
        if len (peep_id) == 1:
            errors["peep_bad_words"] = f"Peep contains the following banned word: {peep_id[0]}"
        elif len (peep_id) > 1:
            errors["peep_bad_words"] = f"Peep contains the following banned words: {', '.join(peep_id)}"
        return jsonify(success=False, errors=errors)

    return jsonify(success=True)


@peep_routes.route('/amend_peep_tags', methods=['POST'])
def amend_peep_tags():
    peep_data = request.form['peep']
    peep_dict = json.loads(peep_data)

    if not current_user.is_authenticated or int(peep_dict["user_id"]) != current_user.id:
        return redirect('/')
    
    no_of_tags = int(request.form['no_of_tags'])
    tags_for_peep = []
    for num in range(1, no_of_tags+1):
        try:
            request.form[f'tag{num}']
            tags_for_peep.append(num)
        except:
            pass

    tags_to_remove = []
    for tag in peep_dict['peep_tags']:
        if int(tag) not in tags_for_peep:
            tags_to_remove.append(int(tag))
    
    tags_to_add = []
    for tag in tags_for_peep:
        if str(tag) not in peep_dict['peep_tags']:
            tags_to_add.append(tag)

    connection = get_flask_database_connection(peep_routes)
    peep_repo = PeepRepository(connection)
    peep_repo.update_tags(int(peep_dict["peep_id"]), tags_to_remove, tags_to_add)

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
    peep_repo.delete(int(peep_dict["peep_id"]), peep_dict["peep_images"])

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
