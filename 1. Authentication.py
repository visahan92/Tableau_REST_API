import requests, json
import urllib3
import configparser
urllib3.disable_warnings()


config = configparser.ConfigParser()
config.read(r'config.txt')  

use_pat_flag = config.get('login', 'use_pat_flag')# True = use personal access token for sign in, false = use username and password for sign in.

server_name = config.get('login', 'server_name')   # Name or IP address of your installation of Tableau Server
version = config.get('login', 'version')     # API version of your server
site_url_id = config.get('login', 'site_url_name')    # Site (subpath) to sign in to. An empty string is used to specify the default site.

# For username and password sign in
user_name = config.get('login', 'user_name')    # User name to sign in as (e.g. admin)
password = config.get('login', 'password')  # User password to sign in as

# For Personal Access Token sign in
personal_access_token_name = config.get('login', 'personal_access_token_name')       # Name of the personal access token.
personal_access_token_secret = config.get('login', 'personal_access_token_secret')   # Value of the token.

signin_url = "https://{server}/api/{version}/auth/signin".format(server=server_name, version=version)

if use_pat_flag:

	payload = { "credentials": { "personalAccessTokenName": personal_access_token_name, "personalAccessTokenSecret": personal_access_token_secret, "site": {"contentUrl": site_url_id }}}

	headers = {
		'accept': 'application/json',
		'content-type': 'application/json'
	}

else:

	payload = { "credentials": { "name": user_name, "password": password, "site": {"contentUrl": site_url_id }}}

	headers = {
		'accept': 'application/json',
		'content-type': 'application/json'
	}

# Send the request to the server
req = requests.post(signin_url, json=payload, headers=headers, verify=False)
req.rais_efor_status()

# Get the response
response = json.loads(req.content)

# Get the authentication token from the credentials element
token = response["credentials"]["token"]

# Get the site ID from the <site> element
site_id = response["credentials"]["site"]["id"]

print('Sign in successful!')

print('\tSite ID: {site_id}'.format(site_id=site_id))

# Set the authentication header using the token returned by the Sign In method.
headers['X-tableau-auth']=token

# Sign out
signout_url = "https://{server}/api/{version}/auth/signout".format(server=server_name, version=version)

req = requests.post(signout_url, data=b'', headers=headers, verify=False)
req.raise_for_status()

print('Sign out successful!')