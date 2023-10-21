from flask import Blueprint, request, render_template
from flask_login import current_user
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.lib.repositories.peeps_images_repository import PeepsImagesRepository
from ChitterApp.constants import all_moods, months, saved_tag_number, add_zero, get_tag_for_peep_viewing


home_route = Blueprint('home_route', __name__)


@home_route.route('/')
def home():
    global saved_tag_number

    connection = get_flask_database_connection(home)
    user_repo = UserRepository(connection)
    all_users = user_repo.get_all()
    peep_repo = PeepRepository(connection)
    all_peeps = peep_repo.get_all()
    tags_repo = TagRepository(connection)
    all_tags = tags_repo.get_all()
    peeps_images_repo = PeepsImagesRepository(connection)

    # Get the tags for which the user wants to see peeps
    current_tag_number, saved_tag_number, all_peeps = get_tag_for_peep_viewing(
        request.args.get('by_tag'), saved_tag_number, all_peeps)
    
    # Get the user's current mood and save the liked method for use in the html file
    if current_user.is_authenticated:
        key_moods = {v: k for k, v in all_moods.items()}
        mood_key = key_moods.get(current_user.current_mood)
        liked = peep_repo.does_user_like_peep
    else:
        mood_key, liked = 1, False

    # Make a dictionary of user_names to display the user_names for each peep
    user_id_to_user_name = {user.id:user.user_name for user in all_users}

    # Get all the image file names to be displayed on the homepage
    peep_images = {}
    for peep in all_peeps:
        image_ids = peep.images
        if len(image_ids) > 0:
            image_file_names = [peeps_images_repo.get_image_file_name(image_id) for image_id in image_ids]
            peep_images[peep.id] = image_file_names

    # Pass all to the html file
    return render_template('index.html', tags=all_tags, current_tag_no=int(current_tag_number),
                            moods=all_moods, current_mood=mood_key,
                            user_is_logged_in=current_user.is_authenticated, user=current_user,
                            peeps=all_peeps, users=user_id_to_user_name, months=months,
                            add_zero=add_zero, liked=liked, images=peep_images)