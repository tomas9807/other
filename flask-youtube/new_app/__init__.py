from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '76b4422b33d7d6bb9160ad80a449a518'
app.config['MYSQL_CONFIG'] = {'user':'root','database':'flask'}

from . import views