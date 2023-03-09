#!/usr/bin/env python3
""" API authentication """
from flask import request
from typing import List, TypeVar
from os import getenv

SESSION_NAME = getenv("SESSION_NAME")


class Auth():
    """ auth system template"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method
            Return: False
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if len(path) == 0:
            return True

        slash = True if path[len(path) - 1] == '/' else False

        tmp_path = path if slash else path + '/'

        for exc in excluded_paths:
            l_exc = len(exc)
            if l_exc == 0:
                continue

            if exc[l_exc - 1] != '*':
                if tmp_path == exc:
                    return False
            else:
                if exc[:-1] == path[:l_exc - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ public method
            Return - None
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('user'):
        """ public method
        Return - None
        """
        return None

    def session_cookie(self, request=None):
        """ Return cookie from request"""
        if request is None:
            return None
        return request.cookies.get(SESSION_NAME)
