from common._fetch_api_user import FetchApiUser
from common._fetch_api_vm import FetchApiVm
from common._fetch_api_disk import FetchApiDisk
from common._fetch_api_os import FetchApiOs
from common._fetch_api_cloud_init import FetchApiCloudInit

from common._fetch_api_vm_utility import FetchApiVmUtility

class FetchApi():
    def __init__(self):
        self.user = FetchApiUser()
        self.vm = FetchApiVm()
        self.vm_utility = FetchApiVmUtility("vm")
        self.disk = FetchApiDisk()
        self.os = FetchApiOs()
        self.cloud_init = FetchApiCloudInit()

