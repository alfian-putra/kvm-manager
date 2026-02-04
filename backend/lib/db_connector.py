from sqlmodel import Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends

from common.config import Config 

config = Config().config

database_url = f'{config['database']['type']}+{config['database']['dialect']}:' + \
        f'//{config['database']['user']}:{config['database']['password']}' + \
        f'@{config['database']['host']}:{config['database']['port']}/{config['database']['name']}'

connect_args = {}
# connect_args = {"check_same_thread": False}

engine = create_engine(database_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

# SessionDep = Session(engine)
SessionDep = Annotated[Session, Depends(get_session)]