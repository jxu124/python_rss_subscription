from webdav4.client import Client
import os
import io
import json
import tempfile


def dav_read_json(file_url, auth):
    url, filename = os.path.split(file_url)
    client = Client(url, auth)
    assert client.exists(filename)
    local_file = tempfile.mkstemp()[1]
    client.download_file(filename, local_file)
    with open(local_file, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    return data


def dav_write_json(file_url, auth, data):
    url, filename = os.path.split(file_url)
    client = Client(url, auth)
    local_file = tempfile.mkstemp()[1]
    with open(local_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    client.upload_file(local_file, filename, overwrite=True)
    


file_url = "https://a.jxu124.ml/webdav/configure/AnimeDB.json"
auth = ("", "")
data = dav_read_json(file_url, auth)
print(data)
dav_write_json(file_url, auth, data)

