from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from forecasting.models import User

class RegistrationForm(FlaskForm):
  firstname = StringField('Firstname',
                          validators=[DataRequired(), Length(min=2, max=25)])
  lastname = StringField('Lastname',
                          validators=[DataRequired(), Length(min=2, max=25)])
  email = StringField('Email',
                          validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField('Sign Up')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email Already Exist')

class LoginForm(FlaskForm):
  email = StringField('Email',
                          validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
  remember = BooleanField('Remember Me')
  
  submit = SubmitField('Log In')
  
class UpdateAccountForm(FlaskForm):
  firstname = StringField('Firstname',
                          validators=[DataRequired(), Length(min=2, max=25)])
  lastname = StringField('Lastname',
                          validators=[DataRequired(), Length(min=2, max=25)])
  email = StringField('Email',
                          validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Update')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('Email Already Exist')
      
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chart = FileField('Chart Image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
  email = StringField('Email',
                          validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
      raise ValidationError('There is no account associated with the email provided')

class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset Password')