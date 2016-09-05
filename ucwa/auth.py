from future.moves.urllib.parse import urlencode
import requests
import json
from .actions import do_autodiscover
from .config import load_config


# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

config = load_config()


def get_signin_url(redirect_uri, client_id, tenant, resource):
    xframe, user_discovery_uri, resource = do_autodiscover(config['domain'])

    # Build the query parameters for the signin url
    params = {
      'client_id': client_id,
      'redirect_uri': redirect_uri,
      'response_type': 'token',
      'response_mode': 'form_post',
      'resource': resource
    }

    # The authorize URL that initiates the OAuth2 client credential flow for admin consent
    authorize_url = '{0}{1}'.format(authority, '/%s/oauth2/authorize?{0}' % tenant)

    # Format the sign-in url for redirection
    signin_url = authorize_url.format(urlencode(params))

    return signin_url


def admin_consent(client_id, tenant, redirect_uri, resource, state):
    # Build the post form for the token request
    params = {
      'client_id': client_id,
      'redirect_uri': redirect_uri,
      'response_type': 'id_token',
      'response_mode': 'form_post',
      'resource': resource,
      'nonce': 'yousaywhat',
      'prompt': 'admin_consent'
    }

    # The token issuing endpoint
    authorize_url = '{0}{1}'.format(authority, '/%s/oauth2/authorize?{0}' % tenant)

    # Format the sign-in url for redirection
    url = authorize_url.format(urlencode(params))

    return url


def grant_flow_token(client_id, tenant, redirect_uri, resource, state):
    # Build the post form for the token request
    params = {
      'client_id': client_id,
      'redirect_uri': redirect_uri,
      'response_type': 'id_token',
      'state': state,
      'resource': resource,
      'nonce': 'yousaywhat'
    }

    # The token issuing endpoint
    authorize_url = '{0}{1}'.format(authority, '/%s/oauth2/authorize?{0}' % tenant)

    # Format the sign-in url for redirection
    url = authorize_url.format(urlencode(params))

    return url


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
