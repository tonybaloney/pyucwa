from future.moves.urllib.parse import urlencode
import requests
import json

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'


def get_signin_url(redirect_uri, client_id, tenant):
    # Build the query parameters for the signin url
    params = {
      'client_id': client_id,
      'redirect_uri': redirect_uri,
      'response_type': 'tp',
      'prompt': 'login',
    }

    # The authorize URL that initiates the OAuth2 client credential flow for admin consent
    authorize_url = '{0}{1}'.format(authority, '/oauth2/authorize?{0}')

    # Format the sign-in url for redirection
    signin_url = authorize_url.format(urlencode(params))

    return signin_url


def get_token_from_code(client_id, tenant, auth_code, redirect_uri, resource, client_secret):
    # Build the post form for the token request
    post_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'resource': resource,
        'client_id': client_id,
        'client_secret': client_secret
      }

    # The token issuing endpoint
    token_url = '{0}{1}'.format(authority, '/{0}/oauth2/token'.format(tenant))

    # Perform the post to get access token
    response = requests.post(token_url, data=post_data, verify=False)

    try:
        # try to parse the returned JSON for an access token
        access_token = response.json()['id_token']
        print(response.text)
        return access_token
    except:
        raise Exception('Error retrieving token: {0} - {1}'.format(
          response.status_code, response.text))


def oauth_request(uri, oauth_token, origin, pool, app_id):
    headers = {
        'Authorization': 'Bearer %s' % oauth_token,
        'X-Ms-Origin': app_id,
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': '%s/Autodiscover/XFrame/XFrame.html' % (pool)
    }
    response = requests.get(uri, headers=headers, verify=False)
    return response.text


def oauth_post_request(uri, oauth_token, origin, pool):
    headers = {
        'Authorization': 'Bearer %s' % oauth_token,
        'X-Ms-Origin': origin,
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': '%s/Autodiscover/XFrame/XFrame' % (pool)
    }
    msg = {
        "UserAgent":"UCWA Samples",
        "EndpointId":"a917c6f4-976c-4cf3-847d-cdfffa28ccdf",
        "Culture":"en-US"
       }
    response = requests.post(uri, data=json.dumps(msg), headers=headers, verify=False)
    return response.text
