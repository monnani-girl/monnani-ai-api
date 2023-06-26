from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
 
def get_service(api_name, api_version, scopes, key_file_location):
 
 
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)
 
    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)
 
    return service
     
     
# Define the auth scopes to request.
scope = 'https://www.googleapis.com/auth/analytics.readonly'
 
key_file_location = './ddokdarman-key.json'
 
# Authenticate and construct service.
service = get_service(
        api_name='analytics',
        api_version='v3',
        scopes=[scope],
        key_file_location=key_file_location)
         
# Get a list of all Google Analytics accounts for this user
accounts = service.management().accounts().list().execute()
 
if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')
 
    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(accountId=account).execute()

     
def get_all_sessions():    
    result = service.data().ga().get(
              ids='ga:288190011',
              start_date='2023-04-01',
              end_date='today',
              metrics='ga:sessions,ga:pageviews').execute()

    return result["totalsForAllResults"]["ga:sessions"]
  