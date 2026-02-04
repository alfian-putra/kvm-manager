import json

from backend.model.model import *
from backend.lib.common_utility import session, create_db_and_tables
from common._fetch_api_user import FetchApiUser

api = FetchApiUser()

u0 = {"id":112, "name":"admin", "username":"admin", "password":"admin", "user_id":"809228620", "role":"ADMIN"}
os0 =   {
    "name": "Fedora",
    "version": 42,
    "disk_size": 0,
    "id": 1,
    "qcow2": "/opt/pool/fedora-42.qcow2",
    "description": None
  }
res = api.create(json.dumps(u0))
print(res["response"])