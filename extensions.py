# extensions.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_login import LoginManager

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

db: SQLAlchemy  = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()