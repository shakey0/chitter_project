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


def get_peep_id_and_validation(peep_id, current_user, peep_repo, Peep):
    if peep_id != None and current_user.is_authenticated and\
        isinstance(peep_repo.find_by_id(peep_id), Peep) and\
        peep_repo.peep_belongs_to_user(int(peep_id), current_user.id):
        peep_id = int(peep_id)
    else:
        peep_id = None
    return peep_id


def get_peep_id_and_image_file_names(peep_id, peep_repo, peeps_images_repo):
    if peep_id != None:
        image_ids = peep_repo.find_by_id(int(peep_id)).images
        if len(image_ids) > 0:
            peep_for_images = peep_repo.find_by_id(int(peep_id))
            image_file_names = [peeps_images_repo.get_image_file_name(image_id) for image_id in image_ids]
        else:
            peep_for_images, image_file_names = None, None
    else:
        peep_for_images, image_file_names = None, None
    return peep_for_images, image_file_names


def get_user_id_and_user_tags(user_id, current_user, tags_repo):
    if user_id != None and current_user.is_authenticated and\
        current_user.id == int(user_id):
        user_id = int(user_id)
        all_tags = tags_repo.get_all()
        user_tags = [tag for tag in all_tags if tags_repo.does_user_favour_tag(current_user.id, tag)]
    else:
        user_id = None
        user_tags = []
    return user_id, user_tags


