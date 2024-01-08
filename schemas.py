from typing_extensions import Required
from marshmallow import Schema, fields

class AthleteSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    sport_type = fields.Str(required=True)
    achievements = fields.Str(required=True)
    

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    athlete_id = fields.Int(Required=True)
    event_type = fields.Str(required=True)
    event_date = fields.Date(required=True)
    location = fields.Str(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)  # load_only for deserialization only

class UserLoginSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)  

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    ticket_id = fields.Int(Required=True)
    payment_date = fields.DateTime(required=True)
    user_id = fields.Int(required=True)

class TicketSchema(Schema):
    id = fields.Int(dump_only=True)
    event_id = fields.Int(required=True)
    ticket_type =  fields.Str(required=True)
    ticket_price = fields.Float(required=True)
    
