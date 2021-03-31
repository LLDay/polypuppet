from polypuppet.config import config
from requests_html import HTMLSession

_server_url = 'https://' + config['PRIMARY_SERVER_DOMAIN'] + ':5000'
_server_url = 'http://localhost:5000'


def request(url=_server_url, path='/', **kwargs):
    session = HTMLSession()
    r = session.post(url + path, data=kwargs)
    return r
