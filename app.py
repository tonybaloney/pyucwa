import ucwa.actions as actions
from ucwa.config import load_config
from contextlib import closing
import time
import yaml

with open('instance.yml', 'r') as instance_f:
    instance_config = yaml.load(instance_f)

config = load_config()

resource = instance_config['resource']
token = instance_config['token']

app = actions.register_application(resource, token, config)

print ('Registered app %s' % app['id'])

print('listening for events')

event_url = resource + app['_links']['events']['href']

print('setting available')

available = actions.set_available(resource, app['id'], token, config)

events = actions.oauth_stream_request(event_url, token, config['redirect_uri'])

event_list = {}

while True:
    with closing(events) as r:
        # Do things with the response here.
        event_list = events.json()
    print('.')
    time.sleep(2)

    # get communication events
    comm_evt = [e for e in event_list['sender'] if e['rel'] == 'communication']

    print(comm_evt)

    events = actions.oauth_stream_request(resource + event_list['_links']['next']['href'], token,
                                          config['redirect_uri'])
