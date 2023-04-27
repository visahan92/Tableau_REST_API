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
group_name = config.get('group', 'group_name')
group_user_name = config.get('group', 'group_user_name')

tableau_auth = TSC.PersonalAccessTokenAuth(personal_access_token_name, personal_access_token_secret, site_url_id)
server = TSC.Server(server_name, use_server_version=True)

# 1. Authenticate
with server.auth.sign_in(tableau_auth):

    req_group_by_name = TSC.RequestOptions()
    req_group_by_name.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 group_name))

    req_group_by_user_name = TSC.RequestOptions()
    req_group_by_user_name.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 group_user_name))
    
    group_receieved = ''
    user_receieved = ''

    # 2. Get Group
    all_groups, pagination_item = server.groups.get(req_group_by_name)
    for group in all_groups:
        print('Group Name : ' + group.name)
        group_receieved = group

    # 3. Get User
    all_users, pagination_item = server.users.get(req_group_by_user_name)
    for user in all_users:
        print('User Name : ' + user.name)
        user_receieved = user

    # 4. Add user to the group
    server.groups.add_user(group_receieved, user_receieved.id)
    print('User added to group successfully')

    # 5. Remove user from the group
    #server.groups.remove_user(group_receieved, user_receieved.id)
    #print('User removed from the group successfully')

    server.auth.sign_out()