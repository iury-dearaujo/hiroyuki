import requests
import json


class APIClient:
    def __init__(self) -> None:
        self.base_url = "https://platform.senior.com.br/t/senior.com.br/bridge/1.0/rest"
        self.token = None
        self.response_complete = None
        self.response_status_code = None

    def login(self, username, password):
        endpoint = f"{self.base_url}/platform/authentication/actions/login"
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(endpoint, headers=headers, data=payload)

        if response.status_code == 200:
            self.response_status_code = response.status_code
            self.response_complete = response.json()

            if "jsonToken" in self.response_complete:
                jsonToken = json.loads(self.response_complete["jsonToken"])
                if "access_token" in jsonToken:
                    self.token = jsonToken['access_token']

            return True
        else:
            self.response_status_code = response.status_code
            self.response_complete = response.json()
            return False
