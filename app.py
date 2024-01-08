from flask import render_template
from flask_smorest import Api
from flask_migrate import Migrate
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from db import db
from flask_cors import CORS

# Register blueprints
from resources.athlete import athlete_bp
from resources.event import event_bp
from resources.user import user_bp
from resources.payment import payment_bp
from resources.ticket import ticket_bp


app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/users/*": {"origins": "http://127.0.0.1:5000"},
                     r"/athletes/*": {"origins": "http://127.0.0.1:5000"},
                     r"/events/*": {"origins": "http://127.0.0.1:5000"}})
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Sport API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://amal:amal@localhost/sport_api'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)    
api = Api(app)
migrate = Migrate()
jwt = JWTManager()
migrate.init_app(app, db)
jwt.init_app(app)
app.config["JWT_SECRET_KEY"] = "amal"

# Create all the tables

with app.app_context(): 
    db.create_all()


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
        if identity ==1:
            return {"is_admin": True}
        return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
        return ( jsonify({"message": "The token has expired.", "error": "token_expired"}),401,)

@jwt.invalid_token_loader
def invalid_token_callback(error):
        return (jsonify( {"message": "Signature verification failed.", "error": "invalid_token"}),401, )
    


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked.", "error": "token_revoked",}),401,)

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
        return ( jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}),401,)

@jwt.unauthorized_loader
def missing_token_callback(error):
        return (jsonify({"description": "Request does not contain an access token.","error": "authorization_required",}),401,)


    
api.register_blueprint(athlete_bp)
api.register_blueprint(event_bp)
api.register_blueprint(user_bp)
api.register_blueprint(payment_bp)
api.register_blueprint(ticket_bp)


@app.route('/')
def login():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('main.html')

@app.route('/booking')
def booking_page():
    return render_template('booking.html')

if __name__ == '__main__':
    app.run(debug=True)