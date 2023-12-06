from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)

    # Определение связи многие-ко-многим
    users = db.relationship('User', secondary='user_applications', back_populates='applications')


user_applications = db.Table('user_applications',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             db.Column('app_id', db.Integer, db.ForeignKey('application.id'), primary_key=True)
                             )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    applications = db.relationship('Application', secondary='user_applications', back_populates='users')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

