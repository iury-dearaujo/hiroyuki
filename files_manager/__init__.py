import json
import os
import urllib
import zipfile
from urllib.parse import urlparse


def create_dir(path_name):
    if not os.path.exists(path_name):
        os.makedirs(path_name)


def read_data():
    return read_file_json("./data.json")


def read_file_json(file_name):

    existFile = os.path.exists(file_name)

    if existFile:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                return 0, f"Success: reading the {file_name}", json.load(file)
        except IOError:
            return 1, f"Error: Can not open the file:{IOError}", None
    else:
        return 1, f"Error: File does not appear to exist: {file_name}", None





def write_file_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def zip_path(dir_name):
    dir_input = f"./files/{dir_name}"
    dir_output = f"./zipFiles/{dir_name}.zip"
    with zipfile.ZipFile(dir_output, 'w') as zipf:
        for root, dirs, files in os.walk(dir_input):
            for file in files:
                path = os.path.join(root, file)
                zipf.write(path, os.path.relpath(path, dir_input))


def download_file(_url, file_name):
    urllib.request.urlretrieve(_url, file_name)


def get_file_name(this_url):
    parsed_url = urlparse(this_url)
    path = parsed_url.path
    file_name = path.split("/")[-1]
    file_name = file_name.split("?")[0]
    return file_name
