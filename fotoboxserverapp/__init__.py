import os
from readline import append_history_file
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE = os.path.join(app.instance_path, 'fotoboxapp.sqlite'),
        UPLOAD_DIR = os.path.join(app.instance_path, 'uploads'),
        SECRET_KEY = 'nope'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        # create instance path and uploads dir
        os.makedirs(app.config['UPLOAD_DIR'])
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import setup
    setup.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import qr
    app.register_blueprint(qr.bp)

    return app

