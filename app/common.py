import os

DEBUG = os.environ.get('APP_DEBUG') == '1'

def generate_unique_id(length=16):
    return os.urandom(length).hex()
