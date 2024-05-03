import json
import requests

from auth import APIClient
from files_manager import read_file_json, create_dir, write_file_json, download_file, get_file_name, zip_path


class Execution:
    def __init__(self, client: APIClient, user, password):
        self.pre_admissions = None
        self.url = "https://platform.senior.com.br/t/senior.com.br/bridge/1.0/rest"
        self.api_client = client
        self.username = user
        self.password = password

    def get_all_URL_files_from_pre_admission(self, id_new):
        endpoint = f"{self.url}hcm/onboarding/queries/getAllURLFilesFromPreAdmissionId"

        payload = json.dumps({
            "preAdmissionId": id_new
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_client.token}'
        }

        while True:
            response = requests.request("POST", endpoint, headers=headers, data=payload)
            if response.status_code == 200:
                break
            else:
                self.api_client.login(self.username, self.password)

        return json.loads(response.text)

    def pre_admission_query(self, id_new):
        endpoint = f"{self.url}hcm/onboarding/queries/preAdmissionQuery"

        payload = json.dumps({
            "preAdmissionId": id_new
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_client.token}'
        }

        while True:
            response = requests.request("POST", endpoint, headers=headers, data=payload)
            if response.status_code == 200:
                break
            else:
                self.api_client.login(self.username, self.password)

            json_ret = json.loads(response.text)

            del json_ret['result']['inviteFields']

            return json_ret['result']

    def start(self):

        for employee in self.pre_admissions:
            links_image = self.get_all_URL_files_from_pre_admission(employee["id"])
            name_zip_file = employee["employee_name"]
            path_name = f'./files/{employee["id"]} - {name_zip_file}'
            create_dir(path_name)

            json_pre_admission = self.pre_admission_query(employee["id"])
            write_file_json(f"{path_name}/{name_zip_file}.json", json_pre_admission)

            if links_image["result"] is not None:
                for link in links_image["result"]:
                    if link["key"] is not None and link["key"]:
                        file_name = get_file_name(link["key"])
                        download_file(link["key"], f'{path_name}/{link["value"]}-{file_name}')

            zip_path(f'{employee["id"]} - {name_zip_file}')
