from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from schemas import EventSchema
from models.event import Event
from flask_jwt_extended import get_jwt
from db import db


event_bp = Blueprint("Events", "events", description = "Operations for events")

def serialize_event(event):
    return {
        'id': event.id,
        'event_type': event.event_type,
        'event_date': event.event_date,
        'location': event.location
    }


#get all events 
@event_bp.route("/events")
class EventListResource(MethodView):
    @event_bp.response(200, EventSchema(many=True))
    def get(self):  # Include 'self' parameter
        events = Event.query.all()
        serialized_events = [serialize_event(event) for event in events]
        return jsonify(serialized_events), 200

    # Create an event by ID
    @event_bp.arguments(EventSchema)
    @event_bp.response(201)
    def post(self, data):
        event = Event(**data)
        db.session.add(event)
        db.session.commit()
        return {"message": "Event created"}, 201



@event_bp.route("/events/<int:id>")
class EventResource(MethodView):
    # Get an event by ID
    @event_bp.response(200, EventSchema)
    def get(self, id):
        event = Event.query.get_or_404(id)
        return event, 200

    

    # Update an event by ID   
    @event_bp.arguments(EventSchema)
    @event_bp.response(200, EventSchema)
    def put(self, data, id):
        event = Event.query.get_or_404(id)
        if event:
           event.athlete_id = data["athlete_id"]
           event.event_type = data["event_type"]
           event.event_date= data["event_date"]
           event.location = data["location"]
        else:
           event = event(id=id, **data)
        db.session.add(event)
        db.session.commit()
        return event
    
    # Delete an event by ID
    @event_bp.response(204)
    def delete(self, id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.") 
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "event deleted"}, 204

    