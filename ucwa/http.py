from flask import Flask, redirect, request
from .auth import get_token_from_code, oauth_request, oauth_post_request
from .config import load_config

app = Flask(__name__)

config = load_config()


@app.route('/')
def main():
    return "Hello."


@app.route('/autodiscover')
def autodiscover():
    return redirect('https://webdir.online.lync.com/autodiscover/autodiscoverservice.svc/root')


@app.route('/token')
def token_stage():
    resource = config['pool']
    code = request.args.get('code', '')
    # session_state = request.args.get('session_state','')
    token = get_token_from_code(config['client_id'],
                                config['domain'],
                                code,
                                config['redirect_uri'] + 'token',
                                resource,
                                config['secret'])

    # resend an autodiscovery request with the new bearer
    uri = config['pool'] + '/autodiscover/autodiscoverservice.svc/root/oauth/user'
    origin = config['redirect_uri']

    r = oauth_request(uri, token, origin, config['pool'], config['app_id'])
    print(r)
    uri = config['pool']  + '/ucwa/oauth/v1/applications'

    r = oauth_post_request(uri, token, origin, config['pool'])
    return r

app.run()