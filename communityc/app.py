import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import User, db, Service, Booking, Pricing
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import base64, requests
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# JWT secret key
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')

# PostgreSQL database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:munezz456@localhost:5432/communityc'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize JWT
jwt = JWTManager(app)

# Initialize and configure the database
migrate = Migrate(app, db)
db.init_app(app)

# Secret key for the app
secret_key = os.urandom(32)
app.secret_key = secret_key
print(secret_key)

MPESA_API_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
MPESA_SHORTCODE = '600977'  # Replace with your shortcode
MPESA_LIPA_NG_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Replace with your passkey
MPESA_LIPA_NG_SHORTCODE = '174379'  # Replace with your shortcode

# The sandbox environment requires basic authentication
MPESA_CONSUMER_KEY = 'mAeMdg6ISlveifhemRILA60mECDBitWvJx5B2s986X6eomWl'  # Replace with your consumer key
MPESA_CONSUMER_SECRET = 'MpGZtqyrNWeXJGg45OhFDOPfrG86aXnPRfn2hBw1AXUJq0uAltGNMVvCYh3GC9WW'  # Replace with your consumer secret

def get_mpesa_access_token():
    MPESA_CONSUMER_KEY = 'mAeMdg6ISlveifhemRILA60mECDBitWvJx5B2s986X6eomWl'
    MPESA_CONSUMER_SECRET = 'MpGZtqyrNWeXJGg45OhFDOPfrG86aXnPRfn2hBw1AXUJq0uAltGNMVvCYh3GC9WW'
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    # Encode consumer key and secret
    auth = base64.b64encode(f'{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}'.encode()).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Print headers and URL
    print(f"Request URL: {auth_url}")
    print(f"Authorization Header: {headers['Authorization']}")

    response = requests.get(auth_url, headers=headers)
    
    # Print detailed response information
    print(f"MPESA access token response status: {response.status_code}")
    print(f"MPESA access token response headers: {response.headers}")
    print(f"MPESA access token response content: {response.text}")

    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data.get('access_token')
        except requests.exceptions.JSONDecodeError:
            raise Exception("Failed to parse JSON response")
    else:
        raise Exception(f"Failed to get access token, status code: {response.status_code}")

@app.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.json
    phone_number = data.get('phoneNumber')
    amount = data.get('amount')

    # Log the incoming data
    app.logger.info(f"Received data: {data}")
    app.logger.info(f"Phone number: {phone_number}")
    app.logger.info(f"Amount: {amount}")

    if not phone_number or not amount:
        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

    access_token = get_mpesa_access_token()
    app.logger.info(f"Access token: {access_token}")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Make the request to MPESA API
    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json={
        'phoneNumber': phone_number,
        'amount': amount
    }, headers=headers)

    app.logger.info(f"MPESA API response status: {response.status_code}")
    app.logger.info(f"MPESA API response content: {response.text}")

    if response.status_code == 200:
        return jsonify({'status': 'success', 'message': 'Payment processed'}), 200
    else:
        return jsonify({'status': 'error', 'message': response.text}), response.status_code

    
    # Prepare the payload
    payload = {
        "BusinessShortCode": MPESA_LIPA_NG_SHORTCODE,
        "Password": base64.b64encode(f'{MPESA_LIPA_NG_SHORTCODE}{MPESA_LIPA_NG_PASSKEY}{datetime.now().strftime("%Y%m%d%H%M%S")}'.encode()).decode(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 600977,  
        "PartyB": 600000,  
        "PhoneNumber": phone_number,
        "CallBackURL": 'https://yourdomain.com/callback',
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for services"
    }

    response = requests.post(MPESA_API_URL, headers=headers, json=payload)
    return jsonify(response.json())


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

# Create account route with JWT
@app.route('/create_account', methods=['POST'])
def create_user():
    data = request.json
    
    # Hash the user's password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    # Create a new user instance with the hashed password
    new_user = User(firstname=data['firstname'],lastname=data['lastname'],username=data['username'], password=hashed_password, email=data['email'], phone_number=data['phone_number'], location=data['location'],)

    try:
        db.session.add(new_user)
        db.session.commit()

        # Create JWT token with user ID
        access_token = create_access_token(identity=str(new_user.id))
        return jsonify(access_token=access_token), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username,
                 'email': user.email, 'phone_number': user.phone_number} for user in users]
    return jsonify(user_list)

