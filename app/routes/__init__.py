from .auth import auth_bp  # Import the auth blueprint
from .camera import camera_bp  # Import the camera blueprint (if you have one)
# Add more imports as needed for other route modules

def init_app(app):
    """
    Initialize and register all the blueprints with the app.
    """
    # Register each blueprint with a URL prefix as required
    app.register_blueprint(auth_bp, url_prefix="/auth")  # Register auth blueprint
    app.register_blueprint(camera_bp, url_prefix="/camera")  # Register camera blueprint
    
    # Register more blueprints as needed
    # app.register_blueprint(another_bp, url_prefix="/another")
