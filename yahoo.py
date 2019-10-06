import datetime
import json
import webbrowser
from rauth import OAuth2Service
from rauth.utils import parse_utf8_qsl

class Yahoo:
    def __init__(self, credentials_path):
        self._credentials_path = credentials_path
        self._load_credentials()

        self.service = OAuth2Service(
            client_id=self.credentials['client_id'],
            client_secret=self.credentials['client_secret'],
            access_token_url='https://api.login.yahoo.com/oauth2/get_token',
            authorize_url='https://api.login.yahoo.com/oauth2/request_auth',
            base_url='https://fantasysports.yahooapis.com/'
        )

        # Use saved token if it hasn't expired
        if 'expires' in self.credentials.keys():
            saved_token_expiration = datetime.datetime.strptime(self.credentials['expires'], "%Y-%m-%d %H:%M:%S.%f")
        else:
            saved_token_expiration = datetime.datetime.min 

        if datetime.datetime.now() < saved_token_expiration:
            data = {
                'client_id': self.credentials['client_id'],
                'client_secret': self.credentials['client_secret'],
                'grant_type': 'refresh_token',
                'refresh_token': self.credentials['refresh_token']
            }
            self.session = self.service.get_auth_session(data=data, decoder=json.loads, verify=False)
        # Request new token
        else:
            # Authorize
            params = {
                'redirect_uri': 'oob',
                'response_type': 'code',
                'language': 'en-us'
            }
            authorize_url = self.service.get_authorize_url(**params)
            webbrowser.open(authorize_url)
            authorization_code = input('Input code from redirect: ')
            
            # Obtain access token
            data = {
                'code': authorization_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'oob'
            }
            auth_date = datetime.datetime.now()
            self.session = self.service.get_auth_session(data=data, decoder=json.loads, verify=False)

            # Save credential info
            self.access_token_response = json.loads(self.service.access_token_response.text)
            # self.credentials['access_token'] = self.access_token_response['access_token']
            self.credentials['refresh_token'] = self.access_token_response['refresh_token']
            self.credentials['expires'] = auth_date + datetime.timedelta(seconds=self.access_token_response['expires_in'])
            self._save_credentials()

    def __del__(self):
        self._save_credentials()

    def _load_credentials(self):
        with open(self._credentials_path, 'r') as credentials_file:
            credentials = json.load(credentials_file)

        self.credentials = credentials

    def _save_credentials(self):
        with open(self._credentials_path, 'w') as credentials_file:
            json.dump(self.credentials, credentials_file, default=str)

    def get(self, *args, **kwargs):
        try:
            data = self.session.get(params={'format': 'json'}, verify=False, *args, **kwargs)
        except:
            # TODO - check for token expiration
            # Obtain new access token
            data = {
                'client_id': self.credentials['client_id'],
                'client_secret': self.credentials['client_secret'],
                'grant_type': 'refresh_token',
                'refresh_token': self.access_token_response['refresh_token']
            }
            self.session = self.service.get_auth_session(data=data, decoder=json.loads, verify=False)
            data = self.session.get(params={'format': 'json'}, verify=False, *args, **kwargs)
        return data.json()