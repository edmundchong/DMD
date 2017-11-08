import httplib2
import pprint

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow,OAuth2Credentials


'''
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive' # Check https://developers.google.com/drive/scopes for all available scopes
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob' # Redirect URI for installed apps

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
txtfile=open('foo.txt','w')
txtfile.write(authorize_url)
txtfile.close()

code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)
'''

FILENAME = '3874_19_3.png'
target_folder='pattern_images'
jsonfile='C:/voyeur_rig_config/json.txt'

def connect(jsonfile=jsonfile):
    txtfile=open(jsonfile,'r')
    json=txtfile.readline()
    txtfile.close()
    credentials=OAuth2Credentials.from_json(json)
    
    http = httplib2.Http()
    http = credentials.authorize(http)

    
    #CLIENT_ID = credentials.client_id
    #CLIENT_SECRET = credentials.client_secret
    drive = build('drive', 'v2', http=http)

    return drive

def upload_png(drive, png, target_folder=target_folder):

    #get folder id
    itemlist=drive.files().list().execute()['items'] 
    for i in itemlist:
        if i['mimeType']=='application/vnd.google-apps.folder' and i['title']==target_folder:
            folderID=i['id']
            
    for i in itemlist:
        if i['title']==target_folder:
            folderID=i['id']
    print target_folder+" -- FOLDERID: "
    print folderID        
    # Insert a file
    media_body = MediaFileUpload(png, mimetype='image/png')
    body = {
      'title': png.split('/')[-1], #remove path from filename
      'mimeType': 'image/png',
      'parents': [{'id':folderID}]
    }
    
    file = drive.files().insert(body=body, media_body=media_body).execute()
