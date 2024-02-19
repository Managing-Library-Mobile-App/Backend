from datetime import datetime

from helpers.init import db


class Error(db.Model):   # type: ignore[name-defined]
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    occurence_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, level: str, description: str, occurence_date: datetime):
        self.level = level
        self.description = description
        self.occurence_date = occurence_date

    def as_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "description": self.description,
            "occurence_date": self.occurence_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
