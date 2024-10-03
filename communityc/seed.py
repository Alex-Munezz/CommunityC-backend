from app import app
from models import db, Pricing, Service, Subcategory  # Adjust import based on your structure

def seed_pricing_data():
    with app.app_context(): 
    # Example services and their corresponding subcategory IDs
    #   services = {
    #     'Freelance Writing Services': 16,
    #     'Plumbing Services': 5,
    #     'Electrical Services': 6,
    #     'Fitness Training Services': 7,
    #     'Braiding/Plaiting Services': 8,
    #     'Cleaning Services': 9,
    #     'Nail Services': 10,
    #     'Gardening Services': 11,
    #     'Pest Control Services': 12,
    #     'Tutoring Services': 13,
    #     'Auto Repair Services': 14,
    #     'Painting Services': 15,
    #     'Web Development Services': 17,
    #     'Graphic Design Services': 18,
    #     'Event Planning Services': 19,
    #     'Photography Services': 20,
    #     'Pet Sitting Services': 21,
    #     'Catering Services': 22,
    #     'Translating Services': 23,
    #     'Interior Designing Services': 24,
    # }

    # # Subcategories and their corresponding IDs
    # subcategories = {
    #     'Blog Writing': 1,
    #     'Technical Writing': 2,
    #     'Copywriting': 3,
    #     'Leak Repair': 4,
    #     'Pipe Installation': 5,
    #     'Drain Cleaning': 6,
    #     'Wiring Installation': 7,
    #     'Electrical Repairs': 8,
    #     'Safety Inspections': 9,
    #     'Personal Training': 10,
    #     'Group Classes': 11,
    #     'Nutritional Coaching': 12,
    #     'Box Braids': 13,
    #     'Cornrows': 14,
    #     'Twists': 15,
    #     'Regular Housekeeping': 16,
    #     'Deep Cleaning': 17,
    #     'Move-In/Move-Out Cleaning': 18,
    #     'Pedicure': 19,
    #     'Manicure': 20,
    #     'Nail Polishing': 21,
    #     'Nail Art': 22,
    #     'Lawn Care': 23,
    #     'Garden Design': 24,
    #     'Plant Maintenance': 25,
    #     'Termite Control': 26,
    #     'Rodent Removal': 27,
    #     'Insect Treatment': 28,
    #     'Primary Tutoring': 29,
    #     'HighSchool Tutoring': 30,
    #     'Kindergarten Tutoring': 31,
    #     'Diagnostics': 32,
    #     'Oil Change': 33,
    #     'Brake Repair': 34,
    #     'Interior Painting': 35,
    #     'Exterior Painting': 36,
    #     'Decorative Painting': 37,
    #     'Front-end Development': 38,
    #     'Back-end Development': 39,
    #     'Full-stack Development': 40,
    #     'Logo Design': 41,
    #     'Brochure Design': 42,
    #     'Social Media Graphics': 43,
    #     'Wedding Planning': 44,
    #     'Corporate Events': 45,
    #     'Private Parties': 46,
    #     'Portrait Photography': 47,
    #     'Event Photography': 48,
    #     'Commercial Photography': 49,
    #     'Dog Walking': 50,
    #     'Pet Feeding': 51,
    #     'Overnight/Day Care': 52,
    #     'Corporate Catering': 53,
    #     'Wedding Catering': 54,
    #     'Event Catering': 55,
    #     'Document Translation': 56,
    #     'Website Translation': 57,
    #     'Interpretation Services': 58,
    #     'Residential Design': 59,
    #     'Commercial Design': 60,
    #     'Space Planning': 61,
    # }

    # Pricing data for each service's subcategories
      pricing_data = [
        (services['Freelance Writing Services'], subcategories['Blog Writing'], 1000.00),
        (services['Freelance Writing Services'], subcategories['Technical Writing'], 1500.00),
        (services['Freelance Writing Services'], subcategories['Copywriting'], 1200.00),
        (services['Plumbing Services'], subcategories['Leak Repair'], 1000.00),
        (services['Plumbing Services'], subcategories['Pipe Installation'], 2000.00),
        (services['Plumbing Services'], subcategories['Drain Cleaning'], 1500.00),
        (services['Electrical Services'], subcategories['Wiring Installation'], 2500.00),
        (services['Electrical Services'], subcategories['Electrical Repairs'], 1500.00),
        (services['Electrical Services'], subcategories['Safety Inspections'], 1000.00),
        (services['Fitness Training Services'], subcategories['Personal Training'], 3000.00),
        (services['Fitness Training Services'], subcategories['Group Classes'], 2000.00),
        (services['Fitness Training Services'], subcategories['Nutritional Coaching'], 5000.00),
        (services['Braiding/Plaiting Services'], subcategories['Box Braids'], 2000.00),
        (services['Braiding/Plaiting Services'], subcategories['Cornrows'], 3000.00),
        (services['Braiding/Plaiting Services'], subcategories['Twists'], 2000.00),
        (services['Cleaning Services'], subcategories['Regular Housekeeping'], 2000.00),
        (services['Cleaning Services'], subcategories['Deep Cleaning'], 4000.00),
        (services['Cleaning Services'], subcategories['Move-In/Move-Out Cleaning'], 5000.00),
        (services['Nail Services'], subcategories['Pedicure'], 800.00),
        (services['Nail Services'], subcategories['Manicure'], 1000.00),
        (services['Nail Services'], subcategories['Nail Polishing'], 500.00),
        (services['Nail Services'], subcategories['Nail Art'], 1000.00),
        (services['Gardening Services'], subcategories['Lawn Care'], 2000.00),
        (services['Gardening Services'], subcategories['Garden Design'], 3000.00),
        (services['Gardening Services'], subcategories['Plant Maintenance'], 5000.00),
        (services['Pest Control Services'], subcategories['Termite Control'], 2000.00),
        (services['Pest Control Services'], subcategories['Rodent Removal'], 1500.00),
        (services['Pest Control Services'], subcategories['Insect Treatment'], 3000.00),
        (services['Tutoring Services'], subcategories['Primary Tutoring'], 3000.00),
        (services['Tutoring Services'], subcategories['HighSchool Tutoring'], 4000.00),
        (services['Tutoring Services'], subcategories['Kindergarten Tutoring'], 5000.00),
        (services['Auto Repair Services'], subcategories['Diagnostics'], 1000.00),
        (services['Auto Repair Services'], subcategories['Oil Change'], 1500.00),
        (services['Auto Repair Services'], subcategories['Brake Repair'], 1500.00),
        (services['Painting Services'], subcategories['Interior Painting'], 5000.00),
        (services['Painting Services'], subcategories['Exterior Painting'], 7000.00),
        (services['Painting Services'], subcategories['Decorative Painting'], 10000.00),
        (services['Web Development Services'], subcategories['Front-end Development'], 15000.00),
        (services['Web Development Services'], subcategories['Back-end Development'], 20000.00),
        (services['Web Development Services'], subcategories['Full-stack Development'], 30000.00),
        (services['Graphic Design Services'], subcategories['Logo Design'], 500.00),
        (services['Graphic Design Services'], subcategories['Brochure Design'], 1000.00),
        (services['Graphic Design Services'], subcategories['Social Media Graphics'], 800.00),
        (services['Event Planning Services'], subcategories['Wedding Planning'], 4000.00),
        (services['Event Planning Services'], subcategories['Corporate Events'], 6000.00),
        (services['Event Planning Services'], subcategories['Private Parties'], 5000.00),
        (services['Photography Services'], subcategories['Portrait Photography'], 2000.00),
        (services['Photography Services'], subcategories['Event Photography'], 6000.00),
        (services['Photography Services'], subcategories['Commercial Photography'], 10000.00),
        (services['Pet Sitting Services'], subcategories['Dog Walking'], 1000.00),
        (services['Pet Sitting Services'], subcategories['Pet Feeding'], 1000.00),
        (services['Pet Sitting Services'], subcategories['Overnight/Day Care'], 2000.00),
        (services['Catering Services'], subcategories['Corporate Catering'], 80000.00),
        (services['Catering Services'], subcategories['Wedding Catering'], 50000.00),
        (services['Catering Services'], subcategories['Event Catering'], 40000.00),
        (services['Translating Services'], subcategories['Document Translation'], 200.00),
        (services['Translating Services'], subcategories['Website Translation'], 1000.00),
        (services['Translating Services'], subcategories['Interpretation Services'], 2000.00),
        (services['Interior Designing Services'], subcategories['Residential Design'], 5000.00),
        (services['Interior Designing Services'], subcategories['Commercial Design'], 10000.00),
        (services['Interior Designing Services'], subcategories['Space Planning'], 10000.00),
    ]

    for service_id, subcategory_id, price in pricing_data:
        pricing = Pricing(service_id=service_id, subcategory_id=subcategory_id, price=price)
        db.session.add(pricing)

    db.session.commit()

if __name__ == '__main__':
    seed_pricing_data()
