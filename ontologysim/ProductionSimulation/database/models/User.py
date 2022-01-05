import datetime

import jwt

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from ontologysim.ProductionSimulation.database.models.Base import Base

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    userName = Column(String,nullable=False,unique=True)
    simulationRuns = relationship("SimulationRun", back_populates="user")

    email = Column(String,unique=True)
    password = Column(String)
    authenticated = Column(Boolean, default=False)
    isAdmin = Column(Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                #app.config.get('SECRET_KEY'),
                "secretKey",
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def verify_password(self, password, bcrypt=None):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        #payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        payload = jwt.decode(auth_token,"secretKey")

        #TODO test

        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'