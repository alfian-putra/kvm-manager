from common.logger import get_logger
from common.config import Config 
from backend.lib.db_connector import SessionDep, engine
from sqlmodel import SQLModel

config = Config().config
log = get_logger('backend')
session = SessionDep
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)