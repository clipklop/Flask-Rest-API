"""
    *
    * Simple REST API build with Flask-rest
    *
"""

from flask import Flask

import models


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000


app = Flask(__name__)


@app.route('/')
def index():
    return '\b<p>Yep, yet another <b>hello-world</b> web-page!</p>'    


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
