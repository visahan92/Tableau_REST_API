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
workbook_name = config.get('workbook', 'workbook_name')

output_file_name = config.get('workbook', 'output_file_name')
filter_key_1 = config.get('workbook', 'filter_key_1')
filter_value_1 = config.get('workbook', 'filter_value_1')
filter_key_2 = config.get('workbook', 'filter_key_2')
filter_value_2 = config.get('workbook', 'filter_value_2')

tableau_auth = TSC.PersonalAccessTokenAuth(personal_access_token_name, personal_access_token_secret, site_url_id)
server = TSC.Server(server_name, use_server_version=True)

# 1. Authenticate
with server.auth.sign_in(tableau_auth):

    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 workbook_name))

    # 2. Get Workbook
    workbooks, pagination = server.workbooks.get(req_option)
    workbook_retrieved =  ''
    view_retrieved =  ''
    for workbook in workbooks:
        workbook_retrieved = workbook

    server.workbooks.populate_views(workbook_retrieved)

    # 3. Get View
    for view in workbook_retrieved.views:
        view_retrieved = view

    # 4. Add Filter
    option_factory = getattr(TSC, "PDFRequestOptions")
    options = option_factory().vf(filter_key_1,filter_value_1)

    server.views.populate_image(view_retrieved,options)

    # 5. Download Image
    filename = output_file_name + "-image-export.png"
    with open(filename, "wb") as f:
        f.write(view_retrieved.image)
    print("Image saved as " + filename)

    # 6. Add Filter
    options = option_factory().vf(filter_key_2,filter_value_2)

    server.views.populate_pdf(view_retrieved,options)

    # 7. Download PDF
    with open(output_file_name, 'wb') as f:
        f.write(view_retrieved.pdf)
    print("PDF saved as " + output_file_name)

    server.auth.sign_out()