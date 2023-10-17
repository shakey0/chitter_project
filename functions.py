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
