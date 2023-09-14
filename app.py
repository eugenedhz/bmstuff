from flask import Flask
from api.extensions import db, migrate, ma, jwt, cors
from configs.app_config import Staging


def create_app():
    app = Flask(__name__)
    
    # Application's configuration
    app.config.from_object(Staging())

    # Initialize extensions
    # To use the application instances above, instantiate with an application:
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    return app


# Create Flask application
app = create_app()