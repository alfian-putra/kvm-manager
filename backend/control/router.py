from fastapi import APIRouter

from ..model.model import User, Vm, Disk, Os, CloudInit
from ._crud_user import CrudUser
from ._crud_vm import CrudVm
from ._crud_os import CrudOs
from ._crud_disk import CrudDisk
from ._crud_cloud_init import CrudCloudInit

from .vm_utility import VmUtils

db_router = APIRouter()

user_router = CrudUser(User, name='user').get_router()
vm_router =  CrudVm(Vm, name='vm').get_router()
disk_router =  CrudDisk(Disk, name='disk').get_router()
os_router =  CrudOs(Os, name='os').get_router()
cloud_init_router = CrudCloudInit(CloudInit, name="cloud_init").get_router()

vm_utils_router = VmUtils(Vm,tags=["vm"],name='vm_utils').get_router()

db_router.include_router(user_router)
db_router.include_router(vm_router)
db_router.include_router(disk_router)
db_router.include_router(os_router)
db_router.include_router(cloud_init_router)

db_router.include_router(vm_utils_router)