# Get a specific user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number
        })
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<string:username>', methods=['GET'])
# @jwt_re`quired
def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()

        if user:
            user_data = {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number, 
            }

            return jsonify({'user': user_data}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a user by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    for key, value in data.items():
        setattr(user, key, value)

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/services', methods=['POST'])
def create_service():
    data = request.json
    
    if isinstance(data, list):
        return jsonify({'error': 'Expected JSON object, but received a list'}), 400
    
    service = Service(
        name=data['name'],
        image=data['image'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully'})

@app.route('/services', methods=['GET'])
def get_services():
    categories = request.args.getlist('categories')

    if categories:
        # Fetch services that belong to the selected categories
        services = Service.query.filter(Service.category.in_(categories)).all()
    else:
        # Fetch all services if no categories are selected
        services = Service.query.all()

    services_data = [
        {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'category': service.category,
            'image': service.image
        } for service in services
    ]
    
    categories_data = list(set(service.category for service in Service.query.all()))  # Get all categories
    
    return jsonify({'services': services_data, 'categories': categories_data})

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if service:
        service_data = {
            'id': service.id, 
            'name': service.name,
            'image': service.image,
            'description': service.description,
            'category': service.category
        }
        return jsonify({'service': service_data})
    return jsonify({'message': 'Service not found'}, 404)

@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}, 404)
    
    data = request.json
    service.name = data.get('name', service.name)
    service.image = data.get('image', service.image)
    service.description = data.get('description', service.description)
    service.category = data.get('category', service.category)
    
    db.session.commit()
    return jsonify({'message': 'Service updated successfully'})

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}, 404)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'})

@app.route('/services/category/<string:category_name>', methods=['GET'])
def get_services_by_category(category_name):
    # Convert the URL parameter to match the format in your database if necessary
    category_name = category_name.replace('-', ' ')  # if using hyphens in URL
    
    services = Service.query.filter_by(category=category_name).all()
    if not services:
        return jsonify({'message': 'No services found in this category'}), 404
    
    # Serialize the services to JSON
    services_list = [
        {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'category': service.category,
            'image': service.image
        }
        for service in services
    ]
    
    return jsonify(services_list)

@app.route('/calculate-price', methods=['POST'])
def calculate_price_route():
    data = request.json
    service_id = data.get('service_id')
    service_type = data.get('service_type')  # 'small', 'medium', or 'hard'

    # Call the calculate_price function
    total_price = calculate_price(service_id, service_type)

    if total_price is None:
        return jsonify({'error': 'Invalid service type or pricing rule not found'}), 404

    return jsonify({'total_price': total_price}), 200

@app.route('/service-pricing', methods=['GET'])
def get_service_pricing():
    service_name = request.args.get('service_name')
    
    # Ensure the service_name is provided
    if not service_name:
        return jsonify({"error": "Missing service_name parameter"}), 400
    
    # Fetch the service from the database
    service = Service.query.filter_by(name=service_name).first()
    
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    # Fetch pricing information for the service
    pricing = Pricing.query.filter_by(service_id=service.id).first()
    
    if not pricing:
        return jsonify({"error": "Pricing information not found for the service"}), 404
    
    # Prepare the pricing data
    pricing_data = {
        "small": pricing.small_service_price,
        "medium": pricing.medium_service_price,
        "hard": pricing.hard_service_price
    }
    
    return jsonify(pricing_data)

@app.route('/pricing', methods=['POST'])
def add_pricing():
    data = request.json

    service_id = data.get('service_id')
    small_price = data.get('small_service_price')
    medium_price = data.get('medium_service_price')
    hard_price = data.get('hard_service_price')

    # Validate the incoming data
    if not all([service_id, small_price, medium_price, hard_price]):
        return jsonify({"message": "All fields are required"}), 400

    try:
        # Check if pricing already exists for this service
        pricing = Pricing.query.filter_by(service_id=service_id).first()
        if pricing:
            # Update existing pricing
            pricing.small_service_price = small_price
            pricing.medium_service_price = medium_price
            pricing.hard_service_price = hard_price
        else:
            # Create new pricing entry
            pricing = Pricing(
                service_id=service_id,
                small_service_price=small_price,
                medium_service_price=medium_price,
                hard_service_price=hard_price
            )
            db.session.add(pricing)
        
        db.session.commit()
        return jsonify({"message": "Pricing information updated successfully"}), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Error occurred while updating pricing"}), 500

@app.route('/pricing/<int:service_id>', methods=['GET'])
def get_pricing(service_id):
    pricing = Pricing.query.filter_by(service_id=service_id).first()
    
    if pricing:
        return jsonify({
            "service_id": pricing.service_id,
            "small_service_price": pricing.small_service_price,
            "medium_service_price": pricing.medium_service_price,
            "hard_service_price": pricing.hard_service_price
        }), 200
    else:
        return jsonify({"message": "Pricing not found"}), 404

