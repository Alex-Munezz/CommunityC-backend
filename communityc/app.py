import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import User, db, Service, Booking, Pricing, Subcategory
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

from flask_mail import Mail, Message

# Initialize Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Or your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bookings.communityc@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'rlwr sumz tzui ztxj'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'bookings.communityc@gmail.com'  # Default sender email

mail = Mail(app)


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

    # Create the new service
    service = Service(
        name=data['name'],
        image=data['image'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(service)
    db.session.commit()  # Commit to get the service ID for subcategories

    # Create subcategories if provided
    subcategories = data.get('subcategories', [])
    for sub_data in subcategories:
        subcategory = Subcategory(name=sub_data['name'], service_id=service.id)  # Use service.id
        db.session.add(subcategory)

    db.session.commit()  # Commit after adding subcategories
    return jsonify({'message': 'Service created successfully'})

# Route to get all services
@app.route('/services', methods=['GET'])
def get_services():
    categories = request.args.getlist('categories')
    subcategories = request.args.getlist('subcategories')

    # Build the filter based on selected categories and subcategories
    query = Service.query

    if categories:
        query = query.filter(Service.category.in_(categories))
    
    if subcategories:
        query = query.join(Service.subcategories).filter(Subcategory.name.in_(subcategories))

    # Fetch services based on filters
    services = query.all()

    services_data = [
        {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'category': service.category,
            'subcategories': [subcategory.name for subcategory in service.subcategories],  # Include all subcategories
            'image': service.image
        } for service in services
    ]
    
    # Get all categories and subcategories for the response
    categories_data = list(set(service.category for service in Service.query.all()))  # Get all categories
    subcategories_data = list(set(subcategory.name for subcategory in Subcategory.query.all()))  # Get all subcategories

    return jsonify({'services': services_data, 'categories': categories_data, 'subcategories': subcategories_data})


# Route to get a service by ID
@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if service:
        service_data = {
            'id': service.id,
            'name': service.name,
            'image': service.image,
            'description': service.description,
            'category': service.category,
            'subcategories': [{'id': sub.id, 'name': sub.name} for sub in service.subcategories]
        }
        return jsonify({'service': service_data})
    return jsonify({'message': 'Service not found'}), 404


# Route to update a service by ID
@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    
    data = request.json
    service.name = data.get('name', service.name)
    service.image = data.get('image', service.image)
    service.description = data.get('description', service.description)
    service.category = data.get('category', service.category)

    # Update subcategories if provided
    if 'subcategories' in data:
        # Clear existing subcategories
        service.subcategories.clear()
        # Add new subcategories
        for subcategory_name in data['subcategories']:
            subcategory = Subcategory.query.filter_by(name=subcategory_name, service_id=service.id).first()
            if subcategory:
                service.subcategories.append(subcategory)
            else:
                # Create new subcategory if it doesn't exist
                new_subcategory = Subcategory(name=subcategory_name, service_id=service.id)
                db.session.add(new_subcategory)
                service.subcategories.append(new_subcategory)

    db.session.commit()
    return jsonify({'message': 'Service updated successfully'}), 200

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    
    # Delete associated subcategories
    for subcategory in service.subcategories:
        db.session.delete(subcategory)

    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'}), 200



@app.route('/pricing', methods=['POST'])
def seed_pricing_data():
    # Load JSON data from request
    data = request.get_json()
    
    # Check if data is provided
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        for item in data:
            pricing = Pricing(
                service_id=item['service_id'],
                subcategory_id=item['subcategory_id'],
                price=item['price']
            )
            db.session.add(pricing)

        db.session.commit()
        return jsonify({"message": "Pricing data seeded successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/pricing', methods=['GET'])
def get_pricing():
    service_id = request.args.get('service_id')
    subcategory_id = request.args.get('subcategory_id')

    # Assuming you have a method to get the IDs based on names
    service = Service.query.filter_by(name=service_id).first()
    subcategory = Subcategory.query.filter_by(name=subcategory_id).first()

    if not service or not subcategory:
        return jsonify({'error': 'Invalid service ID or subcategory ID'}), 400

    pricing = Pricing.query.filter_by(service_id=service.id, subcategory_id=subcategory.id).first()
    
    if not pricing:
        return jsonify({'error': 'Pricing not found'}), 404

    return jsonify({
        'id': pricing.id,
        'price': pricing.price
    })



# Route to get a pricing entry by ID
@app.route('/pricing/<int:id>', methods=['GET'])
def get_pricing_by_id(id):
    pricing = Pricing.query.get_or_404(id)
    return jsonify({
        'id': pricing.id,
        'service_id': pricing.service_id,
        'subcategory_id': pricing.subcategory_id,
        'price': pricing.price
    }), 200

# Route to update a pricing entry by ID
@app.route('/pricing/<int:id>', methods=['PUT'])
def update_pricing(id):
    pricing = Pricing.query.get_or_404(id)
    data = request.get_json()
    
    pricing.service_id = data.get('service_id', pricing.service_id)
    pricing.subcategory_id = data.get('subcategory_id', pricing.subcategory_id)
    pricing.price = data.get('price', pricing.price)
    
    db.session.commit()
    return jsonify({
        'id': pricing.id,
        'service_id': pricing.service_id,
        'subcategory_id': pricing.subcategory_id,
        'price': pricing.price
    }), 200

# Route to delete a pricing entry by ID
@app.route('/pricing/<int:id>', methods=['DELETE'])
def delete_pricing(id):
    pricing = Pricing.query.get_or_404(id)
    db.session.delete(pricing)
    db.session.commit()
    return jsonify({'message': 'Pricing entry deleted successfully'}), 204


@app.route('/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()

        # Check for required fields
        required_fields = ['name', 'email', 'phone_number', 'county', 'town', 'street', 'service_name', 'date', 'time', 'subcategory', 'price', 'additional_info']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Validate email format
        if '@' not in data['email']:
            return jsonify({'error': 'Invalid email format'}), 400

        # Validate phone number format
        if not data['phone_number'].isdigit() or len(data['phone_number']) < 10:
            return jsonify({'error': 'Invalid phone number'}), 400

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
            subcategory=",".join(data['subcategory']),
            price=data['price'],
            additional_info=data.get('additional_info')
        )

        # Add the booking to the database
        db.session.add(new_booking)
        db.session.commit()

        # Send confirmation email to the user
        send_booking_confirmation_email(data['email'], data['name'], new_booking)

        return jsonify({'message': 'Booking created successfully', 'booking_id': new_booking.id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_booking_confirmation_email(email, name, booking):
    try:
        msg = Message(
            subject="Booking Confirmation",
            recipients=[email],  # The recipient's email address
            body=f"Dear {name},\n\nYour booking for {booking.service_name} on {booking.date} at {booking.time} has been confirmed. \nThe Total price for your service is {booking.price} Kshs. Please pay it to the following till number : 00100 two days before your booking date then reply to this email and attach confirmation message from Mpesa as a screenshot so as we can confirm it on our side. Failure to do so, we will cancel your booking. \n\n Thank you for choosing CommunityCrafters, your no. 1 marketplace for all your services!\n\nFor any questions, inquiries or changing the time/date of your booking, feel free to reply to this email or call +254768453442\n\nBest regards,\nThe CommunityCrafters Team"
        )
        mail.send(msg)
        print(f"Confirmation email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")



@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    booking_list = []
    for booking in bookings:
        booking_list.append({
            'id': booking.id,
            'name': booking.name,
            'email': booking.email,
            'phone_number': booking.phone_number,
            'county': booking.county,
            'town': booking.town,
            'street': booking.street,
            'service_name': booking.service_name,
            'date': booking.date,
            'time': booking.time,
            'subcategory': booking.subcategory,
            'price': booking.price,
            'additional_info': booking.additional_info
        })
    return jsonify({'bookings': booking_list}), 200

@app.route('/bookings/<int:id>', methods=['GET'])
def get_booking_by_id(id):
    booking = Booking.query.get(id)
    if booking:
        booking_data = {
            'id': booking.id,
            'name': booking.name,
            'email': booking.email,
            'phone_number': booking.phone_number,
            'county': booking.county,
            'town': booking.town,
            'street': booking.street,
            'service_name': booking.service_name,
            'date': booking.date,
            'time': booking.time,
            'subcategory': booking.subcategory,
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
                'name': booking.name,
                'email': booking.email,
                'phone_number': booking.phone_number,
                'county': booking.county,
                'town': booking.town,
                'street': booking.street,
                'service_name': booking.service_name,
                'date': booking.date,
                'time': booking.time,
                'subcategory': booking.subcategory,
                'price': booking.price,
                'additional_info': booking.additional_info
            }

            return jsonify({'booking': booking_data}), 200
        else:
            return jsonify({'error': 'Booking not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        # Find the booking by ID
        booking = Booking.query.get(booking_id)
        
        # If the booking doesn't exist, return a 404 error
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Delete the booking
        db.session.delete(booking)
        db.session.commit()
        
        return jsonify({'message': 'Booking deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    try:
        data = request.get_json()

        # Find the booking by ID
        booking = Booking.query.get(booking_id)

        # If the booking doesn't exist, return a 404 error
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Update the booking fields with new data
        booking.name = data.get('name', booking.name)
        booking.email = data.get('email', booking.email)
        booking.phone_number = data.get('phone_number', booking.phone_number)
        booking.county = data.get('county', booking.county)
        booking.town = data.get('town', booking.town)
        booking.street = data.get('street', booking.street)
        booking.service_name = data.get('service_name', booking.service_name)
        booking.date = data.get('date', booking.date)
        booking.time = data.get('time', booking.time)
        booking.subcategory = ",".join(data['subcategory']) if 'subcategory' in data else booking.subcategory
        booking.price = data.get('price', booking.price)
        booking.additional_info = data.get('additional_info', booking.additional_info)

        # Save the updated booking to the database
        db.session.commit()

        return jsonify({'message': 'Booking updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/subcategories', methods=['POST'])
def create_subcategory():
    data = request.get_json()
    new_subcategory = Subcategory(name=data['name'], service_id=data['service_id'])
    db.session.add(new_subcategory)
    db.session.commit()
    return jsonify({'id': new_subcategory.id, 'name': new_subcategory.name, 'service_id': new_subcategory.service_id}), 201

# Route to get all subcategories
@app.route('/subcategories', methods=['GET'])
def get_subcategories():
    subcategories = Subcategory.query.all()
    return jsonify([{ 'id': subcategory.id, 'name': subcategory.name, 'service_id': subcategory.service_id } for subcategory in subcategories]), 200

# Route to get a subcategory by ID
@app.route('/subcategories/<int:id>', methods=['GET'])
def get_subcategory(id):
    subcategory = Subcategory.query.get_or_404(id)
    return jsonify({'id': subcategory.id, 'name': subcategory.name, 'service_id': subcategory.service_id}), 200

# Route to update a subcategory by ID
@app.route('/subcategories/<int:id>', methods=['PUT'])
def update_subcategory(id):
    subcategory = Subcategory.query.get_or_404(id)
    data = request.get_json()
    subcategory.name = data.get('name', subcategory.name)
    subcategory.service_id = data.get('service_id', subcategory.service_id)
    db.session.commit()
    return jsonify({'id': subcategory.id, 'name': subcategory.name, 'service_id': subcategory.service_id}), 200

# Route to delete a subcategory by ID
@app.route('/subcategories/<int:id>', methods=['DELETE'])
def delete_subcategory(id):
    subcategory = Subcategory.query.get_or_404(id)
    db.session.delete(subcategory)
    db.session.commit()
    return jsonify({'message': 'Subcategory deleted successfully'}), 204

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
# @app.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
# def delete_booking(booking_id):
#     booking = Booking.query.get(booking_id)
#     if booking:
#         db.session.delete(booking)
#         db.session.commit()
#         return jsonify({'message': 'Booking deleted successfully'})
#     return jsonify({'message': 'Booking not found'}), 404

# Route to update a booking
# @app.route('/admin/bookings/<int:booking_id>', methods=['PUT'])
# def update_booking(booking_id):
#     data = request.json
#     booking = Booking.query.get(booking_id)
#     if booking:
#         booking.status = data.get('status', booking.status)
#         db.session.commit()
#         return jsonify({'message': 'Booking updated successfully'})
#     return jsonify({'message': 'Booking not found'}), 404

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