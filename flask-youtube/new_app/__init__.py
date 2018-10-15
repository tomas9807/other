from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = '76b4422b33d7d6bb9160ad80a449a518'
app.config['MYSQL_CONFIG'] = {'user':'root','database':'flask'}
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
from . import views