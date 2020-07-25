from flaskqna import db
from datetime import datetime
from flask_login import UserMixin
from flaskqna import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    questions = db.relationship('Question', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

    def __repr__(self):
        return f"('{self.email}', '{self.username}', '{self.password}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    date_asked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    context = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"('{self.question}', '{self.date_asked}', '{self.context}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date_replied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"('{self.comment}', '{self.date_replied}', '{self.user_id}')"
        