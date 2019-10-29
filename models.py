"""
    *
    * Yep, this is models for our app
    *
"""

import peewee as pw
import datetime


DB = pw.SqliteDatabase('courses.sqlite')


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

    class Meta:
        database = DB


def initialize():
    DB.connect()
    DB.create_tables([Course, Review], safe=True)
    DB.close()
