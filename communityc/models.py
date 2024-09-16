from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)  # Changed to String for better compatibility
    location = db.Column(db.String(50), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(10000), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'

class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    small_service_price = db.Column(db.Float, nullable=False)
    medium_service_price = db.Column(db.Float, nullable=False)
    hard_service_price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    county = db.Column(db.String(100), nullable=True)
    town = db.Column(db.String(100), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    service_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    service_difficulty = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    additional_info = db.Column(db.String(200))

class Review(db.Model):
    __tablename__ ='review'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # e.g., pending, completed, failed
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)  # For third-party payment reference
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, user_id, booking_id, amount, status='pending', transaction_id=None):
        self.user_id = user_id
        self.booking_id = booking_id
        self.amount = amount
        self.status = status
        self.transaction_id = transaction_id
