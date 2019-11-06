# Review resource for APi

from flask_restful import (
    Resource, Api, reqparse, inputs, fields, marshal, marshal_with, abort, g
)
from flask import Blueprint, jsonify, url_for, make_response

from auth import auth
import models
import json


review_fields = {
    'id': fields.Integer,
    'for_course': fields.String,
    'rating': fields.Integer,
    'comment': fields.String(default=''),
    'created_at': fields.DateTime,
}


def add_course(review):
    """Adding course for each review."""
    review.for_course = url_for('resources.course.course', id=review.course.id)
    return review


def review_or_404(review_id):
    """If review is not find - throw an excpetion."""
    try:
        review = models.Review.get(models.Review.id == review_id)
    except models.Review.DoesNotExist:
        abort(404, message="Review {} doesn't exit.".format(review_id))
    else:
        return review


class ReviewList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            type=inputs.positive,
            required=True,
            help='No course provided',
            location=['form', 'json'],
        )
        self.reqparse.add_argument(
            'rating',
            type=inputs.int_range(1, 5),
            required=True,
            help='No rating provided',
            location=['form', 'json'],
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            nullable=True,
            location=['form', 'json'],
            default='',
        )
        super().__init__()

    def get(self):
        return {
            'reviews': [
                marshal(add_course(review), review_fields)
                for review in models.Review.select()]
            }

    @marshal_with(review_fields)
    @auth.login_required
    def post(self):
        # necessary for checking provided attributes
        args = self.reqparse.parse_args()
        review = models.Review.create(
            create_by=g.user,
            **args)
        return (add_course(review), 201, {
            'Location': url_for('resources.reviews.review', id=review.id)
        })


class Review(Resource):
    @marshal_with(review_fields)
    def get(self, id):
        return add_course(review_or_404(id))

    @marshal_with(review_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            review = models.Review.select().where(
                models.Review.created_by==g.user,
                models.Review.id==id
            ).get()
        except models.Review.DoesNotExist:
            return make_response(json.dums(
                {'error': 'That review does not exit or is not editable.'}
            ), 403)
        query = review.update(**args)
        query.execute()
        review = add_course(review_or_404(id))
        return (review, 200, {
            'Location': url_for('resources.reviews.review', id=review.id)
        })

    @auth.login_required
    def delete(self, id):
        try:
            review = models.Review.select().where(
                models.Review.created_by==g.user,
                models.Review.id==id
            ).get()
        except models.Review.DoesNotExist:
            return make_response(json.dums(
                {'error': 'That review does not exit or is not editable.'}
            ), 403)
        query = review.delete()
        query.execute()
        return '', 204, {
            'Location': url_for('resources.reviews.reviews')
        }


reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    ReviewList,
    '/reviews',
    endpoint='reviews'
)
api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint='review'
)
