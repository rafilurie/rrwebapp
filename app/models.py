from app import db
from flask_user import UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from flask import url_for

# Following.followers association table

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('created', db.DateTime())
)

class User(db.Model, UserMixin):
    
    # Automatically set by the DB when a user is added
    id = db.Column(db.Integer, primary_key=True)

    # These are the items we add to the DB when the user signs up
    first_name = db.Column(db.String(120), nullable=False, server_default='')
    last_name = db.Column(db.String(120), nullable=False, server_default='')
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    created = db.Column(db.DateTime())

    # Other pieces of profile information that a user can add/edit
    about_me = db.Column(db.String(140))
    job_title = db.Column(db.String(120))
    company = db.Column(db.String(64))
    linkedin_url = db.Column(db.String(140))

    # Other columns
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    deleted = db.Column(db.DateTime())
    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Shows all the articles that this user has uploaded
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    followed = db.relationship(
        'User', 
        secondary=followers, 
        primaryjoin=(followers.c.follower_id == id), 
        secondaryjoin=(followers.c.followed_id == id), 
        backref=db.backref('followers', lazy='dynamic'), 
        lazy='dynamic'
    )

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created = datetime.now()

    # OpenID Methods

    # Return True unless the object represents a user that should not be allowed to authenticate for some reason
    def is_authenticated(self):
        return True

    # Return True for users unless they are inactive, for example because they have been banned.
    def is_active(self):
        return self.is_enabled

    # Return True only for fake users that are not supposed to log in to the system.
    def is_anonymous(self):
        return False

    # Return a unique identifier for the user, in unicode format
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
    # Shows how the object will be printed
    def __repr__(self):
        return '<User %r>' % (self.first_name + ' '+self.last_name)

    def get_profile_url(self):
        return "/{0}".format(self.id)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Article.query.join(followers, (followers.c.followed_id == Article.user_id)).filter(followers.c.follower_id == self.id).order_by(Article.created.desc())

    # @classmethod
    # def get(cls,id):
    #     return cls.user_database.get(id)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime())

    # the user associated with this article
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(40), nullable=False)
    url = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Article %r, %r>' % (self.title, self.user_id)

    def get_article_url(self):
        return self.url

    def get_article_user(self):
        return User.query.filter(User.id == self.user_id).first()

    def __init__(self, title, user_id, url):
        self.title = title
        self.user_id = user_id
        self.url = url
        self.created = datetime.now()


####################################################################################################################################

class Perpetrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    name = db.Column(db.String(40), nullable=False)
    display_name = db.Column(db.String(40))
    photos = db.relationship('Photo', backref=db.backref('perpetrators', lazy='joined'),
                               lazy='dynamic')

    # the user associated with this perpetrator
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Perpetrator %r, %r>' % (self.name, self.user_id)

    # def get_photo_url(self):
    #     return "/reported/{0}/photos".format(self.id)

    def __init__(self, name, display_name, user_id):
        self.name = name
        self.user_id = user_id
        self.display_name = display_name
        self.created = datetime.now()


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    comments = db.relationship('Comment', backref=db.backref('photos', lazy='joined'),
                               lazy='dynamic')

    created = db.Column(db.DateTime())
    when = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    extension = db.Column(db.String(1000))

    # the user associated with this photo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    perpetrator_id = db.Column(db.Integer, db.ForeignKey('perpetrator.id'))

    def list_comments(self):
        return self.comments.all()

    def get_url(self):
        url = "/images/{0}.{1}".format(self.id, self.extension)
        return url

    def get_help_url(self):
        url = "/detail/{0}".format(self.id)
        return url

    def __repr__(self):
        return '<Photo %r, %r>' % (self.extension, self.user_id)

    def __init__(self, extension, user_id, when=datetime.now()):
        self.extension = extension
        self.user_id = user_id
        self.created = datetime.now()
        self.when = when


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100000))

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    def __repr__(self):
        return '<Comment %r, %r>' % (self.content, self.photo_id)

    def __init__(self, content, photo_id):
        self.content = content
        self.photo_id = photo_id
        self.created = datetime.now()
