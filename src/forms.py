from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FormNome(FlaskForm):
    nome = StringField('Digite seu nome:', validators=[DataRequired()])
    submit = SubmitField('Gerar Certificado')
