from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from apps.app import db, login_manager


# User class extends db.Model class and UserMixin class
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user_images = db.relationship(
        "UserImage", backref="user", order_by="desc(UserImage.id)"
    )

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # check mail address's duplication
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


# function to get User information of logged in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
