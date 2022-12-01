from datetime import datetime

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_link = db.Column(db.String(128), nullable=False)
    short = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

