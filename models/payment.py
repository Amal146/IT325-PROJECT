from db import db

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

    # Define relationships
    ticket = db.relationship('Ticket', backref=db.backref('payments', lazy=True))
    user = db.relationship('User', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f"Payment('{self.user_id}', '{self.payment_date}')"
