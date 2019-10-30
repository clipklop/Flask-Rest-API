# Review resource for APi

from flask_restful import Resources
from flask import jsonify

import models


class ReviewList(Resources):
    def get(self):
        return jsonify({'review': [{'course': 1, 'rating': 5}]})


class Review(Resources):
    def get(self, id):
        return jsonify({'course': 1, 'rating': 5})

    def put(self, id):
        return jsonify({'course': 1, 'rating': 5})

    def delete(self, id):
        return jsonify({'course': 1, 'rating': 5})
