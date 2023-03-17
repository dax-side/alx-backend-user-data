#!/usr/bin/env python3
""" Testing of main files """

import requests

BASE_URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test for validating user registration """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post('{}/users'.format(BASE_URL), data=data)

    msg = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test for validating log in with wrong password """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post('{}/sessions'.format(BASE_URL), data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test for validating succesful log in """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post('{}/sessions'.format(BASE_URL), data=data)

    msg = {"email": email, "message": "logged in"}

    assert response.status_code == 200
    assert response.json() == msg

    session_id = response.cookies.get("session_id")

    return session_id


def profile_unlogged() -> None:
    """ Test for validating profile request without log in """
    cookies = {
        "session_id": ""
    }
    response = requests.get('{}/profile'.format(BASE_URL), cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test for validating profile request logged in """
    cookies = {
        "session_id": session_id
    }
    response = requests.get('{}/profile'.format(BASE_URL), cookies=cookies)

    msg = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """ Test for validating log out endpoint """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete('{}/sessions'.format(BASE_URL), cookies=cookies)

    msg = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """ Test for validating password reset token """
    data = {
        "email": email
    }
    response = requests.post('{}/reset_password'.format(BASE_URL), data=data)

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")

    msg = {"email": email, "reset_token": reset_token}

    assert response.json() == msg

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for validating password reset (update) """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put('{}/reset_password'.format(BASE_URL), data=data)

    msg = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == msg


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
