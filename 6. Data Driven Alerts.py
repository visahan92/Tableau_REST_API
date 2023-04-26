import tableauserverclient as TSC
import configparser


config = configparser.ConfigParser()
config.read(r'config.txt')  

use_pat_flag = config.get('login', 'use_pat_flag') #True  # True = use personal access token for sign in, false = use username and password for sign in.

server_name = config.get('login', 'server_name')   # Name or IP address of your installation of Tableau Server
version = config.get('login', 'version')     # API version of your server
site_url_id = config.get('login', 'site_url_name')    # Site (subpath) to sign in to. An empty string is used to specify the default site.

# For username and password sign in
user_name = config.get('login', 'user_name')    # User name to sign in as (e.g. admin)
password = config.get('login', 'password')

# For Personal Access Token sign in
personal_access_token_name = config.get('login', 'personal_access_token_name')         # Name of the personal access token.
personal_access_token_secret = config.get('login', 'personal_access_token_secret')   # Value of the token.
datasource_name = 'Sample - Superstore Datasource'

tableau_auth = TSC.PersonalAccessTokenAuth(personal_access_token_name, personal_access_token_secret, site_url_id)
server = TSC.Server(server_name, use_server_version=True)
server.auth.sign_in(tableau_auth)

req_option = TSC.RequestOptions()
req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 datasource_name))

with server.auth.sign_in(tableau_auth):