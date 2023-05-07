from google.oauth2 import id_token
from google.auth.transport import requests
import config
from scripts import db

class User:
    def __init__(self, user_info, conn=None):
        if not user_info == None: # Info dict Passed in:
            self.id = user_info['sub']
            self.name = user_info['name']
            self.is_authenticated = True # We don't create user objects for non-authenticated users
            self.is_active = True # Inactivity not tracked
            self.is_anonymous = False # All users are not anonymous
            if conn:
                db.add_or_update_user(conn, user_info)
        else: # id == None:
            self.id = None
            self.name = None
            self.is_authenticated = False
            self.is_active = False
            self.is_anonymous = True

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }
# https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
def verify_token(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), config.client_id)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        return idinfo
    except ValueError:
        # Invalid token
        return None