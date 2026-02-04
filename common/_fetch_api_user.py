import requests
from common._fetch_api import FetchApi
from common.common_utility import response_api_format

class FetchApiUser(FetchApi):
    def __init__(self):
        FetchApi.__init__(self, 'user')
    
    def read_by_user_id(self, user_id):
        url_read_by_user_id = self.url + f"{self.model_name}/user_id/{user_id}"
        response = requests.get(url_read_by_user_id)

        return response_api_format(url_read_by_user_id, response.status_code, response.json())
    
    # GET  /user?name={name}
    def read_by_username(self, username):
        url_read_by_user_id = self.url + f"{self.model_name}/username/{username}"
        response = requests.get(url_read_by_user_id)

        return response_api_format(url_read_by_user_id, response.status_code, response.json())
    
    # POST /user/hashing_password={password}
    def hash_password(self, password):
        url_hashing_password = self.url + f"{self.model_name}/hashing_password={password}"
        print(url_hashing_password)
        response = requests.post(url_hashing_password)

        return response_api_format(url_hashing_password, response.status_code, response.json())
    
    # POST /user/authenticate/name={name}&password={password}
    def login(self, name, password):
        url_login = self.url + f"{self.model_name}/authenticate/name={name}&password={password}"
        response = requests.get(url_login)

        return response_api_format(url_login, response.status_code, response.json())
    
    # POST /user/authenticate/validate_token={token}
    def validate_token(self,token):
        url_token_validator = self.url + f"{self.model_name}/authenticate/validate_token={token}"
        response = requests.get(url_token_validator)

        return response_api_format(url_token_validator, response.status_code, response.json())

    def init(self):
        url = self.url + f"{self.model_name}/init"
        response = requests.post(url)

        return response_api_format(url, response.status_code, response.json())
