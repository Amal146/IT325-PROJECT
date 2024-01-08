from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PaymentSchema
from models.payment import Payment
from models.user import User
from models.ticket import Ticket
from flask_jwt_extended import jwt_required, get_jwt
from db import db

payment_bp = Blueprint("Payments", "payments", description = "Operations for payments",url_prefix="/payments")


# Get a list of payments
@payment_bp.route("")
class PaymentListResource(MethodView):
    @payment_bp.response(200, PaymentSchema(many=True))
    def get(self):
        payments = Payment.query.all()
        return [payment for payment in payments], 200

    @payment_bp.arguments(PaymentSchema)
    @payment_bp.response(201, PaymentSchema)
    def post(self, data):
        user_id = data.get("user_id")
        ticket_id = data.get("ticket_id")
        
        # Check if the provided user_id exists in the users table
        if db.session.query(User.query.filter_by(id=user_id).exists()).scalar():
            # Check if the provided ticket_id exists in the tickets table
            if db.session.query(Ticket.query.filter_by(id=ticket_id).exists()).scalar():
                new_payment = Payment(**data)
                db.session.add(new_payment)
                db.session.commit()
                return new_payment, 201
            else:
                return abort(400, message="Invalid ticket_id provided")
        else:
            return abort(400, message="Invalid user_id provided")


# Get a payment by ID
@payment_bp.route("/<int:id>")
class PaymentResource(MethodView):
    @payment_bp.response(200, PaymentSchema)
    def get(self, id):
        payment = Payment.query.get_or_404(id)
        return payment , 200
    
    # Update a payment by ID
    @payment_bp.arguments(PaymentSchema)
    @payment_bp.response(200, PaymentSchema)
    def put(self, data, id):
        payment = Payment.query.get_or_404(id)
        if payment:
            payment.user_id = data.get("user_id", payment.user_id)
            payment.ticket_id = data.get("ticket_id", payment.ticket_id)
            payment.payment_date = data.get("payment_date", payment.payment_date)
            db.session.commit()
            return payment, 200
        else:
            abort(404, message="Payment not found")

    # Delete a payment by ID
    @payment_bp.response(204)
    def delete(self, id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        payment = Payment.query.get_or_404(id)
        db.session.delete(payment)
        db.session.commit()
        return {"message": "payment deleted"}, 204


