def generate_user_id(last_user_id):
    if last_user_id is None:
        return 'anfa0001'
    num_part = int(last_user_id[4:])
    new_num_part = str(num_part + 1).zfill(4)
    return f'anfa{new_num_part}'