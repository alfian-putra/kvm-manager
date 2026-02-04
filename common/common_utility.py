from common.logger import get_logger
from common.config import Config 

config = Config().config

def response_api_format(api, code, response):
    return { 'api' : api, 'code': code, 'response' : response }