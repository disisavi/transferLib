import google_auth_oauthlib.flow


def a():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_id.json"
    redirectURI = "http://localhost:5000/ytmusic/redirect"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes)

    flow.redirect_uri = redirectURI

    credentials = flow.authorization_url()
    return credentials
