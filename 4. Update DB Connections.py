import tableauserverclient as TSC
import configparser


config = configparser.ConfigParser()
config.read(r'config.txt')  

use_pat_flag = config.get('login', 'use_pat_flag') #True  # True = use personal access token for sign in, false = use username and password for sign in.

server_name = config.get('login', 'server_name')   # Name or IP address of your installation of Tableau Server
version = config.get('login', 'version')     # API version of your server
site_url_id = config.get('login', 'site_url_name')    # Site (subpath) to sign in to. An empty string is used to specify the default site.

# For Personal Access Token sign in
personal_access_token_name = config.get('login', 'personal_access_token_name')         # Name of the personal access token.
personal_access_token_secret = config.get('login', 'personal_access_token_secret')   # Value of the token.
datasource_name = config.get('datasource', 'datasource_name')
current_db_username = config.get('db', 'current_db_username')
new_db_username = config.get('db', 'db_username')
current_db_password = config.get('db', 'db_password')

tableau_auth = TSC.PersonalAccessTokenAuth(personal_access_token_name, personal_access_token_secret, site_url_id)
server = TSC.Server(server_name, use_server_version=True)

# 1. Authenticate
with server.auth.sign_in(tableau_auth):

    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 datasource_name))

    # 2. Get Datasource
    datasources, pagination = server.datasources.get(req_option)
    datasource_receieved = ''
    for datasource in datasources:
        datasource_receieved = datasource

    # get the datasource information
    server.datasources.populate_connections(datasource_receieved)

    # 3. create endpoint object
    endpoint = {"workbook": server.workbooks, "datasource": server.datasources}.get('datasource')
    
    update_function = endpoint.update_connection

    # 4. Get connection
    connection_receieved = ''
    for connection in datasource_receieved.connections:
        connection_receieved = connection

    # 5. Update Credentials
    connection.username = new_db_username
    connection.password = current_db_password
    connection.embed_password = True
    update_function(datasource_receieved, connection).__dict__

    print("Datasource connection credentials updated successfully")

    server.auth.sign_out()