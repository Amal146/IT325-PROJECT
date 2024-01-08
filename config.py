import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sport'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/sport_api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_key'

