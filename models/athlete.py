from db import db

class Athlete(db.Model):
    __tablename__ = "athletes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sport_type = db.Column(db.String(50), nullable=False)
    achievements = db.Column(db.Text, nullable=True)
