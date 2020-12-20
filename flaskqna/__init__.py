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

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qna.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://TRIPLE_E_HEREipoewygqnbe:33221acb0b74a9eb64bb0d09c3655afcb7d112be096b498c2701a476b0c416b7@ec2-50-19-26-235.compute-1.amazonaws.com:5432/d1h6g66ju650eq'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 
# DATABASE CONFIGS ---------------------------------------------------------------------------

from flaskqna import routes 

