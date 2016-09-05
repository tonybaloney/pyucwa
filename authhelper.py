from ucwa.auth import get_signin_url
from ucwa.config import load_config
import webbrowser

config = load_config()

url = get_signin_url(config['redirect_uri'] + '/token', config['client_id'], config['domain'], config['app_id'])

# Open URL in a new tab, if a browser window is already open.Which it probably is in 2016
webbrowser.open_new_tab(url)
