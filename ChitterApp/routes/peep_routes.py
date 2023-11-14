from flask import Blueprint, request, redirect, flash, jsonify
from flask_login import current_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.peep_repository import PeepRepository
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

    validated_files = []
    valid_files = False
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            validated_files.append(file)
            valid_files = True
    if valid_files == False and (content.strip() == "" or content == None):
        flash("Peeps need literate or visual content!", "peep_error")
        return redirect_to
    if len(validated_files) > 6:
        flash("There is a maximum allowance of 6 images per peep!", "peep_error")
        return redirect_to
    
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
        for word in peep_id:
            flash(f"The word(s) '{word}' is not allowed in peeps!", "peep_error")
        return redirect_to

    return redirect_to


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
