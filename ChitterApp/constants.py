import os
from redis import StrictRedis
running_in_docker = os.environ.get('RUNNING_IN_DOCKER', False)
if running_in_docker:
    redis = StrictRedis(host='localhost', port=6379, db=0)
else:
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    redis = StrictRedis(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)

def timeout(user_name, attempt_type, no_of_tries, timer):
    default_timeout = timer
    redis_timeout = int(os.environ.get('REDIS_TIMEOUT', default_timeout))
    cache_name = f"{user_name}_{attempt_type}_attempt"
    if redis.get(cache_name) == None:
        redis.setex(cache_name, redis_timeout, 1)
    else:
        attempts = int(redis.get(cache_name).decode('utf-8'))
        attempts += 1
        if attempts >= no_of_tries:
            return "Too many tries! Wait 2 minutes."
        redis.setex(cache_name, redis_timeout, attempts)
    return True


UPLOAD_FOLDER = 'ChitterApp/static/uploads'


ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg', 'ico', 'avif'
}
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


def get_tag_for_peep_viewing(current_tag_number, saved_tag_number, all_peeps):
    if current_tag_number == None and saved_tag_number != 0:
        all_peeps = [peep for peep in all_peeps if saved_tag_number in peep.tags]
        current_tag_number = saved_tag_number
    elif current_tag_number == None or current_tag_number == "0":
        current_tag_number = "0"
        saved_tag_number = 0
    else:
        all_peeps = [peep for peep in all_peeps if int(current_tag_number) in peep.tags]
        saved_tag_number = int(current_tag_number)
    return current_tag_number, saved_tag_number, all_peeps
