from .auth_controller import auth_bp
from .home_controller import home_bp
from .form_controller import form_bp
from .form_degradation_controller import form_dg_bp


def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(form_dg_bp)