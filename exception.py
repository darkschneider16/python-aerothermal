"""Exceptions for iber module"""

class IberException(Exception):
    """Iber exception"""

class ResponseException(IberException):
    """Iber response exception"""
    def __init__(self, status_code):
        super().__init__(f"Response error, code: {status_code}")


class LoginException(IberException):
    """Iber login exception"""
    def __init__(self, username):
        super().__init__(f'Unable to log in with user {username}')


class SessionException(IberException):
    """Iber session exception"""
    def __init__(self):
        super().__init__('Session required, use login() method to obtain a session')


class NoResponseException(IberException):
    """Iber no response exception"""

class SelectContractException(IberException):
    """Iber select contract exception"""
