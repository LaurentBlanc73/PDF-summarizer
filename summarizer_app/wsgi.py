from dotenv import load_dotenv
from frontend.dash_app import server

# Load environment variables from .env file
load_dotenv()

# single callable WSGI app
app = server
