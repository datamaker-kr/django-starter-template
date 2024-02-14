import random
import string


def generate_random(type='char', length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def str_to_bool(value):
    return value.lower() in ['true', '1', 'yes']
