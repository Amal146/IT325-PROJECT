from flask import Blueprint

athlete_bp = Blueprint('athlete', __name__)
event_bp = Blueprint('event', __name__)
user_bp = Blueprint('user', __name__)
payment_bp = Blueprint('payment', __name__)
ticket_bp = Blueprint('ticket', __name__)

from . import athlete, event, user, payment, ticket
