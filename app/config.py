import os
from common.constants import INSTANCE_FOLDER_PATH

class BaseConfig(object):

   PROJECT = "app"

   # Get app root path, also can use flask.root_path.
   PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

   DEBUG = False
   TESTING = False

   ADMINS = ['ganeshrevanakar@gmail.com']

   # http://flask.pocoo.org/docs/quickstart/#sessions
   SECRET_KEY = 'secret key'

class DefaultConfig(BaseConfig):

   # Statement for enabling the development environment
   DEBUG = True

   SQLALCHEMY_DATABASE_URI = "mysql://b21a60cbdf5aa1:d4e25cf9@us-cdbr-iron-east-05.cleardb.net/heroku_8f6b40cddd2ebcb?reconnect=true"
   SQLALCHEMY_BINDS = {
    'login':        "mysql://b21a60cbdf5aa1:d4e25cf9@us-cdbr-iron-east-05.cleardb.net/heroku_8f6b40cddd2ebcb",
    # 'employees':      "mysql://root:ganesh123@localhost/mytestdb"
   }
   
   # Secret key for signing cookies
   SECRET_KEY = 'development key'

class LocalConfig(DefaultConfig):
   # config for local development
   pass

class StagingConfig(DefaultConfig):
    # config for staging environment
    pass

class ProdConfig(DefaultConfig):
    # config for production environment
    pass

def get_config(MODE):
   SWITCH = {
      'LOCAL'     : LocalConfig,
      'STAGING'   : StagingConfig,
      'PRODUCTION': ProdConfig
   }
   return SWITCH[MODE]