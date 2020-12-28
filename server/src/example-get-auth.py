from os import path
import pyperclip
import configparser
from requests_oauthlib import OAuth2Session

if not path.exists('config.ini'):
    print('Config file not found')
    exit(1)

parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['DEFAULT']

# Hardcoded values for Github's OAuth2 Authentication Server
client_id = config['client_id']
client_secret = config['client_secret']
authorization_base_url = 'https://github.com/login/oauth/authorize?scope=user%20public_repo'
token_url = 'https://github.com/login/oauth/access_token'

# Get the authorization url (grant)
github = OAuth2Session(client_id)
authorization_url, state = github.authorization_url(authorization_base_url)

# Present to the user and copy to clipboard
print('Please go here and authorize,', authorization_url)
pyperclip.copy(authorization_url)

# https://gitinit.io/connected?code=ceadc5ced9474fc4a9e0&state=ITzW7dudbUTVvdUUW1j9DNcmcEx60T
redirect_response = input('Paste the full redirect URL here:')

# {'access_token': 'eb84244f65c993e8ed6028c605f841a763bc01b6', 'token_type': 'bearer', 'scope': ['public_repo,user']}
github.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

r = github.get('https://api.github.com/user')
print(r.content)
