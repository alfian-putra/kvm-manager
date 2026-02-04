import os

from fastapi import APIRouter, \
                    HTTPException, \
                    BackgroundTasks
from pydantic import BaseModel
from sqlmodel import select

from ..model.model import Disk, Os, Vm, OsDownload, CloudInit
from ..lib.common_utility import session, config
from ..lib.vm_utility import vm_create, \
                             vm_reboot, \
                             vm_start, \
                             vm_status, \
                             vm_stop, \
                             vm_extract_all_pool, \
                             download_os, \
                             kvm_server_status

router = APIRouter()

class VmUtils():
    def __init__(self, model,tags,name=''):
        self.name = name
        self.session = session
        self.tags=tags

    # if self.name='user' will produce this api
    #
    # CREATE  POST      /user
    # READ    GET       /user?id=1
    # READ    GET       /user
    # UPDATE  PUT       /user?id=1
    # DELETE  DELETE    /user?id=1
    def get_router(self):
        router = APIRouter()
       
        @router.post(f'/{self.name}/create', tags=self.tags)
        def create_vm_utility(vm: Vm, cloud_init: CloudInit, session: self.session):
            QEMU_URL = config["kvm"]["qemu_url"]

            _os = session.execute(select(Os).where(Os.id==vm.os_id)).scalar_one_or_none()
            _path = session.execute(select(Disk).where(Disk.vm_id==vm.id)).scalar_one_or_none()

            vm_created = vm_create(qemu_url=QEMU_URL, 
                                   cloud_init_tmp=cloud_init.filename, 
                                   var=cloud_init.vars,
                                   vm=vm,
                                   os_data=_os,
                                   disk_os_path=_os.qcow2,
                                   disk_vm_path=_path.qcow2)
            
            if vm_created:
                return { "status" : True}
            
            return { "status" : False}

        @router.get(f'/{self.name}/start'+'?name={name}', tags=self.tags)
        def start_vm_utility(name):
            QEMU_URL = config["kvm"]["qemu_url"]
            return vm_start(QEMU_URL, name)

        @router.get(f'/{self.name}/status'+'?name={name}', tags=self.tags)
        def status_vm_utility(name):
            QEMU_URL = config["kvm"]["qemu_url"]
            return vm_status(QEMU_URL, name)

        @router.post(f'/{self.name}/reboot'+'?name={name}', tags=self.tags)
        def reboot_vm_utility(name):
            QEMU_URL = config["kvm"]["qemu_url"]
            return vm_reboot(QEMU_URL, name)

        @router.post(f'/{self.name}/stop'+'?name={name}', tags=self.tags)
        def stop_vm_utility(name):
            QEMU_URL = config["kvm"]["qemu_url"]
            return vm_stop(QEMU_URL, name)

        @router.get(f'/{self.name}/list_pool_path', tags=self.tags)
        def listing_pool():
            return vm_extract_all_pool()

        @router.post(f'/{self.name}/download_os_qcow2', tags=self.tags)
        async def download_os_qcow2(os_download: OsDownload, background_tasks: BackgroundTasks):
            filepath = os.path.join(config["kvm"]["pool"]["path"], os_download.name)
            
            background_tasks.add_task(download_os,os_download.url, os_download.name)
            
            return {'status' : 'success', 'filepath': filepath}
        
        @router.get(f'/{self.name}/kvm_server_status', tags=self.tags)
        def kvm_server_status_utils():
            return kvm_server_status()
        
        #   READ ALL    GET /cloud_init
        #   READ        GET /cloud_init/filename.tmp
                # {
                #     "file" : "example.jinja",
                #     "content": "example: {path}",
                #     "kwargs": {
                #             "hostname":"hostname.com",
                #             "kvm_admin":"kvmAdmin",
                #             "kvm_password":"kvmP4$$!"
                #         }
                # }
        #   CREATE       POST /cloud_init/new_filename.tmp
        #   UPDATE       PUT  /cloud_init/filename.tmp
        #   DELETE       DELETE  /cloud_init/filename.tmp
        
        return router