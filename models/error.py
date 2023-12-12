from datetime import datetime

from helpers.init import db


class Error(db.Model):
    _id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    type = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    occurence_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<Error %s>" % self._id
