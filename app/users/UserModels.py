from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.orm import synonym
from flask_login import UserMixin
from ..common.helpers import JsonSerializer, get_current_time
from ..extensions import db

import UserConstants

class UserJsonSerializer(JsonSerializer):
    __json_public__ = ['userid', 'email']
    
class User(db.Model, UserMixin, UserJsonSerializer):
   __bind_key__ = 'login'
   __tablename__ = "login_creds"
   def __repr__(self):
      return '<User %r>' % (self.id)
      
   userid        = db.Column(db.Integer, primary_key = True)
   id            = synonym('userid')
   email         = db.Column(db.String(UserConstants.STRING_LEN), index = True, unique = True, nullable=False)
   
   # User Password
   _password = db.Column('password', db.String(UserConstants.PW_STRING_LEN), nullable=False)
   
   def _get_password(self):
      return self._password

   def _set_password(self, password):
      self._password = generate_password_hash(password, method='pbkdf2:sha1')
   
   password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))
   
   def check_password(self, password):
      if self.password is None:
         return False
      return check_password_hash(self.password, password)
      
   # methods
   @classmethod
   def authenticate(cls, userid, password):
      user = User.query.filter(db.or_(User.id == userid)).first()
      print("login data", user)

      if user:
         authenticated = user.check_password(password)
      else:
         authenticated = False
      return user, authenticated
    
   @classmethod
   def authenticate_user(cls, userid):
     user = User.query.filter(db.or_(User.id == userid)).first()
     print("retrieved data", user)
     if user:
       return user
     else:
       return False