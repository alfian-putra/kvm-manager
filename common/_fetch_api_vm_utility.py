import json
import requests
from common.config import Config
from common.common_utility import response_api_format

class FetchApiVmUtility():
    def __init__(self, model_name):
        self.config = Config().config
        self.model_name = model_name
        self.url = f'{self.config["backend"]["protocol"]}://{self.config["backend"]["host"]}:{self.config["backend"]["port"]}/vm_utils/'

    def create_vm(self, cloud_init, vm):
        url = self.url + f"create"
        data = {"vm": vm, "cloud_init": cloud_init}
        print("=============================     ===")
        print(data)
        response = requests.post(url, json.dumps(data))
        return response_api_format(url, response.status_code, response.json())

    def start_vm(self, name):
        url = self.url + f'start?name={name}'
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())
    
    def status_vm(self,name):
        url = self.url + f'status?name={name}'
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())
    
    def reboot_vm(self,name):
        url = self.url + f'reboot?name={name}'
        response = requests.post(url)
        return response_api_format(url, response.status_code, response.json())
    
    def stop_vm(self,name):
        url = self.url + f'status?name={name}'
        response = requests.post(url)
        return response_api_format(url, response.status_code, response.json())
    
    def listing_pool(self):
        url = self.url + f'list_pool_path'
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())
    
    def download_os(self, filename, os_download):
        url = self.url + 'download_os_qcow2'
        data = {'name': filename, 'url': os_download}
        response = requests.post(url, data)
        return response_api_format(url, response.status_code, response.json)
    
    def kvm_server_status(self):
        url = self.url + f'kvm_server_status'
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())
    