from db import db

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    ticket_type = db.Column(db.String(50), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)

    # Define relationships
    event = db.relationship('Event', backref=db.backref('tickets', lazy=True))

