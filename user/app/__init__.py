from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'sua_chave_super_secreta'

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.students_routes import student_bp
    from .routes.teachers_routes import teachers_bp
    from .routes.login import auth_bp
    app.register_blueprint(student_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(auth_bp)

    return app
