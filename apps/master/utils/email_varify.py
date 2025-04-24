import re


def email_varify(email):
    patterns = r'^[a-zA-Z0-9]+@[A-Za-z]+\.[a-zA-Z]{3,4}+$'
    return re.match(patterns,email) is not None