@app.route('/pricing/<int:service_id>', methods=['PUT'])
def update_pricing(service_id):
    data = request.json

    small_price = data.get('small_service_price')
    medium_price = data.get('medium_service_price')
    hard_price = data.get('hard_service_price')

    # Validate the incoming data
    if not all([small_price, medium_price, hard_price]):
        return jsonify({"message": "All fields are required"}), 400

    pricing = Pricing.query.filter_by(service_id=service_id).first()
    
    if pricing:
        pricing.small_service_price = small_price
        pricing.medium_service_price = medium_price
        pricing.hard_service_price = hard_price
        db.session.commit()
        return jsonify({"message": "Pricing information updated successfully"}), 200
    else:
        return jsonify({"message": "Pricing not found"}), 404

@app.route('/pricing/<int:service_id>', methods=['DELETE'])
def delete_pricing(service_id):
    pricing = Pricing.query.filter_by(service_id=service_id).first()
    
    if pricing:
        db.session.delete(pricing)
        db.session.commit()
        return jsonify({"message": "Pricing information deleted successfully"}), 200
    else:
        return jsonify({"message": "Pricing not found"}), 404


@app.route('/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()

        # Check for required fields
        required_fields = ['name', 'email', 'phone_number', 'service_name', 'date', 'time', 'service_difficulty', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create a new booking
        new_booking = Booking(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            county=data.get('county'),
            town=data.get('town'),
            street=data.get('street'),
            service_name=data['service_name'],
            date=data['date'],
            time=data['time'],
            service_difficulty=data['service_difficulty'],
            price=data['price'],
            additional_info=data.get('additional_info')
        )

        # Add to the database
        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking created successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    booking_list = []
    for booking in bookings:
        booking_list.append({
            'id': booking.id,
            'user_id': booking.user_id,
            'service_id': booking.service_id,
            'name': booking.name,
            'email': booking.email,
            'phone_number': booking.phone_number,
            'county': booking.county,
            'town': booking.town,
            'street': booking.street,
            'service_name': booking.service_name,
            'date': booking.date,
            'time': booking.time,
            'service_difficulty': booking.service_difficulty,
            'price': booking.price,
            'additional_info': booking.additional_info
        })
    return jsonify({'bookings': booking_list}), 200

@app.route('/booking/<int:id>', methods=['GET'])
def get_booking_by_id(id):
    booking = Booking.query.get(id)
    if booking:
        booking_data = {
            'id': booking.id,
            'user_id': booking.user_id,
            'service_id': booking.service_id,
            'name': booking.name,
            'email': booking.email,
            'phone_number': booking.phone_number,
            'county': booking.county,
            'town': booking.town,
            'street': booking.street,
            'service_name': booking.service_name,
            'date': booking.date,
            'time': booking.time,
            'service_difficulty': booking.service_difficulty,
            'price': booking.price,
            'additional_info': booking.additional_info
        }
        return jsonify({'booking': booking_data}), 200
    else:
        return jsonify({'error': 'Booking not found'}), 404

@app.route('/booking/<string:username>', methods=['GET'])
def get_booking_by_username(username):
    try:
        booking = Booking.query.filter_by(name=username).first()

        if booking:
            booking_data = {
                'id': booking.id,
                'user_id': booking.user_id,
                'service_id': booking.service_id,
                'name': booking.name,
                'email': booking.email,
                'phone_number': booking.phone_number,
                'county': booking.county,
                'town': booking.town,
                'street': booking.street,
                'service_name': booking.service_name,
                'date': booking.date,
                'time': booking.time,
                'service_difficulty': booking.service_difficulty,
                'price': booking.price,
                'additional_info': booking.additional_info
            }

            return jsonify({'booking': booking_data}), 200
        else:
            return jsonify({'error': 'Booking not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/booking/<int:id>', methods=['DELETE'])
# def delete_booking(id):
#     booking = Booking.query.get(id)
#     if booking:
#         db.session.delete(booking)
#         db.session.commit()
#         return jsonify({'message': 'Booking deleted successfully'}), 200
#     else:
#         return jsonify({'error': 'Booking not found'}), 404

@app.route('/admin/bookings', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

# Route to get all users
@app.route('/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username,
                 'email': user.email, 'phone_number': user.phone_number} for user in users]
    return jsonify(user_list)

# Route to delete a booking
@app.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted successfully'})
    return jsonify({'message': 'Booking not found'}), 404

# Route to update a booking
@app.route('/admin/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.json
    booking = Booking.query.get(booking_id)
    if booking:
        booking.status = data.get('status', booking.status)
        db.session.commit()
        return jsonify({'message': 'Booking updated successfully'})
    return jsonify({'message': 'Booking not found'}), 404

# Route to add a new booking
@app.route('/admin/bookings', methods=['POST'])
def add_booking():
    data = request.json
    new_booking = Booking(**data)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking added successfully'}), 201   

if __name__ == '__main__':
  app.run(debug=True, port=5000)