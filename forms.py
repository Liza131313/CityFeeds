from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SelectField
from wtforms.fields import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, equal_to, Email, Optional

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=25)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), equal_to("password")])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class UserForm(FlaskForm):
    img = FileField("Profile Image", validators={FileAllowed(["png", "jpeg", "jpg"])})
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("New Password", validators=[Optional(), Length(min=8, max=25)])
    repeat_password = PasswordField("Repeat password", validators=[Optional(), equal_to("password")])
    submit = SubmitField("Update Profile")

class PostForm(FlaskForm):
    img = FileField("Cover image", validators=[FileAllowed(["png", "jpeg", "jpg"])])
    title = StringField("Post title", validators=[DataRequired()])
    description = TextAreaField("Short Description", validators=[DataRequired()])
    content = TextAreaField("Content")
    category = SelectField(choices=["Category", "Politics", "Education", "Culture", "Society", "Sport"," Entertainment", "Tourism","Environment"], validators=[DataRequired()])
    location = SelectField(choices=["Location", "Tbilisi", "Georgia", "World"], validators=[DataRequired()])
    submit = SubmitField("Publish")

class CommentForm(FlaskForm):
    content = TextAreaField("Add a comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    profile_image = FileField('Profile Image', validators=[FileAllowed(["png", "jpeg", "jpg"])])
    submit = SubmitField('Save Changes')