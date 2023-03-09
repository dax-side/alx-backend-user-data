#!/usr/bin/env python3
""" handles all routes for Session auth"""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login_auth() -> str:
    """ session auth"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email is None:
        return jsonify({'error': "email missing"}), 400

    if not password or password is None:
        return jsonify({'error': "password missing"}), 400

    # check user in DB
    users = User.search({"email": email})
    if not users:
        return jsonify({'error': "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({'error': "wrong password"}), 401
        from api.v1.app import auth
        response = make_response(user.to_json())
        session_id = auth.create_session(user.id)
        SESSION_NAME = getenv("SESSION_NAME")
        response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ delete user session"""
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(401)

    return jsonify({}), 200
