import requests
import shutil
import os
import time
from bs4 import BeautifulSoup
import zipfile
from dotenv import load_dotenv
import datetime

load_dotenv()
game_paths_list = os.environ.get("GAME_PATH")
game_paths_list = [path.strip() for path in game_paths_list.split(",")]
game_paths_list = [path for path in game_paths_list if path]
print(game_paths_list)
TPU_DOWNLOAD_SERVER_ID = 14
urls = {"DLSS": "https://www.techpowerup.com/download/nvidia-dlss-dll/", "DLSS_FG": "https://www.techpowerup.com/download/nvidia-dlss-3-frame-generation-dll/"}


def get_file_id(url):
    try:
        url = "https://www.techpowerup.com/download/nvidia-dlss-dll/"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")

        dll = soup.find("div", {"class": "version"})
        file_name = dll.find("div", {"class": "filename"})
        file_name = file_name.text
        id = dll.find("input", {"name": "id"})
        id = id["value"]
        return id, file_name
    except Exception as e:
        print(f"Failed to scrape {url}:{e}")
        exit()

def check_if_zip_exists(file_name):
    if os.path.exists(file_name):
        print(f"The file at '{file_name}' exists.")
        return True

    print(f"The file at '{file_name}' does not exist.")
    return False


def download_dll_zip(url, id, file_name):
    payload = {"server_id": TPU_DOWNLOAD_SERVER_ID, "id": id}
    print(f"Downloading {file_name} ......")
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
            print(f"{file_name} successfully downloaded")

    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        exit()