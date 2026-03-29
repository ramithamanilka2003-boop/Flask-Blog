from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[
        DataRequired(),Length(min=2,max=20)
    ])
    email=StringField("Emal",validators=[
        DataRequired(),Email()
    ])
    password=PasswordField("Password",validators=[
        DataRequired()
    ])
    confirm_password=PasswordField("Confirm Password",validators=[
        DataRequired(),EqualTo("password")
    ])
    submit=SubmitField("Sign up")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        
        if user:
            raise ValidationError("That usernname is taken")
        
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        
        if email:
            raise ValidationError("That email is taken")

class LoginForm(FlaskForm):
    email=StringField("Emal",validators=[
        DataRequired(),Email()
    ])
    password=PasswordField("Password",validators=[
        DataRequired()
    ])
    remember=BooleanField("remember me")
    submit=SubmitField("Login")


class Updateaccount(FlaskForm):
    username=StringField("Username",validators=[
        DataRequired(),Length(min=2,max=20)
    ])
    email=StringField("Email",validators=[
        DataRequired(),Email()
    ])
    picture=FileField('Update Profile',validators=[FileAllowed(["jpg","png"])])
    submit=SubmitField("Update")

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            
            if user:
                raise ValidationError("That usernname is taken")
   
    def validate_email(self,email):
        if email.data != current_user.email:
            email=User.query.filter_by(email=email.data).first()
            
            if email:
                raise ValidationError("That email is taken")
            

class RequestResetForm(FlaskForm):
    email=StringField("Email",validators=[
        DataRequired(),Email()])
    submit=SubmitField("Request Password Reset")

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        
        if user is None:
            raise ValidationError("There is no account with that email.Register")
        
class ResetPasswordForm(FlaskForm):
    password=PasswordField("Password",validators=[
        DataRequired()
    ])
    confirm_password=PasswordField("Confirm Password",validators=[
        DataRequired(),EqualTo("password")
    ])
    submit=SubmitField("Reset Password")
