from .models import Pricing

def calculate_price(service_id, service_type):
    # Fetch the pricing rules from the database
    pricing = Pricing.query.filter_by(service_id=service_id).first()

    if not pricing:
        return None  # Or handle accordingly if no pricing rule is found

    # Determine the price based on service type
    if service_type == 'small':
        total_price = pricing.small_service_price
    elif service_type == 'medium':
        total_price = pricing.medium_service_price
    elif service_type == 'hard':
        total_price = pricing.hard_service_price
    else:
        return None  # Or handle accordingly if service type is invalid

    return total_price
