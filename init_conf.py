from flask import Flask
import routes


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('REPORTS_CONFIG')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    routes.init_app(app)
    return app
