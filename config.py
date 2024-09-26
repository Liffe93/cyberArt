import os

# Flask Secret Key
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'your_default_secret_key')  # Set your default secret key here

# Have I Been Pwned API Key
HIBP_API_KEY = os.environ.get('HIBP_API_KEY')  # Set your default HIBP API key here

# Email Configuration
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # Set your default email address here
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Set your default email password here
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')  # Set your default email server here