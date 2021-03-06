from time import time
import datetime
import jwt
import os

class UserActions():
    SECRET_KEY = 'D\xde@\xe4\x1ch/\xa8\xed\xd3\xc6\x98?D\xbb\xb8Bo\xc0\xb7\xc6\xc7\x92\x19'

    @classmethod
    def encode_auth_token(cls, user_id):
        """
        Generate the auth token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=500),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                cls.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @classmethod
    def decode_auth_token(cls, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        print('Decoding auth token')
        payload = jwt.decode(auth_token, cls.SECRET_KEY)
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            print('token is blacklisted!')
            raise Exception('token blacklisted. Please log in again')
        return payload['sub']

class BlacklistToken:
    """
    Token Model for storing JWT tokens
    """
    blacklisted_tokens = []

    def __init__(self, token):
        self.id = int(time())
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @classmethod
    def check_blacklist(cls, auth_token):
        # check whether auth token has been blacklisted
        print(cls.blacklisted_tokens)
        print('Checking for auth token if blacklisted')
        for token in cls.blacklisted_tokens:
            if token.token == auth_token:
                return True
        return False