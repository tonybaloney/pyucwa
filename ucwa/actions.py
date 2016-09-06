import uuid
import requests
from future.moves.urllib.parse import urlparse
import json


USER_AGENT = 'SkypeWeb/0.4.275 master UCWA/1.0.0-e4a1abbd7ca7d-84c26b3703da8'

def do_autodiscover(domain):
    r = requests.get('https://webdir.online.lync.com/autodiscover/autodiscoverservice.svc/root?originalDomain=%s' % domain)
    discovery = r.json()
    path = discovery['_links']['user']['href']
    domain = urlparse(path)
    host = '{0}://{1}'.format(domain.scheme, domain.netloc)
    return (discovery['_links']['xframe']['href'], path, host)


def do_user_discovery(resource, token, config):
    return oauth_request(
        resource + '/Autodiscover/AutodiscoverService.svc/root/oauth/user', token,
        config['redirect_uri'])


def do_application_discovery(resource, token, config):
    return oauth_request(
        resource + '/ucwa/oauth/v1/applications', token,
        config['redirect_uri'])


def register_application(resource, token, config):
    msg = {
        "UserAgent": USER_AGENT,
        "EndpointId": str(uuid.uuid1()),
        "Culture": "en-US"
       }
    return oauth_post_request(
        resource + '/ucwa/oauth/v1/applications', token,
        config['redirect_uri'], msg)


def set_available(resource, app_id, token, config):
    path = '/ucwa/oauth/v1/applications/%s/me/makeMeAvailable' % app_id
    msg = {
        "SupportedModalities": ["Messaging"]
        }
    return oauth_post_request(
        resource + path, token,
        config['redirect_uri'], msg)


def oauth_post_request(uri, oauth_token, origin, msg):
    uid = uuid.uuid1()
    headers = {
        'Authorization': 'Bearer %s' % oauth_token,
        'Origin': origin,
        'Client-Request-Id': 'WebSDK/%s' % uid,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-MS-Correlation-Id': uid,
        'X-Ms-Namespace': 'internal',
        'X-Ms-SDK-Instance': USER_AGENT,
        'Referer': origin + '/'
    }
    response = requests.post(uri, data=json.dumps(msg), headers=headers, verify=False)
    if response.text != '':
        return response.json()
    else:
        return {}


def oauth_stream_request(uri, oauth_token, origin):
    uid = uuid.uuid1()
    headers = {
        'Authorization': 'Bearer %s' % oauth_token,
        'Origin': origin,
        'Client-Request-Id': 'WebSDK/%s' % uid,
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MS-Correlation-Id': uid,
        'X-Ms-Namespace': 'internal',
        'X-Ms-SDK-Instance': USER_AGENT,
        'Referer': origin + '/'
    }
    response = requests.get(uri, headers=headers, verify=False, stream=True)
    return response


def oauth_request(uri, oauth_token, origin):
    uid = uuid.uuid1()
    headers = {
        'Authorization': 'Bearer %s' % oauth_token,
        'Origin': origin,
        'Client-Request-Id': 'WebSDK/%s' % uid,
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MS-Correlation-Id': uid,
        'X-Ms-Namespace': 'internal',
        'X-Ms-SDK-Instance': USER_AGENT,
        'Referer': origin + '/'
    }
    response = requests.get(uri, headers=headers, verify=False)
    return response.json()
