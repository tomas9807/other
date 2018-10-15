from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,DateField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username:',validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired(),Length(min=5,max=30)])
    confirm_password = PasswordField('Password:',validators=[EqualTo('password')])
    submit = SubmitField('sign up')

class LoginForm(FlaskForm):
    email = StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired(),Length(min=5,max=30)])
    confirm_password = PasswordField('Password:',validators=[EqualTo('password')])
    remember_me = BooleanField('Remember me:')
    submit = SubmitField('log in')

class NewPostForm(FlaskForm):
    title = StringField('Title:',validators=[DataRequired(),Length(min=3,max=50)])
    content = StringField('Content:',validators=[DataRequired(),Length(max=65000)])
    date_posted = DateField('Date:',format='%m/%d/%y',validators=[DataRequired()])
    submit = SubmitField('submit')