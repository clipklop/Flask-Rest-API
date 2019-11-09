"""
    *
    * Yep, this is models for our app
    *
"""

from argon2 import PasswordHasher
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
)
import peewee as pw
import datetime

import config


DB = pw.SqliteDatabase('courses.sqlite')
HASHER = PasswordHasher()


class User(pw.Model):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    class Meta:
        database = DB

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email) | (cls.username**username) # ** is like operator, doesn't need for SQLite
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already exist.")

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id == data['id'])
            return user

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)
    
    def verify_password(self, password):
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expires=3600):
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})

class Course(pw.Model):
    title = pw.CharField()
    url = pw.CharField(unique=True)
    created_at = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DB


class Review(pw.Model):
    course = pw.ForeignKeyField(Course, backref='review_set')
    rating = pw.IntegerField()
    comment = pw.TextField(default='')
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    created_by = pw.ForeignKeyField(User, backref='review_set')

    class Meta:
        database = DB


def initialize():
    DB.connect()
    DB.create_tables([User, Course, Review], safe=True)
    DB.close()
