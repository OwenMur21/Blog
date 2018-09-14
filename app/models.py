from . import db
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """
    Creates User class
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer ,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        """
        Function that blocks access to the password
        """
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Commentjoke', backref='title', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def update_blog(self):
        Blog.query.filter_by(id).update()
        db.session.commit()

    @classmethod
    def get_blogs(cls):
        blogs = Blog.query.all()
        return blogs