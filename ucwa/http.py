from flask import Flask, redirect, request
from future.moves.urllib.parse import urlparse

from .config import load_config
from .actions import (do_autodiscover, do_user_discovery,
                      do_application_discovery,
                      register_application)
from .auth import grant_flow_token
import yaml

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
    # find out where this account is
    xframe, user_discovery_uri, resource = do_autodiscover(config['domain'])

    # Get the inbound token as posted from a form
    token = request.form['access_token']
    state = request.form['session_state']

    # discover which web server we have been assigned to
    user_discovery_data = do_user_discovery(resource, token, config)

    # Link to the current session server resource (we need a token for this.)
    instance_url = user_discovery_data['_links']['applications']['href']

    instance_parts = urlparse(instance_url)
    instance_resource = '{0}://{1}'.format(instance_parts.scheme, instance_parts.netloc)

    url = grant_flow_token(config['client_id'],
                                     config['redirect_uri'] + '/directsession',
                                     instance_resource, state, token)

    return redirect(url)


@app.route('/directsession', methods=['GET', 'POST'])
def direct_sesssion_stage():
    # Get the inbound token as posted from a form
    token = request.form['access_token']
    resource = request.form['state']

    # app = register_application(resource, token, config)
    # r = do_application_discovery(resource, token, config)

    app = {
        'token': str(token),
        'resource': str(resource)
    }

    with open('instance.yml', 'w') as instance_f:
        instance_f.write(yaml.dump(app))

    return 'done. now run app.py'

app.run()