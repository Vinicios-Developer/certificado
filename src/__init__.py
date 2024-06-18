from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificado.db'
app.config['SECRET_KEY'] = '8d128903f0d3bcec0f4866d4444951f02b1f22c891dafe2f'

database = SQLAlchemy(app)


from certificado.src import routes
