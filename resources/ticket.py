from email.mime import image
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TicketSchema
from models.ticket import Ticket
from models.event import Event
from flask_jwt_extended import get_jwt
from db import db

ticket_bp = Blueprint("Tickets", "tickets" ,description = "operations on tickets")

# Get tickets by event ID
@ticket_bp.route("/tickets/event/<int:event_id>")
class TicketResource(MethodView):
    @ticket_bp.response(200, TicketSchema(many=True))
    def get(self, event_id):
        tickets = Ticket.query.filter_by(event_id=event_id).all()
        if not tickets:
            abort(404, message="No tickets found for this event")
        return [ticket for ticket in tickets], 200


@ticket_bp.route("/tickets/<int:id>")
class TicketResource(MethodView):
    # Get a ticket by ID
    @ticket_bp.response(200, TicketSchema)
    def get(self, id):
        ticket = Ticket.query.get_or_404(id)
        return ticket , 200
    
    # Update a ticket by ID
    @ticket_bp.arguments(TicketSchema)
    @ticket_bp.response(200, TicketSchema)
    def put(self, data, id):
        ticket = Ticket.query.get_or_404(id)
        if not ticket:
            return abort(404, message="Ticket not found")

        event_id = data.get("event_id")
        existing_event = Event.query.get(event_id)
        if not existing_event:
           return abort(400, message="Invalid event_id provided")
        ticket.event_id = event_id
        ticket.ticket_type = data.get("ticket_type")
        ticket.ticket_price = data.get("ticket_price")
        db.session.commit()
        return ticket
    
    # Delete a ticket by ID
    @ticket_bp.response(204)
    def delete(self, id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        ticket = Ticket.query.get_or_404(id)
        db.session.delete(ticket)
        db.session.commit()
        return {"message": "ticket deleted"}, 204


# Get a list of tickets
@ticket_bp.route("/tickets")
class TicketListResource(MethodView):
    @ticket_bp.response(200, TicketSchema(many=True))
    def get(self):
        tickets = Ticket.query.all()
        return [ticket for ticket in tickets], 200

    # Create a new ticket
    @ticket_bp.arguments(TicketSchema)
    @ticket_bp.response(201)
    def post(self, data):
        ticket =Ticket(**data)
        db.session.add(ticket)
        db.session.commit()
        return {"message": "Ticket created"}, 201

    
