import requests
from common._fetch_api import FetchApi
from common.common_utility import response_api_format

class FetchApiVm(FetchApi):
    def __init__(self):
        FetchApi.__init__(self, 'vm')

    # vm
    def _vm_data_to_json(self, name, hostname):
        pass
    
    def read_by_hostname(self, hostname):
        url_read_by_user_id = self.url + f"/{self.model_name}" + f"?hostname={hostname}"
        response = requests.get(url_read_by_user_id)

        return response_api_format(url_read_by_user_id, response.status_code, response.json()) 

    def read_by_name(self, name):
        url_read_by_user_id = self.url + f"/{self.model_name}" + f"?name={name}"
        response = requests.get(url_read_by_user_id)

        return response_api_format(url_read_by_user_id, response.status_code, response.json()) 
    
    # vm_utility
    def start(self, name):
        url_vm_start = self.url + f"/{self.model_name}_utility" + f"/start?name={name}"
        response = requests.post(url_vm_start)

        return response_api_format(url_vm_start, response.status_code, response.json())

    def stop(self, name):
        url_vm_stop = self.url + f"/{self.model_name}_utility" + f"/stop?name={name}"
        response = requests.post(url_vm_stop)
        
        return response_api_format(url_vm_stop, response.status_code, response.json())

    def reboot(self, name):
        url_vm_reboot = self.url + f"/{self.model_name}_utility" + f"/reboot?name={name}"
        response = requests.post(url_vm_reboot)

        return response_api_format(url_vm_reboot, response.status_code, response.json())
    
    def create_vm(self, name, cloud_init):
        # fetch vm data
        vm = self.read_by_name(name)["response"]
        # create vm in kvm
        url_vm_utility_create = FetchApi.url + f"/{self.model_name}_utility" + f"/create?cloud_init={cloud_init}"
        response = requests.post(url_vm_utility_create, vm)

        res = response.json()["status"]
        # update status vm to ON or OFF
        status = ""

        if res:
            status = "ON"
        else:
            status = "OFF"
        
        vm["status"] = status

        self.update(vm)

    def create_vm(self, name):
        return self.create_vm(name, "default")
