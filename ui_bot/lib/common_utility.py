from common.fetch_api import FetchApi
from common.config import Config
from common.logger import get_logger

config = Config().config
log = get_logger("ui_bot")
api = FetchApi()