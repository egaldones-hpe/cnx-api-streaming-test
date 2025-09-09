import argparse
import os
import sys
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


def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetch OAuth2 API token for CNX API')
    parser.add_argument('--client-id', help='OAuth2 client ID (default: from CNX_CLIENT_ID env var)')
    parser.add_argument('--client-secret', help='OAuth2 client secret (default: from CNX_CLIENT_SECRET env var)')
    parser.add_argument('--token-url', help='OAuth2 token URL (default: from CNX_TOKEN_URL env var)')
    args = parser.parse_args()

    client_id = args.client_id or os.getenv('CNX_CLIENT_ID')
    client_secret = args.client_secret or os.getenv('CNX_CLIENT_SECRET')
    token_url = args.token_url or os.getenv('CNX_TOKEN_URL')

    missing = []
    if not client_id:
        missing.append('--client-id or CNX_CLIENT_ID')
    if not client_secret:
        missing.append('--client-secret or CNX_CLIENT_SECRET')
    if not token_url:
        missing.append('--token-url or CNX_TOKEN_URL')
    if missing:
        print('Missing required arguments:')
        for m in missing:
            print(f'  {m}')
        sys.exit(1)
    return client_id, client_secret, token_url


def main():
    client_id, client_secret, token_url = parse_arguments()
    fetcher = ApiTokenFetcher(client_id, client_secret, token_url)
    try:
        token = fetcher.fetch_token()
        print(token)
    except Exception as e:
        print(f'Error fetching token: {e}')
        sys.exit(1)


if __name__ == "__main__":
    main()
