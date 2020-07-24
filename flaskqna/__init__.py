from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt(app)


# DATABASE CONFIGS ---------------------------------------------------------------------------
db = SQLAlchemy(app) 

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qna.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 
# DATABASE CONFIGS ---------------------------------------------------------------------------

from flaskqna import routes 

