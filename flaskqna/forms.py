from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=24)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=120)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=24)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=120)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(max=100)])
    context = TextAreaField('Context')
    submit = SubmitField('Submit')
