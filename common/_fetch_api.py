import json
import requests
from common.config import Config
from common.common_utility import response_api_format

class FetchApi():
    def __init__(self, model_name):
        self.config = Config().config
        self.url = f'{self.config["backend"]["protocol"]}://{self.config["backend"]["host"]}:{self.config["backend"]["port"]}/'
        self.model_name = model_name

    def structure(self):
        url_structure = self.url + f"/{self.model_name}/model"
        response = requests.get(url_structure)

        return response_api_format(url_structure,response, response.json())
    
    def create(self, data):
        url_add = self.url + f"/{self.model_name}"
        response = requests.post(url_add, data)

        return response_api_format(url_add, response, response.json())

    def read_all(self):
        url_read_all = self.url + f"/{self.model_name}"
        response = requests.get(url_read_all)

        return response_api_format(url_read_all, response.status_code,response.json())

    def read(self, id):
        url_read = self.url + f"/{self.model_name}/{id}"
        response = requests.get(url_read)

        return response_api_format(url_read,response, response.json())
    
    def update(self, id, data):
        url_update = self.url + f"{self.model_name}/{id}"
        response = requests.patch(url_update, json.dumps(data))

        return response_api_format(url_update,response, response.json())

    def delete(self, id):
        url_delete = self.url + f"/{self.model_name}/{id}"
        response = requests.delete(url_delete)

        return response_api_format(url_delete,response, response.json())