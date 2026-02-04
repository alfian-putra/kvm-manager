import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import select

from backend.control.router import db_router
from backend.lib.common_utility import create_db_and_tables, log
from backend.lib.common_utility import session
from backend.model.model import User
from backend.lib.vm_utility import vm_is_pool_exist, vm_create_pool

from common.config import Config

config = Config().config
app = FastAPI()

if not vm_is_pool_exist(config["kvm"]["pool"]["name"]):
    vm_create_pool(name=config["kvm"]["pool"]["name"],path=config["kvm"]["pool"]["path"])

origins = [
    f"http://127.0.0.1:{config['backend']['port']}",
    f"http://localhost",
    f"http://localhost:{config['backend']['port']}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_db_and_tables()


app.include_router(db_router)

