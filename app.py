import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, render_template, flash
from lib.database_connection import get_flask_database_connection
from flask_login import LoginManager, login_user, logout_user, current_user
from lib.user_repository import *
from lib.peep_repository import *
from lib.tag_repository import *
from lib.peeps_images_repository import *


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.jinja_env.autoescape = True


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


all_moods = {1:'content', 2:'excited', 3:'fabulous', 4:'angry', 5:'let down',
            6:'lucky', 7:'anxious', 8:'worried', 9:'scared', 10:'sad',
            11:'calm', 12:'buzzing', 13:'happy', 14:'okay', 15:'bored'}
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
        7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

def add_zero(number):
    if len(str(number)) == 1:
        return f"0{number}"
    return str(number)


saved_tag_number = 0


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    return repo.find_by_id(user_id)


@app.route('/')
def home():
    global saved_tag_number
    # Get all the repository data to be displayed on the main/home page
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    all_users = user_repo.get_all()
    peep_repo = PeepRepository(connection)
    all_peeps = peep_repo.get_all()
    tags_repo = TagRepository(connection)
    all_tags = tags_repo.get_all()
    # Get the tags for which the user wants to see peeps
    current_tag_no = request.args.get('by_tag')
    if current_tag_no == None and saved_tag_number != 0:
        all_peeps = [peep for peep in all_peeps if saved_tag_number in peep.tags]
        current_tag_no = saved_tag_number
    elif current_tag_no == None or current_tag_no == "0":
        current_tag_no = "0"
        saved_tag_number = 0
    else:
        all_peeps = [peep for peep in all_peeps if int(current_tag_no) in peep.tags]
        saved_tag_number = int(current_tag_no)
    # Get the user's current mood and save the liked method for use in the html file
    if current_user.is_authenticated:
        key_moods = {v: k for k, v in all_moods.items()}
        mood_key = key_moods.get(current_user.current_mood)
        liked = peep_repo.does_user_like_peep
    else:
        mood_key = 1
        liked = False
    # Make a dictionary of user_names to display the user_names for each peep
    user_id_to_user_name = {user.id:user.user_name for user in all_users}
    # Get the peep_id for amending tags on and validate the peep belongs to the user
    amend_peep_tags = request.args.get('amend_peep_tags')
    if amend_peep_tags != None and current_user.is_authenticated and\
        peep_repo.peep_belongs_to_user(int(amend_peep_tags), current_user.id):
        amend_peep_tags = int(amend_peep_tags)
    else:
        amend_peep_tags = None
    # Get the peep_id to delete and validate the peep belongs to the user
    delete_peep = request.args.get('delete_peep')
    if delete_peep != None and current_user.is_authenticated and\
        peep_repo.peep_belongs_to_user(int(delete_peep), current_user.id):
        delete_peep = int(delete_peep)
    else:
        delete_peep = None
    # IMAGES
    peep_images = request.args.get('peep_images')
    if peep_images != None:
        image_ids = peep_repo.find_by_id(int(peep_images)).images
        if len(image_ids) > 0:
            peep_for_images = peep_repo.find_by_id(int(peep_images))
            peeps_images_repo = PeepsImagesRepository(connection)
            image_file_names = [peeps_images_repo.get_image_file_name(image_id) for image_id in image_ids]
        else:
            peep_for_images, image_file_names = None, None
    else:
        peep_for_images, image_file_names = None, None
    # Pass all to the html file
    return render_template('index.html', tags=all_tags, current_tag_no=int(current_tag_no),
                            moods=all_moods, current_mood=mood_key,
                            user_is_logged_in=current_user.is_authenticated, user=current_user,
                            peeps=all_peeps, users=user_id_to_user_name, months=months,
                            add_zero=add_zero, liked=liked, amend_peep_tags=amend_peep_tags,
                            find_peep=peep_repo.find_by_id, delete_peep=delete_peep,
                            images=image_file_names, peep_for_images=peep_for_images)


@app.route('/new_peep', methods=['POST'])
def add_new_peep():
    connection = get_flask_database_connection(app)
    peep_repo = PeepRepository(connection)
    tags_repo = TagRepository(connection)
    tags = tags_repo.get_all()
    content = request.form['content']

    tags_for_peep = []
    for num in range(1, len(tags)+1):
        try:
            request.form[f'tag{num}']
            tags_for_peep.append(num)
        except:
            pass
    
    peep_id = peep_repo.add_peep(content, current_user.id, tags_for_peep)

    uploaded_files = request.files.getlist("files")
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            peeps_images_repo = PeepsImagesRepository(connection)
            peeps_images_repo.add_image_for_peep(filename, peep_id)

    return redirect('/')


@app.route('/amend_peep_tags', methods=['POST'])
def amend_peep_tags():
    connection = get_flask_database_connection(app)
    tags_repo = TagRepository(connection)
    tags = tags_repo.get_all()
    peep_id = int(request.form['peep_id'])
    for num in range(1, len(tags)+1):
        try:
            request.form[f'tag{num}']
            tags_repo.add_tag_to_peep(peep_id, num)
        except:
            tags_repo.remove_tag_from_peep(peep_id, num)
    return redirect('/')


@app.route('/delete_peep', methods=['POST'])
def delete_peep():
    connection = get_flask_database_connection(app)
    peep_repo = PeepRepository(connection)
    peep_id = int(request.form['peep_id'])
    peep_repo.delete(peep_id)
    return redirect('/')


@app.route('/like', methods=['POST'])
def reverse_like():
    user_id = request.form['user_id']
    peep_id = request.form['peep_id']
    connection = get_flask_database_connection(app)
    peep_repo = PeepRepository(connection)
    peep_repo.update_likes(user_id, peep_id)
    if request.form['from'] == 'images':
        return redirect(f'/?peep_images={peep_id}')
    return redirect('/')


@app.route('/change_mood', methods=['POST'])
def change_mood():
    mood_value = request.form.get('mood')
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    repo.update(current_user.id, current_mood=all_moods[int(mood_value)])
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    if user_name == "" and password == "":
        flash("Enter your username and password.", "error")
        return redirect('/')
    if user_name == "":
        flash("Enter your username.", "error")
        return redirect('/')
    if password == "":
        flash("Enter your password.", "error")
        return redirect('/')

    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    user_id = repo.user_name_password_match(user_name, password)
    
    if isinstance(user_id, int):  # If we got an integer, it's the user's ID, which means authentication succeeded
        user = repo.find_by_id(user_id)
        login_user(user)
        flash(f"Welcome to your Chitter, {user.user_name}!", "success")
        return redirect('/')
    elif user_id == "Incorrect password.":
        flash("Incorrect password. Please try again.", "error")
    elif user_id == "Username does not exist.":
        flash("Username does not exist. Please try again.", "error")
    return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect('/')


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', user=current_user)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
