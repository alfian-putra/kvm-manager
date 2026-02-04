import requests
from common._fetch_api import FetchApi

class FetchApiDisk(FetchApi):
    def __init__(self):
        FetchApi.__init__(self, 'disk')

