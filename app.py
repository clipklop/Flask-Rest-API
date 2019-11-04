"""
    *
    * Simple REST API build with Flask-rest
    *
"""

from flask import Flask

from resources.courses import courses_api
from resources.reviews import reviews_api

import config
import models


app = Flask(__name__)
app.register_blueprint(courses_api)
app.register_blueprint(reviews_api, url_prefix='/api/v1')


@app.route('/')
def index():
    return '\b<p>Yep, yet another <b>hello-world</b> web-page!</p>'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
