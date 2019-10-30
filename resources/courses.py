# Course resource for APi

from flask_restful import Resources
from flask import jsonify

import models


class CourseList(Resources):
    def get(self):
        return jsonify({'courses': [{'title': 'Python Basics'}]})


class Course(Resources):
    def get(self, id):
        return jsonify({'title': 'Python Basics'})

    def put(self, id):
        return jsonify({'title': 'Python Basics'})

    def delete(self, id):
        return jsonify({'title': 'Python Basics'})
