from polypuppet.config import Config
from requests_html import HTMLSession

config = Config()


def request(url, path='/', **kwargs):
    session = HTMLSession()
    r = session.post(url + path, data=kwargs)
    return r
