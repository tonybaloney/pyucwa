import logging
from .actions import oauth_post_request, oauth_request, send_message
from .datauri import DataURI
import urllib


def process_events(event_list, resource, token, config):
    rel_map = {
        'messagingInvitation': process_message_invitation_event,
        'communication': process_communication_event,
        'conversation': process_conversation_event,
        'missedItems': process_missed_items_event,
        'message': process_message_event,
    }

    for event in event_list:
        try:
            rel = event['link']['rel']
            func = rel_map[rel]
            func(event, resource, token, config)
        except KeyError:
            logging.warn("Not sure how to process - %s" % rel)
            logging.debug(event)



def process_message_invitation_event(message, resource, token, config):
    print('accepting messaging invite from %s' % message['_embedded']['messagingInvitation']['_embedded']['from']['name'])
    if str(message.get('status', '')) == 'Success':
        logging.debug('Received successful conversation acceptance from sender.')
        return
    try:
        accept_uri = message['_embedded']['messagingInvitation']['_links']['accept']['href']
        oauth_post_request(resource + accept_uri, token, config['redirect_uri'], {})
        logging.info('Accepted invitation')

    except KeyError:
        logging.error('Failed message')


def process_communication_event(message, resource, token, config):
    print('communication event')
    message_type = str(message['type'])
    if message_type == 'updated':
        # get existing conversations
        conversations_uri = message['_embedded']['communication']['_links']['conversations']['href']
        conversations = oauth_request(resource + conversations_uri, token, config['redirect_uri'])
    pass


def process_conversation_event(message, resource, token, config):
    message_type = str(message['type'])
    conversation_url = message['link']['href']

    logging.debug('%s conversation at %s' % (message_type, conversation_url))
    conversation_uri = message['link']['href']

    conversation = oauth_request(resource + conversation_uri, token, config['redirect_uri'])

    messaging_uri = conversation['_links']['messaging']['href']

    if message_type == 'added':
        thread_id = message['_embedded']['conversation']['threadId']
        send_message(resource + messaging_uri + '/messages', 'hello from the bot', token, config['redirect_uri'])


def process_missed_items_event(message, resource, token, config):
    print('missed items event')
    pass


def process_message_event(message, resource, token, config):
    logging.debug('Processing message event')
    try:
        if str(message['_embedded']['message']['direction']) == 'Incoming':
            message_uri = message['_embedded']['message']['_links']['plainMessage']['href']
            logging.debug("Received raw message - %s" % message_uri)

            inbound_message = urllib.unquote_plus(DataURI(message_uri).data)
            logging.info("Received message - %s" % inbound_message)

            thread_uri = message['_embedded']['message']['_links']['messaging']['href']
            send_message(resource + thread_uri + '/messages', 'you say "%s", I say potato' % inbound_message, token, config['redirect_uri'])
    except KeyError:
        logging.debug('not an inbound message')
    pass