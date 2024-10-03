from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Consider hashing
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False) 
    location = db.Column(db.String(50), nullable=False)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)  # Adjusted length
    category = db.Column(db.String(100), nullable=False)

    subcategories = db.relationship('Subcategory', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name}>'

class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    def __repr__(self):
        return f'<Subcategory {self.name}>'

class Pricing(db.Model):
    __tablename__ = 'pricing'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Using Numeric for precision

    subcategory = db.relationship('Subcategory', backref='pricing')

    def __repr__(self):
        return f'<Pricing {self.price} for subcategory {self.subcategory.name}>'

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)  
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    county = db.Column(db.String(100), nullable=True)
    town = db.Column(db.String(100), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)
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

    user = db.relationship('User', foreign_keys=[user_id])
    provider = db.relationship('User', foreign_keys=[provider_id])
    service = db.relationship('Service')

class Payment(db.Model):
    __tablename__='payment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Using Numeric for precision
    status = db.Column(db.String(20), nullable=False, default='pending')
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship('User')
    booking = db.relationship('Booking')
