from flask import Flask, jsonify
from flask_cors import CORS

from . import urls
from . import urls_private


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    CORS(app)

    @app.get("/")
    def index():
        return jsonify({
            "status": 200,
            "message": "Welcome"
        })

    app.register_blueprint(urls.bp)
    app.register_blueprint(urls_private.bp)
    return app
