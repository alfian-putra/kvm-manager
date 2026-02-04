import requests
from common._fetch_api import FetchApi

class FetchApiOs(FetchApi):
    def __init__(self):
        FetchApi.__init__(self, 'os')
