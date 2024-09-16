from app import app, db
from models import Pricing

def seed_pricing():

 pricing_data = [
        {
            "service_id": 1,  
            "small_service_price": "1500",
            "medium_service_price": "2000",
            "hard_service_price": "3000"
        },
        {
            "service_id": 2,  
            "small_service_price": "1500",
            "medium_service_price": "2000",
            "hard_service_price": "3000"
        },
        {
            "service_id": 3,  
            "small_service_price": "3000",
            "medium_service_price": "5000",
            "hard_service_price": "10000"
        },
        {
            "service_id": 4,  
            "small_service_price": "2000",
            "medium_service_price": "3000",
            "hard_service_price": "5000"
        },
        {
            "service_id": 5,  
            "small_service_price": "2000",
            "medium_service_price": "4000",
            "hard_service_price": "6000"
        },
        {
            "service_id": 6,  
            "small_service_price": "3000",
            "medium_service_price": "5000",
            "hard_service_price": "7000"
        },
        {
            "service_id": 7,  
            "small_service_price": "2000",
            "medium_service_price": "4000",
            "hard_service_price": "6000"
        },
        {
            "service_id": 8,  
            "small_service_price": "4000",
            "medium_service_price": "6000",
            "hard_service_price": "8000"
        },
        {
            "service_id": 9,  
            "small_service_price": "2000",
            "medium_service_price": "4000",
            "hard_service_price": "6000"
        },
        {
            "service_id": 10,  
            "small_service_price": "2000",
            "medium_service_price": "4000",
            "hard_service_price": "6000"
        },
        {
            "service_id": 11,  
            "small_service_price": "8000",
            "medium_service_price": "10000",
            "hard_service_price": "20000"
        },
        {
            "service_id": 12,  
            "small_service_price": "3000",
            "medium_service_price": "6000",
            "hard_service_price": "10000"
        },
        {
            "service_id": 13,  
            "small_service_price": "5000",
            "medium_service_price": "10000",
            "hard_service_price": "20000"
        },
        {
            "service_id": 14,  
            "small_service_price": "700",
            "medium_service_price": "1500",
            "hard_service_price": "3000"
        },
        {
            "service_id": 15,  
            "small_service_price": "5000",
            "medium_service_price": "10000",
            "hard_service_price": "15000"
        },
        {
            "service_id": 16,  
            "small_service_price": "10000",
            "medium_service_price": "15000",
            "hard_service_price": "20000"
        },
        {
            "service_id": 17,  
            "small_service_price": "2500",
            "medium_service_price": "3000",
            "hard_service_price": "5000"
        },
        {
            "service_id": 18,  
            "small_service_price": "20000",
            "medium_service_price": "50000",
            "hard_service_price": "80000"
        },
        {
            "service_id": 19,  
            "small_service_price": "5000",
            "medium_service_price": "10000",
            "hard_service_price": "15000"
        },
        {
            "service_id": 20,  
            "small_service_price": "10000",
            "medium_service_price": "20000",
            "hard_service_price": "30000"
       }
    ]

 with app.app_context():
        db.create_all()

        for data in pricing_data:
            pricing = Pricing(
                service_id=data["service_id"],
                small_service_price=data["small_service_price"],
                medium_service_price=data["medium_service_price"],
                hard_service_price=data["hard_service_price"]
            )
            db.session.add(pricing)

        db.session.commit()
        print("Seed data added to the Pricing table.")

if __name__ == "__main__":
    seed_pricing()







