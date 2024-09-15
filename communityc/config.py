import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///communitycrafters.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another-secret-key'
    MPESA_CONSUMER_KEY = os.environ.get('n4OHB0GMQBA3RcnrXoIgJ5twGwJeL6VkAPY9RYklGRVjfdVc')
    MPESA_CONSUMER_SECRET = os.environ.get('gYgQwSzDNPdUKr4DjBzjEKGjiGF53T2zGquxM5UURTjukbGO2fGwZfrRwaGtEDZT')
    # MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
    # MPESA_LIPA_NGWE = os.environ.get('MPESA_LIPA_NGWE')
