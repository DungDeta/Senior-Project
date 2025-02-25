import secrets
import uuid
from datetime import datetime, timedelta

import shortuuid


def generate_id():
    # Generate a UUID and return it as a string
    return str(uuid.uuid4())


def convert_user_id_json_to_user_id(user_id_json):
    user_id = user_id_json['id']
    return user_id


def generate_alias(url):
    # Generate a UUID from the URL and shorten it to get a unique alias
    alias = shortuuid.uuid(name=url)[:5]
    return alias


def generate_verification_token():
    return secrets.token_urlsafe(16)


def get_current_timestamp():
    return int(datetime.utcnow().timestamp())


def generate_expiration_timestamp(duration_seconds):
    # Get the current datetime
    current_datetime = datetime.utcnow()

    # Calculate the expiration datetime by adding the duration in seconds
    expiration_datetime = current_datetime + timedelta(seconds=duration_seconds)

    # Convert the expiration datetime to a Unix timestamp
    expiration_timestamp = int(expiration_datetime.timestamp())

    return expiration_timestamp
