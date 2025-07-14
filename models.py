from flask_login import UserMixin
from ext import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer(), primary_key=True)
    img = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    content = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    created_at = db .Column(db.DateTime, default=datetime.now)
    author = db.relationship('User', backref='posts')

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    img = db.Column(db.String(), default="default.png")
    username = db.Column(db.String(), unique= True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="Guest")

    def __init__(self, username, email, password, role="Guest", img="default.png"):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.img = img

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post = db.relationship('Post', backref='comments')
    user = db.relationship('User', backref='comments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
