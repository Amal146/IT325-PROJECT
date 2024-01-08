import requests
from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from schemas import UserSchema, UserLoginSchema
from models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
from db import db

user_bp = Blueprint("Users", "users", url_prefix="/users", description="Operations on users")


@user_bp.route("/<int:id>")
class UserResource(MethodView):
    @user_bp.response(200, UserSchema)
    #Get user by id
    def get(self, id):
        user = User.query.get_or_404(id)
        return user , 200

    @user_bp.arguments(UserSchema)
    @user_bp.response(200, UserSchema)
    #Update user by id
    def put(self, data, id):
        user = User.query.get_or_404(id)
        if user:
            User.username = data["username"]
            User.email = data["email"]
            User.password = pbkdf2_sha256.hash(data["password"])
        else:
            user = User(id=id, **data)
        db.session.add(user)
        db.session.commit()
        return user , 200

    @user_bp.response(204)
    #Delete user by id
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return "user deleted", 204


@user_bp.route("")
class UserListResource(MethodView):
    @user_bp.response(200, UserSchema(many=True))
    #Get all users
    def get(self):
        users = User.query.all()
        return [user for user in users], 200

    @user_bp.arguments(UserSchema)
    @user_bp.response(201, UserSchema)
    
    #Create new user by admin
    def post(self, data):
        user = User(**data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding the user.")
        return user , 201


@user_bp.route("/register" , methods = ['POST'] )
class UserRegister(MethodView):
    @user_bp.arguments(UserSchema)
    #Register new user
    def post(self, user_data):
        
        if User.query.filter(User.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        if User.query.filter(User.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")
            
        user = User(
            username=user_data["username"],
            email = user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return 'Registration successful', 200


@user_bp.route("/login", methods=['POST'])
class UserLogin(MethodView):
    @user_bp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = User.query.filter(User.email == user_data["email"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token, "user_id": user.id}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401



def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
        auth=("api", "YOUR_API_KEY"),
        data={
            "from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
            "to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!",
        },
    )
