import requests
import os
import pandas as pd


def download_file_from_gdrive(url, destination_folder):
    file_id = url.split("/")[-2]
    base_url = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(base_url, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(base_url, params=params, stream=True)

    file_name = get_file_name(response)
    destination = os.path.join(destination_folder, file_name)
    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None


def get_file_name(response):
    header = response.headers["Content-Disposition"]
    file_name_start_index = header.index('filename="') + len('filename="')
    file_name_end_index = header.index('"', file_name_start_index)
    return header[file_name_start_index:file_name_end_index]


def save_response_content(response, destination):
    chunk_size = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)


csv_file = "url.csv"  # name csv file
destination_folder = "hasil"  # foledr hasil

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

df = pd.read_csv(csv_file)
urls = df["url"]

for url in urls:
    download_file_from_gdrive(url, destination_folder)
