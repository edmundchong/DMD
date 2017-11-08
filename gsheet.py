'''
Created on May 30, 2014


to use, must install google API:
    pip install --upgrade google-api-python-client
    https://code.google.com/p/gdata-python-client/downloads/list


 

@author: chris, edmund
'''

import gdata.spreadsheet.service
import getpass
import time

token='DQAAAOgAAADZ55GfwJA2DpgUuZhHbnICTCejZn5gKI_Kh2HsXbp21q4D-H1KmMpLLqWr31-mxf-CL5QvTSDNtSDAM878qrhhq_cABxvs3mDre2Ay31FxjH2QlFv5QXIg1AX2jTb4afDbAN5gJvq0BoaH8GH5wZFcEMOBPiG-EK2EcTRIHeqJwBm9qstweK-gSEZA_RYnWe-dM8oF6jaTaRk1GBHmVrnJHmO11ms7qbenNS_mYgkAJrW1pei1Rd4-L3bPBWfbR6aNvijXBlBeSJPhJBuG_joIlbe7W-aJUCxsBgl5bDbhOZobbntQFsn0XF26WmeIlMs'
sheet='mightex pattern stim'
imagefolder='http://googledrive.com/host/0B54p0-ShxNRdNDdsU0N3Q2NlUHM/'


filename = imagefolder+'3874_19_3.png'




class GDriveWksheet(object):

    def __init__(self, auth_token=None, spreadsheet_name=None, wksheet_name=None):
        '''
        Constructor. Connects to google drive, asks user to make an API token if needed,
        verifies that spreadsheet and worksheet requested are actually present. There
        is no ability to add a spreadsheet or worksheet to the drive at this time.
        
        Keyword arguments:
        auth_token -- Google authorization token (if none, system will prompt for your Google Doc username and password)
        spreadsheet_name -- string containing the name of your spreadsheet to load. This determines the scope of the drive that you can access.            
        worksheet_name -- string containing name of worksheet to load
        '''
        self.client = gdata.spreadsheet.service.SpreadsheetsService()
        self.client.source = 'Voyeur'
        if auth_token is None:
            auth_token = self._get_token()
        self.client.SetClientLoginToken(auth_token)
        try:
            self.ss_id = self._verify_spreadsheet(spreadsheet_name)
            self.ws_id = self._verify_worksheet(wksheet_name)
            self._update_wksheet()
        except gdata.service.RequestError as e:
            if e[0]['status'] == 401:  # authentication error
                print 'Bad authentication, try to get new token.'
                auth_token = self._get_token()
                if auth_token:
                    self.ss_id = self._verify_spreadsheet(spreadsheet_name)
                    self.ws_id = self._verify_worksheet(wksheet_name)
                    self._update_wksheet()

    def _verify_spreadsheet(self, spreadsheet_name):
        ''' verify that spreadsheet of name == spreadsheet_name is present in drive scope'''
        feed = self.client.GetSpreadsheetsFeed()
        for i, entry in enumerate(feed.entry):
            spreadsheet_str = entry.title.text
            if spreadsheet_str == spreadsheet_name:
                spreadsheet_id = entry.id.text.split('/')[-1]
                print 'Spreadsheet found.'
                return spreadsheet_id
        print 'ERROR: spreadsheet not found!!! \N Listing available spreadsheets below:'
        for i, entry in enumerate(feed.entry):
            print entry.title.text
        # try again with different worksheet input.
        h = raw_input('\N to choose a new worksheet, enter title here: \N')
        if h == '':
            return
        else:
            self._verify_spreadsheet(h)

    def _verify_worksheet(self, wksheet_name):
        feed = self.client.GetWorksheetsFeed(self.ss_id)
        for i, entry in enumerate(feed.entry):
            wksheet_str = entry.title.text
            if wksheet_name == wksheet_str:
                print 'Worksheet found'
                return entry.id.text.split('/')[-1]
        print 'ERROR: worksheet not found!!'
        
        # TODO: make error handling work with command prompt for alternate
        # choice.

    def _get_token(self):
        '''gets token from google for addition to future code. Prompts user for gmail username (email) and pw
        Importantly, the returned token is only useful for accessing google spreadsheets - it does NOT 
        give access to gmail or other google services.'''

        print('\nNo authentication token provided for Google Drive, please enter login information below to retrieve new token.'
              '\nThis token is specific to the scope of Google Spreadsheets within your account (ie not gmail, etc).')
        l = raw_input('\nGoogle Drive account name: ')
        p = getpass.getpass()
        tok = self.client.ClientLogin(l, p, service='wise') #gets token which is specific for google spreadsheets! this token cannot be used for other services (docs, mail, etc).
        print 'Token retrieved, please save for future use!!.'
        print self.client._GetAuthToken()
        return self.client._GetAuthToken()

    def _update_wksheet(self):
        '''refresh worksheet from server'''
        self.worksheet = self.client.GetListFeed(self.ss_id, self.ws_id).entry




class PatternStimGSheet(GDriveWksheet):
    imgpath='http://googledrive.com/host/0B54p0-ShxNRdNDdsU0N3Q2NlUHM/'
    clientid='1093370777233-t82lfb97macr063kto6nn3rp4d0gtsdu.apps.googleusercontent.com'
    clientsecret='nZqot8mW1Mat1RdYvlhbg5Ac'
        
    def __init__(self, auth_token=None, spreadsheet_name=None, wksheet_name=None):
        super(PatternStimGSheet, self).__init__(
            auth_token, spreadsheet_name, wksheet_name)
        return 

def loaddoc(mouse):
    doc=PatternStimGSheet(token,sheet,mouse)
    return doc

def addRow(doc,row):
    doc.client.InsertRow(row,doc.ss_id,doc.ws_id)


