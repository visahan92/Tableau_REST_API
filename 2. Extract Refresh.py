import tableauserverclient as TSC
import configparser
import time


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

tableau_auth = TSC.PersonalAccessTokenAuth(personal_access_token_name, personal_access_token_secret, site_url_id)
server = TSC.Server(server_name, use_server_version=True)

req_option = TSC.RequestOptions()
req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 datasource_name))

with server.auth.sign_in(tableau_auth):
    datasources, pagination = server.datasources.get(req_option)
    datasource_retrieved = ''

    for datasource in datasources:
        datasource_retrieved = datasource

    result = server.datasources.refresh(datasource_retrieved)

    progress = '0'
    timeout = 300  # seconds
    wait_time = 0

    while int(progress) < 100 and wait_time < timeout:
        progress = server.jobs.get_by_id(result.id).progress or '0'
        time.sleep(1)
        wait_time += 1

    job = server.jobs.get_by_id(result.id)
    job_data = {
        'id': job.id,
        'datasource': datasource_name,
        'created_at': job.created_at,
        'started_at': job.started_at,
        'completed_at': job.completed_at,
        'mode': job.mode,
        'type': job.type,
        'notes': job.notes,
    }


    print(job_data)
    server.auth.sign_out()