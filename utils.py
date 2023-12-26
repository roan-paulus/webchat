import hashlib

from flask import abort, get_flashed_messages


def logged_in(session):
    logged_in = False
    if "username" in session:
        logged_in = bool(session["username"])

    return logged_in


def get_flashed_message():
    flash_messages = get_flashed_messages()
    l = len(flash_messages)
    if l == 0:
        return
    if l > 1:
        abort(400)
    return flash_messages[0]


def hash_password(password: str, salt: str) -> str:
    """Returns the hashed version of a password."""
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), iterations=200_000
    )
    return hashed.hex()

