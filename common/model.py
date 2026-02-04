from sqlmodel import SQLModel, \
                     Field
from pydantic import BaseModel
from enum import Enum


# ## DB
#     - user  {id, name, password, role, vm} | role : user, admin (can delete and access web)
#     - vm    {id, hostname, vcpu, memmory, disk_size, os, status, approval_status, user}
##          status : ON, OFF, DELETED
##          approval_status : waiting, approve, unapprove, 
#     - request {id, user_requester, list[[vm]] }

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(SQLModel, table=True):
    __tablename__ = "user_"
    id: int | None = Field(primary_key=True)
    name: str = Field(index=True)
    username: str = Field(index=True)
    password: str
    user_id: str
    role: UserRole = Field(default="USER")

class VmStatus(str, Enum):
    REQUEST = "REQUEST"
    FAIL = "FAIL"
    OFF = "OFF"
    ON = "ON"

class Vm(SQLModel, table=True):
    __tablename__="vm"
    id: int | None = Field(primary_key=True)
    user_id: int | None = Field(default=None, foreign_key='user_.id')
    name: str = Field(index=True)
    hostname: str = Field(index=True)
    group_name: str = Field(index=True)
    ip: str
    vcpu: int
    memmory: int 
    os_id: int | None = Field(default=None, foreign_key='os.id')
    status: VmStatus = Field(default='REQUEST')

class Os(SQLModel, table=True):
    __tablename__="os"
    id: int | None = Field(primary_key=True)
    name: str 
    version: int
    iso: str = Field(default=True)
    qcow2: str = Field(default=True)
    disk_size: int = Field(default=0)
    description: str

class Disk(SQLModel, table=True):
    __tablename__="disk"
    id: int | None = Field(primary_key=True)
    vm_id: int = Field(default=None, foreign_key='vm.id') 
    name: str
    disk_size: int = Field(default=0)
    qcow2 : str

class OsDownload(BaseModel):
    name: str
    url: str