import requests
from future.moves.urllib.parse import urlparse


def do_autodiscover(domain):
    r = requests.get('https://webdir.online.lync.com/autodiscover/autodiscoverservice.svc/root?originalDomain=%s' % domain)
    discovery = r.json()
    path = discovery['_links']['user']['href']
    domain = urlparse(path)
    host = '{0}://{1}'.format(domain.scheme, domain.netloc)
    return (discovery['_links']['xframe']['href'], path, host)