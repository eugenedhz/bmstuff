from app import app
from api.extensions import db
from flask_migrate import upgrade, migrate, init, stamp

from api.models import Admin
from api.models import User, Todo, File, TodoTag, FileTag


def deploy():
    app.app_context().push()

    # create database and tables
    db.create_all()

    # migrate the database
    stamp()
    migrate()
    upgrade()


deploy()
