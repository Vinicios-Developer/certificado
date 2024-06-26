from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sqlalchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres.pndbegbnjyvrvmbnotpc:Vinicios0608@aws-0-sa-east-1.pooler.supabase.com:6543/postgres')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '8d128903f0d3bcec0f4866d4444951f02b1f22c891dafe2f')

database = SQLAlchemy(app)


from certificado.src import routes
