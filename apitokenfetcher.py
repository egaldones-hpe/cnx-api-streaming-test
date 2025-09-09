from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class ApiTokenFetcher:
    """Handles OAuth2 token fetching for CNX API."""
    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

    def fetch_token(self):
        client = BackendApplicationClient(self.client_id)
        oauth = OAuth2Session(client=client)
        token_data = oauth.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        return token_data["access_token"]
