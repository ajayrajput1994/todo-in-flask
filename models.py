# models.py
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db
from datetime import datetime

class Todo(db.Model):
  sno: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(nullable=True)
  desc: Mapped[str] = mapped_column(nullable=True) 
  update_at = db.Column(db.DateTime, default=datetime.utcnow)