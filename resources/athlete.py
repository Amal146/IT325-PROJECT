from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AthleteSchema
from models.athlete import Athlete
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from db import db

athlete_bp = Blueprint(
    "Athletes", "athletes", description="Operation for Payments transactions"
)


# Serialize Athlete
def serialize_athlete(athlete):
    return {
        "id": athlete.id,
        "name": athlete.name,
        "sport_type": athlete.sport_type,
        "achievements": athlete.achievements,
    }


@athlete_bp.route("/athletes")
class AthleteView(MethodView):
    @athlete_bp.response(200)
    def get(self):
        athletes = Athlete.query.all()
        serialized_athletes = [serialize_athlete(athlete) for athlete in athletes]
        return jsonify(serialized_athletes), 200
        
    @athlete_bp.arguments(AthleteSchema)
    @athlete_bp.response(201)
    def post(self, athlete_data):
        athlete = Athlete(**athlete_data)
        try:
            db.session.add(athlete)
            db.session.commit()
            return {"message": "Athlete created"}, 201
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding the athlete.")    


@athlete_bp.route("/athletes/<int:athlete_id>")
class SingleAthleteView(MethodView):
    @athlete_bp.response(200)
    def get(self, athlete_id):
        athlete = Athlete.query.get_or_404(athlete_id)
        serialized_athlete = serialize_athlete(athlete)
        return jsonify(serialized_athlete), 200

    

    @athlete_bp.arguments(AthleteSchema)
    @athlete_bp.response(200)
    def put(self, athlete_data, athlete_id):
        athlete = Athlete.query.get_or_404(athlete_id)
        if athlete:
            athlete.name = athlete_data["name"]
            athlete.sport_type = athlete_data["sport_type"]
            athlete.achievements = athlete_data["achievements"]
            db.session.commit()
            serialized_athlete = serialize_athlete(athlete)
            return jsonify(serialized_athlete), 200
        else:
            abort(404, message="Athlete not found")

    @athlete_bp.response(204)
    def delete(self, athlete_id):
        '''jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")'''
        athlete = Athlete.query.get_or_404(athlete_id)
        db.session.delete(athlete)
        db.session.commit()
        return {"message": "Athlete deleted"}, 201
        