#  {
#             "name": "Plumbing Services",
#             "description": "Professional plumbing services to fix leaks, install pipes, and maintain your plumbing systems. We ensure that your water supply and drainage are working efficiently.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRbvGLS5mjh3GzSxDaEzoR2Whs9OXCmGLQLBfIfGzES0RjCwm9QhrLEFeyRUrqQjzRWXw&usqp=CAU",
#             "category": "Home Services"
#         },
#         {
#             "name": "Electrical Services",
#             "description": "Expert electrical services for residential and commercial properties. From wiring installations to electrical repairs, our electricians ensure safety and efficiency.",
#             "image": "https://us.123rf.com/450wm/bermek/bermek2304/bermek230403255/202409630-power-cord-plugged-into-electrical-outlet-on-insulated-wall-in-hospital-room.jpg?ver=6",
#             "category": "Home Services"
#         },
#                 {
#             "name": "Fitness Training Services",
#             "description": "Personalized fitness training sessions to help you achieve your health and fitness goals. Our trainers provide tailored workouts, whether you’re looking to lose weight, build muscle, or improve overall fitness.",
#             "image": "https://thumbor.forbes.com/thumbor/fit-in/x/https://www.forbes.com/health/wp-content/uploads/2023/02/strength_training.jpeg.jpg",
#             "category": "Beauty and Wellness"
#         },
#                 {
#             "name": "Braiding/Plaiting Services",
#             "description": "Get beautiful and intricate braiding services to enhance your natural beauty. Our stylists specialize in various braiding styles, perfect for any occasion.",
#             "image": "https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/04/2-stunning-african-braids-CLPMe82H6Kw.jpg?resize=1073%2C1080&ssl=1",
#             "category": "Beauty and Wellness"
#         },
#                 {
#             "name": "Cleaning Services",
#             "description": "Comprehensive cleaning services for your home or office. From regular housekeeping to deep cleaning, our team ensures a spotless and hygienic environment.",
#             "image": "https://nextdaycleaning.com/wp-content/uploads/2020/06/Main-Benefits-of-Residential-Cleaning-Services-1024x663.jpg",
#             "category": "Home Services"
#         },
#                {
#             "name": "Chauffering Services",
#             "description": "Hire a professional chauffeur for safe and comfortable transportation. Whether you need a driver for a day or on a regular basis, our chauffeurs are reliable and courteous.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNQGVNChOwQkRxeYdZALSSNWbap2SsIrLviw&s",
#             "category": "Transportation"
#         },
#                 {
#             "name": "Gardening Services",
#             "description": "Professional gardening services including lawn care, garden design, and plant maintenance. Let us help you create and maintain a beautiful, thriving garden.",
#             "image": "https://www.collinsdictionary.com/images/full/gardening_380327731_1000.jpg",
#             "category": "Home Services"
#         },
#                     {
#             "name": "Pest Control Services",
#             "description": "Effective pest control services to eliminate and prevent infestations. We offer treatments for termites, rodents, insects, and more, ensuring your property stays pest-free.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4tspuipeUeW4F2XwGQQUXyAcMp-SC6dsRAw&s",
#             "category": "Home Services"
#         },
#                         {
#             "name": "Tutoring Services",
#             "description": "Personalized tutoring services for students of all ages. Our tutors provide support in various subjects, helping students improve their academic performance and confidence.",
#             "image": "https://homeschool.co.ke/storage/NHS-1.jpg",
#             "category": "Education"
#         },
#                         {
#             "name": "Auto Repair Services",
#             "description": "Comprehensive auto repair services, including diagnostics, maintenance, and repairs. Our skilled mechanics ensure your vehicle runs smoothly and safely.",
#             "image": "https://img.freepik.com/free-vector/auto-repair-logos_1051-1008.jpg",
#             "category": "Auto Services"
#         },
#                         {
#             "name": "Painting Services",
#             "description": "Professional painting services for residential and commercial properties. We provide high-quality interior and exterior painting to give your space a fresh new look.",
#             "image": "https://piconepaintingandpaperhanging.com/wp-content/uploads/2017/01/Interior-House-Painting.jpg",
#             "category": "Home Services"
#         },
#                         {
#             "name": "Freelance Writing Services",
#             "description": "Expert freelance writing services for various content needs. From blog posts to technical writing, our writers deliver high-quality, well-researched content tailored to your audience.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2pdnYVqvij22MccsW5rrGw_PTEDBI8QcPEg&s",
#             "category": "Home Services"
#         },
#                         {
#             "name": "Web Development Services",
#             "description": "Custom web development services to create responsive, user-friendly websites. Our developers specialize in building websites that are visually appealing and optimized for performance.",
#             "image": "https://media.licdn.com/dms/image/D5612AQE9FeaaErOp9w/article-cover_image-shrink_600_2000/0/1676361066049?e=2147483647&v=beta&t=EBUFpz75f86mJISEy2I3etuIShJC1EyQl0I1w-Ga8Mw",
#             "category": "Technology"
#         },
#                         {
#             "name": "Graphic Design Services",
#             "description": "Creative graphic design services for logos, brochures, social media, and more. Our designers help you communicate your brand’s message through compelling visuals.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYt5jiyvNI3p4X6n9loQGAKNUZ_DqyyPTXEQ&s",
#             "category": "Creative Services"
#         },
#                         {
#             "name": "Event Planning Services",
#             "description": "Comprehensive event planning services for weddings, corporate events, and private parties. We handle everything from venue selection to day-of coordination to ensure a memorable event.",
#             "image": "https://www.proglobalevents.com/wp-content/uploads/bigstock-People-Planning-Concept-Entre-327380749-1.jpgfreelan",
#             "category": "Events"
#         },
#                         {
#             "name": "Photography Services",
#             "description": "Professional photography services for portraits, events, and commercial shoots. Our photographers capture high-quality images that tell your story and meet your needs.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROhxcyAxoRMQVVvAs7IDPi3wfQ6sg6q2Gc9Q&s",
#             "category": "Events"
#         },
#                         {
#             "name": "Pet Sitting Services",
#             "description": "Reliable pet sitting services to care for your pets while you’re away. Our pet sitters provide loving care, including feeding, walking, and companionship, to ensure your pets are happy and comfortable.",
#             "image": "https://i.cbc.ca/1.6654160.1668638085!/fileImage/httpImage/image.jpg_gen/derivatives/original_780/what-to-consider-when-looking-for-a-pet-sitter.jpg",
#             "category": "Pet Services"
#         },
#                         {
#             "name": "Catering Services",
#             "description": "Delicious catering services for events of all sizes. Our caterers provide a wide range of menu options, from appetizers to desserts, ensuring your guests are satisfied and impressed.",
#             "image": "https://media.licdn.com/dms/image/D5612AQEm62hYmINu4g/article-cover_image-shrink_600_2000/0/1700656734556?e=2147483647&v=beta&t=ycVtNIXrVl7LSpBVPoJ2SLF7OmkGIRkS5qZrrUPKrbg",
#             "category": "Food and Beverage"
#         },
#                         {
#             "name": "Translating Services",
#             "description": "Accurate and reliable translation services for documents, websites, and more. Our translators are fluent in multiple languages, providing clear and culturally appropriate translations.",
#             "image": "https://circletranslations.com/wp-content/uploads/2024/03/The-Cost-of-Translation-Services-in-2023.jpg",
#             "category": "Professional Services"
#         },
#                         {
#             "name": "Interior Designing Services",
#             "description": "Creative interior design services to transform your space. Whether you’re redesigning a room or an entire property, our designers work with you to create a functional and aesthetically pleasing environment.",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbENYwW_PLemHtZ49muWbU7DkBPVBQnfPzDw&s",
#             "category": "Home Services"
#         }