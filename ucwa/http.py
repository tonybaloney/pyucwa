from flask import Flask, redirect, request
from .auth import get_token_from_code, oauth_request, oauth_post_request, admin_consent
from .config import load_config
from .actions import do_autodiscover

app = Flask(__name__)

config = load_config()


@app.route('/')
def main():
    return "Hello."


@app.route('/autodiscover')
def autodiscover():
    return redirect('https://webdir.online.lync.com/autodiscover/autodiscoverservice.svc/root')


@app.route('/token', methods=['POST'])
def token_stage():
    client_id = config['client_id']
    tenant = config['domain']
    redirect_uri = config['redirect_uri'] + '/token'

    # find out where this account is
    xframe, user_discovery_uri, resource = do_autodiscover(config['domain'])

    token = request.form['access_token']

    r = oauth_request(resource + '/ucwa/oauth/v1/applications', token,
                      config['redirect_uri']+'/',
                      resource, config['redirect_uri'])
    print(r)

    # implicit grant flow token
    state = '8f0f4eff-360f-4c50-acf0-99cf8174a58b'
    url = admin_consent(client_id, tenant, redirect_uri + '2',
                        resource, state)
    print(url)
    return redirect(url)


@app.route('/token2', methods=['POST'])
def token_stage2():
    id_token = request.form['id_token']
    session_state = request.form['session_state']
    xframe, user_discovery_uri, resource = do_autodiscover(config['domain'])
    # resend an autodiscovery request with the new bearer
    origin = config['redirect_uri'] +'/'

    r = oauth_request(user_discovery_uri, id_token, origin, resource, config['app_id'])
    print(r)

    uri = resource  + '/ucwa/oauth/v1/applications'

    r = oauth_post_request(uri, id_token, origin, resource)
    return r

app.run()