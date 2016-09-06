import logging
from .actions import oauth_post_request


def process_events(event_list, resource, token, config):
    rel_map = {
        'messagingInvitation': process_message_invitation_event,
        'communication': process_communication_event,
        'conversation': process_conversation_event,
        'missedItems': process_missed_items_event
    }

    for event in event_list:
        try:
            rel = event['link']['rel']
            func = rel_map[rel]
            func(event, resource, token, config)
        except KeyError:
            logging.warn("Not sure how to process - %s" % rel)


def process_message_invitation_event(message, resource, token, config):
    print('accepting messaging invite from %s' % message['_embedded']['messagingInvitation']['_embedded']['from']['name'])
    if message['status'] == 'Success':
        logging.debug('Received successful conversation acceptance from sender.')
        return
    try:
        accept_uri = message['_embedded']['messagingInvitation']['_links']['accept']['href']
        oauth_post_request(resource + accept_uri, token, config['redirect_uri'], {})
        logging.info('Accepted invitation')
    except KeyError:
        logging.error('Failed message')
        logging.debug(message)


def process_communication_event(message, resource, token, config):
    print(message)

def process_conversation_event(message, resource, token, config):
    print(message)

def process_missed_items_event(message, resource, token, config):
    print(message)
