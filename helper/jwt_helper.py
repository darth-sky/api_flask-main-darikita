"""JWT Helper to few standard stuff relate with JWT"""
from flask_jwt_extended import get_jwt


def get_roles():
    """Get roles based on jwt decoded"""
    decoded_jwt = get_jwt()
    user_roles = decoded_jwt.get('roles', [])
    return user_roles

def get_user_id():
    """Get user id based on jwt decoded"""
    decoded_jwt = get_jwt()
    user_id = decoded_jwt.get('user_id', None)
    return user_id