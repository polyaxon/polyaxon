import re


def sanitize_name(name):
    return re.sub(
        '-+',
        '-',
        re.sub('[^-0-9a-z]+', '-', name.lower())).lstrip('-').rstrip('-')


def validate_name(name):
    return name == sanitize_name(name)
