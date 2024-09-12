import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace these with your actual values
CLIENT_ID = os.getenv('TRAKT_CLIENT_ID')
CLIENT_SECRET = os.getenv('TRAKT_CLIENT_SECRET')
REDIRECT_URI = os.getenv('TRAKT_REDIRECT_URI')
CODE = os.getenv('TRAKT_AUTHORISATION_CODE')

token_url = 'https://api.trakt.tv/oauth/token'

data = {
    'code': CODE,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}

response = requests.post(token_url, data=data)
print(response.json())
