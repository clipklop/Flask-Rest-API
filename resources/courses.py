#

from flask_restful import Resources
from flask import Flask

import models


class CourseList(Resources):
    def get(self):
        return jsonify({'courses': [{'title': 'Python Basics'}]})


class Course(Resources):
    return
