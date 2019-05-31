import os
import re
import csv
import pandas as pd

import json
import requests
from requests.exceptions import RequestException

from secret import CLUBHOUSE_API_TOKEN

headers = {
    'Content-type': 'application/json',
}

dir_name = os.getcwd()
fold_att = "attachments"
os.makedirs(fold_att, exist_ok=True)

def get_files(files_url):
    r = requests.get(files_url, headers=headers).json()
    jsons = json.dumps(r)
    files = pd.read_json(jsons)
    file_path = os.path.join(dir_name, "get_files.csv")
    files.to_csv(file_path)
    return files

def download_attachment(url, filename):
    url_token = url + "?token=%s" %CLUBHOUSE_API_TOKEN
    try:
        with requests.get(url_token) as r:
            attachment_data = r.content
            # save to file
            filepath = os.path.join(dir_name, fold_att, filename)
            with open(filepath, 'wb') as f:
                f.write(attachment_data)
    except RequestException as e:
        print(e)

files_url = "https://api.clubhouse.io/api/v2/files?token=%s" %CLUBHOUSE_API_TOKEN
files = get_files(files_url)
urls = files["url"]
filenames = files["filename"]
for url, filename in zip(urls, filenames):
    download_attachment(url, filename)
