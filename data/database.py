from sqlalchemy.orm import DeclarativeBase

from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
