from flask import Blueprint, request, render_template, session
from flask_login import current_user
import os
from redis import StrictRedis
running_in_docker = os.environ.get('RUNNING_IN_DOCKER', False)
if running_in_docker:
    redis = StrictRedis(host='localhost', port=6379, db=0)
else:
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)
from ChitterApp.lib.database_connection import get_flask_database_connection
from ChitterApp.lib.repositories.peep_repository import PeepRepository
from ChitterApp.lib.repositories.tag_repository import TagRepository
from ChitterApp.constants import all_moods, months, add_zero, get_tag_for_peep_viewing
import json


home_route = Blueprint('home_route', __name__)

@home_route.route('/')
def home():
    if 'saved_tag_number' not in session:
        session['saved_tag_number'] = 0

    connection = get_flask_database_connection(home)
    peep_repo = PeepRepository(connection)
    
    # Get the peep data based on the authenticated user and the user's current mood
    if current_user.is_authenticated:
        all_peeps = peep_repo.get(current_user_id=current_user.id)
        key_moods = {v: k for k, v in all_moods.items()}
        mood_key = key_moods.get(current_user.current_mood)
    else:
        all_peeps = peep_repo.get()
        mood_key = False

    # Get the tags for which the user wants to see peeps
    current_tag_number, session['saved_tag_number'], all_peeps = get_tag_for_peep_viewing(
        request.args.get('by_tag'), session['saved_tag_number'], all_peeps)

    # Get all the tags
    tags = redis.get(f"all_tags")
    if tags:
        all_tags = {int(k): v for k, v in json.loads(tags.decode('utf-8')).items()}
    else:
        tags_repo = TagRepository(connection)
        all_tags = tags_repo.get_all()
        redis.setex(f"all_tags", 7200, json.dumps(all_tags))

    # Pass all to the html file
    return render_template('index.html', tags=all_tags, current_tag_no=int(current_tag_number),
                            moods=all_moods, current_mood=mood_key,
                            user_is_logged_in=current_user.is_authenticated, user=current_user,
                            peeps=all_peeps, months=months, add_zero=add_zero)
