import os
import requests
from common._fetch_api import FetchApi
from common.common_utility import response_api_format, config

class FetchApiCloudInit(FetchApi):
    def __init__(self):
        FetchApi.__init__(self, 'cloud_init')

    def fullpath_tmp(filename):
        return os.path.join(config["backend"]["cloud_init"]["tmp"],filename)
    
    def fullpath_generated(filename):
        return os.path.join(config["backend"]["cloud_init"]["generated"],filename)
    
    def const_value(self):
        url = self.url + "const_value"
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())

    def get_content_by_filename(self,filename):
        url = self.url + f"{self.model_name}/content/{filename}"
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())

    def post_content(self,data):
        url = self.url + f"{self.model_name}/content"
        response = requests.post(url, data)
        return response_api_format(url, response.status_code, response.json())

    def generate(self,filename, vm_id):
        url = self.url + f"{self.model_name}/content/generate/{filename}?vmId={vm_id}"
        response = requests.get(url)
        return response_api_format(url, response.status_code, response.json())

    def update_content(self,id,data):
        url = self.url + f"{self.model_name}/content/{id}"
        response = requests.patch(url, data)
        return response_api_format(url, response.status_code, response.json())

    def init(self):
        url = self.url + f"{self.model_name}/init"
        response = requests.post(url)

        return response_api_format(url, response.status_code, response.json())